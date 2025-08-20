import os
import logging
import uuid
from typing import List, Dict, Any, Optional

import psycopg  # psycopg 3
from psycopg.types.json import Json
from pgvector.psycopg import register_vector
from openai import OpenAI

LOGGER = logging.getLogger(__name__)

EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBED_DIM = 1536  # text-embedding-3-small

_CONN = None
_READY = False
_OPENAI: Optional[OpenAI] = None


def _get_openai() -> Optional[OpenAI]:
    global _OPENAI
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "your_openai_api_key_here":
        return None
    if _OPENAI is None:
        try:
            _OPENAI = OpenAI(api_key=api_key)
        except Exception as e:
            LOGGER.error(f"Failed to init OpenAI for embeddings: {e}")
            _OPENAI = None
    return _OPENAI


def _connect() -> Optional[psycopg.Connection]:
    global _CONN
    db_url = os.getenv("DATABASE_URL", "").strip()
    if not db_url:
        LOGGER.info("DATABASE_URL not set; semantic retrieval disabled")
        return None
    
    # Log more details about the connection attempt (sanitized)
    masked_url = "*****" + db_url[-20:] if len(db_url) > 20 else "[masked]"
    LOGGER.info(f"Attempting database connection with URL ending in: {masked_url}")
    
    try:
        LOGGER.info("Establishing PostgreSQL connection...")
        
        # Enhanced connection parameters for Supabase pooler compatibility
        conn_params = {
            "application_name": "jusimples_app",
            "connect_timeout": 30,              # Increased timeout for better reliability
            "keepalives": 1,
            "keepalives_idle": 60,
            "keepalives_interval": 10,
            "keepalives_count": 3,
            "sslmode": "require",               # Ensure SSL is used
            "client_encoding": "utf8"           # Explicit encoding
        }
        
        # For pooled connections, we need to handle the connection more carefully
        conn = psycopg.connect(db_url, **conn_params)
        
        LOGGER.info("PostgreSQL connection successful!")
        
        # Set autocommit for better pooler compatibility
        conn.autocommit = True
        
        # Register vector type
        try:
            register_vector(conn)
            LOGGER.info("Vector extension registered successfully")
        except Exception as e:
            LOGGER.warning(f"Failed to register vector extension: {e}")
        
        # Test the connection with a simple query
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version_info = cur.fetchone()
            LOGGER.info(f"Connected to PostgreSQL: {version_info[0] if version_info else 'Unknown version'}")
            
        return conn
    except Exception as e:
        LOGGER.error(f"Database connection error: {str(e)}")
        
        # Enhanced error diagnosis
        error_str = str(e).lower()
        if "timeout" in error_str or "timed out" in error_str:
            LOGGER.error("⚠️  Connection timeout - check network connectivity and firewall settings")
            LOGGER.error("💡 Try: 1) Check internet connection, 2) Verify Supabase project is active")
        elif "authentication" in error_str or "password" in error_str or "auth" in error_str:
            LOGGER.error("🔐 Authentication failed - check DATABASE_URL credentials")
            LOGGER.error("💡 Verify: 1) Password is correct, 2) User has proper permissions")
        elif "database" in error_str and ("not exist" in error_str or "does not exist" in error_str):
            LOGGER.error("🗄️  Database does not exist - check database name in DATABASE_URL")
        elif "connection refused" in error_str or "could not connect" in error_str:
            LOGGER.error("🚫 Connection refused - check host and port in DATABASE_URL")
            LOGGER.error("💡 Verify: 1) Host is reachable, 2) Port 6543 is correct for pooler")
        elif "ssl" in error_str:
            LOGGER.error("🔒 SSL connection issue - check SSL configuration")
        else:
            LOGGER.error(f"❓ Unknown connection error: {type(e).__name__}")
            
        return None


