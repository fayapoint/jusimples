# Additional analytics and monitoring functions for JuSimples
import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import psycopg
from psycopg.types.json import Json

LOGGER = logging.getLogger(__name__)

def log_ask_advanced(question: str, answer: str, top_k: int, min_relevance: float, 
                    result_ids: List[str], search_type: str, success: bool, 
                    session_id: str = None, user_id: str = None, response_time_ms: int = 0,
                    llm_model: str = None, llm_tokens_used: int = 0, llm_cost: float = 0.0,
                    user_agent: str = None, ip_address: str = None, context_found: int = 0,
                    input_tokens: int = 0, output_tokens: int = 0, finish_reason: str = None,
                    system_fingerprint: str = None, response_id: str = None, 
                    created_timestamp: int = None, logprobs: str = None, conn=None) -> bool:
    """Enhanced ask logging with comprehensive OpenAI analytics"""
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            # First ensure all columns exist
            try:
                cur.execute("""
                    ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS response_id VARCHAR(255);
                    ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS created_timestamp INTEGER;
                    ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS logprobs TEXT;
                """)
            except Exception as schema_e:
                LOGGER.warning(f"Schema update failed (may already exist): {schema_e}")
            
            # Insert into ask_logs with comprehensive OpenAI analytics
            cur.execute("""
                INSERT INTO ask_logs (
                    question, answer, top_k, min_relevance, result_ids, search_type, 
                    success, session_id, user_id, response_time_ms, llm_model, 
                    llm_tokens_used, llm_cost, user_agent, ip_address, context_found,
                    input_tokens, output_tokens, finish_reason, system_fingerprint,
                    response_id, created_timestamp, logprobs
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                question, answer, top_k, min_relevance, Json(result_ids), search_type,
                success, session_id, user_id, response_time_ms, llm_model,
                llm_tokens_used, llm_cost, user_agent, ip_address, context_found,
                input_tokens, output_tokens, finish_reason, system_fingerprint,
                response_id, created_timestamp, logprobs
            ))
        conn.commit()
        
        LOGGER.info(f"✅ Advanced ask logged: question={question[:50]}..., tokens={llm_tokens_used}, cost=${llm_cost:.4f}, model={llm_model}")
        return True
    except Exception as e:
        LOGGER.error(f"Failed to log advanced ask: {e}")
        return False


def log_search_advanced(query: str, top_k: int, min_relevance: float, 
                       result_ids: List[str], search_type: str, success: bool,
                       session_id: str = None, user_id: str = None, response_time_ms: int = 0,
                       user_agent: str = None, ip_address: str = None, context_found: int = 0,
                       conn=None) -> bool:
    """Enhanced search logging with comprehensive analytics"""
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            # Insert into search_logs with all new fields  
            cur.execute("""
                INSERT INTO search_logs (
                    query, top_k, min_relevance, result_ids, search_type,
                    success, session_id, user_id, response_time_ms,
                    user_agent, ip_address, context_found
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                query, top_k, min_relevance, Json(result_ids), search_type,
                success, session_id, user_id, response_time_ms,
                user_agent, ip_address, context_found
            ))
        conn.commit()
        
        LOGGER.info(f"✅ Advanced search logged: query={query[:50]}..., results={context_found}")
        return True
    except Exception as e:
        LOGGER.error(f"Failed to log advanced search: {e}")
        return False


