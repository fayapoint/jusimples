import os
import logging
from datetime import datetime
from typing import Dict, List

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from admin_dashboard import admin_bp

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

client = None
try:
    if openai_api_key and openai_api_key != 'your_openai_api_key_here' and len(openai_api_key.strip()) > 10:
        # Initialize client without immediate test (test on first use)
        client = OpenAI(api_key=openai_api_key.strip())
        logger.info("OpenAI client initialized successfully")
    else:
        logger.warning(f"OpenAI API key invalid: key={'exists' if openai_api_key else 'missing'}, length={len(openai_api_key) if openai_api_key else 0}")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {type(e).__name__}: {str(e)}")
    client = None

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

def generate_ai_response(question: str, context: List[Dict]) -> str:
    """Generate AI response using OpenAI with legal context"""
    if not client:
        return "Sistema de IA não disponível no momento. Serviço está sendo configurado."
    
    try:
        # Build context from legal knowledge
        context_text = ""
        if context:
            context_text = "Contexto legal relevante:\n"
            for item in context:
                context_text += f"- {item['title']}: {item['content']}\n"
        
        prompt = f"""Você é um assistente jurídico especializado em direito brasileiro. 
        Responda a pergunta de forma clara, precisa e acessível para pessoas sem conhecimento jurídico avançado.

        {context_text}

        Pergunta: {question}

        Forneça uma resposta estruturada que inclua:
        1. Resposta direta e clara
        2. Base legal quando aplicável
        3. Orientações práticas
        4. Recomendação de consultar um advogado para casos complexos

        Mantenha a resposta concisa mas completa."""

        model = os.getenv('OPENAI_MODEL', 'gpt-5-nano')
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error generating AI response: {str(e)}")
        return "Não foi possível gerar uma resposta no momento. Tente novamente ou consulte um advogado."

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
            "disclaimer": "Esta resposta é baseada em IA e tem caráter informativo. Para casos complexos, consulte um advogado especializado.",
            "debug_info": {
                "openai_available": client is not None,
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

@app.route('/api/debug')
def debug_system():
    """Debug endpoint to check system status"""
    return jsonify({
        "openai_api_key_set": openai_api_key is not None and openai_api_key != 'your_openai_api_key_here',
        "openai_client_available": client is not None,
        "cors_origins": os.getenv('CORS_ORIGINS', 'not_set'),
        "flask_env": os.getenv('FLASK_ENV', 'not_set'),
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
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting JuSimples API (Simplified) on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
