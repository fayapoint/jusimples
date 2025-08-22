"""
JuSimples Admin Dashboard v3.0
Comprehensive admin panel with dedicated feature management sections
"""

import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash

# Database and utility imports
from db_utils import get_db_manager
from openai_utils import get_openai_status, openai_manager

# Optional imports with fallbacks
try:
    from retrieval_extensions import (
        get_rag_performance_metrics, 
        get_api_library_metrics,
        get_vector_database_health
    )
except ImportError:
    def get_rag_performance_metrics(*args, **kwargs): return {}
    def get_api_library_metrics(*args, **kwargs): return {}
    def get_vector_database_health(*args, **kwargs): return {}

try:
    from lexml_api import get_lexml_status, search_legal_documents
except ImportError:
    def get_lexml_status(): return {"status": "unavailable", "message": "LexML API not configured"}
    def search_legal_documents(*args, **kwargs): return []

logger = logging.getLogger(__name__)

# Create Blueprint
admin_bp_v3 = Blueprint('admin_v3', __name__, url_prefix='/admin/v3')

@admin_bp_v3.route('/')
def dashboard():
    """Main dashboard with system overview"""
    try:
        db_manager = get_db_manager()
        
        # Get comprehensive system metrics
        db_overview = db_manager.admin_db_overview()
        openai_status = get_openai_status()
        lexml_status = get_lexml_status()
        
        # Get recent activity summary
        recent_queries = []
        query_analytics = {}
        
        if db_manager.is_ready():
            # Recent queries
            results = db_manager.execute_query("""
                SELECT question, created_at, success, llm_cost, search_type
                FROM ask_logs 
                ORDER BY created_at DESC 
                LIMIT 10
            """)
            
            for row in results:
                recent_queries.append({
                    'question': row[0][:100] + '...' if len(row[0]) > 100 else row[0],
                    'timestamp': row[1].strftime('%Y-%m-%d %H:%M') if row[1] else 'N/A',
                    'success': row[2],
                    'cost': float(row[3]) if row[3] else 0,
                    'search_type': row[4] or 'keyword'
                })
            
            # Query analytics summary
            analytics_results = db_manager.execute_query("""
                SELECT 
                    COUNT(*) as total_queries,
                    COUNT(*) FILTER (WHERE success = true) as successful_queries,
                    SUM(llm_cost) as total_cost,
                    AVG(response_time_ms) as avg_response_time
                FROM ask_logs 
                WHERE created_at > now() - interval '7 days'
            """)
            
            if analytics_results:
                row = analytics_results[0]
                query_analytics = {
                    'total_queries': int(row[0] or 0),
                    'successful_queries': int(row[1] or 0),
                    'success_rate': (int(row[1] or 0) / max(int(row[0] or 1), 1)) * 100,
                    'total_cost': float(row[2] or 0),
                    'avg_response_time': float(row[3] or 0)
                }
        
        return render_template('admin_dashboard_v3.html',
                             db_overview=db_overview,
                             openai_status=openai_status,
                             lexml_status=lexml_status,
                             recent_queries=recent_queries,
                             query_analytics=query_analytics,
                             page_title="JuSimples Admin Dashboard v3.0")
    
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return render_template('admin_dashboard_v3.html',
                             error=f"Dashboard error: {str(e)}",
                             page_title="JuSimples Admin Dashboard v3.0")

@admin_bp_v3.route('/knowledge-base')
def knowledge_base():
    """Enhanced knowledge base management"""
    try:
        db_manager = get_db_manager()
        
        # Get all knowledge base items with enhanced details
        items = []
        if db_manager.is_ready():
            results = db_manager.execute_query("""
                SELECT 
                    id, title, content, category, metadata, 
                    created_at, updated_at, 
                    (CASE WHEN embedding IS NOT NULL THEN true ELSE false END) as has_embedding
                FROM legal_chunks 
                ORDER BY updated_at DESC 
                LIMIT 100
            """)
            
            for row in results:
                metadata = row[4] if row[4] else {}
                items.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2][:500] + '...' if len(row[2]) > 500 else row[2],
                    'full_content': row[2],
                    'category': row[3],
                    'keywords': metadata.get('keywords', []),
                    'source': metadata.get('source', 'Unknown'),
                    'law_type': metadata.get('law_type', ''),
                    'jurisdiction': metadata.get('jurisdiction', 'BR'),
                    'complexity_level': metadata.get('complexity_level', 'medium'),
                    'tags': metadata.get('tags', []),
                    'created_at': row[5].strftime('%Y-%m-%d %H:%M') if row[5] else 'N/A',
                    'updated_at': row[6].strftime('%Y-%m-%d %H:%M') if row[6] else 'N/A',
                    'has_embedding': row[7]
                })
        
        # Get category statistics
        category_stats = {}
        if db_manager.is_ready():
            results = db_manager.execute_query("""
                SELECT category, COUNT(*) as count
                FROM legal_chunks 
                GROUP BY category 
                ORDER BY count DESC
            """)
            category_stats = {row[0]: int(row[1]) for row in results}
        
        return render_template('knowledge_base_v3.html',
                             items=items,
                             category_stats=category_stats,
                             page_title="Knowledge Base Management")
    
    except Exception as e:
        logger.error(f"Knowledge base error: {e}")
        return render_template('knowledge_base_v3.html',
                             error=f"Error loading knowledge base: {str(e)}",
                             page_title="Knowledge Base Management")

