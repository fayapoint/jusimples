import os
import sys
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

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
        preferred_model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        
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
        active_model = "gpt-4o-mini"
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
    """Generate AI response using OpenAI with relevant legal context"""
    # Re-initialize client if not available
    if not client:
        logger.info("Client not available, attempting to re-initialize...")
        initialize_success = initialize_openai_client()
        if not initialize_success:
            return "Sistema de IA não disponível no momento. Serviço está sendo configurado."
    
    try:
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

        response = client.chat.completions.create(
            model=active_model or "gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente jurídico especializado em direito brasileiro."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        # Try to re-initialize on error
        initialize_openai_client()
        return "Erro ao processar sua pergunta. Tente novamente em alguns instantes."

@app.route('/')
def home():
    return jsonify({
        "message": "JuSimples Legal AI API",
        "version": "2.1.0",
        "status": "running",
        "mode": "simplified"
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

@app.route('/api/switch-model', methods=['POST'])
def switch_model():
    """Switch OpenAI model and reinitialize client"""
    try:
        data = request.get_json()
        new_model = data.get('model', 'gpt-4o-mini')
        
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint não encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Erro interno do servidor"}), 500

if __name__ == '__main__':
    try:
        port = int(os.getenv('PORT', 5000))
        logger.info(f"Starting Flask app on port {port}")
        logger.info(f"OpenAI client status: {'Available' if client else 'Not available'}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        logger.error(f"Failed to start Flask app: {e}")
        sys.exit(1)
