"""
Query Storage and Analytics Module for JuSimples
Handles all query logging and analytics functionality
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import psycopg
from psycopg.types.json import Json
from db_utils import get_db_manager

logger = logging.getLogger(__name__)

class QueryStorage:
    """Handles storage and retrieval of user queries and analytics"""
    
    def __init__(self):
        self.db_manager = get_db_manager()
        
    def save_query(self, 
                   question: str, 
                   answer: str,
                   context_docs: List[Dict],
                   search_type: str = "keyword",
                   user_info: Dict = None,
                   api_metrics: Dict = None) -> bool:
        """Save a complete query with all associated data"""
        try:
            if not self.db_manager.is_ready():
                logger.error("Database not ready for query storage")
                return False
                
            conn = self.db_manager.get_connection()
            if not conn:
                logger.error("No database connection available")
                return False
                
            # Extract user information
            user_id = user_info.get('user_id') if user_info else None
            session_id = user_info.get('session_id') if user_info else None
            ip_address = user_info.get('ip_address') if user_info else None
            user_agent = user_info.get('user_agent') if user_info else None
            
            # Extract API metrics
            response_time_ms = api_metrics.get('response_time_ms', 0) if api_metrics else 0
            llm_model = api_metrics.get('model', 'gpt-4o-mini') if api_metrics else 'gpt-4o-mini'
            tokens_used = api_metrics.get('tokens_used', 0) if api_metrics else 0
            input_tokens = api_metrics.get('input_tokens', 0) if api_metrics else 0
            output_tokens = api_metrics.get('output_tokens', 0) if api_metrics else 0
            cost = api_metrics.get('cost', 0.0) if api_metrics else 0.0
            
            # Extract document IDs
            result_ids = [doc.get('id', '') for doc in context_docs if doc.get('id')]
            
            with conn.cursor() as cur:
                # Save to ask_logs
                cur.execute("""
                    INSERT INTO ask_logs (
                        question, answer, search_type, result_ids, total_sources,
                        user_id, session_id, ip_address, user_agent,
                        response_time_ms, llm_model, llm_tokens_used, llm_cost,
                        input_tokens, output_tokens, context_found, success
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    question, answer, search_type, Json(result_ids), len(result_ids),
                    user_id, session_id, ip_address, user_agent,
                    response_time_ms, llm_model, tokens_used, cost,
                    input_tokens, output_tokens, len(context_docs), True
                ))
                
                query_id = cur.fetchone()[0]
                
                # Update query analytics
                normalized_query = self._normalize_query(question)
                cur.execute("""
                    INSERT INTO query_analytics (query_normalized, total_count, avg_response_time_ms)
                    VALUES (%s, 1, %s)
                    ON CONFLICT (query_normalized) DO UPDATE
                    SET total_count = query_analytics.total_count + 1,
                        last_queried = now(),
                        avg_response_time_ms = (
                            (COALESCE(query_analytics.avg_response_time_ms, 0) * query_analytics.total_count + %s) / 
                            (query_analytics.total_count + 1)
                        ),
                        updated_at = now()
                """, (normalized_query, response_time_ms, response_time_ms))
                
            conn.commit()
            logger.info(f"✅ Query saved successfully with ID: {query_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save query: {e}")
            return False
    
    def _normalize_query(self, query: str) -> str:
        """Normalize query for analytics"""
        # Remove extra spaces and convert to lowercase
        normalized = ' '.join(query.lower().split())
        # Truncate to reasonable length
        return normalized[:500]
    
    def get_top_queries(self, limit: int = 20, days: int = 30) -> List[Dict]:
        """Get top queries by frequency"""
        try:
            if not self.db_manager.is_ready():
                return []
                
            conn = self.db_manager.get_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        query_normalized,
                        total_count,
                        last_queried,
                        avg_response_time_ms,
                        success_rate
                    FROM query_analytics
                    WHERE last_queried > now() - interval '%s days'
                    ORDER BY total_count DESC
                    LIMIT %s
                """, (days, limit))
                
                results = []
                for row in cur.fetchall():
                    results.append({
                        'query': row[0],
                        'count': row[1],
                        'last_asked': row[2].isoformat() if row[2] else None,
                        'avg_response_time': float(row[3]) if row[3] else 0,
                        'success_rate': float(row[4]) if row[4] else 100
                    })
                    
                return results
                
        except Exception as e:
            logger.error(f"Failed to get top queries: {e}")
            return []
    
    def get_recent_queries(self, limit: int = 50) -> List[Dict]:
        """Get recent queries with full details"""
        try:
            if not self.db_manager.is_ready():
                return []
                
            conn = self.db_manager.get_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        id,
                        created_at,
                        question,
                        answer,
                        search_type,
                        context_found,
                        response_time_ms,
                        llm_model,
                        llm_tokens_used,
                        llm_cost,
                        user_id,
                        session_id
                    FROM ask_logs
                    ORDER BY created_at DESC
                    LIMIT %s
                """, (limit,))
                
                results = []
                for row in cur.fetchall():
                    results.append({
                        'id': row[0],
                        'timestamp': row[1].isoformat() if row[1] else None,
                        'question': row[2],
                        'answer': row[3][:200] + '...' if row[3] and len(row[3]) > 200 else row[3],
                        'search_type': row[4],
                        'context_found': row[5],
                        'response_time_ms': row[6],
                        'model': row[7],
                        'tokens': row[8],
                        'cost': float(row[9]) if row[9] else 0,
                        'user_id': row[10],
                        'session_id': row[11]
                    })
                    
                return results
                
        except Exception as e:
            logger.error(f"Failed to get recent queries: {e}")
            return []
    
    def get_query_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get comprehensive query statistics"""
        try:
            if not self.db_manager.is_ready():
                return {}
                
            conn = self.db_manager.get_connection()
            stats = {}
            
            with conn.cursor() as cur:
                # Total queries
                cur.execute("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(*) FILTER (WHERE created_at > now() - interval '%s days') as recent,
                        AVG(response_time_ms) as avg_response_time,
                        SUM(llm_cost) as total_cost,
                        SUM(llm_tokens_used) as total_tokens
                    FROM ask_logs
                """, (days,))
                
                row = cur.fetchone()
                stats['total_queries'] = row[0] or 0
                stats['recent_queries'] = row[1] or 0
                stats['avg_response_time'] = float(row[2]) if row[2] else 0
                stats['total_cost'] = float(row[3]) if row[3] else 0
                stats['total_tokens'] = row[4] or 0
                
                # Success rate
                cur.execute("""
                    SELECT 
                        COUNT(*) FILTER (WHERE success = true) * 100.0 / NULLIF(COUNT(*), 0) as success_rate
                    FROM ask_logs
                    WHERE created_at > now() - interval '%s days'
                """, (days,))
                
                row = cur.fetchone()
                stats['success_rate'] = float(row[0]) if row[0] else 100
                
                # Search type distribution
                cur.execute("""
                    SELECT 
                        search_type,
                        COUNT(*) as count
                    FROM ask_logs
                    WHERE created_at > now() - interval '%s days'
                    GROUP BY search_type
                """, (days,))
                
                search_types = {}
                for row in cur.fetchall():
                    search_types[row[0] or 'unknown'] = row[1]
                stats['search_types'] = search_types
                
                # Hourly distribution
                cur.execute("""
                    SELECT 
                        EXTRACT(hour FROM created_at) as hour,
                        COUNT(*) as count
                    FROM ask_logs
                    WHERE created_at > now() - interval '%s days'
                    GROUP BY hour
                    ORDER BY hour
                """, (days,))
                
                hourly = {}
                for row in cur.fetchall():
                    hourly[int(row[0])] = row[1]
                stats['hourly_distribution'] = hourly
                
                return stats
                
        except Exception as e:
            logger.error(f"Failed to get query stats: {e}")
            return {}

# Global instance
query_storage = QueryStorage()