@admin_bp_v3.route('/openai-management')
def openai_management():
    """Dedicated OpenAI API management section"""
    try:
        db_manager = get_db_manager()
        
        # Get OpenAI status and configuration
        openai_status = get_openai_status()
        
        # Get usage statistics
        usage_stats = {}
        recent_calls = []
        
        if db_manager.is_ready():
            # Usage statistics for the last 30 days
            stats_results = db_manager.execute_query("""
                SELECT 
                    COUNT(*) as total_calls,
                    SUM(llm_tokens_used) as total_tokens,
                    SUM(llm_cost) as total_cost,
                    AVG(llm_tokens_used) as avg_tokens_per_call,
                    AVG(llm_cost) as avg_cost_per_call,
                    COUNT(DISTINCT llm_model) as models_used,
                    COUNT(*) FILTER (WHERE success = true) * 100.0 / COUNT(*) as success_rate
                FROM ask_logs 
                WHERE created_at > now() - interval '30 days' 
                AND llm_tokens_used > 0
            """)
            
            if stats_results:
                row = stats_results[0]
                usage_stats = {
                    'total_calls': int(row[0] or 0),
                    'total_tokens': int(row[1] or 0),
                    'total_cost': float(row[2] or 0),
                    'avg_tokens_per_call': float(row[3] or 0),
                    'avg_cost_per_call': float(row[4] or 0),
                    'models_used': int(row[5] or 0),
                    'success_rate': float(row[6] or 100)
                }
            
            # Recent API calls
            calls_results = db_manager.execute_query("""
                SELECT 
                    question, llm_model, llm_tokens_used, llm_cost,
                    created_at, success, response_time_ms
                FROM ask_logs 
                WHERE created_at > now() - interval '7 days'
                AND llm_tokens_used > 0
                ORDER BY created_at DESC 
                LIMIT 20
            """)
            
            for row in calls_results:
                recent_calls.append({
                    'question': row[0][:100] + '...' if len(row[0]) > 100 else row[0],
                    'model': row[1],
                    'tokens': int(row[2] or 0),
                    'cost': float(row[3] or 0),
                    'timestamp': row[4].strftime('%Y-%m-%d %H:%M') if row[4] else 'N/A',
                    'success': row[5],
                    'response_time': int(row[6] or 0)
                })
        
        return render_template('openai_management_v3.html',
                             openai_status=openai_status,
                             usage_stats=usage_stats,
                             recent_calls=recent_calls,
                             page_title="OpenAI API Management")
    
    except Exception as e:
        logger.error(f"OpenAI management error: {e}")
        return render_template('openai_management_v3.html',
                             error=f"Error loading OpenAI management: {str(e)}",
                             page_title="OpenAI API Management")

