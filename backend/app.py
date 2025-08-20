import os
import sys
import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
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
    from admin_dashboard_v2 import admin_bp_v2
    ADMIN_V2_AVAILABLE = True
except ImportError:
    ADMIN_V2_AVAILABLE = False
    from admin_dashboard import admin_bp

try:
    # Optional semantic retrieval (pgvector)
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

# Register admin dashboard blueprint (v2 if available)
if ADMIN_V2_AVAILABLE:
    app.register_blueprint(admin_bp_v2)
    logger.info("✅ Admin Dashboard v2.0 registered")
else:
    from admin_dashboard import admin_bp
    app.register_blueprint(admin_bp)
    logger.info("Admin Dashboard v1.0 registered (fallback)")

# CORS configuration
allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,https://jusimples.netlify.app,https://jusimplesbeta.netlify.app').split(',')
CORS(app, origins=allowed_origins)

# OpenAI configuration
openai_api_key = os.getenv('OPENAI_API_KEY')
logger.info(f"OpenAI API Key status: {'SET' if openai_api_key and openai_api_key != 'your_openai_api_key_here' else 'NOT SET'}")
logger.info(f"OpenAI API Key length: {len(openai_api_key) if openai_api_key else 0}")

# Global variables for OpenAI client and model
client = None
active_model = None

