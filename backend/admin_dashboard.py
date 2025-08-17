import os
import logging
from datetime import datetime
from typing import Dict, List
from flask import Blueprint, jsonify, request, render_template_string
from openai import OpenAI

# Create admin blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin Dashboard HTML Template
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JuSimples Admin Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: #2563eb; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .status-good { color: #059669; }
        .status-bad { color: #dc2626; }
        .status-warning { color: #d97706; }
        .btn { background: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #1d4ed8; }
        .log-entry { padding: 8px; margin: 4px 0; background: #f8f9fa; border-left: 3px solid #2563eb; }
        .test-form { margin-top: 20px; }
        .test-form input, .test-form textarea { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 4px; }
        .response-box { background: #f8f9fa; padding: 15px; border-radius: 4px; margin-top: 10px; white-space: pre-wrap; }
        .env-var { display: flex; justify-content: space-between; align-items: center; padding: 8px; border-bottom: 1px solid #eee; }
        .knowledge-item { border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏛️ JuSimples Admin Dashboard</h1>
            <p>Sistema de monitoramento e configuração da plataforma jurídica</p>
        </div>

        <div class="grid">
            <!-- System Status -->
            <div class="card">
                <h3>📊 Status do Sistema</h3>
                <div id="system-status">Carregando...</div>
            </div>

            <!-- Environment Variables -->
            <div class="card">
                <h3>⚙️ Variáveis de Ambiente</h3>
                <div id="env-vars">Carregando...</div>
            </div>

            <!-- Knowledge Base -->
            <div class="card">
                <h3>📚 Base de Conhecimento</h3>
                <div id="knowledge-base">Carregando...</div>
            </div>

            <!-- Test RAG System -->
            <div class="card">
                <h3>🧪 Testar Sistema RAG</h3>
                <div class="test-form">
                    <textarea id="test-question" placeholder="Digite uma pergunta jurídica para testar..." rows="3"></textarea>
                    <button class="btn" onclick="testRAG()">Testar RAG</button>
                    <div id="test-response" class="response-box" style="display: none;"></div>
                </div>
            </div>

            <!-- System Logs -->
            <div class="card">
                <h3>📝 Logs do Sistema</h3>
                <button class="btn" onclick="refreshLogs()">Atualizar Logs</button>
                <div id="system-logs">Carregando...</div>
            </div>

            <!-- API Statistics -->
            <div class="card">
                <h3>📈 Estatísticas da API</h3>
                <div id="api-stats">Carregando...</div>
            </div>
        </div>
    </div>

    <script>
        // Load dashboard data
        async function loadDashboard() {
            try {
                const [status, envVars, knowledge, logs, stats] = await Promise.all([
                    fetch('/admin/api/status').then(r => r.json()),
                    fetch('/admin/api/env-vars').then(r => r.json()),
                    fetch('/admin/api/knowledge-base').then(r => r.json()),
                    fetch('/admin/api/logs').then(r => r.json()),
                    fetch('/admin/api/stats').then(r => r.json())
                ]);

                displaySystemStatus(status);
                displayEnvVars(envVars);
                displayKnowledgeBase(knowledge);
                displayLogs(logs);
                displayStats(stats);
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }

        function displaySystemStatus(status) {
            const statusHtml = `
                <div class="env-var">
                    <span>Sistema:</span>
                    <span class="${status.system_healthy ? 'status-good' : 'status-bad'}">
                        ${status.system_healthy ? '✅ Operacional' : '❌ Com problemas'}
                    </span>
                </div>
                <div class="env-var">
                    <span>OpenAI Client:</span>
                    <span class="${status.openai_available ? 'status-good' : 'status-bad'}">
                        ${status.openai_available ? '✅ Conectado' : '❌ Não disponível'}
                    </span>
                </div>
                <div class="env-var">
                    <span>Base de Conhecimento:</span>
                    <span class="status-good">✅ ${status.knowledge_count} documentos</span>
                </div>
                <div class="env-var">
                    <span>Última atualização:</span>
                    <span>${new Date(status.timestamp).toLocaleString('pt-BR')}</span>
                </div>
            `;
            document.getElementById('system-status').innerHTML = statusHtml;
        }

        function displayEnvVars(envVars) {
            const envHtml = Object.entries(envVars).map(([key, value]) => `
                <div class="env-var">
                    <span><strong>${key}:</strong></span>
                    <span class="${value.status === 'set' ? 'status-good' : 'status-bad'}">
                        ${value.status === 'set' ? '✅ Configurada' : '❌ Não configurada'}
                    </span>
                </div>
            `).join('');
            document.getElementById('env-vars').innerHTML = envHtml;
        }

        function displayKnowledgeBase(knowledge) {
            const knowledgeHtml = `
                <p><strong>Total:</strong> ${knowledge.total} documentos</p>
                <p><strong>Categorias:</strong> ${knowledge.categories.join(', ')}</p>
                <div style="max-height: 200px; overflow-y: auto; margin-top: 10px;">
                    ${knowledge.documents.map(doc => `
                        <div class="knowledge-item">
                            <strong>${doc.title}</strong><br>
                            <small>Categoria: ${doc.category} | Palavras-chave: ${doc.keywords.join(', ')}</small>
                        </div>
                    `).join('')}
                </div>
            `;
            document.getElementById('knowledge-base').innerHTML = knowledgeHtml;
        }

        function displayLogs(logs) {
            const logsHtml = logs.entries.slice(-10).map(log => `
                <div class="log-entry">
                    <small>${log.timestamp}</small><br>
                    <strong>${log.level}:</strong> ${log.message}
                </div>
            `).join('');
            document.getElementById('system-logs').innerHTML = logsHtml || '<p>Nenhum log disponível</p>';
        }

        function displayStats(stats) {
            const statsHtml = `
                <div class="env-var">
                    <span>Total de perguntas:</span>
                    <span>${stats.total_questions}</span>
                </div>
                <div class="env-var">
                    <span>Perguntas hoje:</span>
                    <span>${stats.questions_today}</span>
                </div>
                <div class="env-var">
                    <span>Taxa de sucesso:</span>
                    <span class="${stats.success_rate > 0.8 ? 'status-good' : 'status-warning'}">
                        ${(stats.success_rate * 100).toFixed(1)}%
                    </span>
                </div>
                <div class="env-var">
                    <span>Tempo médio de resposta:</span>
                    <span>${stats.avg_response_time}ms</span>
                </div>
            `;
            document.getElementById('api-stats').innerHTML = statsHtml;
        }

        async function testRAG() {
            const question = document.getElementById('test-question').value;
            if (!question.trim()) {
                alert('Digite uma pergunta para testar');
                return;
            }

            const responseDiv = document.getElementById('test-response');
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = 'Processando...';

            try {
                const response = await fetch('/admin/api/test-rag', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question })
                });

                const result = await response.json();
                responseDiv.innerHTML = JSON.stringify(result, null, 2);
            } catch (error) {
                responseDiv.innerHTML = `Erro: ${error.message}`;
            }
        }

        function refreshLogs() {
            fetch('/admin/api/logs')
                .then(r => r.json())
                .then(displayLogs)
                .catch(console.error);
        }

        // Load dashboard on page load
        loadDashboard();
        
        // Auto-refresh every 30 seconds
        setInterval(loadDashboard, 30000);
    </script>
</body>
</html>
"""

@admin_bp.route('/')
def dashboard():
    """Admin dashboard main page"""
    return render_template_string(ADMIN_TEMPLATE)

@admin_bp.route('/api/status')
def api_status():
    """API endpoint for system status"""
    from app import client, LEGAL_KNOWLEDGE, active_model
    
    return jsonify({
        "system": "Operacional" if client else "Com problemas",
        "openai_client": "Disponível" if client else "Não disponível",
        "active_model": active_model or "Não configurado",
        "knowledge_base": f"{len(LEGAL_KNOWLEDGE)} documentos",
        "last_update": datetime.utcnow().isoformat()
    })

@admin_bp.route('/api/env-vars')
def get_env_vars():
    """Get environment variables status"""
    env_vars = {
        "OPENAI_API_KEY": {
            "status": "set" if os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here' else "not_set",
            "value": "***" if os.getenv('OPENAI_API_KEY') else None
        },
        "OPENAI_MODEL": {
            "status": "set" if os.getenv('OPENAI_MODEL') else "not_set",
            "value": os.getenv('OPENAI_MODEL', 'not_set')
        },
        "CORS_ORIGINS": {
            "status": "set" if os.getenv('CORS_ORIGINS') else "not_set",
            "value": os.getenv('CORS_ORIGINS', 'not_set')
        },
        "FLASK_ENV": {
            "status": "set" if os.getenv('FLASK_ENV') else "not_set",
            "value": os.getenv('FLASK_ENV', 'not_set')
        },
        "PORT": {
            "status": "set" if os.getenv('PORT') else "not_set",
            "value": os.getenv('PORT', 'not_set')
        }
    }
    
    return jsonify(env_vars)

@admin_bp.route('/api/knowledge-base')
def get_knowledge_base():
    """Get knowledge base information"""
    from app import LEGAL_KNOWLEDGE
    
    categories = list(set(doc['category'] for doc in LEGAL_KNOWLEDGE))
    
    return jsonify({
        "total": len(LEGAL_KNOWLEDGE),
        "categories": categories,
        "documents": LEGAL_KNOWLEDGE,
        "last_updated": datetime.utcnow().isoformat()
    })

@admin_bp.route('/api/logs')
def get_system_logs():
    """Get system logs (simplified)"""
    # In a real system, you'd read from log files
    logs = {
        "entries": [
            {
                "timestamp": datetime.utcnow().isoformat(),
                "level": "INFO",
                "message": "Admin dashboard accessed"
            },
            {
                "timestamp": datetime.utcnow().isoformat(),
                "level": "INFO", 
                "message": f"System status: OpenAI client {'available' if os.getenv('OPENAI_API_KEY') else 'not available'}"
            }
        ]
    }
    
    return jsonify(logs)

@admin_bp.route('/api/stats')
def get_api_stats():
    """Get API statistics (mock data for now)"""
    return jsonify({
        "total_questions": 0,
        "questions_today": 0,
        "success_rate": 0.0 if not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your_openai_api_key_here' else 0.95,
        "avg_response_time": 1200,
        "last_updated": datetime.utcnow().isoformat()
    })

@admin_bp.route('/api/test-rag', methods=['POST'])
def test_rag_system():
    """Test the RAG system with a question"""
    try:
        from app import search_legal_knowledge, generate_ai_response
        
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        # Test the full RAG pipeline
        start_time = datetime.utcnow()
        
        # Step 1: Search knowledge base
        relevant_context = search_legal_knowledge(question)
        
        # Step 2: Generate AI response
        ai_answer = generate_ai_response(question, relevant_context)
        
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds() * 1000
        
        return jsonify({
            "question": question,
            "relevant_context": relevant_context,
            "ai_answer": ai_answer,
            "processing_time_ms": processing_time,
            "timestamp": start_time.isoformat(),
            "system_status": {
                "openai_available": os.getenv('OPENAI_API_KEY') is not None and os.getenv('OPENAI_API_KEY') != 'your_openai_api_key_here',
                "knowledge_base_size": len(relevant_context)
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@admin_bp.route('/api/update-knowledge', methods=['POST'])
def update_knowledge_base():
    """Update knowledge base (future feature)"""
    return jsonify({
        "message": "Knowledge base update feature coming soon",
        "status": "not_implemented"
    }), 501