def get_rag_performance_metrics(days: int = 7, conn=None) -> Dict[str, Any]:
    """Get comprehensive RAG performance metrics"""
    if not conn:
        return {}
    
    try:
        # First ensure the necessary columns exist
        with conn.cursor() as cur:
            try:
                # Add error_message column to ask_logs if it doesn't exist
                cur.execute("""
                    ALTER TABLE ask_logs ADD COLUMN IF NOT EXISTS error_message TEXT;
                """)
                conn.commit()
                LOGGER.info("✅ Added error_message column to ask_logs table")
            except Exception as schema_e:
                LOGGER.warning(f"Schema update failed: {schema_e}")
        
        with conn.cursor() as cur:
            # Vector search performance
            cur.execute("""
                SELECT 
                    COUNT(*) as total_vector_searches,
                    COUNT(*) FILTER (WHERE search_type = 'semantic') as semantic_searches,
                    COUNT(*) FILTER (WHERE search_type = 'keyword') as keyword_searches,
                    AVG(response_time_ms) FILTER (WHERE search_type = 'semantic') as avg_semantic_time,
                    AVG(response_time_ms) FILTER (WHERE search_type = 'keyword') as avg_keyword_time,
                    AVG(context_found) as avg_context_found
                FROM search_logs 
                WHERE created_at > now() - interval '%s days'
            """, (days,))
            
            search_metrics = cur.fetchone()
            
            # LLM performance 
            cur.execute("""
                SELECT 
                    COUNT(*) as total_llm_calls,
                    SUM(llm_tokens_used) as total_tokens,
                    SUM(llm_cost) as total_cost,
                    AVG(llm_tokens_used) as avg_tokens_per_request,
                    AVG(llm_cost) as avg_cost_per_request,
                    AVG(response_time_ms) as avg_llm_response_time,
                    COUNT(DISTINCT llm_model) as models_used,
                    COUNT(*) FILTER (WHERE success = true) * 100.0 / COUNT(*) as success_rate
                FROM ask_logs 
                WHERE created_at > now() - interval '%s days' AND llm_tokens_used > 0
            """, (days,))
            
            llm_metrics = cur.fetchone()
            
            # Context quality metrics
            cur.execute("""
                SELECT 
                    AVG(context_found) as avg_documents_retrieved,
                    COUNT(*) FILTER (WHERE context_found = 0) * 100.0 / COUNT(*) as no_context_rate,
                    COUNT(*) FILTER (WHERE context_found >= 3) * 100.0 / COUNT(*) as good_context_rate
                FROM ask_logs 
                WHERE created_at > now() - interval '%s days'
            """, (days,))
            
            context_metrics = cur.fetchone()
            
            # Popular failure patterns - handle case where error_message column might not exist yet
            try:
                cur.execute("""
                    SELECT error_message, COUNT(*) as error_count
                    FROM ask_logs 
                    WHERE created_at > now() - interval '%s days' 
                    AND success = false 
                    AND error_message IS NOT NULL
                    GROUP BY error_message 
                    ORDER BY error_count DESC 
                    LIMIT 5
                """, (days,))
                
                error_patterns = [{"error": row[0], "count": int(row[1])} for row in cur.fetchall()]
            except Exception as error_query_e:
                LOGGER.warning(f"Error fetching failure patterns: {error_query_e}")
                error_patterns = []
            
            return {
                "vector_search": {
                    "total_searches": int(search_metrics[0] or 0),
                    "semantic_searches": int(search_metrics[1] or 0),
                    "keyword_searches": int(search_metrics[2] or 0),
                    "avg_semantic_time_ms": float(search_metrics[3] or 0),
                    "avg_keyword_time_ms": float(search_metrics[4] or 0),
                    "avg_context_found": float(search_metrics[5] or 0)
                },
                "llm_performance": {
                    "total_calls": int(llm_metrics[0] or 0),
                    "total_tokens": int(llm_metrics[1] or 0),
                    "total_cost": float(llm_metrics[2] or 0),
                    "avg_tokens_per_request": float(llm_metrics[3] or 0),
                    "avg_cost_per_request": float(llm_metrics[4] or 0),
                    "avg_response_time_ms": float(llm_metrics[5] or 0),
                    "models_used": int(llm_metrics[6] or 0),
                    "success_rate": float(llm_metrics[7] or 100)
                },
                "context_quality": {
                    "avg_documents_retrieved": float(context_metrics[0] or 0),
                    "no_context_rate": float(context_metrics[1] or 0),
                    "good_context_rate": float(context_metrics[2] or 0)
                },
                "error_patterns": error_patterns
            }
    except Exception as e:
        LOGGER.error(f"Failed to get RAG performance metrics: {e}")
        return {}


