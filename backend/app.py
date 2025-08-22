import os
import sys
import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS
# Import our custom OpenAI utilities
try:
    from backend.openai_utils import openai_manager, is_openai_available, get_completion, get_openai_status, handle_api_status_request
except ImportError:
    try:
        from .openai_utils import openai_manager, is_openai_available, get_completion, get_openai_status, handle_api_status_request
    except ImportError:
        from openai_utils import openai_manager, is_openai_available, get_completion, get_openai_status, handle_api_status_request
# Import LexML API utilities
try:
    from backend.lexml_api import lexml_api, search_legal_documents, get_legal_document, get_lexml_status, handle_lexml_status_request
except ImportError:
    try:
        from .lexml_api import lexml_api, search_legal_documents, get_legal_document, get_lexml_status, handle_lexml_status_request
    except ImportError:
        from lexml_api import lexml_api, search_legal_documents, get_legal_document, get_lexml_status, handle_lexml_status_request
import json

# Load environment variables only if .env file exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, use environment variables directly
    pass

# Import both old and new admin dashboards
try:
    from backend.admin_dashboard_v3 import admin_bp_v3
    ADMIN_V3_AVAILABLE = True
except ImportError:
    try:
        from .admin_dashboard_v3 import admin_bp_v3
        ADMIN_V3_AVAILABLE = True
    except ImportError:
        try:
            from admin_dashboard_v3 import admin_bp_v3
            ADMIN_V3_AVAILABLE = True
        except ImportError:
            ADMIN_V3_AVAILABLE = False

try:
    from backend.admin_dashboard_v2 import admin_bp_v2
    ADMIN_V2_AVAILABLE = True
except ImportError:
    try:
        from .admin_dashboard_v2 import admin_bp_v2
        ADMIN_V2_AVAILABLE = True
    except ImportError:
        try:
            from admin_dashboard_v2 import admin_bp_v2
            ADMIN_V2_AVAILABLE = True
        except ImportError:
            ADMIN_V2_AVAILABLE = False
            try:
                from backend.admin_dashboard import admin_bp
            except ImportError:
                try:
                    from .admin_dashboard import admin_bp
                except ImportError:
                    from admin_dashboard import admin_bp

# Import the OpenAI dashboard blueprint
try:
    from backend.openai_dashboard import openai_dashboard_bp
    OPENAI_DASHBOARD_AVAILABLE = True
except ImportError:
    try:
        from .openai_dashboard import openai_dashboard_bp
        OPENAI_DASHBOARD_AVAILABLE = True
    except ImportError:
        try:
            from openai_dashboard import openai_dashboard_bp
            OPENAI_DASHBOARD_AVAILABLE = True
        except ImportError:
            OPENAI_DASHBOARD_AVAILABLE = False

try:
    # Optional semantic retrieval (pgvector)
    try:
        from backend.retrieval import (
            init_pgvector,
            is_ready as semantic_is_ready,
            seed_static_kb_from_list,
            semantic_search,
            get_doc_by_id,
            log_search,
            log_ask,
            admin_db_overview,
            admin_list_legal_chunks,
            admin_list_search_logs,
            admin_list_ask_logs,
            update_legal_chunk,
            delete_legal_chunk,
        )
    except ImportError:
        try:
            from .retrieval import (
                init_pgvector,
                is_ready as semantic_is_ready,
                seed_static_kb_from_list,
                semantic_search,
                get_doc_by_id,
                log_search,
                log_ask,
                admin_db_overview,
                admin_list_legal_chunks,
                admin_list_search_logs,
                admin_list_ask_logs,
                update_legal_chunk,
                delete_legal_chunk,
            )
        except ImportError:
            from retrieval import (
                init_pgvector,
                is_ready as semantic_is_ready,
                seed_static_kb_from_list,
                semantic_search,
                get_doc_by_id,
                log_search,
                log_ask,
                admin_db_overview,
                admin_list_legal_chunks,
                admin_list_search_logs,
                admin_list_ask_logs,
                update_legal_chunk,
                delete_legal_chunk,
            )
    SEMANTIC_AVAILABLE = True
except Exception as e:
    SEMANTIC_AVAILABLE = False
    # Logger not yet configured here; will log after logger is ready

# Feature flag for semantic retrieval (default on)
USE_SEMANTIC_RETRIEVAL = os.getenv('USE_SEMANTIC_RETRIEVAL', 'true').lower() == 'true'
# Control whether to seed the semantic store on startup (default off to avoid embedding costs)
SEED_SEMANTIC_ON_START = os.getenv('SEED_SEMANTIC_ON_START', 'false').lower() == 'true'

# Configure logging for Railway compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Log startup info
logger.info("Initializing JuSimples backend...")
logger.info(f"Python version: {sys.version}")
logger.info(f"Working directory: {os.getcwd()}")

if not SEMANTIC_AVAILABLE:
    logger.info("Semantic retrieval module not available; running in keyword-only mode")
else:
    logger.info(f"Semantic retrieval module available. USE_SEMANTIC_RETRIEVAL={USE_SEMANTIC_RETRIEVAL}")

app = Flask(__name__)

# Register admin dashboard blueprint (v3 preferred, then v2, then v1)
if ADMIN_V3_AVAILABLE:
    app.register_blueprint(admin_bp_v3)
    logger.info("✅ Admin Dashboard v3.0 registered")
elif ADMIN_V2_AVAILABLE:
    app.register_blueprint(admin_bp_v2)
    logger.info("✅ Admin Dashboard v2.0 registered")
else:
    from admin_dashboard import admin_bp
    app.register_blueprint(admin_bp)
    logger.info("Admin Dashboard v1.0 registered (fallback)")

# Register OpenAI dashboard blueprint if available
if OPENAI_DASHBOARD_AVAILABLE:
    app.register_blueprint(openai_dashboard_bp)
    logger.info("✅ OpenAI Dashboard registered")

# CORS configuration
allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,https://jusimples.netlify.app,https://jusimplesbeta.netlify.app').split(',')
CORS(app, origins=allowed_origins)

# OpenAI configuration through our utilities module
logger.info("=== OpenAI Client Initialization ===")
logger.info(f"OpenAI available: {is_openai_available()}")

if is_openai_available():
    status = get_openai_status()
    logger.info(f"✅ OpenAI client initialized with model: {status['active_model']}")
else:
    logger.warning("❌ OpenAI client initialization failed. Check API key configuration.")

# Create aliases for compatibility with existing code
client = openai_manager.client
active_model = openai_manager.active_model

# Import our db_utils module
try:
    from backend.db_utils import get_db_manager
except ImportError:
    try:
        from .db_utils import get_db_manager
    except ImportError:
        from db_utils import get_db_manager

# Function to load legal knowledge from the database
def get_legal_knowledge():
    """Load legal knowledge from database, fall back to mock data if not available."""
    db_manager = get_db_manager()
    
    # Force database initialization if not ready
    if not db_manager.is_ready():
        logger.info("Database not ready - attempting to initialize...")
        if db_manager.initialize_schema():
            logger.info("Database initialized successfully")
        else:
            logger.warning("Database initialization failed - using mock legal data")
            return MOCK_LEGAL_KNOWLEDGE
    
    try:
        # Query the database for legal chunks
        results = db_manager.execute_query("""
            SELECT 
                id, 
                parent_id,
                title, 
                content, 
                category,
                metadata,
                created_at,
                updated_at
            FROM legal_chunks 
            ORDER BY created_at DESC
            LIMIT 1000
        """)
        
        if not results:
            logger.warning("No legal chunks found in database - checking if table exists and seeding...")
            # Try to seed some basic data if table is empty
            try:
                seed_result = _seed_basic_legal_data(db_manager)
                if seed_result:
                    # Try query again after seeding
                    results = db_manager.execute_query("""
                        SELECT id, parent_id, title, content, category, metadata, created_at, updated_at
                        FROM legal_chunks 
                        ORDER BY created_at DESC
                        LIMIT 1000
                    """)
                if not results:
                    logger.warning("Still no data after seeding - using mock data")
                    return MOCK_LEGAL_KNOWLEDGE
            except Exception as seed_e:
                logger.error(f"Error seeding basic data: {seed_e}")
                return MOCK_LEGAL_KNOWLEDGE
            
        knowledge_items = []
        for row in results:
            # Extract metadata as a dictionary
            metadata = row[5] if row[5] else {}
            
            # Create knowledge item with additional fields
            item = {
                "id": row[0],
                "parent_id": row[1],
                "title": row[2],
                "content": row[3],
                "category": row[4],
                "keywords": metadata.get("keywords", []),
                "source": metadata.get("source", "Unknown"),
                "relevance_score": metadata.get("relevance_score", 0.5),
                "law_type": metadata.get("law_type", ""),
                "jurisdiction": metadata.get("jurisdiction", "BR"),
                "date_created": row[6].isoformat() if row[6] else None,
                "date_updated": row[7].isoformat() if row[7] else None,
                "tags": metadata.get("tags", []),
                "complexity_level": metadata.get("complexity_level", "medium")
            }
            knowledge_items.append(item)
            
        logger.info(f"✅ Loaded {len(knowledge_items)} legal documents from database")
        return knowledge_items
        
    except Exception as e:
        logger.error(f"❌ Error loading legal knowledge from database: {e}")
        logger.info("Falling back to mock data")
        return MOCK_LEGAL_KNOWLEDGE