def init_pgvector() -> bool:
    """Initialize pgvector schema and table. Returns True if ready."""
    global _CONN, _READY
    if _READY:
        LOGGER.info("pgvector already initialized and ready")
        return True

    LOGGER.info("Initializing pgvector connection...")
    _CONN = _connect()
    if not _CONN:
        LOGGER.error("Failed to establish database connection, pgvector initialization failed")
        _READY = False
        return False
    
    LOGGER.info("Database connection established, proceeding with table creation/verification...")
    

    try:
        with _CONN.cursor() as cur:
            # Try to enable extension; ignore if not permitted
            try:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            except Exception as ext_err:
                LOGGER.warning(f"Could not create extension 'vector': {ext_err}")

            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS legal_chunks (
                    id TEXT PRIMARY KEY,
                    parent_id TEXT,
                    title TEXT,
                    content TEXT,
                    category TEXT,
                    metadata JSONB,
                    embedding vector({EMBED_DIM})
                );
                """
            )

            # Enhanced analytics tables
            cur.execute(
                """
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
                    category TEXT,
                    success BOOLEAN DEFAULT true
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ask_logs (
                    id BIGSERIAL PRIMARY KEY,
                    created_at TIMESTAMPTZ DEFAULT now(),
                    question TEXT,
                    top_k INT,
                    min_relevance DOUBLE PRECISION,
                    total_sources INT,
                    result_ids JSONB,
                    user_id TEXT,
                    session_id TEXT,
                    response_time_ms INT,
                    llm_model TEXT,
                    llm_tokens_used INT,
                    llm_cost DECIMAL(10,6),
                    category TEXT,
                    success BOOLEAN DEFAULT true,
                    error_message TEXT
                );
                """
            )
            
            # API usage tracking
            cur.execute(
                """
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
                """
            )
            
            # Popular queries and trending topics
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS query_analytics (
                    id BIGSERIAL PRIMARY KEY,
                    query_normalized TEXT UNIQUE,
                    total_count INT DEFAULT 1,
                    last_queried TIMESTAMPTZ DEFAULT now(),
                    avg_response_time_ms DECIMAL(10,2),
                    success_rate DECIMAL(5,2),
                    categories JSONB,
                    related_queries JSONB,
                    created_at TIMESTAMPTZ DEFAULT now(),
                    updated_at TIMESTAMPTZ DEFAULT now()
                );
                """
            )
            
            # System performance metrics
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id BIGSERIAL PRIMARY KEY,
                    recorded_at TIMESTAMPTZ DEFAULT now(),
                    metric_type TEXT,
                    metric_name TEXT,
                    value DECIMAL(15,4),
                    unit TEXT,
                    metadata JSONB
                );
                """
            )
            
            # User sessions tracking
            cur.execute(
                """
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
                    pages_visited JSONB,
                    ended_at TIMESTAMPTZ
                );
                """
            )

            # Performance: IVFFlat cosine index (no-op if not supported)
            try:
                cur.execute(
                    """
                    CREATE INDEX IF NOT EXISTS legal_chunks_embedding_ivfflat_cos
                    ON legal_chunks
                    USING ivfflat (embedding vector_cosine_ops)
                    WITH (lists = 100);
                    """
                )
            except Exception as e:
                LOGGER.warning(f"Could not create IVFFlat index: {e}")
        _READY = True
        LOGGER.info("pgvector ready: table legal_chunks available")
        return True
    except Exception as e:
        LOGGER.error(f"Failed to initialize pgvector schema: {e}")
        _READY = False
        return False


def _ensure_connection() -> bool:
    """Ensure we have a valid database connection, reconnecting if needed"""
    global _CONN, _READY
    
    # If we don't have a connection or _READY is False, try to connect
    if _CONN is None or not _READY:
        LOGGER.info("No active connection, attempting to connect")
        _CONN = _connect()
        _READY = (_CONN is not None)
        return _READY
    
    # If we have a connection, check if it's still valid
    try:
        with _CONN.cursor() as cur:
            cur.execute("SELECT 1;")
            # Connection is good
            return True
    except Exception as e:
        LOGGER.warning(f"Connection check failed: {e}. Attempting to reconnect...")
        try:
            # Connection might be stale, try to close it first
            try:
                _CONN.close()
            except:
                pass
                
            # Try to connect again
            _CONN = _connect()
            _READY = (_CONN is not None)
            return _READY
        except Exception as reconnect_err:
            LOGGER.error(f"Reconnection failed: {reconnect_err}")
            _READY = False
            return False


def is_ready() -> bool:
    """Check if the database connection is ready"""
    # Try to ensure we have a connection
    _ensure_connection()
    return _READY and (_CONN is not None)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed texts with OpenAI, with robust fallbacks.

    Order:
    1) Try EMBED_MODEL (default text-embedding-3-small, 1536 dims)
    2) Fallback to text-embedding-3-large
    3) Fallback to zero-vector of EMBED_DIM to keep semantic search operational
    """
    client = _get_openai()
    if not client:
        LOGGER.warning(
            "OPENAI_API_KEY not configured for embeddings; using zero-vector fallback"
        )
        return [[0.0] * EMBED_DIM for _ in texts]

    models_to_try = [EMBED_MODEL]
    if EMBED_MODEL != "text-embedding-3-large":
        models_to_try.append("text-embedding-3-large")

    last_error: Optional[Exception] = None
    for model in models_to_try:
        try:
            LOGGER.info(f"Embedding {len(texts)} text(s) with model: {model}")
            resp = client.embeddings.create(model=model, input=texts)
            vectors = [d.embedding for d in resp.data]
            if not vectors or len(vectors[0]) != EMBED_DIM:
                LOGGER.warning(
                    f"Embedding dims mismatch or empty (got {len(vectors[0]) if vectors else 0}); expected {EMBED_DIM}"
                )
            return vectors
        except Exception as e:
            last_error = e
            LOGGER.warning(f"Embedding failed with model {model}: {e}")

    # Final fallback: zero-vector to keep pipeline functional (dev-only behavior)
    LOGGER.warning(
        f"All embedding attempts failed (last error: {last_error}). Using zero-vector fallback of size {EMBED_DIM}."
    )
    return [[0.0] * EMBED_DIM for _ in texts]