def get_api_library_metrics(days: int = 7, conn=None) -> Dict[str, Any]:
    """Get metrics for external API library usage (lexml, etc.)"""
    if not conn:
        return {}
    
    try:
        with conn.cursor() as cur:
            # Get API usage from api_usage_logs if table exists
            try:
                cur.execute("""
                    SELECT 
                        api_name,
                        COUNT(*) as total_calls,
                        COUNT(*) FILTER (WHERE success = true) as successful_calls,
                        AVG(response_time_ms) as avg_response_time,
                        SUM(cost) as total_cost
                    FROM api_usage_logs 
                    WHERE created_at > now() - interval '%s days'
                    GROUP BY api_name
                    ORDER BY total_calls DESC
                """, (days,))
                
                api_metrics = [
                    {
                        "api_name": row[0],
                        "total_calls": int(row[1]),
                        "successful_calls": int(row[2]),
                        "success_rate": (int(row[2]) / int(row[1]) * 100) if int(row[1]) > 0 else 0,
                        "avg_response_time": float(row[3] or 0),
                        "total_cost": float(row[4] or 0)
                    }
                    for row in cur.fetchall()
                ]
                
                # Get error patterns for APIs
                cur.execute("""
                    SELECT api_name, error_message, COUNT(*) as error_count
                    FROM api_usage_logs 
                    WHERE created_at > now() - interval '%s days' 
                    AND success = false 
                    AND error_message IS NOT NULL
                    GROUP BY api_name, error_message 
                    ORDER BY error_count DESC 
                    LIMIT 10
                """, (days,))
                
                api_errors = [
                    {
                        "api_name": row[0],
                        "error": row[1],
                        "count": int(row[2])
                    }
                    for row in cur.fetchall()
                ]
                
            except psycopg.ProgrammingError:
                # api_usage_logs table doesn't exist yet
                api_metrics = []
                api_errors = []
            
            return {
                "api_metrics": api_metrics,
                "api_errors": api_errors,
                "total_apis": len(api_metrics),
                "period_days": days
            }
    except Exception as e:
        LOGGER.error(f"Failed to get API library metrics: {e}")
        return {}


def log_api_usage(api_name: str, endpoint: str, success: bool, response_time_ms: int,
                 cost: float = 0.0, error_message: str = None, request_data: Dict = None,
                 response_data: Dict = None, conn=None) -> bool:
    """Log external API usage (lexml, etc.)"""
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            # Create api_usage_logs table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS api_usage_logs (
                    id SERIAL PRIMARY KEY,
                    api_name VARCHAR(100) NOT NULL,
                    endpoint VARCHAR(255),
                    success BOOLEAN NOT NULL DEFAULT true,
                    response_time_ms INTEGER,
                    cost DECIMAL(10,6) DEFAULT 0.0,
                    error_message TEXT,
                    request_data JSONB,
                    response_data JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
                );
            """)
            
            # Insert the log entry
            cur.execute("""
                INSERT INTO api_usage_logs (
                    api_name, endpoint, success, response_time_ms, cost,
                    error_message, request_data, response_data
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                api_name, endpoint, success, response_time_ms, cost,
                error_message, Json(request_data or {}), Json(response_data or {})
            ))
        conn.commit()
        return True
    except Exception as e:
        LOGGER.error(f"Failed to log API usage: {e}")
        return False


def get_vector_database_health(conn=None) -> Dict[str, Any]:
    """Get pgvector database health and performance metrics"""
    if not conn:
        return {}
    
    try:
        with conn.cursor() as cur:
            # Get vector index stats
            cur.execute("""
                SELECT 
                    schemaname, tablename, indexname, 
                    idx_tup_read, idx_tup_fetch
                FROM pg_stat_user_indexes 
                WHERE indexname LIKE '%embedding%' OR indexname LIKE '%vector%'
            """)
            
            vector_indexes = [
                {
                    "schema": row[0],
                    "table": row[1], 
                    "index": row[2],
                    "reads": int(row[3] or 0),
                    "fetches": int(row[4] or 0)
                }
                for row in cur.fetchall()
            ]
            
            # Get table sizes
            cur.execute("""
                SELECT 
                    schemaname, tablename, 
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                    pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
                FROM pg_tables 
                WHERE tablename IN ('legal_chunks', 'search_logs', 'ask_logs')
            """)
            
            table_sizes = [
                {
                    "schema": row[0],
                    "table": row[1],
                    "size": row[2],
                    "size_bytes": int(row[3])
                }
                for row in cur.fetchall()
            ]
            
            # Get document counts and embedding status
            try:
                cur.execute("SELECT COUNT(*) FROM legal_chunks WHERE embedding IS NOT NULL")
                embedded_docs = int(cur.fetchone()[0])
                
                cur.execute("SELECT COUNT(*) FROM legal_chunks WHERE embedding IS NULL")
                missing_embeddings = int(cur.fetchone()[0])
            except:
                embedded_docs = 0
                missing_embeddings = 0
            
            return {
                "vector_indexes": vector_indexes,
                "table_sizes": table_sizes,
                "embedding_status": {
                    "embedded_documents": embedded_docs,
                    "missing_embeddings": missing_embeddings,
                    "embedding_coverage": (embedded_docs / (embedded_docs + missing_embeddings) * 100) if (embedded_docs + missing_embeddings) > 0 else 0
                }
            }
    except Exception as e:
        LOGGER.error(f"Failed to get vector database health: {e}")
        return {}