@admin_bp_v3.route('/lexml-management')
def lexml_management():
    """Dedicated LexML API management section"""
    try:
        db_manager = get_db_manager()
        
        # Get LexML status
        lexml_status = get_lexml_status()
        
        # Get usage statistics if available
        usage_stats = {}
        recent_calls = []
        
        if db_manager.is_ready():
            try:
                # Check if lexml_api_logs table exists
                stats_results = db_manager.execute_query("""
                    SELECT 
                        COUNT(*) as total_calls,
                        COUNT(*) FILTER (WHERE success = true) as successful_calls,
                        AVG(response_time_ms) as avg_response_time,
                        SUM(documents_found) as total_documents_found
                    FROM lexml_api_logs 
                    WHERE created_at > now() - interval '30 days'
                """)
                
                if stats_results:
                    row = stats_results[0]
                    usage_stats = {
                        'total_calls': int(row[0] or 0),
                        'successful_calls': int(row[1] or 0),
                        'success_rate': (int(row[1] or 0) / max(int(row[0] or 1), 1)) * 100,
                        'avg_response_time': float(row[2] or 0),
                        'total_documents_found': int(row[3] or 0)
                    }
                
                # Recent API calls
                calls_results = db_manager.execute_query("""
                    SELECT 
                        search_query, endpoint, success, response_time_ms,
                        documents_found, created_at, law_type
                    FROM lexml_api_logs 
                    ORDER BY created_at DESC 
                    LIMIT 20
                """)
                
                for row in calls_results:
                    recent_calls.append({
                        'query': row[0][:100] + '...' if row[0] and len(row[0]) > 100 else (row[0] or 'N/A'),
                        'endpoint': row[1],
                        'success': row[2],
                        'response_time': int(row[3] or 0),
                        'documents_found': int(row[4] or 0),
                        'timestamp': row[5].strftime('%Y-%m-%d %H:%M') if row[5] else 'N/A',
                        'law_type': row[6] or 'N/A'
                    })
            except Exception:
                # Table doesn't exist yet
                pass
        
        return render_template('lexml_management_v3.html',
                             lexml_status=lexml_status,
                             usage_stats=usage_stats,
                             recent_calls=recent_calls,
                             page_title="LexML API Management")
    
    except Exception as e:
        logger.error(f"LexML management error: {e}")
        return render_template('lexml_management_v3.html',
                             error=f"Error loading LexML management: {str(e)}",
                             page_title="LexML API Management")

@admin_bp_v3.route('/rag-system')
def rag_system():
    """Comprehensive RAG system management"""
    rag_metrics = {}
    vector_health = {}
    search_distribution = {"semantic": 60, "keyword": 40}
    top_queries = []
    
    try:
        db_manager = get_db_manager()
        conn = db_manager.get_connection() if db_manager.is_ready() else None
        
        # Get RAG performance metrics
        rag_metrics = get_rag_performance_metrics(days=7, conn=conn)
        vector_health = get_vector_database_health(conn=conn)
        
        # Get search type distribution
        if db_manager.is_ready():
            results = db_manager.execute_query("""
                SELECT search_type, COUNT(*) as count
                FROM search_logs
                WHERE created_at > now() - interval '7 days'
                GROUP BY search_type
            """)
            for row in results:
                search_distribution[row[0]] = int(row[1])
        
        # Get top performing queries
        if db_manager.is_ready():
            results = db_manager.execute_query("""
                SELECT 
                    question, COUNT(*) as frequency,
                    AVG(context_found) as avg_context,
                    AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) * 100 as success_rate
                FROM ask_logs 
                WHERE created_at > now() - interval '7 days'
                GROUP BY question
                ORDER BY frequency DESC, success_rate DESC
                LIMIT 10
            """)
            
            for row in results:
                top_queries.append({
                    'question': row[0][:150] + '...' if len(row[0]) > 150 else row[0],
                    'frequency': int(row[1]),
                    'avg_context': float(row[2] or 0),
                    'success_rate': float(row[3] or 0)
                })
        
    except Exception as e:
        logger.error(f"RAG system error: {e}")
    
    return render_template('rag_system_v3.html',
                         rag_metrics=rag_metrics,
                         vector_health=vector_health,
                         search_distribution=search_distribution,
                         top_queries=top_queries,
                         page_title="RAG System Management")

@admin_bp_v3.route('/query-analytics')
def query_analytics():
    """Query analytics and prioritization page."""
    db_manager = get_db_manager()
    
    # Initialize default data
    query_stats = {
        'total_queries': 0,
        'successful_queries': 0,
        'success_rate': 0,
        'total_cost': 0.0,
        'avg_response_time': 0,
        'unique_sessions': 0
    }
    top_queries = []
    query_trends = []
    failed_queries = []
    
    try:
        if db_manager.is_ready():
            # Get basic stats from ask_logs
            stats_results = db_manager.execute_query("""
                SELECT 
                    COUNT(*) as total_queries,
                    COUNT(CASE WHEN success = true THEN 1 END) as successful_queries,
                    AVG(CASE WHEN response_time_ms IS NOT NULL THEN response_time_ms END) as avg_response_time,
                    SUM(CASE WHEN llm_cost IS NOT NULL THEN llm_cost END) as total_cost
                FROM ask_logs
            """)
            
            if stats_results and stats_results[0]:
                row = stats_results[0]
                total = int(row[0] or 0)
                successful = int(row[1] or 0)
                query_stats = {
                    'total_queries': total,
                    'successful_queries': successful,
                    'success_rate': (successful / (total or 1)) * 100,
                    'avg_response_time': float(row[2] or 0),
                    'total_cost': float(row[3] or 0),
                    'unique_sessions': 1  # Simplified
                }
            
            # Get top queries
            top_results = db_manager.execute_query("""
                SELECT 
                    question, COUNT(*) as frequency,
                    AVG(CASE WHEN response_time_ms IS NOT NULL THEN response_time_ms END) as avg_response_time,
                    COUNT(CASE WHEN success = true THEN 1 END) * 100.0 / COUNT(*) as success_rate
                FROM ask_logs 
                GROUP BY question
                ORDER BY frequency DESC
                LIMIT 10
            """)
            
            for row in top_results or []:
                if row and row[0]:
                    top_queries.append({
                        'question': row[0],
                        'frequency': int(row[1] or 0),
                        'avg_response_time': float(row[2] or 0),
                        'success_rate': float(row[3] or 0),
                        'priority_score': int(row[1] or 0) * (float(row[3] or 0) / 100),
                        'avg_context': 3.0  # Mock value
                    })

            # Simple trend data
            query_trends = [{
                'date': '2024-08-20',
                'query_count': query_stats['total_queries'],
                'successful_count': query_stats['successful_queries']
            }]
        
    except Exception as e:
        print(f"Query analytics error: {e}")
        # Keep default fallback data
        
    return render_template('query_analytics_v3.html',
                         page_title='Query Analytics & Prioritization',
                         query_stats=query_stats,
                         top_queries=top_queries,
                         query_trends=query_trends,
                         failed_queries=failed_queries)

