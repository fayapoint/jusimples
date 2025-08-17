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
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
        }
        .container { max-width: 1250px; margin: 0 auto; padding: 24px; }
        .header {
            background: rgba(37, 99, 235, 0.2);
            color: #fff;
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.18);
            backdrop-filter: blur(8px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }
        .card {
            background: rgba(255, 255, 255, 0.08);
            padding: 20px; border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.18);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        }
        h3 { color: #fff; margin-bottom: 10px; }
        .status-good { color: #34d399; }
        .status-bad { color: #f87171; }
        .status-warning { color: #fbbf24; }
        .btn { background: #2563eb; color: white; padding: 10px 16px; border: none; border-radius: 10px; cursor: pointer; }
        .btn:hover { background: #1d4ed8; }
        .btn.secondary { background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.18); }
        .log-entry { padding: 8px; margin: 4px 0; background: rgba(255,255,255,0.06); border-left: 3px solid #60a5fa; border-radius: 6px; }
        .test-form { margin-top: 12px; }
        .test-form textarea, select, input {
            width: 100%; padding: 10px; margin: 6px 0;
            background: rgba(255,255,255,0.06); color: #e2e8f0;
            border: 1px solid rgba(255,255,255,0.2); border-radius: 10px;
        }
        .response-box { background: rgba(255,255,255,0.06); padding: 15px; border-radius: 10px; margin-top: 10px; white-space: pre-wrap; border: 1px solid rgba(255,255,255,0.2); }
        .env-var { display: flex; justify-content: space-between; align-items: center; padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .knowledge-item { border: 1px solid rgba(255,255,255,0.12); padding: 10px; margin: 5px 0; border-radius: 10px; background: rgba(255,255,255,0.04); }
        .small { font-size: 12px; opacity: 0.8; }
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

            <!-- Model Controls -->
            <div class="card">
                <h3>🤖 Controle de Modelo</h3>
                <div class="test-form">
                    <div class="small">Modelo atual: <span id="current-model">-</span></div>
                    <select id="model-select">
                        <option value="gpt-5-nano">gpt-5-nano (padrão)</option>
                        <option value="gpt-4o-mini">gpt-4o-mini</option>
                        <option value="gpt-mini">gpt-mini</option>
                    </select>
                    <button class="btn" onclick="updateModel()">Aplicar</button>
                </div>
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
                populateModelControls(status.active_model);
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
                const sourcesHtml = (result.relevant_context || []).map((doc) => `
                    <div class="knowledge-item">
                        <strong>${doc.title}</strong><br>
                        <small>Categoria: ${doc.category} | Palavras-chave: ${(doc.keywords||[]).join(', ')}</small>
                        <div class="small">Trecho: ${doc.content?.slice(0,160) || ''}...</div>
                    </div>
                `).join('');

                responseDiv.innerHTML = `
                    <div><strong>Resposta da IA:</strong></div>
                    <div style="margin-top:6px;">${result.ai_answer || 'Sem resposta'}</div>
                    <div class="small" style="margin-top:10px;">Tempo: ${Math.round(result.processing_time_ms||0)}ms</div>
                    <hr style="margin:10px 0; border-color: rgba(255,255,255,0.1);">
                    <div><strong>Fontes:</strong></div>
                    ${sourcesHtml || '<div class="small">Sem fontes</div>'}
                `;
            } catch (error) {
                responseDiv.innerHTML = `Erro: ${error.message}`;
            }
        }

        function populateModelControls(activeModel) {
            const select = document.getElementById('model-select');
            const current = document.getElementById('current-model');
            if (activeModel) {
                current.textContent = activeModel;
                for (const opt of select.options) {
                    if (opt.value === activeModel) opt.selected = true;
                }
            }
        }

        async function updateModel() {
            const model = document.getElementById('model-select').value;
            try {
                const res = await fetch('/api/switch-model', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ model })
                });
                const data = await res.json();
                if (data.success) {
                    document.getElementById('current-model').textContent = data.active_model;
                    alert(`Modelo atualizado para: ${data.active_model}`);
                    loadDashboard();
                } else {
                    alert('Falha ao atualizar modelo: ' + (data.message || ''));
                }
            } catch (e) {
                alert('Erro ao atualizar modelo: ' + e.message);
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
    
    # Test OpenAI client availability (non-fatal)
    openai_available = False
    if client:
        try:
            _ = client.chat.completions.create(
                model=active_model or "gpt-5-nano",
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=1
            )
            openai_available = True
        except Exception:
            openai_available = False

    now_iso = datetime.utcnow().isoformat()
    knowledge_count = len(LEGAL_KNOWLEDGE)
    system_healthy = openai_available and knowledge_count >= 0

    # Return both the new structure (used by JS) and legacy fields (for compatibility)
    return jsonify({
        # New fields expected by JS
        "system_healthy": system_healthy,
        "openai_available": openai_available,
        "knowledge_count": knowledge_count,
        "timestamp": now_iso,
        "active_model": active_model or "Não configurado",
        # Legacy fields kept for compatibility
        "system": "Operacional" if system_healthy else "Com problemas",
        "openai_client": "Disponível" if openai_available else "Não disponível",
        "knowledge_base": f"{knowledge_count} documentos",
        "last_update": now_iso
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