def seed_static_kb_from_list(items: List[Dict[str, Any]]) -> int:
    """Seed from simple items (title, content, category). Only if table empty."""
    if not is_ready() or not items:
        return 0
    try:
        with _CONN.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM legal_chunks;")
            count = cur.fetchone()[0]
            if count and count > 0:
                LOGGER.info("legal_chunks already populated; skipping seed")
                return 0
    except Exception as e:
        LOGGER.error(f"Failed to count legal_chunks: {e}")
        return 0

    texts = [it.get("content", "") for it in items]
    try:
        vectors = embed_texts(texts)
    except Exception as e:
        LOGGER.error(f"Embedding failed during seed: {e}")
        return 0

    inserted = 0
    try:
        with _CONN.cursor() as cur:
            for it, vec in zip(items, vectors):
                chunk_id = str(uuid.uuid4())
                cur.execute(
                    """
                    INSERT INTO legal_chunks (id, parent_id, title, content, category, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    (
                        chunk_id,
                        None,
                        it.get("title"),
                        it.get("content"),
                        it.get("category"),
                        Json({"keywords": it.get("keywords", [])}),
                        vec,
                    ),
                )
                inserted += 1
        LOGGER.info(f"Seeded {inserted} chunks into legal_chunks")
    except Exception as e:
        LOGGER.error(f"Failed to seed legal_chunks: {e}")
        return 0
    return inserted


def semantic_search(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    if not is_ready():
        return []
    try:
        qvec = embed_texts([query])[0]
    except Exception as e:
        LOGGER.error(f"Embedding failed for query: {e}")
        return []

    # Prefer cosine distance operator '<=>'; fallback to L2 '<->' if not available
    sql_cos = """
        SELECT id, title, content, category, metadata, (1 - (embedding <=> %s::vector(1536))) AS relevance
        FROM legal_chunks
        ORDER BY embedding <=> %s::vector(1536)
        LIMIT %s;
    """
    sql_l2 = """
        SELECT id, title, content, category, metadata, NULL::float AS relevance
        FROM legal_chunks
        ORDER BY embedding <-> %s::vector(1536)
        LIMIT %s;
    """
    rows: List[tuple] = []
    try:
        with _CONN.cursor() as cur:
            cur.execute(sql_cos, (qvec, qvec, top_k))
            rows = cur.fetchall()
    except Exception as e:
        LOGGER.warning(f"Cosine operator failed, falling back to L2: {e}")
        try:
            with _CONN.cursor() as cur:
                cur.execute(sql_l2, (qvec, top_k))
                rows = cur.fetchall()
        except Exception as e2:
            LOGGER.error(f"Vector search failed: {e2}")
            return []

    results: List[Dict[str, Any]] = []
    for row in rows:
        doc_id, title, content, category, metadata, relevance = row
        results.append({
            "id": doc_id,
            "title": title,
            "content": content,
            "category": category,
            "keywords": (metadata or {}).get("keywords", []) if isinstance(metadata, dict) else [],
            "relevance": float(relevance) if relevance is not None else 0.0,
        })
    return results


def upsert_kb_from_list(items: List[Dict[str, Any]]) -> int:
    """Insert or ignore (by deterministic id) knowledge items.

    - Computes a deterministic UUIDv5 from title|category|content when id is not provided
    - Embeds content in batch and inserts with ON CONFLICT DO NOTHING
    - Returns number of attempted inserts (may be > actual new rows if conflicts)
    """
    if not is_ready() or not items:
        return 0
    texts = [it.get("content", "") for it in items]
    try:
        vectors = embed_texts(texts)
    except Exception as e:
        LOGGER.error(f"Embedding failed during upsert: {e}")
        return 0

    inserted = 0
    try:
        with _CONN.cursor() as cur:
            for it, vec in zip(items, vectors):
                base = f"{it.get('title','')}|{it.get('category','')}|{it.get('content','')}"
                doc_id = it.get("id") or str(uuid.uuid5(uuid.NAMESPACE_URL, base))
                # Merge provided metadata with keywords under a single JSON
                md = it.get("metadata", {}) or {}
                if not isinstance(md, dict):
                    md = {}
                merged_md = {**md, "keywords": it.get("keywords", [])}
                cur.execute(
                    """
                    INSERT INTO legal_chunks (id, parent_id, title, content, category, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                    """,
                    (
                        doc_id,
                        None,
                        it.get("title"),
                        it.get("content"),
                        it.get("category"),
                        Json(merged_md),
                        vec,
                    ),
                )
                inserted += 1
        LOGGER.info(f"Upsert attempted for {inserted} chunks (conflicts ignored)")
    except Exception as e:
        LOGGER.error(f"Failed to upsert legal_chunks: {e}")
        return 0
    return inserted


def get_doc_by_id(doc_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a single document from legal_chunks by id."""
    if not is_ready() or not doc_id:
        return None
    try:
        with _CONN.cursor() as cur:
            cur.execute(
                """
                SELECT id, parent_id, title, content, category, metadata
                FROM legal_chunks WHERE id = %s
                """,
                (doc_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            rid, parent_id, title, content, category, metadata = row
            return {
                "id": rid,
                "parent_id": parent_id,
                "title": title,
                "content": content,
                "category": category,
                "metadata": metadata or {},
            }
    except Exception as e:
        LOGGER.error(f"Failed to fetch doc by id: {e}")
        return None


def log_search(query: str, top_k: int, min_relevance: float, search_type: str, result_ids: List[str], 
               user_id: str = None, session_id: str = None, response_time_ms: int = None, 
               category: str = None, success: bool = True) -> None:
    if not is_ready():
        return
    try:
        with _CONN.cursor() as cur:
            cur.execute(
                """
                INSERT INTO search_logs (query, top_k, min_relevance, search_type, total, result_ids, 
                                       user_id, session_id, response_time_ms, category, success)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (query, top_k, float(min_relevance), search_type, len(result_ids), Json(result_ids),
                 user_id, session_id, response_time_ms, category, success),
            )
            # Update query analytics
            _update_query_analytics(query, response_time_ms, success, category)
    except Exception as e:
        LOGGER.warning(f"Failed to log search: {e}")


def log_ask(question: str, top_k: int, min_relevance: float, result_ids: List[str],
            user_id: str = None, session_id: str = None, response_time_ms: int = None,
            llm_model: str = None, llm_tokens_used: int = None, llm_cost: float = None,
            category: str = None, success: bool = True, error_message: str = None) -> None:
    if not is_ready():
        return
    try:
        with _CONN.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ask_logs (question, top_k, min_relevance, total_sources, result_ids,
                                    user_id, session_id, response_time_ms, llm_model, llm_tokens_used,
                                    llm_cost, category, success, error_message)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (question, top_k, float(min_relevance), len(result_ids), Json(result_ids),
                 user_id, session_id, response_time_ms, llm_model, llm_tokens_used,
                 llm_cost, category, success, error_message),
            )
            # Update query analytics  
            _update_query_analytics(question, response_time_ms, success, category)
    except Exception as e:
        LOGGER.warning(f"Failed to log ask: {e}")


# ============================
# Admin helpers for DB access
# ============================

def admin_db_overview() -> Dict[str, Any]:
    """Return high-level DB overview: counts and category breakdown."""
    overview = {
        "ready": is_ready(),
        "counts": {"legal_chunks": 0, "search_logs": 0, "ask_logs": 0},
        "categories": [],
        "recent": {"documents": [], "search_logs": [], "ask_logs": []},
    }
    if not is_ready():
        return overview
    try:
        with _CONN.cursor() as cur:
            # Counts
            cur.execute("SELECT COUNT(*) FROM legal_chunks;")
            overview["counts"]["legal_chunks"] = int(cur.fetchone()[0])
            try:
                cur.execute("SELECT COUNT(*) FROM search_logs;")
                overview["counts"]["search_logs"] = int(cur.fetchone()[0])
            except Exception:
                overview["counts"]["search_logs"] = 0
            try:
                cur.execute("SELECT COUNT(*) FROM ask_logs;")
                overview["counts"]["ask_logs"] = int(cur.fetchone()[0])
            except Exception:
                overview["counts"]["ask_logs"] = 0

            # Categories
            cur.execute("SELECT COALESCE(category,'nd') AS category, COUNT(*) FROM legal_chunks GROUP BY 1 ORDER BY 2 DESC LIMIT 50;")
            overview["categories"] = [{"category": r[0], "count": int(r[1])} for r in cur.fetchall()]

            # Recent documents
            cur.execute("SELECT id, title, category FROM legal_chunks ORDER BY id DESC LIMIT 10;")
            overview["recent"]["documents"] = [
                {"id": r[0], "title": r[1], "category": r[2]} for r in cur.fetchall()
            ]
            # Recent logs
            try:
                cur.execute("SELECT created_at, query, total FROM search_logs ORDER BY created_at DESC LIMIT 10;")
                overview["recent"]["search_logs"] = [
                    {"created_at": str(r[0]), "query": r[1], "total": int(r[2])} for r in cur.fetchall()
                ]
            except Exception:
                pass
            try:
                cur.execute("SELECT created_at, question, total_sources FROM ask_logs ORDER BY created_at DESC LIMIT 10;")
                overview["recent"]["ask_logs"] = [
                    {"created_at": str(r[0]), "question": r[1], "total_sources": int(r[2])} for r in cur.fetchall()
                ]
            except Exception:
                pass
    except Exception as e:
        LOGGER.warning(f"admin_db_overview failed: {e}")
    return overview


def admin_list_legal_chunks(q: Optional[str] = None, category: Optional[str] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    """List legal_chunks with optional filters and pagination."""
    result = {"total": 0, "items": []}
    if not is_ready():
        return result
    q = (q or "").strip()
    try:
        with _CONN.cursor() as cur:
            # Build WHERE clause
            where = []
            params: List[Any] = []
            if q:
                where.append("(title ILIKE %s OR content ILIKE %s)")
                like = f"%{q}%"
                params.extend([like, like])
            if category:
                where.append("category = %s")
                params.append(category)
            where_sql = (" WHERE " + " AND ".join(where)) if where else ""

            # Count
            cur.execute(f"SELECT COUNT(*) FROM legal_chunks{where_sql};", params)
            result["total"] = int(cur.fetchone()[0])

            # Items
            params_items = list(params)
            params_items.extend([limit, offset])
            cur.execute(
                f"SELECT id, title, category, left(content, 300) AS preview FROM legal_chunks{where_sql} ORDER BY title ASC LIMIT %s OFFSET %s;",
                params_items,
            )
            result["items"] = [
                {"id": r[0], "title": r[1], "category": r[2], "preview": r[3]} for r in cur.fetchall()
            ]
    except Exception as e:
        LOGGER.warning(f"admin_list_legal_chunks failed: {e}")
    return result


def admin_list_search_logs(limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    out = {"total": 0, "items": []}
    if not is_ready():
        return out
    try:
        with _CONN.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM search_logs;")
            out["total"] = int(cur.fetchone()[0])
            cur.execute(
                "SELECT created_at, query, top_k, min_relevance, search_type, total FROM search_logs ORDER BY created_at DESC LIMIT %s OFFSET %s;",
                (limit, offset),
            )
            out["items"] = [
                {
                    "created_at": str(r[0]),
                    "query": r[1],
                    "top_k": int(r[2]) if r[2] is not None else None,
                    "min_relevance": float(r[3]) if r[3] is not None else None,
                    "search_type": r[4],
                    "total": int(r[5]) if r[5] is not None else 0,
                }
                for r in cur.fetchall()
            ]
    except Exception as e:
        LOGGER.warning(f"admin_list_search_logs failed: {e}")
    return out


def get_db_status() -> Dict[str, Any]:
    """Get database status information including version and installed extensions"""
    status = {
        "connected": is_ready(),
        "version": "unknown",
        "extensions": []
    }
    
    if not is_ready():
        return status
    
    try:
        with _CONN.cursor() as cur:
            # Get PostgreSQL version
            cur.execute("SELECT version();")
            version_info = cur.fetchone()
            if version_info and version_info[0]:
                # Extract version number from the full version string
                version_str = version_info[0]
                status["version"] = version_str.split()[1] if len(version_str.split()) > 1 else version_str
            
            # Get installed extensions
            cur.execute("SELECT name, installed_version FROM pg_available_extensions WHERE installed_version IS NOT NULL;")
            extensions = cur.fetchall()
            status["extensions"] = [ext[0] for ext in extensions]
            
            # Check if pgvector is properly installed
            status["vector_ready"] = "vector" in status["extensions"]
            
            # Get additional database information
            try:
                cur.execute("SELECT current_database(), current_user;")
                db_info = cur.fetchone()
                if db_info:
                    status["database_name"] = db_info[0]
                    status["user"] = db_info[1]
            except Exception as e:
                LOGGER.warning(f"Could not fetch additional DB info: {e}")
    
    except Exception as e:
        LOGGER.error(f"Failed to get database status: {e}")
        status["error"] = str(e)
    
    return status


def admin_list_ask_logs(limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    out = {"total": 0, "items": []}
    if not is_ready():
        return out
    try:
        with _CONN.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM ask_logs;")
            out["total"] = int(cur.fetchone()[0])
            cur.execute(
                "SELECT created_at, question, top_k, min_relevance, total_sources FROM ask_logs ORDER BY created_at DESC LIMIT %s OFFSET %s;",
                (limit, offset),
            )
            out["items"] = [
                {
                    "created_at": str(r[0]),
                    "question": r[1],
                    "top_k": int(r[2]) if r[2] is not None else None,
                    "min_relevance": float(r[3]) if r[3] is not None else None,
                    "total_sources": int(r[4]) if r[4] is not None else 0,
                }
                for r in cur.fetchall()
            ]
    except Exception as e:
        LOGGER.warning(f"admin_list_ask_logs failed: {e}")
    return out


def update_legal_chunk(doc_id: str, title: Optional[str] = None, content: Optional[str] = None,
                       category: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> bool:
    """Update a legal chunk fields. If content changes, refresh embedding."""
    if not is_ready() or not doc_id:
        return False
    try:
        new_vec = None
        if content is not None:
            # create single embedding for content
            try:
                new_vec = embed_texts([content])[0]
            except Exception as e:
                LOGGER.warning(f"Embedding failed during update_legal_chunk: {e}")
                new_vec = [0.0] * EMBED_DIM
        sets = []
        params: List[Any] = []
        if title is not None:
            sets.append("title = %s")
            params.append(title)
        if content is not None:
            sets.append("content = %s")
            params.append(content)
        if category is not None:
            sets.append("category = %s")
            params.append(category)
        if metadata is not None:
            sets.append("metadata = %s")
            params.append(Json(metadata))
        if new_vec is not None:
            sets.append("embedding = %s")
            params.append(new_vec)
        if not sets:
            return True  # nothing to update
        params.append(doc_id)
        with _CONN.cursor() as cur:
            cur.execute(f"UPDATE legal_chunks SET {', '.join(sets)} WHERE id = %s;", params)
        return True
    except Exception as e:
        LOGGER.warning(f"update_legal_chunk failed: {e}")
        return False


def delete_legal_chunk(doc_id: str) -> bool:
    if not is_ready() or not doc_id:
        return False
    try:
        with _CONN.cursor() as cur:
            cur.execute("DELETE FROM legal_chunks WHERE id = %s;", (doc_id,))
        return True
    except Exception as e:
        LOGGER.warning(f"delete_legal_chunk failed: {e}")
        return False


# ============================
# Advanced Analytics Functions
# ============================

def _update_query_analytics(query: str, response_time_ms: int = None, success: bool = True, 
                           category: str = None) -> None:
    """Update aggregated query analytics"""
    if not query or not is_ready():
        return
    
    # Normalize query for analytics
    normalized = query.lower().strip()
    
    try:
        with _CONN.cursor() as cur:
            # Use UPSERT to update or insert query analytics
            cur.execute(
                """
                INSERT INTO query_analytics (query_normalized, total_count, last_queried, 
                                           avg_response_time_ms, success_rate, categories)
                VALUES (%s, 1, now(), %s, %s, %s)
                ON CONFLICT (query_normalized) DO UPDATE SET
                    total_count = query_analytics.total_count + 1,
                    last_queried = now(),
                    avg_response_time_ms = CASE 
                        WHEN %s IS NOT NULL THEN 
                            (COALESCE(query_analytics.avg_response_time_ms, 0) * query_analytics.total_count + %s) / (query_analytics.total_count + 1)
                        ELSE query_analytics.avg_response_time_ms
                    END,
                    success_rate = (query_analytics.success_rate * query_analytics.total_count + %s) / (query_analytics.total_count + 1),
                    categories = CASE 
                        WHEN %s IS NOT NULL THEN 
                            COALESCE(query_analytics.categories, '{}') || jsonb_build_object(%s, 1)
                        ELSE query_analytics.categories
                    END,
                    updated_at = now()
                """,
                (normalized, response_time_ms, 100.0 if success else 0.0, Json({category: 1} if category else {}),
                 response_time_ms, response_time_ms, 100.0 if success else 0.0, 
                 category, category)
            )
    except Exception as e:
        LOGGER.warning(f"Failed to update query analytics: {e}")


def log_api_usage(endpoint: str, method: str, status_code: int, response_time_ms: int,
                  user_id: str = None, session_id: str = None, ip_address: str = None,
                  user_agent: str = None, request_size: int = None, response_size: int = None,
                  error_message: str = None) -> None:
    """Log API usage for analytics"""
    if not is_ready():
        return
    try:
        with _CONN.cursor() as cur:
            cur.execute(
                """
                INSERT INTO api_usage_logs (endpoint, method, status_code, response_time_ms,
                                          user_id, session_id, ip_address, user_agent,
                                          request_size_bytes, response_size_bytes, error_message)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (endpoint, method, status_code, response_time_ms, user_id, session_id,
                 ip_address, user_agent, request_size, response_size, error_message)
            )
    except Exception as e:
        LOGGER.warning(f"Failed to log API usage: {e}")


def record_system_metric(metric_type: str, metric_name: str, value: float, unit: str = None,
                        metadata: Dict[str, Any] = None) -> None:
    """Record system performance metrics"""
    if not is_ready():
        return
    try:
        with _CONN.cursor() as cur:
            cur.execute(
                """
                INSERT INTO system_metrics (metric_type, metric_name, value, unit, metadata)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (metric_type, metric_name, float(value), unit, Json(metadata or {}))
            )
    except Exception as e:
        LOGGER.warning(f"Failed to record system metric: {e}")


def get_popular_queries(limit: int = 10, days: int = 7) -> List[Dict[str, Any]]:
    """Get most popular queries from actual search and ask logs in the last N days"""
    if not is_ready():
        return []
    try:
        with _CONN.cursor() as cur:
            cur.execute(
                """
                WITH combined_queries AS (
                    SELECT 
                        query as search_term,
                        created_at,
                        response_time_ms,
                        success,
                        'search' as query_type
                    FROM search_logs 
                    WHERE created_at > now() - interval '%s days'
                    AND query IS NOT NULL
                    AND length(trim(query)) > 0
                    
                    UNION ALL
                    
                    SELECT 
                        question as search_term,
                        created_at,
                        response_time_ms,
                        success,
                        'ask' as query_type
                    FROM ask_logs 
                    WHERE created_at > now() - interval '%s days'
                    AND question IS NOT NULL
                    AND length(trim(question)) > 0
                )
                SELECT 
                    search_term,
                    COUNT(*) as total_count,
                    AVG(response_time_ms) as avg_response_time,
                    AVG(CASE WHEN success THEN 100.0 ELSE 0.0 END) as success_rate,
                    MAX(created_at) as last_queried,
                    string_agg(DISTINCT query_type, ', ') as query_types
                FROM combined_queries
                GROUP BY search_term
                HAVING COUNT(*) >= 1
                ORDER BY total_count DESC, last_queried DESC
                LIMIT %s;
                """,
                (days, days, limit)
            )
            
            results = []
            for row in cur.fetchall():
                search_term = row[0]
                # Clean up the search term
                if search_term and len(search_term.strip()) > 2:
                    results.append({
                        "query": search_term.strip(),
                        "count": int(row[1]),
                        "avg_response_time": float(row[2]) if row[2] else 0,
                        "success_rate": float(row[3]) if row[3] else 100,
                        "last_queried": str(row[4]),
                        "query_types": row[5] or "search"
                    })
            
            return results
            
    except Exception as e:
        LOGGER.warning(f"Failed to get popular queries: {e}")
        return []


def get_analytics_overview(days: int = 7) -> Dict[str, Any]:
    """Get comprehensive analytics overview"""
    if not is_ready():
        return {}
    
    try:
        with _CONN.cursor() as cur:
            # Total queries
            cur.execute(
                "SELECT COUNT(*) FROM search_logs WHERE created_at > now() - interval '%s days';",
                (days,)
            )
            total_searches = int(cur.fetchone()[0])
            
            cur.execute(
                "SELECT COUNT(*) FROM ask_logs WHERE created_at > now() - interval '%s days';",
                (days,)
            )
            total_asks = int(cur.fetchone()[0])
            
            # Average response times
            cur.execute(
                "SELECT AVG(response_time_ms) FROM search_logs WHERE created_at > now() - interval '%s days' AND response_time_ms IS NOT NULL;",
                (days,)
            )
            avg_search_time = float(cur.fetchone()[0] or 0)
            
            cur.execute(
                "SELECT AVG(response_time_ms) FROM ask_logs WHERE created_at > now() - interval '%s days' AND response_time_ms IS NOT NULL;",
                (days,)
            )
            avg_ask_time = float(cur.fetchone()[0] or 0)
            
            # Success rates
            cur.execute(
                "SELECT COUNT(*) FILTER (WHERE success = true) * 100.0 / COUNT(*) FROM search_logs WHERE created_at > now() - interval '%s days';",
                (days,)
            )
            search_success_rate = float(cur.fetchone()[0] or 100)
            
            cur.execute(
                "SELECT COUNT(*) FILTER (WHERE success = true) * 100.0 / COUNT(*) FROM ask_logs WHERE created_at > now() - interval '%s days';",
                (days,)
            )
            ask_success_rate = float(cur.fetchone()[0] or 100)
            
            # Unique users
            cur.execute(
                "SELECT COUNT(DISTINCT session_id) FROM search_logs WHERE created_at > now() - interval '%s days' AND session_id IS NOT NULL;",
                (days,)
            )
            unique_sessions = int(cur.fetchone()[0])
            
            # Top categories
            cur.execute(
                "SELECT category, COUNT(*) FROM search_logs WHERE created_at > now() - interval '%s days' AND category IS NOT NULL GROUP BY category ORDER BY COUNT(*) DESC LIMIT 5;",
                (days,)
            )
            top_categories = [{"category": row[0], "count": int(row[1])} for row in cur.fetchall()]
            
            return {
                "total_queries": total_searches + total_asks,
                "total_searches": total_searches,
                "total_asks": total_asks,
                "avg_response_time": (avg_search_time + avg_ask_time) / 2 if avg_search_time or avg_ask_time else 0,
                "avg_search_time": avg_search_time,
                "avg_ask_time": avg_ask_time,
                "success_rate": (search_success_rate + ask_success_rate) / 2,
                "search_success_rate": search_success_rate,
                "ask_success_rate": ask_success_rate,
                "unique_sessions": unique_sessions,
                "top_categories": top_categories,
                "period_days": days
            }
    except Exception as e:
        LOGGER.warning(f"Failed to get analytics overview: {e}")
        return {}


def get_query_trends(hours: int = 24) -> List[Dict[str, Any]]:
    """Get query volume trends by hour"""
    if not is_ready():
        return []
    try:
        with _CONN.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    date_trunc('hour', created_at) as hour,
                    COUNT(*) as total_queries,
                    COUNT(*) as successful_queries,
                    0 as avg_response_time
                FROM (
                    SELECT created_at FROM search_logs 
                    WHERE created_at > now() - interval '%s hours'
                    UNION ALL
                    SELECT created_at FROM ask_logs
                    WHERE created_at > now() - interval '%s hours'
                ) combined
                GROUP BY hour
                ORDER BY hour;
                """,
                (hours, hours)
            )
            return [
                {
                    "hour": str(row[0]),
                    "total_queries": int(row[1]),
                    "successful_queries": int(row[2]),
                    "avg_response_time": float(row[3]) if row[3] else 0
                }
                for row in cur.fetchall()
            ]
    except Exception as e:
        LOGGER.warning(f"Failed to get query trends: {e}")
        return []