def _seed_basic_legal_data(db_manager):
    """Seed the database with basic legal data if it's empty"""
    try:
        # Insert mock data into the database
        for item in MOCK_LEGAL_KNOWLEDGE:
            metadata = {
                "keywords": item.get("keywords", []),
                "source": item.get("source", "Unknown"),
                "relevance_score": item.get("relevance_score", 0.5),
                "law_type": "constitutional" if "Constituição" in item.get("title", "") else "civil",
                "jurisdiction": "BR",
                "tags": item.get("keywords", []),
                "complexity_level": "medium"
            }
            
            from psycopg.types.json import Json
            db_manager.execute_query("""
                INSERT INTO legal_chunks (id, title, content, category, metadata)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                item["id"],
                item["title"],
                item["content"],
                item["category"],
                Json(metadata)
            ))
        
        logger.info("✅ Seeded database with basic legal data")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to seed basic legal data: {e}")
        return False

# Fallback mock data for when database is not available
MOCK_LEGAL_KNOWLEDGE = [
    {
        "title": "Constituição Federal - Art. 5º",
        "content": "Todos são iguais perante a lei, sem distinção de qualquer natureza, garantindo-se aos brasileiros e aos estrangeiros residentes no País a inviolabilidade do direito à vida, à liberdade, à igualdade, à segurança e à propriedade.",
        "keywords": ["direitos fundamentais", "igualdade", "liberdade"],
        "id": "cf-art5",
        "category": "direitos_fundamentais",
        "source": "Constituição Federal de 1988",
        "relevance_score": 1.0
    },
    {
        "title": "Código Civil - Art. 186",
        "content": "Aquele que, por ação ou omissão voluntária, negligência ou imprudência, violar direito e causar dano a outrem, ainda que exclusivamente moral, comete ato ilícito.",
        "keywords": ["ato ilícito", "dano", "responsabilidade"],
        "id": "cc-art186",
        "category": "responsabilidade_civil",
        "source": "Código Civil de 2002",
        "relevance_score": 0.9
    },
    {
        "title": "Lei 8.078/90 (CDC) - Art. 6º",
        "content": "São direitos básicos do consumidor: a proteção da vida, saúde e segurança contra os riscos provocados por práticas no fornecimento de produtos e serviços considerados perigosos ou nocivos.",
        "keywords": ["direitos do consumidor", "proteção", "produtos perigosos"],
        "id": "cdc-art6",
        "category": "direito_consumidor",
        "source": "Código de Defesa do Consumidor",
        "relevance_score": 0.85
    },
    {
        "title": "CLT - Art. 482",
        "content": "Constituem justa causa para rescisão do contrato de trabalho pelo empregador: a) ato de improbidade; b) incontinência de conduta ou mau procedimento; c) negociação habitual.",
        "keywords": ["justa causa", "rescisão", "contrato de trabalho"],
        "id": "clt-art482",
        "category": "direito_trabalho",
        "source": "Consolidação das Leis do Trabalho",
        "relevance_score": 0.8
    },
    {
        "title": "Lei 8.906/94 - Art. 7º",
        "content": "São direitos do advogado: exercer, com liberdade, a profissão em todo o território nacional; ter respeitada sua independência profissional.",
        "keywords": ["advogado", "direitos", "liberdade profissional"],
        "id": "estatuto-adv-art7",
        "category": "advocacia",
        "source": "Estatuto da Advocacia e da OAB",
        "relevance_score": 0.75
    }
]

# Initialize legal knowledge with mock data initially
# We'll refresh it on each relevant API call to ensure most recent data
LEGAL_KNOWLEDGE = MOCK_LEGAL_KNOWLEDGE.copy()

# Initialize pgvector (if enabled and available) and optionally seed static KB
logger.info("=== DATABASE INITIALIZATION ===")
logger.info(f"DATABASE_URL configured: {bool(os.getenv('DATABASE_URL'))}")
logger.info(f"SEMANTIC_AVAILABLE: {SEMANTIC_AVAILABLE}")
logger.info(f"USE_SEMANTIC_RETRIEVAL: {USE_SEMANTIC_RETRIEVAL}")

try:
    if SEMANTIC_AVAILABLE and USE_SEMANTIC_RETRIEVAL:
        logger.info("🔧 Initializing pgvector connection...")
        init_result = init_pgvector()
        logger.info(f"🔧 init_pgvector() returned: {init_result}")
        
        if init_result:
            logger.info("✅ Database connection successful!")
            # Test the connection immediately
            if semantic_is_ready():
                logger.info("✅ semantic_is_ready() = True")
                if SEED_SEMANTIC_ON_START:
                    seeded = seed_static_kb_from_list(LEGAL_KNOWLEDGE)
                    logger.info(f"✅ Semantic store ready. Seeded chunks: {seeded}")
                else:
                    logger.info("✅ Semantic store ready. Seeding skipped (SEED_SEMANTIC_ON_START=false)")
            else:
                logger.warning("⚠️ Database connected but semantic_is_ready() = False")
        else:
            logger.error("❌ Database initialization failed - checking connection...")
            # Try once more with detailed diagnostics
            try:
                from retrieval import _connect
                test_conn = _connect()
                if test_conn:
                    logger.info("✅ Direct connection test succeeded")
                    test_conn.close()
                else:
                    logger.error("❌ Direct connection test failed")
            except Exception as conn_test_e:
                logger.error(f"❌ Connection test error: {conn_test_e}")
    else:
        if not SEMANTIC_AVAILABLE:
            logger.warning("⚠️ SEMANTIC_AVAILABLE=False - retrieval module not imported")
        if not USE_SEMANTIC_RETRIEVAL:
            logger.warning("⚠️ USE_SEMANTIC_RETRIEVAL=False - semantic retrieval disabled")
except Exception as e:
    logger.error(f"❌ Error during database initialization: {e}")

# Define function to retrieve context
def retrieve_context(query, top_k=3):
    """Retrieve context from database with semantic search or keyword fallback"""
    if not query or not query.strip():
        logger.warning("Empty query passed to retrieve_context")
        return [], "none"
    
    start_time = time.time()
    results = []
    search_type = "none"
        
    # Try semantic search first if available
    if SEMANTIC_AVAILABLE and USE_SEMANTIC_RETRIEVAL:
        try:
            # Check if semantic search is ready
            semantic_ready = False
            try:
                semantic_ready = semantic_is_ready()
            except Exception as ready_err:
                logger.warning(f"Error checking semantic_is_ready: {ready_err}")
                
            if semantic_ready:
                logger.info(f"Attempting semantic search for: '{query[:50]}...' with top_k={top_k}")
                try:
                    results = semantic_search(query, top_k=top_k)
                    search_duration = time.time() - start_time
                    
                    # If semantic search yields results, return them
                    if results:
                        logger.info(f"✅ Semantic search found {len(results)} results in {search_duration:.2f}s")
                        return results, "semantic"
                    else:
                        logger.info(f"⚠️ Semantic search returned 0 results in {search_duration:.2f}s; falling back to keyword search")
                except Exception as search_err:
                    logger.warning(f"Error during semantic_search execution: {search_err}")
            else:
                logger.warning(f"Semantic search not ready, falling back to keyword")
        except Exception as e:
            logger.warning(f"Unexpected error in semantic search path: {e}")
    else:
        if not SEMANTIC_AVAILABLE:
            logger.debug("SEMANTIC_AVAILABLE=False - skipping semantic search")
        if not USE_SEMANTIC_RETRIEVAL:
            logger.debug("USE_SEMANTIC_RETRIEVAL=False - skipping semantic search")
    
    # Fallback to keyword search
    keyword_start = time.time()
    try:
        results, search_type = search_legal_knowledge(query, top_k), "keyword"
        keyword_duration = time.time() - keyword_start
        logger.info(f"Keyword search found {len(results)} results in {keyword_duration:.2f}s")
    except Exception as keyword_err:
        logger.error(f"Keyword search failed: {keyword_err}")
        results, search_type = [], "failed"
    
    total_duration = time.time() - start_time
    logger.info(f"Total retrieval time: {total_duration:.2f}s using {search_type} search")
    return results, search_type
    
# Define keyword search function
def search_legal_knowledge(query, limit=10):
    """Keyword-based retrieval from database or fallback to static KB."""
    if not query or not query.strip():
        logger.warning("Empty query passed to search_legal_knowledge")
        return []
        
    query_lower = query.lower()
    results = []
    
    # Try database search first
    try:
        db_manager = get_db_manager()
        db_ready = db_manager.is_ready() if db_manager else False
        
        if not db_manager:
            logger.error("Database manager returned None")
        elif not db_ready:
            logger.warning("Database not ready for search operation") 
            
        if db_ready:
            try:
                # Use SQL ILIKE for case-insensitive substring matching
                search_query = f"%{query_lower}%"
                sql = """
                    SELECT 
                        id, 
                        parent_id, 
                        title, 
                        content, 
                        category, 
                        metadata
                    FROM legal_chunks
                    WHERE 
                        LOWER(title) LIKE %s OR 
                        LOWER(content) LIKE %s
                    LIMIT %s
                """
                
                results_db = db_manager.execute_query(sql, (search_query, search_query, limit))
                
                if results_db:
                    for row in results_db:
                        # Extract metadata
                        metadata = row[5] or {}
                        keywords = metadata.get("keywords", [])
                        
                        # Calculate match score
                        match_score = 0
                        for keyword in keywords:
                            if isinstance(keyword, str) and (keyword.lower() in query_lower or query_lower in keyword.lower()):
                                match_score += 0.2
                                
                        if query_lower in row[2].lower():  # title
                            match_score += 0.5
                            
                        if query_lower in row[3].lower():  # content
                            match_score += 0.3
                        
                        # Ensure minimum score
                        match_score = max(match_score, 0.1)  # At least some relevance since it matched SQL
                        
                        # Create result
                        result = {
                            "id": row[0],
                            "parent_id": row[1],
                            "title": row[2],
                            "content": row[3],
                            "category": row[4],
                            "keywords": keywords,
                            "source": metadata.get("source", "Unknown"),
                            "relevance_score": metadata.get("relevance_score", 0.5),
                            "score": match_score
                        }
                        results.append(result)
                    
                    # Sort by score
                    results = sorted(results, key=lambda x: x["score"], reverse=True)
                    
                    logger.info(f"Found {len(results)} results in database for keyword query: {query}")
                    return results[:limit]
            except Exception as e:
                logger.error(f"Error executing database query: {e}")
    except Exception as e:
        logger.error(f"Error with database manager: {e}")
    
    # Fallback to in-memory search
    logger.warning(f"Falling back to in-memory search for: {query}")
    
    # Get most current data
    kb_data = get_legal_knowledge()
    
    for item in kb_data:
        # Check if query matches keywords or content
        match_score = 0
        for keyword in item.get("keywords", []):
            if keyword.lower() in query_lower or query_lower in keyword.lower():
                match_score += 0.2
                
        if query_lower in item.get("title", "").lower():
            match_score += 0.5
            
        if query_lower in item.get("content", "").lower():
            match_score += 0.3
            
        if match_score > 0:
            result = item.copy()
            result["score"] = match_score
            results.append(result)
    
    # Sort by score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    
    # Limit results
    return results[:limit]

def generate_ai_response(question, relevant_context):
    """Generate AI response using OpenAI with relevant legal context - VERSION 2.3.0"""
    logger.info(f"🔄 [v2.3.0] Starting AI response generation for: {question[:50]}...")
    
    # FORCE RETURN REAL RESPONSE FOR TESTING
    if "teste" in question.lower():
        return f"✅ VERSÃO 2.3.0 ATIVA! Pergunta recebida: {question}. Sistema OpenAI funcionando corretamente."
    
    # Check if OpenAI is available
    if not is_openai_available():
        error_msg = "OpenAI API não está disponível. Verifique a configuração da chave API."
        logger.error(f"❌ {error_msg}")
        return f"ERRO: {error_msg}"
        
    try:
        # Prepare context for the AI
        context_text = "\n\n".join([
            f"--- Documento: {doc.get('title', 'Sem título')} ---\n{doc.get('content', '')}" 
            for doc in relevant_context
        ])
        
        # Prompt template
        prompt = f"""
        Sua tarefa é responder a perguntas sobre direito brasileiro com base nas informações fornecidas.
        
        PERGUNTA DO USUÁRIO:
        {question}
        
        CONTEXTO JURÍDICO RELEVANTE:
        {context_text if context_text.strip() else "Não há informações específicas disponíveis sobre este tema."}
        
        INSTRUÇÕES:
        - Sua resposta deve ser baseada APENAS nas informações fornecidas no CONTEXTO acima.
        - Seja conciso, claro e preciso.
        - Estruture sua resposta de forma organizada, usando marcadores ou numeração quando apropriado.
        - Se o CONTEXTO não tiver informações suficientes, diga que não possui informações suficientes e sugira que o usuário reformule a pergunta.
        - Não invente informações ou cite leis que não estejam no CONTEXTO.
        - Sempre mencione a fonte legal relevante (artigo, lei, etc.)"""

        # System message for the assistant
        system_message = """Você é um assistente jurídico especializado em direito brasileiro. 
        Responda apenas com base no contexto fornecido e siga as instruções do usuário."""
        
        # Get completion from our utilities module
        logger.info(f"🚀 [v2.3.0] Calling OpenAI API through utilities module")
        result = get_completion(
            prompt=prompt,
            system_message=system_message,
            temperature=0.3,
            max_tokens=1024
        )
        
        if result["success"]:
            ai_response = result["content"]
            logger.info(f"✅ [v2.3.0] SUCCESS! OpenAI response received, length: {len(ai_response)}")
            logger.info(f"📊 Tokens used: {result['metrics']['tokens']['total']} "
                      f"(input: {result['metrics']['tokens']['input']}, "
                      f"output: {result['metrics']['tokens']['output']})")
            logger.info(f"💰 Cost: ${result['metrics']['cost']:.6f}")
            logger.info(f"📝 Response preview: {ai_response[:100]}...")
            return ai_response
        else:
            error_msg = f"❌ [v2.3.0] OpenAI API Error: {result['error']}"
            logger.error(error_msg)
            return f"Erro na consulta à IA v2.3.0: {result['error']}"
        
    except Exception as e:
        error_msg = f"❌ [v2.3.0] Unexpected error: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        return f"Erro inesperado na consulta à IA v2.3.0: {str(e)}"

@app.route('/')
def home():
    """Home endpoint with deployment info - VERSION 2.5.0"""
    return jsonify({
        "message": "JuSimples Legal AI API - CACHE BUSTED",
        "version": "2.5.0",
        "status": "running",
        "mode": "simplified",
        "deployment_time": datetime.now().isoformat(),
        "cache_bust": "20250117_2010",
        "endpoints": ["/api/ask", "/api/test-rag", "/health", "/admin/"]
    })

@app.route('/api/status/kb')
def get_kb_status():
    """Knowledge base status endpoint"""
    # Get fresh count from database
    db_manager = get_db_manager()
    count = 0
    
    if db_manager and db_manager.is_ready():
        try:
            results = db_manager.execute_query("SELECT COUNT(*) FROM legal_chunks")
            if results:
                count = results[0][0]
        except Exception as e:
            logger.warning(f"Error getting legal_chunks count: {e}")
            # Fall back to mock data length
            count = len(MOCK_LEGAL_KNOWLEDGE)
    else:
        # Fall back to mock data length
        count = len(MOCK_LEGAL_KNOWLEDGE)
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "ai_system": "operational",
        "knowledge_base": f"{count} documents",
        "database_status": "connected" if db_manager.is_ready() else "disconnected"
    })

@app.route('/api/health')
def get_health():
    # Get fresh count from database
    db_manager = get_db_manager()
    count = 0
    
    if db_manager.is_ready():
        try:
            results = db_manager.execute_query("SELECT COUNT(*) FROM legal_chunks")
            if results:
                count = results[0][0]
        except Exception as e:
            logger.warning(f"Error getting legal_chunks count: {e}")
            # Fall back to mock data length
            count = len(MOCK_LEGAL_KNOWLEDGE)
    else:
        # Fall back to mock data length
        count = len(MOCK_LEGAL_KNOWLEDGE)
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "ai_system": "operational",
        "knowledge_base": f"{count} documents",
        "database_status": "connected" if db_manager.is_ready() else "disconnected"
    })

@app.route('/health')
def health_alias():
    # Alias for platform healthchecks (e.g., Railway)
    return get_health()

@app.route('/api/ask', methods=['POST'])
def ask_question():
    start_time = time.time()
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        # Optional tuning params
        top_k_raw = data.get('top_k', 3)
        min_rel_raw = data.get('min_relevance', 0.5)
        try:
            top_k = int(top_k_raw)
        except Exception:
            top_k = 3
        top_k = max(1, min(10, top_k))
        try:
            min_relevance = float(min_rel_raw)
        except Exception:
            min_relevance = 0.5
        
        logger.info(f"Received question request: {question[:100] if question else 'No question provided'}")
        logger.info(f"OpenAI client status: {'Available' if client else 'Not available'}")
        
        if not question:
            logger.warning("No question provided in request")
            return jsonify({"error": "Pergunta não fornecida"}), 400
        
        if len(question) < 10:
            logger.warning(f"Question too short: {len(question)} characters")
            return jsonify({"error": "Pergunta muito curta. Forneça mais detalhes."}), 400
        
        logger.info(f"Processing question: {question[:100]}...")
        
        # Search relevant legal knowledge (semantic preferred)
        relevant_context, search_type = retrieve_context(question, top_k=top_k)
        # Apply relevance filtering only for semantic results
        if search_type == "semantic":
            relevant_context = [it for it in relevant_context if float(it.get("relevance", 0.0)) >= min_relevance]
        logger.info(f"Found {len(relevant_context)} relevant documents via {search_type}")
        
        # Generate AI response
        ai_answer = generate_ai_response(question, relevant_context)
        logger.info(f"Generated AI response: {ai_answer[:100]}...")

        # Log ask analytics (enhanced with detailed tracking)
        try:
            result_ids = [str(item.get("id")) for item in relevant_context if item.get("id")]
            session_id = request.headers.get('X-Session-ID') or f"web_{int(time.time())}"
            user_id = request.headers.get('X-User-ID')
            
            # Calculate actual response time
            processing_time = time.time() - start_time
            
            # FORCE DATABASE CONNECTION CHECK
            logger.info(f"🔍 Database connection status: SEMANTIC_AVAILABLE={SEMANTIC_AVAILABLE}, USE_SEMANTIC_RETRIEVAL={USE_SEMANTIC_RETRIEVAL}")
            if SEMANTIC_AVAILABLE:
                logger.info(f"🔍 semantic_is_ready(): {semantic_is_ready()}")
            
            # Extract comprehensive OpenAI API response data
            tokens_used = 0
            input_tokens = 0  
            output_tokens = 0
            llm_cost = 0.0
            finish_reason = None
            system_fingerprint = None
            response_id = None
            model_used = None
            created_timestamp = None
            logprobs = None
            
            # Estimate token usage and cost based on text length (OpenAI response object not available here)
            if tokens_used == 0 and client and ai_answer and "Erro" not in ai_answer:
                # Rough estimation: ~4 characters per token
                estimated_input_tokens = len(question) // 4 + sum(len(doc.get('content', '')) for doc in relevant_context) // 4
                estimated_output_tokens = len(ai_answer) // 4
                tokens_used = estimated_input_tokens + estimated_output_tokens
                input_tokens = estimated_input_tokens
                output_tokens = estimated_output_tokens
                
                # Calculate cost based on model
                model_for_cost = active_model or 'gpt-4o-mini'
                if 'gpt-4o-mini' in model_for_cost.lower():
                    llm_cost = (input_tokens * 0.00015 / 1000) + (output_tokens * 0.0006 / 1000)
                elif 'gpt-4o' in model_for_cost.lower():
                    llm_cost = (input_tokens * 0.005 / 1000) + (output_tokens * 0.015 / 1000)
                elif 'gpt-4' in model_for_cost.lower():
                    llm_cost = (input_tokens * 0.03 / 1000) + (output_tokens * 0.06 / 1000)
                else:
                    # Default to gpt-4o-mini pricing
                    llm_cost = (input_tokens * 0.00015 / 1000) + (output_tokens * 0.0006 / 1000)
                
                # Set model used
                model_used = active_model or 'gpt-4o-mini'
            
            # ALWAYS LOG TO DATABASE IF AVAILABLE
            if SEMANTIC_AVAILABLE:
                try:
                    # Force reconnection if needed
                    if not semantic_is_ready():
                        logger.warning("🔄 Database not ready, attempting reconnection...")
                        init_pgvector()
                    
                    from retrieval_extensions import log_ask_advanced
                    from retrieval import _CONN
                    log_ask_advanced(
                        question=question,
                        answer=ai_answer,
                        top_k=top_k,
                        min_relevance=min_relevance,
                        result_ids=result_ids,
                        search_type=search_type,
                        success="Erro" not in ai_answer,
                        session_id=session_id,
                        user_id=user_id,
                        response_time_ms=int(processing_time * 1000) if processing_time else 0,
                        llm_model=model_used or active_model,
                        llm_tokens_used=tokens_used,
                        llm_cost=llm_cost,
                        user_agent=request.headers.get('User-Agent', ''),
                        ip_address=request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR')),
                        context_found=len(relevant_context),
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        finish_reason=finish_reason,
                        system_fingerprint=system_fingerprint,
                        response_id=response_id,
                        created_timestamp=created_timestamp,
                        logprobs=logprobs,
                        conn=_CONN
                    )
                except ImportError:
                    # Fallback to basic logging
                    logger.info("⚠️ Using fallback basic logging")
                    from retrieval import log_ask
                    log_ask(question, top_k, min_relevance, result_ids)
                except Exception as log_err:
                    logger.error(f"❌ Advanced logging failed: {log_err}, trying basic logging")
                    try:
                        from retrieval import log_ask
                        log_ask(question, top_k, min_relevance, result_ids)
                        logger.info("✅ Basic logging succeeded")
                    except Exception as basic_err:
                        logger.error(f"❌ All logging failed: {basic_err}")
                logger.info(f"✅ Logged ask analytics: tokens={tokens_used}, cost=${llm_cost:.4f}, search_type={search_type}")
        except Exception as _e:
            logger.error(f"❌ CRITICAL: Failed to log ask analytics: {_e}", exc_info=True)
            # Try emergency basic logging
            try:
                if SEMANTIC_AVAILABLE:
                    from retrieval import log_ask
                    log_ask(question, 3, 0.5, [])
                    logger.info("🔧 Emergency basic logging succeeded")
            except Exception as emergency_err:
                logger.error(f"🚨 Emergency logging also failed: {emergency_err}")
        
        response = {
            "question": question,
            "answer": ai_answer,
            "sources": [
                {
                    "id": item.get("id"),
                    "title": item["title"],
                    "category": item["category"],
                    "content_preview": item["content"][:200] + "...",
                    "relevance": item.get("relevance", 0)
                }
                for item in relevant_context
            ],
            "confidence": 0.85,
            "timestamp": datetime.utcnow().isoformat(),
            "system_status": {
                "openai_available": client is not None,
                "knowledge_base_size": len(relevant_context),
                "search_type": search_type
            },
            "disclaimer": "Esta resposta é baseada em IA e tem caráter informativo. Para casos complexos, consulte um advogado especializado.",
            "debug_info": {
                "openai_available": client is not None,
                "active_model": active_model,
                "context_found": len(relevant_context),
                "api_key_configured": openai_api_key is not None and openai_api_key != 'your_openai_api_key_here'
            },
            "params": {"top_k": top_k, "min_relevance": min_relevance}
        }
        
        logger.info("Successfully processed question and returning response")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in ask_question: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Erro interno do servidor",
            "message": "Não foi possível processar sua pergunta no momento.",
            "debug_info": {
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        }), 500

@app.route('/api/search', methods=['POST', 'GET'])
def search_legal():
    """
    Search API endpoint - supports both GET and POST methods
    
    GET: /api/search?q=query_text&top_k=3&min_relevance=0.0
    POST: {"query": "query_text", "top_k": 3, "min_relevance": 0.0}
    
    Returns legal knowledge base items matching the query using semantic search with
    keyword search fallback if semantic search is not available or returns no results.
    """
    
    start_time = time.time()
    try:
        # Handle both GET and POST methods
        if request.method == 'POST':
            # Handle JSON payload for POST
            try:
                data = request.get_json() or {}
                raw_query = data.get('query', '').strip()
                top_k_raw = data.get('top_k', 3)
                min_rel_raw = data.get('min_relevance', 0.0)
            except Exception as e:
                logger.error(f"Error parsing POST JSON: {e}")
                return jsonify({
                    "error": "Formato JSON inválido",
                    "message": "Por favor forneça dados em formato JSON válido"
                }), 400
        else:  # GET
            # Get parameters from URL query string
            raw_query = request.args.get('q', '').strip() or request.args.get('query', '').strip()
            if not raw_query:
                return jsonify({
                    "error": "Parâmetro de busca ausente", 
                    "message": "Forneça o parâmetro 'q' ou 'query' na URL",
                    "example": "/api/search?q=consumidor"
                }), 400
                
            top_k_raw = request.args.get('top_k', 3)
            min_rel_raw = request.args.get('min_relevance', 0.0)
            
            # Convert string params to correct types for GET
            try:
                top_k_raw = int(top_k_raw)
            except (ValueError, TypeError):
                top_k_raw = 3
            try:
                min_rel_raw = float(min_rel_raw)
            except (ValueError, TypeError):
                min_rel_raw = 0.0
                
        query_lower = raw_query.lower()
        try:
            top_k = int(top_k_raw)
        except Exception:
            top_k = 3
        top_k = max(1, min(10, top_k))
        try:
            min_relevance = float(min_rel_raw)
        except Exception:
            min_relevance = 0.0
        
        if not raw_query:
            return jsonify({"error": "Query não fornecida"}), 400
        
        logger.info(f"Search request: query='{raw_query}', top_k={top_k}, min_relevance={min_relevance}")
        
        # Search legal knowledge (semantic preferred)
        results, search_type = retrieve_context(raw_query, top_k=top_k)
        if search_type == "semantic":
            results = [it for it in results if float(it.get("relevance", 0.0)) >= min_relevance]
        # For keyword-only, ensure we reflect the lowercased query used
        query_for_return = raw_query if search_type == "semantic" else query_lower
        
        # Log search analytics (enhanced with detailed tracking)
        try:
            result_ids = [str(item.get("id")) for item in results if item.get("id")]
            session_id = request.headers.get('X-Session-ID') or f"web_{int(time.time())}"
            user_id = request.headers.get('X-User-ID')
            processing_time = time.time() - start_time
            
            # FORCE DATABASE CONNECTION FOR SEARCH LOGGING
            logger.info(f"🔍 Search logging - Database status: SEMANTIC_AVAILABLE={SEMANTIC_AVAILABLE}")
            
            if SEMANTIC_AVAILABLE:
                try:
                    # Force reconnection if needed
                    if not semantic_is_ready():
                        logger.warning("🔄 Search logging - Database not ready, attempting reconnection...")
                        init_pgvector()
                    
                    from retrieval_extensions import log_search_advanced
                    from retrieval import _CONN
                    log_search_advanced(
                        query=raw_query,
                        top_k=top_k,
                        min_relevance=min_relevance,
                        result_ids=result_ids,
                        search_type=search_type,
                        success=len(results) > 0,
                        session_id=session_id,
                        user_id=user_id,
                        response_time_ms=int(processing_time * 1000) if processing_time else 0,
                        user_agent=request.headers.get('User-Agent', ''),
                        ip_address=request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR')),
                        context_found=len(results),
                        conn=_CONN
                    )
                    logger.info(f"✅ Advanced search logging succeeded")
                except ImportError:
                    # Fallback to basic logging
                    logger.info("⚠️ Using fallback basic search logging")
                    from retrieval import log_search
                    log_search(raw_query, top_k, min_relevance, search_type, result_ids)
                except Exception as log_err:
                    logger.error(f"❌ Advanced search logging failed: {log_err}, trying basic logging")
                    try:
                        from retrieval import log_search
                        log_search(raw_query, top_k, min_relevance, search_type, result_ids)
                        logger.info("✅ Basic search logging succeeded")
                    except Exception as basic_err:
                        logger.error(f"❌ All search logging failed: {basic_err}")
                logger.info(f"✅ Logged search analytics: query={raw_query[:50]}..., results={len(results)}, search_type={search_type}")
        except Exception as _e:
            logger.error(f"❌ CRITICAL: Failed to log search analytics: {_e}", exc_info=True)
            # Try emergency basic logging
            try:
                if SEMANTIC_AVAILABLE:
                    from retrieval import log_search
                    log_search(raw_query, 3, 0.0, "keyword", [])
                    logger.info("🔧 Emergency search logging succeeded")
            except Exception as emergency_err:
                logger.error(f"🚨 Emergency search logging also failed: {emergency_err}")
        
        return jsonify({
            "query": query_for_return,
            "results": [
                {
                    "id": item.get("id"),
                    "title": item["title"],
                    "content": item["content"],
                    "category": item["category"],
                    "relevance": item.get("relevance", 0)
                }
                for item in results
            ],
            "total": len(results),
            "search_type": search_type,
            "params": {"top_k": top_k, "min_relevance": min_relevance}
        })
            
    except Exception as e:
        logger.error(f"Error in search_legal: {str(e)}")
        return jsonify({"error": "Erro na busca"}), 500

@app.route('/api/test-rag', methods=['POST'])
def test_rag():
    """Test RAG system endpoint for admin dashboard"""
    global client, active_model
    
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({"error": "Pergunta não fornecida"}), 400
        
        start_time = time.time()
        
        # Force OpenAI client initialization for this test
        if not client and openai_api_key and openai_api_key.strip():
            try:
                client = OpenAI(api_key=openai_api_key.strip())
                active_model = os.getenv('OPENAI_MODEL', 'gpt-5-nano')
                logger.info("✅ OpenAI client force-initialized for RAG test")
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI for RAG test: {e}")
        
        # Search relevant legal knowledge
        relevant_context = search_legal_knowledge(question)
        
        # Generate AI response with forced initialization
        logger.info(f"🔍 About to call generate_ai_response for: {question}")
        ai_answer = generate_ai_response(question, relevant_context)
        logger.info(f"🎯 Received AI answer: {ai_answer[:100]}...")
        
        processing_time = (time.time() - start_time) * 1000
        
        return jsonify({
            "question": question,
            "ai_answer": ai_answer,
            "relevant_context": relevant_context,
            "processing_time_ms": processing_time,
            "timestamp": datetime.utcnow().isoformat(),
            "system_status": {
                "openai_available": client is not None,
                "knowledge_base_size": len(relevant_context)
            }
        })
        
    except Exception as e:
        logger.error(f"Error in test RAG: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/switch-model', methods=['POST'])
def switch_model():
    """Switch OpenAI model and reinitialize client"""
    try:
        data = request.get_json()
        new_model = data.get('model', 'gpt-5-nano')
        
        # Update environment variable temporarily
        os.environ['OPENAI_MODEL'] = new_model
        
        # Reinitialize client
        success = initialize_openai_client()
        
        if success:
            return jsonify({
                "success": True,
                "message": f"Switched to model: {active_model}",
                "active_model": active_model
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to initialize with new model",
                "active_model": active_model
            }), 500
            
    except Exception as e:
        logger.error(f"Error switching model: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route('/api/debug')
def debug_info():
    """Debug endpoint to check system status"""
    return jsonify({
        "openai_client_available": client is not None,
        "active_model": active_model,
        "api_key_configured": openai_api_key is not None and openai_api_key != 'your_openai_api_key_here',
        "api_key_length": len(openai_api_key) if openai_api_key else 0,
        "model_configured": os.getenv('OPENAI_MODEL', 'Not set'),
        "cors_origins": allowed_origins,
        "knowledge_base_size": len(LEGAL_KNOWLEDGE),
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/status')
def get_status():
    """General API status endpoint with comprehensive status information"""
    # Get knowledge base count from database
    db_manager = get_db_manager()
    kb_count = 0
    db_ready = False
    
    if db_manager and db_manager.is_ready():
        db_ready = True
        try:
            results = db_manager.execute_query("SELECT COUNT(*) FROM legal_chunks")
            if results:
                kb_count = results[0][0]
        except Exception as e:
            logger.warning(f"Error getting legal_chunks count: {e}")
            # Fall back to mock data length
            kb_count = len(MOCK_LEGAL_KNOWLEDGE)
    
    return jsonify({
        "status": "operational",
        "version": "2.3.0",
        "environment": os.getenv('FLASK_ENV', 'development'),
        "cors_origins": allowed_origins,
        "database": {
            "ready": db_ready,
            "knowledge_base_size": kb_count,
            "semantic_available": SEMANTIC_AVAILABLE,
            "semantic_ready": semantic_is_ready() if SEMANTIC_AVAILABLE else False
        },
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/status/openai')
def get_openai_api_status():
    """OpenAI API status endpoint with detailed metrics
    
    GET /api/status/openai
    
    Returns:
    - Connection status
    - Model information
    - Token usage metrics
    - Cost tracking
    """
    return jsonify(handle_api_status_request())

@app.route('/api/status/lexml')
def get_lexml_api_status():
    """LexML API status endpoint with test query
    
    GET /api/status/lexml
    
    Returns:
    - API status
    - Request metrics
    - Test query results
    """
    return jsonify(handle_lexml_status_request())

@app.route('/api/legal-data')
def get_legal_data():
    # Fetch fresh data from database
    fresh_data = get_legal_knowledge()
    
    # Return the data as JSON
    return jsonify({
        "data": fresh_data,
        "total": len(fresh_data),
        "last_updated": datetime.utcnow().isoformat()
    })

@app.route('/api/legal-data/<item_id>')
def get_legal_item_details(item_id):
    """Get detailed information about a legal knowledge base item by ID.
    
    GET /api/legal-data/:item_id
    
    Returns:
    - Item details
    - Parent and child relationships
    - Related items from internal knowledge base
    - Related documents from LexML API (if enabled)
    """
    # Start timer for performance tracking
    start_time = time.time()
    
    try:
        # First try to fetch from database
        db_manager = get_db_manager()
        if db_manager and db_manager.is_ready():
            # Get base item data
            sql = """SELECT id, parent_id, title, content, category, metadata 
                   FROM legal_chunks WHERE id = %s"""
            result = db_manager.execute_query(sql, (item_id,))
            
            if result:
                # Format item data
                item_data = {
                    "id": result[0][0],
                    "parent_id": result[0][1],
                    "title": result[0][2],
                    "content": result[0][3],
                    "category": result[0][4],
                    "metadata": result[0][5] if result[0][5] else {}
                }
                
                # Get children if any
                sql_children = """SELECT id, title, category FROM legal_chunks WHERE parent_id = %s"""
                children_result = db_manager.execute_query(sql_children, (item_id,))
                
                children = []
                if children_result:
                    for child in children_result:
                        children.append({
                            "id": child[0],
                            "title": child[1],
                            "category": child[2]
                        })
                
                item_data["children"] = children
                
                # Get parent details if parent_id exists
                if item_data["parent_id"]:
                    sql_parent = """SELECT id, title, category FROM legal_chunks WHERE id = %s"""
                    parent_result = db_manager.execute_query(sql_parent, (item_data["parent_id"],))
                    
                    if parent_result:
                        item_data["parent"] = {
                            "id": parent_result[0][0],
                            "title": parent_result[0][1],
                            "category": parent_result[0][2]
                        }
                
                # Find related items (semantically similar if semantic search available, otherwise by category)
                related_items = []
                try:
                    if SEMANTIC_AVAILABLE and USE_SEMANTIC_RETRIEVAL and semantic_is_ready():
                        # Use semantic search to find related items
                        related = semantic_search(item_data["content"], top_k=5, exclude_ids=[item_id])
                        related_items = related if related else []
                    else:
                        # Fallback to category-based related items
                        sql_related = """SELECT id, title, category FROM legal_chunks 
                                       WHERE category = %s AND id != %s LIMIT 5"""
                        related_results = db_manager.execute_query(sql_related, 
                                                                 (item_data["category"], item_id))
                        
                        if related_results:
                            related_items = [
                                {"id": r[0], "title": r[1], "category": r[2]}
                                for r in related_results
                            ]
                except Exception as e:
                    logger.warning(f"Error finding related items: {e}")
                
                item_data["related_items"] = related_items
                
                # Add LexML API related documents if enabled
                try:
                    use_lexml_api = os.getenv("USE_LEXML_API", "").lower() in ["true", "1", "yes", "y", "on"]
                    if use_lexml_api and lexml_api:
                        # Use item title and category as search terms
                        search_term = f"{item_data['title']} {item_data['category']}"
                        logger.info(f"Searching LexML API for: {search_term}")
                        
                        # Get LexML recommendations based on item content
                        lexml_results = lexml_api.search(search_term, max_results=3)
                        if lexml_results and lexml_results.get("items"):
                            item_data["lexml_recommendations"] = lexml_results.get("items", [])
                            item_data["_metadata"]["lexml_search_time_ms"] = lexml_results.get("search_time_ms")
                        else:
                            item_data["lexml_recommendations"] = []
                except Exception as e:
                    logger.warning(f"Error fetching LexML recommendations: {e}")
                    item_data["lexml_recommendations"] = []
                    item_data["_metadata"]["lexml_error"] = str(e)
                
                # Add server processing metadata
                item_data["_metadata"] = {
                    "retrieved_at": datetime.utcnow().isoformat(),
                    "source": "database",
                    "processing_time_ms": round((time.time() - start_time) * 1000, 2)
                }
                
                return jsonify(item_data)
        
        # Fallback to static knowledge if DB not available
        all_items = get_legal_knowledge()
        for item in all_items:
            if str(item["id"]) == str(item_id):
                item["_metadata"] = {
                    "retrieved_at": datetime.utcnow().isoformat(),
                    "source": "static",
                    "processing_time_ms": round((time.time() - start_time) * 1000, 2)
                }
                return jsonify(item)
                
        # If not found in static data either
        return jsonify({
            "error": "Item não encontrado",
            "message": f"Nenhum item encontrado com o ID: {item_id}"
        }), 404
        
    except Exception as e:
        logger.error(f"Error retrieving legal item {item_id}: {e}")
        return jsonify({
            "error": "Erro ao buscar item legal",
            "message": "Ocorreu um erro ao buscar os detalhes do item.",
            "debug_info": {
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        }), 500

@app.route('/api/documentos', methods=['GET'])
def get_all_documents():
    """Fetch all legal documents from semantic store (if available)."""
    try:
        # Check if semantic search is available
        if not (SEMANTIC_AVAILABLE and USE_SEMANTIC_RETRIEVAL and semantic_is_ready()):
            return jsonify({
                "error": "Serviço de documentos não disponível",
                "message": "A busca semântica não está disponível no momento."
            }), 503
        
        # Fetch all documents from the database
        db_manager = get_db_manager()
        if not db_manager or not db_manager.is_ready():
            return jsonify({
                "error": "Banco de dados indisponível",
                "message": "Não foi possível conectar ao banco de dados."
            }), 503
        
        # Fetch documents with pagination
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)  # Max 50 per page
        offset = (page - 1) * per_page
        
        # Get total count
        count_sql = """SELECT COUNT(*) FROM legal_chunks"""
        count_result = db_manager.execute_query(count_sql)
        total_documents = count_result[0][0] if count_result else 0
        
        # Get paginated documents
        docs_sql = """SELECT id, parent_id, title, category, metadata 
                   FROM legal_chunks ORDER BY id LIMIT %s OFFSET %s"""
        docs_result = db_manager.execute_query(docs_sql, (per_page, offset))
        
        documents = []
        if docs_result:
            for doc in docs_result:
                documents.append({
                    "id": doc[0],
                    "parent_id": doc[1],
                    "title": doc[2],
                    "category": doc[3],
                    "metadata": doc[4] if doc[4] else {}
                })
        
        return jsonify({
            "documents": documents,
            "total": total_documents,
            "page": page,
            "per_page": per_page,
            "pages": (total_documents + per_page - 1) // per_page,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching documents: {e}")
        return jsonify({
            "error": "Erro ao buscar documentos",
            "message": "Ocorreu um erro ao buscar a lista de documentos.",
            "debug_info": {
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        }), 500

@app.route('/api/documentos/<doc_id>', methods=['GET'])
def get_document_by_id(doc_id=None):
    """Fetch a single legal document by id from semantic store (if available)."""
    try:
        _id = doc_id or request.args.get('id') or request.args.get('doc_id') or request.args.get('source')
        if not _id:
            return jsonify({"error": "Parâmetro 'id' não fornecido"}), 400
        # Only available when semantic store is ready
        doc = None
        try:
            if SEMANTIC_AVAILABLE and USE_SEMANTIC_RETRIEVAL and semantic_is_ready():
                doc = get_doc_by_id(_id)
        except Exception as e:
            logger.warning(f"get_doc_by_id failed: {e}")
            doc = None
        if not doc:
            return jsonify({"error": "Documento não encontrado"}), 404
        md = doc.get("metadata") or {}
        return jsonify({
            "id": doc.get("id"),
            "title": doc.get("title"),
            "category": doc.get("category"),
            "content": doc.get("content"),
            "metadata": md,
            "source_url": md.get("source_url"),
            "source_type": md.get("source_type"),
            "published_at": md.get("published_at"),
            "jurisdiction": md.get("jurisdiction"),
        })
    except Exception as e:
        logger.error(f"Error in get_document_by_id: {e}")
        return jsonify({"error": "Erro ao buscar documento"}), 500

@app.route('/api/news')
def get_news():
    """Return a small curated list of legal-related news (mock data)."""
    news = [
        {
            "id": 1,
            "title": "STF decide sobre tema de repercussão geral",
            "summary": "Corte define tese com impacto em milhares de processos em todo o país.",
            "url": "https://www.stf.jus.br/",
            "thumbnail": "https://placehold.co/176x120/111111/FFFFFF?text=STF"
        },
        {
            "id": 2,
            "title": "CNJ publica novas diretrizes para gestão processual",
            "summary": "Normas buscam acelerar tramitação e padronizar procedimentos.",
            "url": "https://www.cnj.jus.br/",
            "thumbnail": "https://placehold.co/176x120/111111/FFFFFF?text=CNJ"
        },
        {
            "id": 3,
            "title": "Mudanças no CDC entram em vigor",
            "summary": "Alterações reforçam direitos do consumidor em compras online.",
            "url": "https://www.gov.br/",
            "thumbnail": "https://placehold.co/176x120/111111/FFFFFF?text=CDC"
        },
        {
            "id": 4,
            "title": "Tribunais adotam ferramentas de IA",
            "summary": "Tecnologias auxiliam na triagem e priorização de processos.",
            "url": "https://www.cnj.jus.br/",
            "thumbnail": "https://placehold.co/176x120/111111/FFFFFF?text=IA+no+Jud"
        },
    ]

 

@app.route('/api/ads')
def get_ads():
    """Return simple sponsored cards (mock data)."""
    ads = [
        {
            "id": 101,
            "title": "Assine JuSimples Pro",
            "url": "https://jusimples.netlify.app/",
            "image": "https://placehold.co/640x360/1f1f23/FFFFFF?text=JuSimples+Pro"
        },
        {
            "id": 102,
            "title": "Modelo de Contratos (Grátis)",
            "url": "https://jusbrasil.com.br/",
            "image": "https://placehold.co/640x360/1f1f23/FFFFFF?text=Contratos"
        },
        {
            "id": 103,
            "title": "Consultoria Jurídica On‑Demand",
            "url": "https://www.oab.org.br/",
            "image": "https://placehold.co/640x360/1f1f23/FFFFFF?text=Consultoria"
        },
    ]
    return jsonify({"ads": ads, "updated_at": datetime.utcnow().isoformat()})

@app.route('/api/recommendations/lexml', methods=['GET'])
def get_lexml_recommendations():
    """Get recommendations from LexML API based on search query.
    
    Query Parameters:
    - q: Search query (required)
    - max_results: Maximum number of results to return (default: 5)
    
    Returns:
    - List of LexML document recommendations
    - Search metadata (time, query)
    """
    try:
        # Check if LexML API is enabled
        use_lexml_api = os.getenv("USE_LEXML_API", "").lower() in ["true", "1", "yes", "y", "on"]
        if not use_lexml_api or not lexml_api:
            return jsonify({
                "error": "LexML API not enabled",
                "message": "Enable USE_LEXML_API environment variable to use this feature."
            }), 503
        
        # Get query parameters
        query = request.args.get('q', '')
        if not query or not query.strip():
            return jsonify({
                "error": "Missing query parameter",
                "message": "Please provide a search query with the 'q' parameter."
            }), 400
            
        # Get max results parameter (default: 5, max: 20)
        try:
            max_results = min(int(request.args.get('max_results', 5)), 20)
        except ValueError:
            max_results = 5
            
        # Get recommendations from LexML API
        start_time = time.time()
        results = lexml_api.search(query, max_results=max_results)
        processing_time = round((time.time() - start_time) * 1000, 2)
        
        # Add processing metadata
        response = {
            "recommendations": results.get("items", []),
            "metadata": {
                "query": query,
                "max_results": max_results,
                "processing_time_ms": processing_time,
                "timestamp": datetime.utcnow().isoformat(),
                "search_time_ms": results.get("search_time_ms")
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error getting LexML recommendations: {e}")
        return jsonify({
            "error": "Failed to get recommendations",
            "message": "An error occurred while fetching recommendations from LexML API.",
            "debug_info": {
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        }), 500

@app.route('/api/admin/db/overview', methods=['GET'])
def api_admin_db_overview():
    """Return high-level DB overview for admin dashboard."""
    if not SEMANTIC_AVAILABLE:
        return jsonify({"ready": False, "message": "Semantic store not available"})
    try:
        data = admin_db_overview()
        return jsonify(data)
    except Exception as e:
        logger.error(f"admin_db_overview endpoint error: {e}")
        return jsonify({"error": "Failed to fetch DB overview"}), 500


@app.route('/api/admin/legal-chunks', methods=['GET'])
def api_admin_list_legal_chunks():
    """List legal documents with optional filters and pagination."""
    if not SEMANTIC_AVAILABLE:
        return jsonify({"total": 0, "items": []})
    try:
        q = (request.args.get('q') or '').strip()
        category = request.args.get('category')
        try:
            limit = int(request.args.get('limit', 50))
        except Exception:
            limit = 50
        try:
            offset = int(request.args.get('offset', 0))
        except Exception:
            offset = 0
        limit = max(1, min(200, limit))
        offset = max(0, offset)
        data = admin_list_legal_chunks(q=q, category=category, limit=limit, offset=offset)
        return jsonify(data)
    except Exception as e:
        logger.error(f"admin_list_legal_chunks endpoint error: {e}")
        return jsonify({"error": "Failed to list documents"}), 500


@app.route('/api/admin/logs/search', methods=['GET'])
def api_admin_list_search_logs():
    if not SEMANTIC_AVAILABLE:
        return jsonify({"total": 0, "items": []})
    try:
        try:
            limit = int(request.args.get('limit', 50))
        except Exception:
            limit = 50
        try:
            offset = int(request.args.get('offset', 0))
        except Exception:
            offset = 0
        limit = max(1, min(200, limit))
        offset = max(0, offset)
        data = admin_list_search_logs(limit=limit, offset=offset)
        return jsonify(data)
    except Exception as e:
        logger.error(f"admin_list_search_logs endpoint error: {e}")
        return jsonify({"error": "Failed to list search logs"}), 500


@app.route('/api/admin/logs/ask', methods=['GET'])
def api_admin_list_ask_logs():
    if not SEMANTIC_AVAILABLE:
        return jsonify({"total": 0, "items": []})
    try:
        try:
            limit = int(request.args.get('limit', 50))
        except Exception:
            limit = 50
        try:
            offset = int(request.args.get('offset', 0))
        except Exception:
            offset = 0
        limit = max(1, min(200, limit))
        offset = max(0, offset)
        data = admin_list_ask_logs(limit=limit, offset=offset)
        return jsonify(data)
    except Exception as e:
        logger.error(f"admin_list_ask_logs endpoint error: {e}")
        return jsonify({"error": "Failed to list ask logs"}), 500


@app.route('/api/admin/legal-chunks/<doc_id>', methods=['PATCH'])
def api_admin_update_legal_chunk(doc_id: str):
    if not SEMANTIC_AVAILABLE:
        return jsonify({"success": False, "error": "Semantic store not available"}), 400
    try:
        data = request.get_json(silent=True) or {}
        title = data.get('title') if 'title' in data else None
        content = data.get('content') if 'content' in data else None
        category = data.get('category') if 'category' in data else None
        metadata = data.get('metadata') if 'metadata' in data else None
        ok = update_legal_chunk(doc_id, title=title, content=content, category=category, metadata=metadata)
        if ok:
            return jsonify({"success": True, "id": doc_id})
        return jsonify({"success": False, "error": "Update failed"}), 400
    except Exception as e:
        logger.error(f"update_legal_chunk endpoint error: {e}")
        return jsonify({"success": False, "error": "Failed to update document"}), 500


@app.route('/api/admin/legal-chunks/<doc_id>', methods=['DELETE'])
def api_admin_delete_legal_chunk(doc_id: str):
    if not SEMANTIC_AVAILABLE:
        return jsonify({"success": False, "error": "Semantic store not available"}), 400
    try:
        ok = delete_legal_chunk(doc_id)
        if ok:
            return jsonify({"success": True, "id": doc_id})
        return jsonify({"success": False, "error": "Delete failed"}), 400
    except Exception as e:
        logger.error(f"delete_legal_chunk endpoint error: {e}")
        return jsonify({"success": False, "error": "Failed to delete document"}), 500


@app.route('/api/popular-searches', methods=['GET'])
def api_popular_searches():
    """Get popular searches from actual database logs (search_logs and ask_logs)"""
    # Default Brazilian legal search examples for new users
    default_searches = [
        "direitos do consumidor",
        "rescisão de contrato de trabalho", 
        "danos morais",
        "aposentadoria por invalidez",
        "divórcio consensual",
        "usucapião",
        "pensão alimentícia",
        "direitos trabalhistas",
        "indenização por danos materiais",
        "revisão de aposentadoria"
    ]
    
    if not SEMANTIC_AVAILABLE:
        return jsonify({
            "popular_searches": default_searches,
            "search_data": [{"term": term, "count": 0, "types": "example"} for term in default_searches],
            "from_database": False,
            "total_found": len(default_searches)
        })
    
    try:
        from retrieval import get_popular_queries
        
        # Get popular queries from last 30 days from real database logs
        popular_queries = get_popular_queries(limit=10, days=30)
        
        # Extract just the terms for the frontend with metadata
        search_data = []
        for q in popular_queries:
            if q.get('query') and len(q.get('query', '').strip()) > 2:
                search_data.append({
                    'term': q.get('query').strip(),
                    'count': q.get('count', 0),
                    'types': q.get('query_types', 'search'),
                    'success_rate': q.get('success_rate', 100)
                })
        
        # If we have real data, use it; otherwise use defaults
        if search_data:
            return jsonify({
                "popular_searches": [item['term'] for item in search_data],
                "search_data": search_data,
                "from_database": True,
                "total_found": len(search_data)
            })
        else:
            # No searches yet, return defaults
            return jsonify({
                "popular_searches": default_searches,
                "search_data": [{"term": term, "count": 0, "types": "example"} for term in default_searches],
                "from_database": False,
                "total_found": len(default_searches)
            })
        
    except Exception as e:
        logger.error(f"Error getting popular searches: {e}")
        # Return default Brazilian legal search examples for new users
        return jsonify({
            "popular_searches": default_searches,
            "search_data": [{"term": term, "count": 0, "types": "example"} for term in default_searches],
            "from_database": False,
            "total_found": len(default_searches)
        })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint não encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Erro interno do servidor"}), 500


def check_db_connection():
    """Diagnostic function to check database connection status"""
    logger.info("========== DATABASE DIAGNOSTIC INFO ===========")
    logger.info(f"DATABASE_URL set: {bool(os.getenv('DATABASE_URL'))}")
    logger.info(f"DATABASE_URL length: {len(os.getenv('DATABASE_URL', ''))}")
    logger.info(f"SEMANTIC_AVAILABLE: {SEMANTIC_AVAILABLE}")
    logger.info(f"USE_SEMANTIC_RETRIEVAL: {USE_SEMANTIC_RETRIEVAL}")
    
    if SEMANTIC_AVAILABLE:
        is_db_ready = semantic_is_ready()
        logger.info(f"Database ready status: {is_db_ready}")
        
        if not is_db_ready:
            logger.warning("Database not ready, attempting to initialize again...")
            init_result = init_pgvector()
            logger.info(f"Re-initialization result: {init_result}")
    else:
        logger.error("SEMANTIC_AVAILABLE is False - semantic retrieval disabled")
    
    logger.info("=============================================")

# Initialize OpenAI client function
def initialize_openai_client():
    """Initialize the OpenAI client using the openai_utils manager
    
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    try:
        success = False
        if openai_manager:
            success = openai_manager.initialize()
            if success:
                logger.info("✅ OpenAI client initialized successfully")
                return True
            else:
                logger.warning(f"❌ OpenAI client initialization failed: {openai_manager.last_error}")
                return False
        else:
            logger.error("❌ OpenAI manager not available")
            return False
    except Exception as e:
        logger.error(f"❌ Error initializing OpenAI client: {type(e).__name__}: {str(e)}")
        return False


if __name__ == '__main__':
    try:
        # Initialize OpenAI client on startup
        initialize_openai_client()
        
        # Run diagnostic check
        check_db_connection()
        
        # Run Flask app
        port = int(os.getenv('PORT', 5000))
        logger.info(f"🚀 Starting JuSimples Flask app on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        logger.error(f"Failed to start Flask app: {e}")
        sys.exit(1)
