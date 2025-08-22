"""
Database Utilities Module for JuSimples
Provides reliable database connection and management functions
"""
import os
import logging
import time
from typing import Optional, Dict, Any, Tuple, List

import psycopg
from pgvector.psycopg import register_vector
from psycopg.types.json import Json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EMBED_DIM = 1536  # text-embedding-3-small

class DatabaseManager:
    """Centralized database connection and management"""
    
    def __init__(self):
        self.conn = None
        self.ready = False
        self.last_error = None
        self.connect_attempts = 0
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        
    def get_connection(self, force_new=False) -> Optional[psycopg.Connection]:
        """Get a database connection, creating a new one if needed"""
        if self.conn is None or force_new:
            self.conn = self._establish_connection()
        
        # Verify connection is still valid
        if self.conn:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    cur.fetchone()
                return self.conn
            except Exception as e:
                logger.warning(f"Connection validation failed: {e}")
                self.conn = self._establish_connection()
                
        return self.conn
        
    def _establish_connection(self) -> Optional[psycopg.Connection]:
        """Establish a new database connection with retry logic"""
        self.connect_attempts += 1
        db_url = os.getenv("DATABASE_URL", "").strip()
        
        if not db_url:
            logger.error("❌ DATABASE_URL not set. Set this environment variable.")
            self.last_error = "DATABASE_URL not set"
            self.ready = False
            return None
            
        logger.info(f"Connecting to database (attempt {self.connect_attempts}/{self.max_retries})...")
        
        try:
            # Enhanced connection parameters for better reliability
            conn_params = {
                "application_name": "jusimples_app",
                "connect_timeout": 30,
                "keepalives": 1,
                "keepalives_idle": 60,
                "keepalives_interval": 10,
                "keepalives_count": 3,
                "sslmode": "require",
                "client_encoding": "utf8"
            }
            
            conn = psycopg.connect(db_url, **conn_params)
            conn.autocommit = True
            
            try:
                register_vector(conn)
                logger.info("✅ Vector extension registered successfully")
            except Exception as e:
                logger.warning(f"Failed to register vector extension: {e}")
            
            # Test the connection with a simple query
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version_info = cur.fetchone()
                logger.info(f"✅ Connected to PostgreSQL: {version_info[0] if version_info else 'Unknown version'}")
                
            self.ready = True
            self.last_error = None
            self.connect_attempts = 0
            return conn
            
        except Exception as e:
            self.last_error = str(e)
            logger.error(f"Database connection error: {str(e)}")
            
            if self.connect_attempts < self.max_retries:
                logger.info(f"Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
                return self._establish_connection()
            else:
                logger.error(f"❌ Failed to connect after {self.max_retries} attempts")
                self.ready = False
                return None
    
    def is_ready(self) -> bool:
        """Check if database connection is ready"""
        if not self.ready or not self.conn:
            conn = self.get_connection()
            self.ready = (conn is not None)
        return self.ready
    
    def execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """Execute a query and return all results"""
        conn = self.get_connection()
        if not conn:
            logger.error("Cannot execute query: No database connection")
            return []
        
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                try:
                    results = cur.fetchall()
                    return results
                except psycopg.ProgrammingError:
                    # No results to fetch (e.g., for INSERT/UPDATE/DELETE)
                    return []
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            return []
    
    def execute_transaction(self, queries: List[Tuple[str, tuple]]) -> bool:
        """Execute multiple queries in a transaction"""
        conn = self.get_connection()
        if not conn:
            logger.error("Cannot execute transaction: No database connection")
            return False
        
        try:
            with conn.cursor() as cur:
                for query, params in queries:
                    cur.execute(query, params)
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction error: {str(e)}")
            return False
    
    def initialize_schema(self) -> bool:
        """Initialize the database schema with all required tables"""
        conn = self.get_connection()
        if not conn:
            logger.error("Cannot initialize schema: No database connection")
            return False
        
        try:
            with conn.cursor() as cur:
                # Enable vector extension
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                logger.info("✅ Vector extension enabled")
                
                # Create legal_chunks table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS legal_chunks (
                        id VARCHAR(255) PRIMARY KEY,
                        parent_id VARCHAR(255),
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        category VARCHAR(100),
                        embedding vector(1536),
                        metadata JSONB,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
                    );
                """)
                logger.info("✅ legal_chunks table created/verified")
                
                # Create indexes
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_legal_chunks_category 
                    ON legal_chunks(category);
                """)
                
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_legal_chunks_embedding 
                    ON legal_chunks USING ivfflat (embedding vector_cosine_ops) 
                    WITH (lists = 100);
                """)
                logger.info("✅ Indexes created/verified")
                
                # Create search_logs table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS search_logs (
                        id BIGSERIAL PRIMARY KEY,
                        created_at TIMESTAMPTZ DEFAULT now(),
                        query TEXT,
                        top_k INT,
                        min_relevance DOUBLE PRECISION,
                        search_type TEXT,
                        total INT,
                        result_ids JSONB,
                        user_id TEXT,
                        session_id TEXT,
                        response_time_ms INT,
                        user_agent TEXT,
                        ip_address INET,
                        context_found INT DEFAULT 0,
                        category TEXT,
                        success BOOLEAN DEFAULT true
                    );
                """)
                
                # Create ask_logs table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS ask_logs (
                        id BIGSERIAL PRIMARY KEY,
                        created_at TIMESTAMPTZ DEFAULT now(),
                        question TEXT,
                        answer TEXT,
                        top_k INT,
                        min_relevance DOUBLE PRECISION,
                        total_sources INT,
                        result_ids JSONB,
                        user_id TEXT,
                        session_id TEXT,
                        response_time_ms INT,
                        user_agent TEXT,
                        ip_address INET,
                        context_found INT DEFAULT 0,
                        search_type TEXT DEFAULT 'keyword',
                        llm_model TEXT,
                        llm_tokens_used INT,
                        llm_cost DECIMAL(10,6),
                        input_tokens INT DEFAULT 0,
                        output_tokens INT DEFAULT 0,
                        finish_reason TEXT,
                        system_fingerprint TEXT,
                        response_id TEXT,
                        created_timestamp INT,
                        logprobs TEXT,
                        category TEXT,
                        success BOOLEAN DEFAULT true,
                        error_message TEXT
                    );
                """)
                
                # Create API usage tracking
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS api_usage_logs (
                        id BIGSERIAL PRIMARY KEY,
                        created_at TIMESTAMPTZ DEFAULT now(),
                        endpoint TEXT,
                        method TEXT,
                        status_code INT,
                        response_time_ms INT,
                        user_id TEXT,
                        session_id TEXT,
                        ip_address INET,
                        user_agent TEXT,
                        request_size_bytes INT,
                        response_size_bytes INT,
                        error_message TEXT
                    );
                """)
                
                # Create query analytics
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS query_analytics (
                        id BIGSERIAL PRIMARY KEY,
                        query_normalized TEXT UNIQUE,
                        total_count INT DEFAULT 1,
                        last_queried TIMESTAMPTZ DEFAULT now(),
                        avg_response_time_ms DECIMAL(10,2),
                        success_rate DECIMAL(5,2),
                        categories JSONB DEFAULT '[]'::jsonb,
                        related_queries JSONB DEFAULT '[]'::jsonb,
                        trending_score DECIMAL(10,2) DEFAULT 0,
                        created_at TIMESTAMPTZ DEFAULT now(),
                        updated_at TIMESTAMPTZ DEFAULT now()
                    );
                """)
                
                # Create system metrics
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS system_metrics (
                        id BIGSERIAL PRIMARY KEY,
                        recorded_at TIMESTAMPTZ DEFAULT now(),
                        metric_type TEXT,
                        metric_name TEXT,
                        value DECIMAL(15,4),
                        unit TEXT,
                        metadata JSONB
                    );
                """)
                
                # Create user sessions
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        id BIGSERIAL PRIMARY KEY,
                        session_id TEXT UNIQUE,
                        user_id TEXT,
                        started_at TIMESTAMPTZ DEFAULT now(),
                        last_activity TIMESTAMPTZ DEFAULT now(),
                        ip_address INET,
                        user_agent TEXT,
                        total_queries INT DEFAULT 0,
                        total_time_seconds INT DEFAULT 0,
                        pages_visited JSONB DEFAULT '[]'::jsonb,
                        ended_at TIMESTAMPTZ
                    );
                """)
                
                # Create OpenAI API logs
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS openai_usage_logs (
                        id BIGSERIAL PRIMARY KEY,
                        created_at TIMESTAMPTZ DEFAULT now(),
                        request_id TEXT,
                        model TEXT,
                        prompt_tokens INT DEFAULT 0,
                        completion_tokens INT DEFAULT 0,
                        total_tokens INT DEFAULT 0,
                        cost DECIMAL(10,6) DEFAULT 0,
                        finish_reason TEXT,
                        system_fingerprint TEXT,
                        response_time_ms INT DEFAULT 0,
                        success BOOLEAN DEFAULT true,
                        error_message TEXT,
                        endpoint TEXT,
                        session_id TEXT,
                        user_id TEXT,
                        prompt_preview TEXT,
                        response_preview TEXT
                    );
                """)
                
                # Create LexML API logs
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS lexml_api_logs (
                        id BIGSERIAL PRIMARY KEY,
                        created_at TIMESTAMPTZ DEFAULT now(),
                        endpoint TEXT,
                        request_params JSONB DEFAULT '{}'::jsonb,
                        response_data JSONB DEFAULT '{}'::jsonb,
                        response_time_ms INT DEFAULT 0,
                        success BOOLEAN DEFAULT true,
                        error_message TEXT,
                        documents_found INT DEFAULT 0,
                        session_id TEXT,
                        user_id TEXT,
                        law_type TEXT,
                        search_query TEXT
                    );
                """)
                
                # Create vector index
                try:
                    cur.execute("""
                        CREATE INDEX IF NOT EXISTS legal_chunks_embedding_ivfflat_cos
                        ON legal_chunks
                        USING ivfflat (embedding vector_cosine_ops)
                        WITH (lists = 100);
                    """)
                except Exception as e:
                    logger.warning(f"Could not create IVFFlat index: {e}")
                
                logger.info("✅ All database tables created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Schema initialization error: {str(e)}")
            return False
        
    def admin_db_overview(self) -> Dict[str, Any]:
        """Get database overview statistics for admin dashboard"""
        if not self.is_ready():
            return {"status": "database_not_ready", "error": self.last_error}
        
        try:
            counts = {}
            tables = [
                "legal_chunks", "search_logs", "ask_logs", "query_analytics",
                "user_sessions", "openai_usage_logs", "lexml_api_logs", "system_metrics"
            ]
            
            for table in tables:
                try:
                    results = self.execute_query(f"SELECT COUNT(*) FROM {table}")
                    count = results[0][0] if results else 0
                    counts[table] = count
                except Exception as e:
                    logger.warning(f"Could not count {table}: {e}")
                    counts[table] = 0
            
            # Get vector status
            vector_status = {}
            try:
                results = self.execute_query(
                    "SELECT COUNT(*) FROM legal_chunks WHERE embedding IS NOT NULL"
                )
                vector_status["embedded_docs"] = results[0][0] if results else 0
                
                results = self.execute_query(
                    "SELECT COUNT(*) FROM legal_chunks WHERE embedding IS NULL"
                )
                vector_status["missing_embeddings"] = results[0][0] if results else 0
                
                total_docs = vector_status["embedded_docs"] + vector_status["missing_embeddings"]
                if total_docs > 0:
                    vector_status["embedding_coverage"] = round(
                        (vector_status["embedded_docs"] / total_docs) * 100, 2
                    )
                else:
                    vector_status["embedding_coverage"] = 0
                    
            except Exception as e:
                logger.warning(f"Could not get vector status: {e}")
                vector_status = {"error": str(e)}
            
            # Get recent queries
            recent_queries = []
            try:
                results = self.execute_query(
                    """
                    SELECT query, created_at, search_type, success
                    FROM search_logs
                    ORDER BY created_at DESC
                    LIMIT 5
                    """
                )
                
                for row in results:
                    recent_queries.append({
                        "query": row[0],
                        "time": row[1].isoformat() if row[1] else None,
                        "type": row[2],
                        "success": row[3]
                    })
            except Exception as e:
                logger.warning(f"Could not get recent queries: {e}")
            
            return {
                "status": "success",
                "counts": counts,
                "vector_status": vector_status,
                "recent_queries": recent_queries
            }
            
        except Exception as e:
            logger.error(f"Error getting DB overview: {str(e)}")
            return {"status": "error", "message": str(e)}

# Create a singleton instance to be imported by other modules
db_manager = DatabaseManager()

def get_db_manager() -> DatabaseManager:
    """Get the database manager singleton instance"""
    return db_manager

# Convenience functions to match existing API
def get_connection() -> Optional[psycopg.Connection]:
    """Get a database connection"""
    return db_manager.get_connection()

def is_ready() -> bool:
    """Check if database connection is ready"""
    return db_manager.is_ready()

def initialize_schema() -> bool:
    """Initialize database schema"""
    return db_manager.initialize_schema()

def admin_db_overview() -> Dict[str, Any]:
    """Get database overview for admin dashboard"""
    return db_manager.admin_db_overview()