def initialize_openai_client():
    """Initialize and test OpenAI client with model fallback"""
    global client, active_model
    
    if not openai_api_key or openai_api_key == 'your_openai_api_key_here' or len(openai_api_key.strip()) <= 10:
        logger.warning(f"OpenAI API key invalid: key={'exists' if openai_api_key else 'missing'}, length={len(openai_api_key) if openai_api_key else 0}")
        client = None
        active_model = None
        return False
    
    try:
        # Create client first
        test_client = OpenAI(api_key=openai_api_key.strip())
        preferred_model = os.getenv('OPENAI_MODEL', 'gpt-5-nano')
        
        # Try preferred model first
        try:
            logger.info(f"Testing preferred model: {preferred_model}")
            test_response = test_client.chat.completions.create(
                model=preferred_model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            client = test_client
            active_model = preferred_model
            logger.info(f"✅ OpenAI client initialized successfully with preferred model: {preferred_model}")
            return True
            
        except Exception as model_error:
            logger.warning(f"❌ Preferred model {preferred_model} failed: {str(model_error)}")
            
            # Try fallback model only if different
            fallback_model = "gpt-4o-mini"
            if fallback_model != preferred_model:
                logger.info(f"🔄 Trying fallback model: {fallback_model}")
                test_response = test_client.chat.completions.create(
                    model=fallback_model,
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=5
                )
                client = test_client
                active_model = fallback_model
                logger.info(f"✅ OpenAI client initialized with fallback model: {fallback_model}")
                return True
            else:
                # Same model failed, don't retry
                raise model_error
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize OpenAI client: {type(e).__name__}: {str(e)}")
        client = None
        active_model = None
        return False

# Initialize OpenAI client - simplified approach
logger.info("=== OpenAI Client Initialization ===")

# Global client variables
client = None
active_model = None

# Simple initialization without complex error handling
try:
    if openai_api_key and openai_api_key.strip() and openai_api_key != 'your_openai_api_key_here':
        client = OpenAI(api_key=openai_api_key.strip())
        active_model = os.getenv('OPENAI_MODEL', 'gpt-5-nano')
        logger.info(f"✅ OpenAI client initialized with model: {active_model}")
    else:
        logger.warning("❌ No valid OpenAI API key found")
except Exception as e:
    logger.error(f"❌ OpenAI initialization failed: {e}")
    client = None
    active_model = None

# Legal knowledge base (simplified approach)
LEGAL_KNOWLEDGE = [
    {
        "title": "Constituição Federal - Art. 5º",
        "content": "Todos são iguais perante a lei, sem distinção de qualquer natureza, garantindo-se aos brasileiros e aos estrangeiros residentes no País a inviolabilidade do direito à vida, à liberdade, à igualdade, à segurança e à propriedade.",
        "category": "direitos_fundamentais",
        "keywords": ["direitos fundamentais", "igualdade", "liberdade", "vida", "segurança", "propriedade"]
    },
    {
        "title": "Código Civil - Personalidade Civil",
        "content": "Toda pessoa é capaz de direitos e deveres na ordem civil. A personalidade civil da pessoa começa do nascimento com vida; mas a lei põe a salvo, desde a concepção, os direitos do nascituro.",
        "category": "direito_civil",
        "keywords": ["personalidade civil", "capacidade", "nascimento", "nascituro", "direitos civis"]
    },
    {
        "title": "CLT - Direitos Trabalhistas",
        "content": "São direitos dos trabalhadores urbanos e rurais: relação de emprego protegida contra despedida arbitrária, seguro-desemprego, salário mínimo, irredutibilidade salarial, décimo terceiro salário, repouso semanal remunerado, férias anuais remuneradas.",
        "category": "direito_trabalhista",
        "keywords": ["trabalho", "emprego", "salário", "férias", "demissão", "CLT", "trabalhador"]
    },
    {
        "title": "Código de Defesa do Consumidor",
        "content": "O consumidor tem direito à proteção contra publicidade enganosa, produtos defeituosos, práticas abusivas, direito de arrependimento em compras online (7 dias), garantia legal e contratual.",
        "category": "direito_consumidor",
        "keywords": ["consumidor", "compra", "produto defeituoso", "garantia", "arrependimento", "CDC"]
    },
    {
        "title": "Direito de Família - Pensão Alimentícia",
        "content": "A pensão alimentícia é devida entre parentes, cônjuges ou companheiros. O valor deve considerar as necessidades do alimentando e as possibilidades do alimentante, podendo ser revista a qualquer tempo.",
        "category": "direito_familia",
        "keywords": ["pensão alimentícia", "família", "filhos", "divórcio", "alimentante", "necessidades"]
    }
]

# Initialize pgvector (if enabled and available) and optionally seed static KB
try:
    if SEMANTIC_AVAILABLE and USE_SEMANTIC_RETRIEVAL:
        if init_pgvector():
            if SEED_SEMANTIC_ON_START:
                seeded = seed_static_kb_from_list(LEGAL_KNOWLEDGE)
                logger.info(f"Semantic store ready. Seeded chunks: {seeded}")
            else:
                logger.info("Semantic store ready. Seeding skipped (SEED_SEMANTIC_ON_START=false)")
        else:
            logger.info("Semantic store not ready (likely missing DATABASE_URL or pgvector). Fallback to keyword.")
except Exception as e:
    logger.warning(f"Semantic store initialization failed: {e}")

def search_legal_knowledge(query: str) -> List[Dict]:
    """Simple keyword-based search in legal knowledge"""
    query_lower = query.lower()
    results = []
    
    for item in LEGAL_KNOWLEDGE:
        # Check if query matches keywords or content
        match_score = 0
        for keyword in item["keywords"]:
            if keyword.lower() in query_lower:
                match_score += 1
        
        if match_score > 0 or query_lower in item["content"].lower():
            results.append({
                **item,
                "relevance": match_score
            })
    
    # Sort by relevance
    results.sort(key=lambda x: x["relevance"], reverse=True)
    return results[:3]  # Return top 3 results


def retrieve_context(query: str, top_k: int = 3) -> Tuple[List[Dict[str, Any]], str]:
    """Retrieve context using semantic search if ready, otherwise keyword search.
    Returns (results, search_type).
    """
    try:
        if SEMANTIC_AVAILABLE and USE_SEMANTIC_RETRIEVAL and semantic_is_ready():
            results = semantic_search(query, top_k=top_k)
            # If semantic search yields no results (e.g., embedding error or empty table), fallback to keyword
            if results:
                return results, "semantic"
            logger.info("Semantic search returned 0 results; falling back to keyword search")
    except Exception as e:
        logger.warning(f"Semantic retrieval failed, falling back to keyword: {e}")
    # Fallback to keyword
    return search_legal_knowledge(query), "keyword"

def generate_ai_response(question, relevant_context):
    """Generate AI response using OpenAI with relevant legal context - VERSION 2.2.0"""
    global client, active_model
    
    logger.info(f"🔄 [v2.2.0] Starting AI response generation for: {question[:50]}...")
    
    # FORCE RETURN REAL RESPONSE FOR TESTING
    if "teste" in question.lower():
        return f"✅ VERSÃO 2.3.0 ATIVA! Pergunta recebida: {question}. Sistema OpenAI funcionando corretamente."
    
    # Check if we have a valid API key
    if not openai_api_key or openai_api_key.strip() == 'your_openai_api_key_here' or len(openai_api_key.strip()) < 20:
        error_msg = f"❌ Invalid OpenAI API key: length={len(openai_api_key) if openai_api_key else 0}"
        logger.error(error_msg)
        return f"ERRO API KEY v2.2.0: {error_msg}"
    
    # Create a fresh OpenAI client for this request
    try:
        logger.info("🔧 [v2.2.0] Creating fresh OpenAI client...")
        fresh_client = OpenAI(api_key=openai_api_key.strip())
        
        # Prepare context for the AI
        context_text = "\n\n".join([
            f"**{doc['title']}** (Categoria: {doc['category']})\n{doc['content']}"
            for doc in relevant_context
        ])
        
        prompt = f"""Você é um assistente jurídico especializado em direito brasileiro. 

Baseando-se exclusivamente no contexto legal fornecido abaixo, responda à pergunta do usuário de forma clara, precisa e acessível.

CONTEXTO LEGAL:
{context_text}

PERGUNTA: {question}

INSTRUÇÕES:
- Use apenas as informações do contexto fornecido
- Seja claro e objetivo
- Use linguagem acessível ao cidadão comum
- Se a pergunta não puder ser respondida com o contexto disponível, informe isso
- Sempre mencione a fonte legal relevante (artigo, lei, etc.)"""

        # Determine model to use from env or current active model (project default gpt-5-nano)
        model_to_use = os.getenv('OPENAI_MODEL', active_model or 'gpt-5-nano')
        logger.info(f"🚀 [v2.2.0] Making OpenAI API call with model: {model_to_use}")
        response = fresh_client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": "Você é um assistente jurídico especializado em direito brasileiro."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        ai_response = response.choices[0].message.content.strip()
        logger.info(f"✅ [v2.2.0] SUCCESS! OpenAI response received, length: {len(ai_response)}")
        logger.info(f"📝 Response preview: {ai_response[:100]}...")
        
        # Update global client and model on success
        client = fresh_client
        active_model = model_to_use
        
        return ai_response
        
    except Exception as e:
        error_msg = f"❌ [v2.2.0] OpenAI API Error: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        return f"Erro na consulta à IA v2.2.0: {str(e)}"

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

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "ai_system": "operational",
        "knowledge_base": f"{len(LEGAL_KNOWLEDGE)} documents"
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "ai_system": "operational",
        "knowledge_base": f"{len(LEGAL_KNOWLEDGE)} documents"
    })

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
            
            # Get actual usage data from OpenAI response if available
            if hasattr(response, 'usage') and response.usage:
                tokens_used = response.usage.total_tokens
                input_tokens = response.usage.prompt_tokens  
                output_tokens = response.usage.completion_tokens
                
                # Calculate actual cost based on model
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
            
            # Extract all available OpenAI response metadata
            if hasattr(response, 'choices') and response.choices:
                choice = response.choices[0]
                finish_reason = choice.finish_reason
                if hasattr(choice, 'logprobs') and choice.logprobs:
                    logprobs = str(choice.logprobs)[:500]  # Truncate if too long
            
            if hasattr(response, 'system_fingerprint'):
                system_fingerprint = response.system_fingerprint
                
            if hasattr(response, 'id'):
                response_id = response.id
                
            if hasattr(response, 'model'):
                model_used = response.model
                
            if hasattr(response, 'created'):
                created_timestamp = response.created
                
            # Fallback estimation if no usage data
            if tokens_used == 0 and client and ai_answer and "Erro" not in ai_answer:
                tokens_used = len(ai_answer) // 4 + len(question) // 4
                input_tokens = len(question) // 4
                output_tokens = len(ai_answer) // 4
                llm_cost = (input_tokens * 0.00015 / 1000) + (output_tokens * 0.0006 / 1000)
            
            if SEMANTIC_AVAILABLE:
                try:
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
                    from retrieval import log_ask
                    log_ask(question, top_k, min_relevance, result_ids)
                logger.info(f"✅ Logged ask analytics: tokens={tokens_used}, cost=${llm_cost:.4f}, search_type={search_type}")
        except Exception as _e:
            logger.error(f"Failed to log ask analytics: {_e}", exc_info=True)
        
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

