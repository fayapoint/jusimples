#!/usr/bin/env python3
"""
OpenAI Dashboard API Backend
This module provides the API endpoints for the OpenAI API dashboard,
including status, metrics, and usage statistics.
"""

import os
import time
import json
import logging
import datetime
from typing import Dict, List, Any, Tuple, Optional
from flask import Blueprint, jsonify, request, render_template, current_app
try:
    from .openai_utils import OpenAIManager
    from .db_utils import get_db_connection
except ImportError:
    # For direct module execution
    from openai_utils import OpenAIManager
    from db_utils import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
openai_dashboard_bp = Blueprint('openai_dashboard', __name__, url_prefix='/admin-openai')

# OpenAI Manager instance
openai_manager = None


@openai_dashboard_bp.before_app_request
def init_openai_manager():
    """Initialize the OpenAI manager before request"""
    global openai_manager
    if openai_manager is None and current_app:
        openai_manager = OpenAIManager()


@openai_dashboard_bp.route('/openai-dashboard')
def standalone_openai_dashboard():
    try:
        logger.info("Rendering OpenAI dashboard template")
        
        # Initialize dictionaries with default values
        config = {
            "api_key_configured": False,
            "api_key_preview": None,
            "default_model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 4000,
            "embedding_model": "text-embedding-ada-002"
        }
        stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost": 0,
            "avg_response_time": 0,
            "error_rate": 0,
            "models": [],
            "daily_usage": []
        }
        
        # Get API configuration if OpenAI manager is available
        if openai_manager and openai_manager.is_ready():
            api_key = openai_manager.api_key
            config["api_key_configured"] = bool(api_key)
            config["api_key_preview"] = f"{api_key[:5]}...{api_key[-4:]}" if api_key and len(api_key) > 10 else None
            config["default_model"] = openai_manager.active_model or "gpt-3.5-turbo"
        
        # Get database stats
        conn = None
        try:
            conn = get_db_connection()
            if conn is None:
                logger.warning("Database connection is None, using default stats values")
                return render_template('openai_dashboard.html', config=config, stats=stats, error=None)
                
            cursor = conn.cursor()
            
            # Check for required columns in search_logs table
            cursor.execute("PRAGMA table_info(search_logs)")
            search_columns = {row[1] for row in cursor.fetchall()}
            
            cursor.execute("PRAGMA table_info(ask_logs)")
            ask_columns = {row[1] for row in cursor.fetchall()}
            
            # Get total requests and tokens with more robust column handling
            required_columns = {'tokens_used', 'prompt_tokens', 'completion_tokens', 'response_time'}
            missing_columns = required_columns - (search_columns.intersection(ask_columns))
            
            if missing_columns:
                logger.warning(f"Missing columns in logs tables: {missing_columns}")
                # Construct a safer query with fallbacks for missing columns
                select_parts = []
                for col in ['tokens_used', 'prompt_tokens', 'completion_tokens', 'response_time']:
                    if col in search_columns and col in ask_columns:
                        select_parts.append(f"{col}")
                    else:
                        select_parts.append(f"NULL as {col}")
                
                query = f"""
                    SELECT COUNT(*) AS total_requests,
                           SUM(COALESCE(tokens_used, 0)) AS total_tokens,
                           SUM(COALESCE(prompt_tokens, 0)) AS total_input_tokens,
                           SUM(COALESCE(completion_tokens, 0)) AS total_output_tokens,
                           AVG(COALESCE(response_time, 0)) AS avg_response_time
                    FROM (
                        SELECT {', '.join(select_parts)}
                        FROM search_logs
                        UNION ALL
                        SELECT {', '.join(select_parts)}
                        FROM ask_logs
                    )
                """
            else:
                query = """
                    SELECT COUNT(*) AS total_requests,
                           SUM(COALESCE(tokens_used, 0)) AS total_tokens,
                           SUM(COALESCE(prompt_tokens, 0)) AS total_input_tokens,
                           SUM(COALESCE(completion_tokens, 0)) AS total_output_tokens,
                           AVG(COALESCE(response_time, 0)) AS avg_response_time
                    FROM (
                        SELECT tokens_used, prompt_tokens, completion_tokens, response_time
                        FROM search_logs
                        UNION ALL
                        SELECT tokens_used, prompt_tokens, completion_tokens, response_time
                        FROM ask_logs
                    )
                """
            
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                stats["total_requests"] = result[0] or 0
                stats["total_tokens"] = result[1] or 0
                stats["total_input_tokens"] = result[2] or 0
                stats["total_output_tokens"] = result[3] or 0
                stats["avg_response_time"] = result[4] or 0
            
            # Calculate approximate cost (very rough estimate)
            # Using $0.001 per 1K tokens for input and $0.002 per 1K output tokens (gpt-3.5-turbo rates)
            input_cost = (stats["total_input_tokens"] / 1000) * 0.001
            output_cost = (stats["total_output_tokens"] / 1000) * 0.002
            stats["total_cost"] = input_cost + output_cost
            
            # Get error rate (with column existence check)
            if 'success' in search_columns and 'success' in ask_columns:
                cursor.execute("""
                    SELECT 
                        COUNT(*) AS total_requests,
                        SUM(CASE WHEN success = 'false' THEN 1 ELSE 0 END) AS error_count
                    FROM (
                        SELECT success FROM search_logs
                        UNION ALL
                        SELECT success FROM ask_logs
                    )
                """)
            else:
                logger.warning("Missing 'success' column in logs tables, using default error rate")
                cursor.execute("""
                    SELECT 
                        COUNT(*) AS total_requests,
                        0 AS error_count
                    FROM (
                        SELECT 1 FROM search_logs
                        UNION ALL
                        SELECT 1 FROM ask_logs
                    )
                """)
            result = cursor.fetchone()
            if result and result[0]:
                stats["error_rate"] = (result[1] or 0) / result[0] * 100
            
            # Get model usage (with column existence check)
            if 'model' in search_columns and 'model' in ask_columns and 'tokens_used' in search_columns and 'tokens_used' in ask_columns:
                cursor.execute("""
                    SELECT 
                        model, 
                        COUNT(*) AS count,
                        SUM(COALESCE(tokens_used, 0)) AS tokens
                    FROM (
                        SELECT model, tokens_used FROM search_logs
                        UNION ALL
                        SELECT model, tokens_used FROM ask_logs
                    )
                    WHERE model IS NOT NULL
                    GROUP BY model
                    ORDER BY count DESC
                """)
            elif 'model' in search_columns and 'model' in ask_columns:
                # Only model column exists but not tokens_used
                cursor.execute("""
                    SELECT 
                        model, 
                        COUNT(*) AS count,
                        0 AS tokens
                    FROM (
                        SELECT model FROM search_logs
                        UNION ALL
                        SELECT model FROM ask_logs
                    )
                    WHERE model IS NOT NULL
                    GROUP BY model
                    ORDER BY count DESC
                """)
            else:
                logger.warning("Missing required columns for model usage stats")
                # Create an empty result set
                models_data = []
                cursor.execute("SELECT 1 WHERE 0")
                models_data = cursor.fetchall() # Will be empty
            models_data = cursor.fetchall()
            
            # Format model data
            for model, count, tokens in models_data:
                if model:  # Skip null models
                    # Calculate approximate cost based on model
                    model_cost = 0
                    if "gpt-4" in model.lower():
                        model_cost = (tokens / 1000) * 0.03  # Higher cost for GPT-4
                    else:
                        model_cost = (tokens / 1000) * 0.002  # Lower cost for others
                    
                    stats["models"].append({
                        "model": model,
                        "count": count,
                        "tokens": tokens or 0,
                        "cost": model_cost
                    })
            
            # Get daily usage (with column existence check)
            if 'created_at' in search_columns and 'created_at' in ask_columns:
                if 'tokens_used' in search_columns and 'tokens_used' in ask_columns:
                    cursor.execute("""
                        SELECT 
                            DATE(created_at) AS date, 
                            COUNT(*) AS requests,
                            SUM(COALESCE(tokens_used, 0)) AS tokens
                        FROM (
                            SELECT created_at, tokens_used FROM search_logs
                            UNION ALL
                            SELECT created_at, tokens_used FROM ask_logs
                        )
                        WHERE created_at IS NOT NULL AND created_at >= DATE('now', '-30 days')
                        GROUP BY DATE(created_at)
                        ORDER BY date DESC
                    """)
                else:
                    # No tokens_used column
                    cursor.execute("""
                        SELECT 
                            DATE(created_at) AS date, 
                            COUNT(*) AS requests,
                            0 AS tokens
                        FROM (
                            SELECT created_at FROM search_logs
                            UNION ALL
                            SELECT created_at FROM ask_logs
                        )
                        WHERE created_at IS NOT NULL AND created_at >= DATE('now', '-30 days')
                        GROUP BY DATE(created_at)
                        ORDER BY date DESC
                    """)
            else:
                logger.warning("Missing 'created_at' column for daily usage stats")
                # Create empty result set
                daily_data = []
                cursor.execute("SELECT 1 WHERE 0")
                daily_data = cursor.fetchall() # Will be empty
            daily_data = cursor.fetchall()
            
            # Format daily usage data
            for date, requests, tokens in daily_data:
                daily_cost = (tokens / 1000) * 0.002 if tokens else 0  # Simple estimate
                stats["daily_usage"].append({
                    "date": date,
                    "requests": requests,
                    "tokens": tokens or 0,
                    "cost": daily_cost
                })
        
        except Exception as e:
            logger.error(f"Error fetching dashboard stats: {e}")
        finally:
            if conn is not None:
                conn.close()
        
        # Return template with data
        return render_template('openai_dashboard.html', config=config, stats=stats, error=None)
        
    except Exception as e:
        logger.error(f"Error rendering OpenAI dashboard: {e}", exc_info=True)
        # Try to render the template with error message but still include any partial data we have
        try:
            return render_template('openai_dashboard.html', config=config or {}, stats=stats or {}, error=str(e))
        except:
            return jsonify({"error": f"Error rendering dashboard: {str(e)}"}), 500


