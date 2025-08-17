import os
import sys
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import json
import sqlite3
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables only if .env file exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available, use environment variables directly
    pass

from admin_dashboard import admin_bp

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

app = Flask(__name__)

# Register admin dashboard blueprint
app.register_blueprint(admin_bp)

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

# Initialize OpenAI client (single path)
logger.info("=== OpenAI Client Initialization ===")
initialize_openai_client()

# ======================
# Authentication & Users
# ======================
# Environment
JWT_SECRET = os.getenv('JWT_SECRET_KEY', os.getenv('SECRET_KEY', 'dev_secret'))
JWT_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '3600'))  # seconds

# Database (SQLite)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_url = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'jusimples.db')}")
if db_url.startswith('sqlite:///'):
    DB_PATH = db_url.replace('sqlite:///', '')
else:
    # Fallback to local file if format differs
    DB_PATH = os.path.join(BASE_DIR, 'jusimples.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_user_table():
    try:
        conn = get_db_connection()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()
        logger.info("✅ Users table ensured in SQLite")
    except Exception as e:
        logger.error(f"❌ Failed to init users table: {e}")

def create_token(payload: Dict[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(seconds=JWT_EXPIRES)
    payload = {**payload, 'exp': expire}
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'Unauthorized'}), 401
        token = auth.split(' ', 1)[1]
        try:
            user = decode_token(token)
            request.user = user
        except Exception as e:
            return jsonify({'error': 'Invalid or expired token', 'detail': str(e)}), 401
        return f(*args, **kwargs)
    return wrapper

# Ensure DB table exists on startup
init_user_table()

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

def generate_ai_response(question, relevant_context):
    """Generate AI response using OpenAI with relevant legal context - VERSION 2.5.0"""
    global client, active_model
    
    logger.info(f"🔄 [v2.5.0] Starting AI response generation for: {question[:50]}...")
    
    # FORCE RETURN REAL RESPONSE FOR TESTING
    if "teste" in question.lower():
        return f"✅ VERSÃO 2.5.0 ATIVA! Pergunta recebida: {question}. Sistema OpenAI funcionando corretamente."
    
    # Check if we have a valid API key
    if not openai_api_key or openai_api_key.strip() == 'your_openai_api_key_here' or len(openai_api_key.strip()) < 20:
        error_msg = f"❌ Invalid OpenAI API key: length={len(openai_api_key) if openai_api_key else 0}"
        logger.error(error_msg)
        return f"ERRO API KEY v2.5.0: {error_msg}"
    
    # Create a fresh OpenAI client for this request
    try:
        logger.info("🔧 [v2.5.0] Creating fresh OpenAI client...")
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
        logger.info(f"🚀 [v2.5.0] Making OpenAI API call with model: {model_to_use}")
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
        logger.info(f"✅ [v2.5.0] SUCCESS! OpenAI response received, length: {len(ai_response)}")
        logger.info(f"📝 Response preview: {ai_response[:100]}...")
        
        # Update global client and model on success
        client = fresh_client
        active_model = model_to_use
        
        return ai_response
        
    except Exception as e:
        error_msg = f"❌ [v2.5.0] OpenAI API Error: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        return f"Erro na consulta à IA v2.5.0: {str(e)}"

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
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        logger.info(f"Received question request: {question[:100] if question else 'No question provided'}")
        logger.info(f"OpenAI client status: {'Available' if client else 'Not available'}")
        
        if not question:
            logger.warning("No question provided in request")
            return jsonify({"error": "Pergunta não fornecida"}), 400
        
        if len(question) < 10:
            logger.warning(f"Question too short: {len(question)} characters")
            return jsonify({"error": "Pergunta muito curta. Forneça mais detalhes."}), 400
        
        logger.info(f"Processing question: {question[:100]}...")
        
        # Search relevant legal knowledge
        relevant_context = search_legal_knowledge(question)
        logger.info(f"Found {len(relevant_context)} relevant documents")
        
        # Generate AI response
        ai_answer = generate_ai_response(question, relevant_context)
        logger.info(f"Generated AI response: {ai_answer[:100]}...")
        
        response = {
            "question": question,
            "answer": ai_answer,
            "sources": [
                {
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
                "knowledge_base_size": len(relevant_context)
            },
            "disclaimer": "Esta resposta é baseada em IA e tem caráter informativo. Para casos complexos, consulte um advogado especializado.",
            "debug_info": {
                "openai_available": client is not None,
                "active_model": active_model,
                "context_found": len(relevant_context),
                "api_key_configured": openai_api_key is not None and openai_api_key != 'your_openai_api_key_here'
            }
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
    try:
        data = request.get_json()
        query = data.get('query', '').lower().strip()
        
        if not query:
            return jsonify({"error": "Query não fornecida"}), 400
        
        # Search legal knowledge
        results = search_legal_knowledge(query)
        
        return jsonify({
            "query": query,
            "results": [
                {
                    "title": item["title"],
                    "content": item["content"],
                    "category": item["category"],
                    "relevance": item.get("relevance", 0)
                }
                for item in results
            ],
            "total": len(results),
            "search_type": "keyword"
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

# ======================
# Auth Endpoints
# ======================
@app.route('/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json() or {}
        email = (data.get('email') or '').strip().lower()
        name = (data.get('name') or '').strip()
        password = data.get('password') or ''
        if not email or not name or not password or len(password) < 6:
            return jsonify({'error': 'Dados inválidos'}), 400

        conn = get_db_connection()
        cur = conn.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cur.fetchone():
            conn.close()
            return jsonify({'error': 'E-mail já cadastrado'}), 409

        pwd_hash = generate_password_hash(password)
        now_iso = datetime.utcnow().isoformat()
        conn.execute(
            'INSERT INTO users (email, name, password_hash, created_at) VALUES (?, ?, ?, ?)',
            (email, name, pwd_hash, now_iso)
        )
        conn.commit()
        conn.close()

        token = create_token({'email': email, 'name': name})
        return jsonify({'token': token, 'user': {'email': email, 'name': name, 'created_at': now_iso}})
    except Exception as e:
        logger.error(f"Register error: {e}", exc_info=True)
        return jsonify({'error': 'Falha no cadastro'}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json() or {}
        email = (data.get('email') or '').strip().lower()
        password = data.get('password') or ''
        if not email or not password:
            return jsonify({'error': 'Credenciais inválidas'}), 400

        conn = get_db_connection()
        cur = conn.execute('SELECT id, email, name, password_hash, created_at FROM users WHERE email = ?', (email,))
        row = cur.fetchone()
        conn.close()
        if not row or not check_password_hash(row['password_hash'], password):
            return jsonify({'error': 'E-mail ou senha incorretos'}), 401

        token = create_token({'email': row['email'], 'name': row['name']})
        return jsonify({'token': token, 'user': {'email': row['email'], 'name': row['name'], 'created_at': row['created_at']}})
    except Exception as e:
        logger.error(f"Login error: {e}", exc_info=True)
        return jsonify({'error': 'Falha no login'}), 500

@app.route('/auth/me')
@auth_required
def me():
    try:
        user_claim = getattr(request, 'user', {})
        email = user_claim.get('email')
        conn = get_db_connection()
        cur = conn.execute('SELECT email, name, created_at FROM users WHERE email = ?', (email,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        return jsonify({'user': {'email': row['email'], 'name': row['name'], 'created_at': row['created_at']}})
    except Exception as e:
        logger.error(f"Me error: {e}", exc_info=True)
        return jsonify({'error': 'Falha ao obter usuário'}), 500

# ======================
# Content Endpoints (Footer)
# ======================
@app.route('/api/news')
def api_news():
    base_thumb = 'https://picsum.photos/seed'
    items = [
        {
            'id': 1,
            'title': 'STF decide sobre marco importante do direito do consumidor',
            'summary': 'Corte define parâmetros para garantias e práticas comerciais, impactando milhões de consumidores em todo o país.',
            'thumbnail': f"{base_thumb}/jusimples1/96/64",
            'url': 'https://www.stf.jus.br/'
        },
        {
            'id': 2,
            'title': 'Nova resolução do CNJ moderniza serviços judiciais digitais',
            'summary': 'Medida incentiva padronização e transparência nos tribunais, ampliando o acesso à justiça e eficiência.',
            'thumbnail': f"{base_thumb}/jusimples2/96/64",
            'url': 'https://www.cnj.jus.br/'
        },
        {
            'id': 3,
            'title': 'Lei Geral de Proteção de Dados: guia prático para cidadãos',
            'summary': 'Entenda seus direitos, como solicitar seus dados e como denunciar abuso de uso de informação pessoal.',
            'thumbnail': f"{base_thumb}/jusimples3/96/64",
            'url': 'https://www.gov.br/anpd/pt-br'
        }
    ]
    return jsonify({'news': items, 'total': len(items), 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/ads')
def api_ads():
    ads = [
        {
            'id': 'a1',
            'title': 'Seguro Jurídico Familiar a partir de R$12/mês',
            'image': 'https://picsum.photos/seed/jusad1/320/100',
            'url': 'https://example.com/seguro-juridico'
        },
        {
            'id': 'a2',
            'title': 'Cursos de Direito Digital - Inscrições Abertas',
            'image': 'https://picsum.photos/seed/jusad2/320/100',
            'url': 'https://example.com/curso-direito-digital'
        }
    ]
    return jsonify({'ads': ads, 'total': len(ads)})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint não encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Erro interno do servidor"}), 500

if __name__ == '__main__':
    try:
        # Initialize OpenAI client on startup
        initialize_openai_client()
        
        # Run Flask app
        port = int(os.getenv('PORT', 5000))
        logger.info(f"🚀 Starting JuSimples Flask app on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        logger.error(f"Failed to start Flask app: {e}")
        sys.exit(1)