@admin_bp_v3.route('/api/knowledge-base/update/<item_id>', methods=['POST'])
def update_knowledge_item(item_id):
    """Update a knowledge base item"""
    try:
        data = request.get_json()
        db_manager = get_db_manager()
        
        if not db_manager.is_ready():
            return jsonify({'success': False, 'error': 'Database not available'})
        
        # Update the item
        from psycopg.types.json import Json
        
        # Prepare metadata
        metadata = {
            'keywords': data.get('keywords', []),
            'source': data.get('source', ''),
            'law_type': data.get('law_type', ''),
            'jurisdiction': data.get('jurisdiction', 'BR'),
            'complexity_level': data.get('complexity_level', 'medium'),
            'tags': data.get('tags', [])
        }
        
        result = db_manager.execute_query("""
            UPDATE legal_chunks 
            SET title = %s, content = %s, category = %s, metadata = %s, updated_at = now()
            WHERE id = %s
        """, (
            data.get('title', ''),
            data.get('content', ''),
            data.get('category', ''),
            Json(metadata),
            item_id
        ))
        
        return jsonify({'success': True, 'message': 'Item updated successfully'})
    
    except Exception as e:
        logger.error(f"Error updating knowledge item {item_id}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@admin_bp_v3.route('/api/lexml/search', methods=['POST'])
def lexml_search():
    """Search LexML API and add results to knowledge base"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        law_type = data.get('law_type', 'lei')
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'})
        
        # Perform LexML search
        results = search_legal_documents(query, law_type=law_type, limit=10)
        
        if not results:
            return jsonify({'success': False, 'error': 'No results found'})
        
        # Add results to knowledge base
        db_manager = get_db_manager()
        added_count = 0
        
        if db_manager.is_ready():
            from psycopg.types.json import Json
            import uuid
            
            for result in results:
                try:
                    # Generate unique ID
                    doc_id = f"lexml_{uuid.uuid4().hex[:8]}"
                    
                    # Prepare metadata
                    metadata = {
                        'source': 'LexML',
                        'law_type': law_type,
                        'jurisdiction': 'BR',
                        'keywords': result.get('keywords', []),
                        'complexity_level': 'medium',
                        'tags': [law_type, 'lexml'],
                        'original_url': result.get('url', ''),
                        'lexml_id': result.get('id', '')
                    }
                    
                    # Insert into database
                    db_manager.execute_query("""
                        INSERT INTO legal_chunks (id, title, content, category, metadata)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, (
                        doc_id,
                        result.get('title', 'Untitled'),
                        result.get('content', ''),
                        result.get('category', 'legislation'),
                        Json(metadata)
                    ))
                    
                    added_count += 1
                except Exception as item_e:
                    logger.error(f"Error adding LexML result: {item_e}")
                    continue
        
        return jsonify({
            'success': True,
            'message': f'Added {added_count} documents from LexML',
            'results_count': len(results),
            'added_count': added_count
        })
    
    except Exception as e:
        logger.error(f"LexML search error: {e}")
        return jsonify({'success': False, 'error': str(e)})

# Error handlers
@admin_bp_v3.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page not found"), 404

@admin_bp_v3.errorhandler(500)
def internal_error(error):
    return render_template('error.html',
                         error_code=500,
                         error_message="Internal server error"), 500