@openai_dashboard_bp.route('/api/openai-status')
def get_openai_status():
    """Get the current status of OpenAI API"""
    global openai_manager
    
    if openai_manager is None:
        return jsonify({
            "initialized": False,
            "error": "OpenAI manager not initialized",
            "api_key_masked": "Not available",
            "model": "Not available",
            "version": "Not available",
            "last_verified": "Never",
            "latency": None
        })
    
    # Get API key masked
    api_key = openai_manager.api_key
    api_key_masked = f"{api_key[:5]}...{api_key[-4:]}" if api_key and len(api_key) > 10 else "sk-***************"
    
    # Get last verified time
    last_verified = "Never"
    if hasattr(openai_manager, 'last_verified') and openai_manager.last_verified:
        last_verified = openai_manager.last_verified.strftime("%Y-%m-%d %H:%M:%S")
    
    # Get latency
    latency = None
    if hasattr(openai_manager, 'last_latency') and openai_manager.last_latency:
        latency = round(openai_manager.last_latency)
    
    return jsonify({
        "initialized": openai_manager.is_ready(),
        "error": openai_manager.last_error,
        "api_key_masked": api_key_masked,
        "model": openai_manager.model,
        "version": getattr(openai_manager, 'client_version', 'Unknown'),
        "last_verified": last_verified,
        "latency": latency
    })