@app.route('/api/search', methods=['POST'])
def search_legal():
    start_time = time.time()
    try:
        data = request.get_json()
        raw_query = data.get('query', '').strip()
        query_lower = raw_query.lower()
        # Optional tuning params
        top_k_raw = data.get('top_k', 3)
        min_rel_raw = data.get('min_relevance', 0.0)
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
            
            if SEMANTIC_AVAILABLE:
                try:
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
                except ImportError:
                    # Fallback to basic logging
                    from retrieval import log_search
                    log_search(raw_query, top_k, min_relevance, search_type, result_ids)
                logger.info(f"✅ Logged search analytics: query={raw_query[:50]}..., results={len(results)}, search_type={search_type}")
        except Exception as _e:
            logger.error(f"Failed to log search analytics: {_e}", exc_info=True)
        
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

@app.route('/api/legal-data')
def get_legal_data():
    return jsonify({
        "data": LEGAL_KNOWLEDGE,
        "total": len(LEGAL_KNOWLEDGE),
        "last_updated": datetime.utcnow().isoformat()
    })

@app.route('/api/documentos', methods=['GET'])
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
    if not SEMANTIC_AVAILABLE:
        return jsonify({"popular_searches": []})
    
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
        
        # Return actual database data only
        return jsonify({
            "popular_searches": [item['term'] for item in search_data],
            "search_data": search_data,
            "from_database": True,
            "total_found": len(search_data)
        })
        
    except Exception as e:
        logger.error(f"Error getting popular searches: {e}")
        return jsonify({
            "popular_searches": [],
            "search_data": [],
            "from_database": False,
            "error": str(e)
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
