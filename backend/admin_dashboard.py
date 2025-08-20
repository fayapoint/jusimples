import os
import logging
from datetime import datetime
from typing import Dict, List
from flask import Blueprint, jsonify, request, render_template_string, current_app

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
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.12); text-align: left; vertical-align: top; }
        .controls { display: flex; gap: 8px; align-items: center; }
        .muted { opacity: 0.7; }
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

            <!-- DB Overview (Semantic) -->
            <div class="card">
                <h3>📦 Banco de Dados (Visão Geral)</h3>
                <div id="db-overview" class="small">Carregando...</div>
            </div>

            <!-- Manage Legal Chunks -->
            <div class="card">
                <h3>🗂️ Documentos (legal_chunks)</h3>
                <div class="controls">
                    <input id="doc-q" placeholder="Buscar por título/conteúdo" />
                    <input id="doc-category" placeholder="Categoria (opcional)" />
                    <button class="btn" onclick="loadDocs(0)">Buscar</button>
                    <button class="btn secondary" onclick="resetDocFilters()">Limpar</button>
                </div>
                <div id="doc-list" class="small" style="max-height: 360px; overflow-y:auto; margin-top: 8px;">Carregando...</div>
                <div class="controls" style="margin-top:8px;">
                    <button class="btn secondary" onclick="prevDocsPage()">◀</button>
                    <span id="doc-page-info" class="muted">Página 1</span>
                    <button class="btn secondary" onclick="nextDocsPage()">▶</button>
                </div>
            </div>

            <!-- Retrieval Logs (semantic) -->
            <div class="card">
                <h3>🔎 Logs de Busca & Perguntas</h3>
                <div class="controls">
                    <button class="btn" onclick="loadSearchLogs()">Carregar Busca</button>
                    <button class="btn secondary" onclick="loadAskLogs()">Carregar Perguntas</button>
                </div>
                <div id="search-logs" class="small" style="margin-top: 8px; max-height: 200px; overflow-y:auto;"></div>
                <div id="ask-logs" class="small" style="margin-top: 8px; max-height: 200px; overflow-y:auto;"></div>
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

                // Load semantic-backed admin data (best-effort)
                loadDbOverview();
                loadDocs(0);
                loadSearchLogs();
                loadAskLogs();
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

        // ===== Admin: Semantic DB overview =====
        async function loadDbOverview() {
            try {
                const res = await fetch('/api/admin/db/overview');
                const data = await res.json();
                if (!data || data.ready === false) {
                    document.getElementById('db-overview').innerHTML = '<div class="small">Semantic store indisponível</div>';
                    return;
                }
                const cats = (data.categories||[]).map(c => `${c.category}: ${c.count}`).join(', ');
                const recentDocs = (data.recent?.documents||[]).map(d => `<div class="knowledge-item"><strong>${d.title||'(sem título)'}</strong><div class="small">${d.category||'-'}</div></div>`).join('');
                document.getElementById('db-overview').innerHTML = `
                    <div class="env-var"><span>Total documentos</span><span>${data.counts?.legal_chunks||0}</span></div>
                    <div class="env-var"><span>Registros de busca</span><span>${data.counts?.search_logs||0}</span></div>
                    <div class="env-var"><span>Registros de perguntas</span><span>${data.counts?.ask_logs||0}</span></div>
                    <div class="small" style="margin-top:8px;"><strong>Categorias:</strong> ${cats||'-'}</div>
                    <div class="small" style="margin-top:8px;"><strong>Recentes:</strong><div style="max-height:140px; overflow:auto;">${recentDocs||'<div class=\"small\">Nenhum</div>'}</div></div>
                `;
            } catch (e) {
                document.getElementById('db-overview').innerHTML = 'Erro ao carregar';
            }
        }

        // ===== Admin: Manage documents =====
        let DOCS_LIMIT = 20;
        let DOCS_OFFSET = 0;
        function resetDocFilters() {
            document.getElementById('doc-q').value = '';
            document.getElementById('doc-category').value = '';
            DOCS_OFFSET = 0;
            loadDocs(0);
        }
        function prevDocsPage() { DOCS_OFFSET = Math.max(0, DOCS_OFFSET - DOCS_LIMIT); loadDocs(); }
        function nextDocsPage() { DOCS_OFFSET = DOCS_OFFSET + DOCS_LIMIT; loadDocs(); }
        async function loadDocs(reset=undefined) {
            try {
                if (reset === 0) DOCS_OFFSET = 0;
                const q = encodeURIComponent(document.getElementById('doc-q').value||'');
                const category = encodeURIComponent(document.getElementById('doc-category').value||'');
                const url = `/api/admin/legal-chunks?q=${q}&category=${category}&limit=${DOCS_LIMIT}&offset=${DOCS_OFFSET}`;
                const res = await fetch(url);
                const data = await res.json();
                const items = data.items || [];
                const total = data.total || 0;
                const page = Math.floor(DOCS_OFFSET / DOCS_LIMIT) + 1;
                const rows = items.map((it) => `
                    <tr>
                        <td class="small muted">${it.id}</td>
                        <td><input id="t_${it.id}" value="${(it.title||'').replace(/"/g,'&quot;')}" /></td>
                        <td><input id="c_${it.id}" value="${(it.category||'').replace(/"/g,'&quot;')}" /></td>
                        <td><textarea id="m_${it.id}" rows="2" placeholder="metadata JSON opcional"></textarea><div class="small muted">Prévia: ${(it.preview||'').replace(/</g,'&lt;').slice(0,160)}...</div></td>
                        <td class="controls">
                            <button class="btn small" onclick="saveDoc('${it.id}')">Salvar</button>
                            <button class="btn secondary small" onclick="deleteDoc('${it.id}')">Excluir</button>
                        </td>
                    </tr>
                `).join('');
                document.getElementById('doc-list').innerHTML = `
                    <div class="small">Total: ${total}</div>
                    <table>
                        <thead><tr><th>ID</th><th>Título</th><th>Categoria</th><th>Metadados/Prévia</th><th>Ações</th></tr></thead>
                        <tbody>${rows || '<tr><td colspan=5 class="small muted">Sem resultados</td></tr>'}</tbody>
                    </table>`;
                document.getElementById('doc-page-info').textContent = `Página ${page}`;
            } catch (e) {
                document.getElementById('doc-list').innerHTML = 'Erro ao listar documentos';
            }
        }
        async function saveDoc(id) {
            try {
                const title = document.getElementById(`t_${id}`).value;
                const category = document.getElementById(`c_${id}`).value;
                const metadataRaw = document.getElementById(`m_${id}`).value.trim();
                let metadata = undefined;
                if (metadataRaw) {
                    try { metadata = JSON.parse(metadataRaw); } catch (e) { alert('Metadata inválido (JSON)'); return; }
                }
                const res = await fetch(`/api/admin/legal-chunks/${id}`, {
                    method: 'PATCH', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, category, metadata })
                });
                const data = await res.json();
                if (!data.success) { alert('Falha ao salvar: ' + (data.error||'')); return; }
                loadDocs();
            } catch (e) { alert('Erro ao salvar: ' + e.message); }
        }
        async function deleteDoc(id) {
            try {
                if (!confirm('Confirma excluir este documento?')) return;
                const res = await fetch(`/api/admin/legal-chunks/${id}`, { method: 'DELETE' });
                const data = await res.json();
                if (!data.success) { alert('Falha ao excluir: ' + (data.error||'')); return; }
                loadDocs();
            } catch (e) { alert('Erro ao excluir: ' + e.message); }
        }

        // ===== Admin: retrieval logs =====
        async function loadSearchLogs() {
            try {
                const res = await fetch('/api/admin/logs/search?limit=50&offset=0');
                const data = await res.json();
                const items = data.items || [];
                document.getElementById('search-logs').innerHTML = items.map(r => `
                    <div class="log-entry"><div class="small">${r.created_at}</div><div><strong>query:</strong> ${r.query}</div><div class="small">top_k=${r.top_k} min_rel=${r.min_relevance} type=${r.search_type} total=${r.total}</div></div>
                `).join('') || '<div class="small muted">Sem logs de busca</div>';
            } catch (e) { document.getElementById('search-logs').innerHTML = 'Erro ao carregar logs de busca'; }
        }
        async function loadAskLogs() {
            try {
                const res = await fetch('/api/admin/logs/ask?limit=50&offset=0');
                const data = await res.json();
                const items = data.items || [];
                document.getElementById('ask-logs').innerHTML = items.map(r => `
                    <div class="log-entry"><div class="small">${r.created_at}</div><div><strong>pergunta:</strong> ${r.question}</div><div class="small">top_k=${r.top_k} min_rel=${r.min_relevance} fontes=${r.total_sources}</div></div>
                `).join('') || '<div class="small muted">Sem logs de perguntas</div>';
            } catch (e) { document.getElementById('ask-logs').innerHTML = 'Erro ao carregar logs de perguntas'; }
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
def get_system_status():
    """Return system status information including database and OpenAI API status."""
    from app import SEMANTIC_AVAILABLE, client, LEGAL_KNOWLEDGE, active_model

    now_iso = datetime.utcnow().isoformat()
    
    # Test OpenAI client availability (non-fatal)
    openai_available = False
    if client:
        try:
            _ = client.chat.completions.create(
                model=active_model or os.getenv('OPENAI_MODEL') or "gpt-5-nano",
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=1
            )
            openai_available = True
            current_app.logger.info("OpenAI API connection successful")
        except Exception as e:
            openai_available = False
            current_app.logger.warning(f"OpenAI API connection failed: {e}")

    knowledge_count = len(LEGAL_KNOWLEDGE)
    system_healthy = openai_available and knowledge_count >= 0
    
    status = {
        "timestamp": now_iso,
        "system": {
            "status": "online",
            "version": "0.1.0",  # Hardcoded for now
            "uptime": "1 day",  # Placeholder
            "healthy": system_healthy
        },
        "database": {
            "status": "unknown",
            "type": "PostgreSQL" if SEMANTIC_AVAILABLE else "None",
            "connection_string": "*****" + (os.getenv('DATABASE_URL', '')[-20:] if os.getenv('DATABASE_URL') else "not_configured")
        },
        "openai_api": {
            "status": "connected" if openai_available else "disconnected",
            "model": active_model or os.getenv('OPENAI_MODEL', 'gpt-4') 
        },
        "embedding": {
            "model": os.getenv('EMBEDDING_MODEL', 'text-embedding-3-small'),
            "dimensions": 1536  # Hardcoded for now
        },
        # Legacy fields for backwards compatibility
        "system_healthy": system_healthy,
        "openai_available": openai_available,
        "knowledge_count": knowledge_count,
        "active_model": active_model or "Não configurado",
        "system_label": "Operacional" if system_healthy else "Com problemas"
    }
    
    # Get real database status if semantic retrieval is available
    if SEMANTIC_AVAILABLE:
        try:
            from retrieval import get_db_status, _ensure_connection
            
            # Force a connection check and potential reconnect before checking status
            _ensure_connection()
            
            db_status = get_db_status()
            current_app.logger.info(f"Database connection status: {db_status.get('connected', False)}")
            
            status["database"]["status"] = "connected" if db_status.get("connected", False) else "disconnected"
            status["database"]["version"] = db_status.get("version", "unknown")
            status["database"]["extensions"] = db_status.get("extensions", [])
            
            # Add more detailed database info
            if db_status.get("connected", False):
                status["database"]["name"] = db_status.get("database_name", "unknown")
                status["database"]["vector_ready"] = db_status.get("vector_ready", False)
                status["source"] = "database"
            
        except ImportError as ie:
            current_app.logger.warning(f"Could not import database functions: {ie}")
            status["database"]["status"] = "error"
            status["database"]["error"] = str(ie)
        except Exception as e:
            current_app.logger.error(f"Error getting database status: {e}")
            status["database"]["status"] = "error"
            status["database"]["error"] = str(e)
    
    return jsonify(status)

@admin_bp.route('/api/stats')
def get_api_stats():
    """Get API statistics using real database data when available"""
    from app import SEMANTIC_AVAILABLE
    
    stats = {
        "total_questions": 0,
        "questions_today": 0,
        "success_rate": 0.0 if not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your_openai_api_key_here' else 0.95,
        "avg_response_time": 1200,
        "last_updated": datetime.utcnow().isoformat(),
        "source": "mock"
    }
    
    # Try to get real stats from database if semantic retrieval is available
    try:
        if SEMANTIC_AVAILABLE:
            from retrieval import is_ready, admin_db_overview
            
            if is_ready():
                logging.info("Using real database data for API stats")
                # Get database overview
                db_overview = admin_db_overview()
                
                # Update stats with real data
                if db_overview:
                    counts = db_overview.get("counts", {})
                    
                    # Update stats from counts
                    stats["total_questions"] = counts.get("ask_logs", 0)
                    
                    # Get today's questions (approximate from most recent logs)
                    today_questions = 0
                    today = datetime.utcnow().date()
                    for log in db_overview.get("recent", {}).get("ask_logs", []):
                        try:
                            log_date = datetime.fromisoformat(log.get("created_at", "")).date()
                            if log_date == today:
                                today_questions += 1
                        except (ValueError, TypeError):
                            pass
                    
                    stats["questions_today"] = today_questions
                    stats["source"] = "database"
                    
                    # If we have search logs, calculate average response time
                    if counts.get("search_logs", 0) > 0:
                        stats["success_rate"] = 0.98  # Placeholder until detailed logging exists
    except Exception as e:
        logging.error(f"Error retrieving API stats from database: {e}")
    
    return jsonify(stats)


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

@admin_bp.route('/api/knowledge-base', methods=['GET'])
def get_knowledge_base():
    """Return knowledge base documents for admin."""
    try:
        # Local import to avoid circular deps
        from app import SEMANTIC_AVAILABLE, LEGAL_KNOWLEDGE

        # Check if semantic retrieval is available and ready
        db_ready = False
        if SEMANTIC_AVAILABLE:
            # Import the necessary functions from retrieval only if available
            try:
                from retrieval import admin_list_legal_chunks, admin_db_overview, is_ready, _ensure_connection
                
                # Force a connection check and potential reconnect
                _ensure_connection()
                db_ready = is_ready()
                current_app.logger.info(f"Knowledge base DB ready status: {db_ready}")
            except ImportError as imp_err:
                current_app.logger.error(f"Import error in get_knowledge_base: {imp_err}")
                pass

        # Use real database data if available
        if db_ready:
            try:
                q = request.args.get('q', '').strip()
                category = request.args.get('category', '').strip() or None
                page = max(1, int(request.args.get('page', 1)))
                per_page = min(100, max(10, int(request.args.get('per_page', 25))))

                # Calculate offset based on page and per_page
                offset = (page - 1) * per_page

                current_app.logger.info(f"Fetching legal chunks from database with params: q={q}, category={category}, limit={per_page}, offset={offset}")
                
                # Get documents from database
                docs_data = admin_list_legal_chunks(
                    q=q, category=category, limit=per_page, offset=offset)
                
                current_app.logger.info(f"Retrieved {docs_data.get('total', 0)} total documents, {len(docs_data.get('items', []))} on current page")

                # Get DB overview with categories
                db_overview = admin_db_overview()
                categories = db_overview.get('categories', [])
                current_app.logger.info(f"Retrieved {len(categories)} categories from database")

                # Map documents and categories to frontend shape
                items = docs_data.get('items', [])
                documents = [
                    {
                        "id": it.get("id"),
                        "title": it.get("title"),
                        "category": it.get("category"),
                        # keywords not included in list endpoint; provide empty list for UI
                        "keywords": []
                    }
                    for it in items
                ]
                category_names = [c.get("category") for c in categories if isinstance(c, dict) and c.get("category")]

                # Return formatted response for frontend
                return jsonify({
                    "total": docs_data.get('total', 0),
                    "documents": documents,
                    "categories": category_names,
                    "source": "database"
                })
            except Exception as e:
                current_app.logger.error(f"Error fetching knowledge base from database: {e}")
                current_app.logger.info("Falling back to mock data due to database error")
                # Fall back to mock data on error
        else:
            current_app.logger.info("Database not ready, using mock knowledge base data")

        # Fallback to mock data if semantic retrieval is not available or ready
        documents = []
        for i, doc in enumerate(LEGAL_KNOWLEDGE):
            documents.append({
                "id": str(i + 1),  # Mock IDs for demo
                "title": doc.get("title", ""),
                "content": doc.get("content", "")[:200] + "...",  # Truncate for display
                "category": doc.get("category", "general"),
                "keywords": doc.get("keywords", []) if isinstance(doc, dict) else [],
                "created_at": "2023-01-01T00:00:00Z",  # Mock date
                "updated_at": "2023-01-01T00:00:00Z"  # Mock date
            })

        # Mock categories as string list
        categories = ["constitutional", "civil", "criminal", "tax", "general"]

        return jsonify({
            "total": len(documents),
            "documents": documents,
            "categories": categories,
            "source": "mock"
        })
    except Exception as e:
        current_app.logger.error(f"Error in get_knowledge_base: {e}")
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/api/logs')
def get_system_logs():
    """Get system logs from database if available"""
    from app import SEMANTIC_AVAILABLE
    
    # Default mock logs
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
        ],
        "source": "mock"
    }
    
    try:
        # Try to get real logs from database if semantic retrieval is available
        if SEMANTIC_AVAILABLE:
            from retrieval import is_ready, admin_list_search_logs, admin_list_ask_logs
            
            if is_ready():
                logging.info("Using real database data for system logs")
                # Get search logs
                search_logs = admin_list_search_logs(limit=10, offset=0)
                ask_logs = admin_list_ask_logs(limit=10, offset=0)
                
                # Combine and format logs
                entries = []
                
                # Process search logs
                for item in search_logs.get("items", []):
                    entries.append({
                        "timestamp": item.get("created_at", ""),
                        "level": "INFO",
                        "type": "search",
                        "message": f"Search query: '{item.get('query', '')}' (found {item.get('total', 0)} results)"
                    })
                
                # Process ask logs
                for item in ask_logs.get("items", []):
                    entries.append({
                        "timestamp": item.get("created_at", ""),
                        "level": "INFO",
                        "type": "ask",
                        "message": f"Question: '{item.get('question', '')}' (used {item.get('total_sources', 0)} sources)"
                    })
                
                # Sort by timestamp if available
                entries.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
                
                if entries:
                    logs = {
                        "entries": entries[:20],  # Limit to most recent 20
                        "total": search_logs.get("total", 0) + ask_logs.get("total", 0),
                        "source": "database"
                    }
    except Exception as e:
        logging.error(f"Error retrieving logs from database: {e}")
        logs["error"] = str(e)
    
    return jsonify(logs)

    # duplicate get_api_stats removed (kept the primary definition earlier in the file)

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