@openai_dashboard_bp.route('/api/test-openai-connection')
def test_openai_connection():
    """Test the connection to OpenAI API"""
    global openai_manager
    
    if openai_manager is None:
        return jsonify({
            "success": False,
            "message": "OpenAI manager not initialized",
        })
    
    start_time = time.time()
    success, message, _ = openai_manager.test_connection()
    latency = round((time.time() - start_time) * 1000)
    
    # Store the last verified time and latency
    if success:
        openai_manager.last_verified = datetime.datetime.now()
        openai_manager.last_latency = latency
    
    # Get API key masked
    api_key = openai_manager.api_key
    api_key_masked = f"{api_key[:5]}...{api_key[-4:]}" if api_key and len(api_key) > 10 else "sk-***************"
    
    return jsonify({
        "success": success,
        "message": message,
        "latency": latency,
        "api_key_masked": api_key_masked,
        "model": openai_manager.model,
        "version": getattr(openai_manager, 'client_version', 'Unknown')
    })


@openai_dashboard_bp.route('/api/token-usage')
def get_token_usage():
    """Get token usage statistics"""
    global openai_manager
    
    if openai_manager is None or not openai_manager.is_ready():
        return jsonify({
            "total_tokens": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "percentage": 0,
            "prompt_tokens_change": 0,
            "completion_tokens_change": 0,
            "history": []
        })
    
    conn = get_db_connection()
    if conn is None:
        logger.error("Failed to connect to database")
        return jsonify({"error": "Database connection failed"})
    
    try:
        # Get total token usage
        cursor = conn.cursor()
        
        # Get current token usage from search_logs
        cursor.execute("""
            SELECT SUM(tokens_used) AS total_search_tokens,
                   SUM(prompt_tokens) AS prompt_search_tokens,
                   SUM(completion_tokens) AS completion_search_tokens
            FROM search_logs
        """)
        search_tokens = cursor.fetchone()
        
        # Get current token usage from ask_logs
        cursor.execute("""
            SELECT SUM(tokens_used) AS total_ask_tokens,
                   SUM(prompt_tokens) AS prompt_ask_tokens,
                   SUM(completion_tokens) AS completion_ask_tokens
            FROM ask_logs
        """)
        ask_tokens = cursor.fetchone()
        
        # Calculate totals
        total_tokens = (search_tokens[0] or 0) + (ask_tokens[0] or 0)
        prompt_tokens = (search_tokens[1] or 0) + (ask_tokens[1] or 0)
        completion_tokens = (search_tokens[2] or 0) + (ask_tokens[2] or 0)
        
        # Calculate usage percentage (assuming a monthly limit of 500,000 tokens)
        monthly_limit = 500000
        percentage = round((total_tokens / monthly_limit) * 100, 1) if total_tokens else 0
        
        # Get token usage history by day (last 7 days)
        cursor.execute("""
            WITH search_daily AS (
                SELECT DATE(timestamp) AS date, 
                       SUM(prompt_tokens) AS prompt_tokens,
                       SUM(completion_tokens) AS completion_tokens
                FROM search_logs
                WHERE timestamp > DATE('now', '-7 day')
                GROUP BY DATE(timestamp)
            ),
            ask_daily AS (
                SELECT DATE(timestamp) AS date,
                       SUM(prompt_tokens) AS prompt_tokens,
                       SUM(completion_tokens) AS completion_tokens
                FROM ask_logs
                WHERE timestamp > DATE('now', '-7 day')
                GROUP BY DATE(timestamp)
            )
            SELECT COALESCE(search_daily.date, ask_daily.date) AS date,
                   COALESCE(search_daily.prompt_tokens, 0) + COALESCE(ask_daily.prompt_tokens, 0) AS prompt_tokens,
                   COALESCE(search_daily.completion_tokens, 0) + COALESCE(ask_daily.completion_tokens, 0) AS completion_tokens
            FROM search_daily
            FULL OUTER JOIN ask_daily ON search_daily.date = ask_daily.date
            ORDER BY date ASC
        """)
        history = cursor.fetchall()
        
        # Format history data
        history_data = []
        for date, p_tokens, c_tokens in history:
            history_data.append({
                "date": date,
                "prompt_tokens": p_tokens or 0,
                "completion_tokens": c_tokens or 0,
                "total_tokens": (p_tokens or 0) + (c_tokens or 0)
            })
        
        # Calculate change percentages from previous week
        cursor.execute("""
            SELECT SUM(prompt_tokens) AS prev_prompt_tokens,
                   SUM(completion_tokens) AS prev_completion_tokens
            FROM (
                SELECT prompt_tokens, completion_tokens FROM search_logs
                WHERE timestamp BETWEEN DATE('now', '-14 day') AND DATE('now', '-7 day')
                UNION ALL
                SELECT prompt_tokens, completion_tokens FROM ask_logs
                WHERE timestamp BETWEEN DATE('now', '-14 day') AND DATE('now', '-7 day')
            )
        """)
        prev_week = cursor.fetchone()
        
        prev_prompt_tokens = prev_week[0] or 1  # Avoid division by zero
        prev_completion_tokens = prev_week[1] or 1
        
        prompt_tokens_change = round(((prompt_tokens - prev_prompt_tokens) / prev_prompt_tokens) * 100, 1)
        completion_tokens_change = round(((completion_tokens - prev_completion_tokens) / prev_completion_tokens) * 100, 1)
        
        return jsonify({
            "total_tokens": total_tokens,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "percentage": percentage,
            "prompt_tokens_change": prompt_tokens_change,
            "completion_tokens_change": completion_tokens_change,
            "history": history_data
        })
    
    except Exception as e:
        logger.error(f"Error getting token usage: {e}")
        return jsonify({"error": str(e)})
    
    finally:
        conn.close()


@openai_dashboard_bp.route('/api/request-stats')
def get_request_stats():
    """Get API request statistics"""
    conn = get_db_connection()
    if conn is None:
        logger.error("Failed to connect to database")
        return jsonify({"error": "Database connection failed"})
    
    try:
        cursor = conn.cursor()
        
        # Get total requests
        cursor.execute("""
            SELECT COUNT(*) AS total_requests,
                   AVG(response_time) AS avg_response_time,
                   SUM(CASE WHEN success = 'true' THEN 1 ELSE 0 END) AS successful_requests,
                   COUNT(*) AS all_requests
            FROM (
                SELECT response_time, success FROM search_logs
                UNION ALL
                SELECT response_time, success FROM ask_logs
            )
        """)
        stats = cursor.fetchone()
        
        total_requests = stats[0] or 0
        avg_response_time = round(stats[1] or 0)
        successful_requests = stats[2] or 0
        all_requests = stats[3] or 1  # Avoid division by zero
        
        # Calculate success and error rates
        success_rate = round((successful_requests / all_requests) * 100, 1)
        error_rate = round(((all_requests - successful_requests) / all_requests) * 100, 1)
        
        # Get request history by day (last 7 days)
        cursor.execute("""
            WITH search_daily AS (
                SELECT DATE(timestamp) AS date, 
                       COUNT(*) AS requests,
                       SUM(CASE WHEN success = 'true' THEN 1 ELSE 0 END) AS successful_requests,
                       COUNT(*) AS total_requests
                FROM search_logs
                WHERE timestamp > DATE('now', '-7 day')
                GROUP BY DATE(timestamp)
            ),
            ask_daily AS (
                SELECT DATE(timestamp) AS date,
                       COUNT(*) AS requests,
                       SUM(CASE WHEN success = 'true' THEN 1 ELSE 0 END) AS successful_requests,
                       COUNT(*) AS total_requests
                FROM ask_logs
                WHERE timestamp > DATE('now', '-7 day')
                GROUP BY DATE(timestamp)
            )
            SELECT COALESCE(search_daily.date, ask_daily.date) AS date,
                   COALESCE(search_daily.requests, 0) + COALESCE(ask_daily.requests, 0) AS requests,
                   COALESCE(search_daily.successful_requests, 0) + COALESCE(ask_daily.successful_requests, 0) AS successful_requests,
                   COALESCE(search_daily.total_requests, 0) + COALESCE(ask_daily.total_requests, 0) AS total_requests
            FROM search_daily
            FULL OUTER JOIN ask_daily ON search_daily.date = ask_daily.date
            ORDER BY date ASC
        """)
        history = cursor.fetchall()
        
        # Format history data
        history_data = []
        for date, requests, successful, total in history:
            success_rate_day = round((successful / total) * 100, 1) if total > 0 else 0
            history_data.append({
                "date": date,
                "requests": requests,
                "successful_requests": successful,
                "success_rate": success_rate_day
            })
        
        # Calculate change percentages from previous week
        cursor.execute("""
            SELECT COUNT(*) AS prev_requests,
                   AVG(response_time) AS prev_avg_response_time
            FROM (
                SELECT response_time FROM search_logs
                WHERE timestamp BETWEEN DATE('now', '-14 day') AND DATE('now', '-7 day')
                UNION ALL
                SELECT response_time FROM ask_logs
                WHERE timestamp BETWEEN DATE('now', '-14 day') AND DATE('now', '-7 day')
            )
        """)
        prev_week = cursor.fetchone()
        
        prev_requests = prev_week[0] or 1  # Avoid division by zero
        prev_avg_response_time = prev_week[1] or 1
        
        requests_change = round(((total_requests - prev_requests) / prev_requests) * 100, 1)
        response_time_change = round(((avg_response_time - prev_avg_response_time) / prev_avg_response_time) * 100, 1)
        
        return jsonify({
            "total_requests": total_requests,
            "avg_response_time": avg_response_time,
            "success_rate": success_rate,
            "error_rate": error_rate,
            "requests_change": requests_change,
            "response_time_change": response_time_change,
            "success_rate_change": 0,  # Would need data from previous periods
            "error_rate_change": 0,    # Would need data from previous periods
            "history": history_data
        })
    
    except Exception as e:
        logger.error(f"Error getting request stats: {e}")
        return jsonify({"error": str(e)})
    
    finally:
        conn.close()


@openai_dashboard_bp.route('/api/model-usage')
def get_model_usage():
    """Get model usage statistics"""
    conn = get_db_connection()
    if conn is None:
        logger.error("Failed to connect to database")
        return jsonify({"error": "Database connection failed"})
    
    try:
        cursor = conn.cursor()
        
        # Get model usage from search_logs and ask_logs
        cursor.execute("""
            WITH model_stats AS (
                SELECT model,
                       COUNT(*) AS requests,
                       SUM(tokens_used) AS tokens,
                       AVG(response_time) AS avg_response_time,
                       SUM(CASE WHEN success = 'true' THEN 1 ELSE 0 END) AS successful_requests,
                       COUNT(*) AS total_requests
                FROM (
                    SELECT model, tokens_used, response_time, success FROM search_logs
                    UNION ALL
                    SELECT model, tokens_used, response_time, success FROM ask_logs
                )
                GROUP BY model
            )
            SELECT model, 
                   requests, 
                   tokens, 
                   avg_response_time,
                   (successful_requests * 100.0 / total_requests) AS success_rate
            FROM model_stats
            ORDER BY requests DESC
        """)
        models_data = cursor.fetchall()
        
        # Format model data
        models = []
        total_usage = 0
        
        for model, requests, tokens, avg_response_time, success_rate in models_data:
            if model:  # Skip null models
                total_usage += requests
                models.append({
                    "name": model,
                    "requests": requests,
                    "tokens": tokens or 0,
                    "avg_response_time": round(avg_response_time or 0),
                    "success_rate": round(success_rate or 0, 1)
                })
        
        # Calculate usage percentage for each model
        for model in models:
            model["usage"] = round((model["requests"] / total_usage) * 100, 1) if total_usage > 0 else 0
        
        return jsonify({
            "models": models
        })
    
    except Exception as e:
        logger.error(f"Error getting model usage: {e}")
        return jsonify({"error": str(e)})
    
    finally:
        conn.close()


@openai_dashboard_bp.route('/api/recent-errors')
def get_recent_errors():
    """Get recent API errors"""
    conn = get_db_connection()
    if conn is None:
        logger.error("Failed to connect to database")
        return jsonify({"error": "Database connection failed"})
    
    try:
        cursor = conn.cursor()
        
        # Get recent errors from search_logs and ask_logs
        cursor.execute("""
            SELECT 'search' AS log_type, 
                   error_type, 
                   error_message, 
                   timestamp
            FROM search_logs
            WHERE success = 'false' AND error_message IS NOT NULL
            UNION ALL
            SELECT 'ask' AS log_type, 
                   error_type, 
                   error_message, 
                   timestamp
            FROM ask_logs
            WHERE success = 'false' AND error_message IS NOT NULL
            ORDER BY timestamp DESC
            LIMIT 10
        """)
        error_data = cursor.fetchall()
        
        # Format error data
        errors = []
        for log_type, error_type, error_message, timestamp in error_data:
            errors.append({
                "type": error_type or f"{log_type.capitalize()} Error",
                "message": error_message or "Unknown error",
                "timestamp": timestamp
            })
        
        return jsonify({
            "errors": errors
        })
    
    except Exception as e:
        logger.error(f"Error getting recent errors: {e}")
        return jsonify({"error": str(e)})
    
    finally:
        conn.close()


@openai_dashboard_bp.route('/api/openai/config', methods=['POST'])
def standalone_update_openai_config():
    """Update OpenAI API key configuration"""
    global openai_manager
    
    try:
        data = request.get_json()
        
        if not data or 'api_key' not in data:
            return jsonify({"error": "API key is required", "success": False}), 400
        
        new_api_key = data.get('api_key')
        
        # Validate API key format
        if not new_api_key.startswith('sk-'):
            return jsonify({"error": "Invalid API key format", "success": False}), 400
        
        # Update the API key in environment
        os.environ['OPENAI_API_KEY'] = new_api_key
        
        # Update .env file if it exists
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        if os.path.exists(env_path):
            try:
                # Read existing env file
                with open(env_path, 'r') as f:
                    lines = f.readlines()
                
                # Update or add API key
                found = False
                for i, line in enumerate(lines):
                    if line.startswith('OPENAI_API_KEY='):
                        lines[i] = f'OPENAI_API_KEY={new_api_key}\n'
                        found = True
                        break
                
                if not found:
                    lines.append(f'OPENAI_API_KEY={new_api_key}\n')
                
                # Write back to file
                with open(env_path, 'w') as f:
                    f.writelines(lines)
                    
                logger.info("Updated OpenAI API key in .env file")
            except Exception as e:
                logger.error(f"Error updating .env file: {e}")
        else:
            logger.warning(".env file not found, only updated environment variable")
        
        # Reinitialize OpenAI manager
        if openai_manager:
            openai_manager.api_key = new_api_key
            reinit_success = openai_manager.initialize()
            
            if reinit_success:
                # Test the connection
                success, message, model = openai_manager.test_connection()
                return jsonify({
                    "success": success,
                    "message": message,
                    "updated": True,
                    "active_model": model or openai_manager.active_model
                })
            else:
                return jsonify({
                    "success": False, 
                    "message": f"API key updated but reinitialization failed: {openai_manager.last_error}",
                    "updated": True
                })
        else:
            # Initialize a new manager
            openai_manager = OpenAIManager()
            success, message, model = openai_manager.test_connection() if openai_manager.is_ready() else (False, "Manager initialization failed", None)
            
            return jsonify({
                "success": success,
                "message": message,
                "updated": True,
                "active_model": model or getattr(openai_manager, 'active_model', None)
            })
            
    except Exception as e:
        logger.error(f"Error updating OpenAI config: {e}")
        return jsonify({"error": str(e), "success": False}), 500


def register_openai_dashboard(app):
    """Register the OpenAI dashboard blueprint with the Flask app"""
    app.register_blueprint(openai_dashboard_bp)
    
    # Add link to the OpenAI dashboard in the admin sidebar
    # This would typically be done via template extension or a context processor
    # but for simplicity, we're just noting it here
    logger.info("Registered OpenAI dashboard blueprint")
