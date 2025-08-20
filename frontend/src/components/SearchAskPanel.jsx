import React, { useState } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default function SearchAskPanel() {
  const [mode, setMode] = useState('search'); // 'search' | 'ask'
  const [query, setQuery] = useState('');
  const [question, setQuestion] = useState('');
  const [topK, setTopK] = useState(3);
  const [minRel, setMinRel] = useState(0.5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchResult, setSearchResult] = useState(null);
  const [askResult, setAskResult] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    setSearchResult(null);
    setAskResult(null);
    try {
      if (mode === 'search') {
        const res = await fetch(`${API_URL}/api/search`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query, top_k: Number(topK), min_relevance: Number(minRel) }),
        });
        if (!res.ok) throw new Error('Falha na busca');
        const data = await res.json();
        setSearchResult(data);
      } else {
        const res = await fetch(`${API_URL}/api/ask`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question, top_k: Number(topK), min_relevance: Number(minRel) }),
        });
        if (!res.ok) throw new Error('Falha ao perguntar');
        const data = await res.json();
        setAskResult(data);
      }
    } catch (err) {
      setError(err.message || 'Erro inesperado');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel-wrapper" style={{ marginTop: 24 }}>
      <div className="panel-card" style={{
        background: 'var(--bg-secondary)',
        border: '1px solid var(--border, rgba(255,255,255,0.1))',
        borderRadius: 12,
        padding: 16,
      }}>
        <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
          <button
            className={`btn ${mode === 'search' ? 'btn-primary' : 'btn-outline-secondary'}`}
            onClick={() => setMode('search')}
            type="button"
          >
            Buscar (Semantic)
          </button>
          <button
            className={`btn ${mode === 'ask' ? 'btn-primary' : 'btn-outline-secondary'}`}
            onClick={() => setMode('ask')}
            type="button"
          >
            Perguntar (RAG)
          </button>
        </div>

        <form onSubmit={onSubmit} style={{ display: 'grid', gap: 12 }}>
          {mode === 'search' ? (
            <div>
              <label className="label">Consulta</label>
              <input
                className="input"
                placeholder="Ex: direitos do consumidor online"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
          ) : (
            <div>
              <label className="label">Pergunta</label>
              <input
                className="input"
                placeholder="Ex: Quais são os direitos do consumidor em compras online?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
            </div>
          )}

          <div style={{ display: 'flex', gap: 12 }}>
            <div style={{ flex: 1 }}>
              <label className="label">top_k</label>
              <input
                className="input"
                type="number"
                min={1}
                max={10}
                value={topK}
                onChange={(e) => setTopK(e.target.value)}
              />
            </div>
            <div style={{ flex: 1 }}>
              <label className="label">min_relevance</label>
              <input
                className="input"
                type="number"
                min={0}
                max={1}
                step={0.05}
                value={minRel}
                onChange={(e) => setMinRel(e.target.value)}
              />
            </div>
          </div>

          <div>
            <button className="btn btn-primary" type="submit" disabled={loading}>
              {loading ? 'Processando...' : (mode === 'search' ? 'Buscar' : 'Perguntar')}
            </button>
          </div>
        </form>

        {error && (
          <div className="alert alert-error" style={{ marginTop: 12 }}>
            {error}
          </div>
        )}

        {/* Results */}
        {mode === 'search' && searchResult && (
          <div style={{ marginTop: 16 }}>
            <div style={{ marginBottom: 8, opacity: 0.8 }}>
              <small>
                Tipo: {searchResult.search_type} · Total: {searchResult.total} · top_k: {searchResult.params?.top_k} · min_rel: {searchResult.params?.min_relevance}
              </small>
            </div>
            <div style={{ display: 'grid', gap: 12 }}>
              {(searchResult.results || []).map((r) => (
                <div key={r.id} className="card" style={{ padding: 12, border: '1px solid var(--border, rgba(255,255,255,0.1))', borderRadius: 8 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                    <h4 style={{ margin: 0 }}>{r.title}</h4>
                    <span style={{ fontSize: 12, opacity: 0.8 }}>Relevância: {(r.relevance ?? 0).toFixed(2)}</span>
                  </div>
                  <div style={{ fontSize: 13, opacity: 0.85, margin: '4px 0 8px' }}>Categoria: {r.category || 'n/d'}</div>
                  <div style={{ fontSize: 13, opacity: 0.9 }}>{(r.content || '').slice(0, 240)}...</div>
                  <div style={{ marginTop: 8 }}>
                    <a className="btn btn-sm btn-outline-secondary" href={`/documentos?source=${encodeURIComponent(r.id)}`}>
                      Ver fonte (id: {r.id})
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {mode === 'ask' && askResult && (
          <div style={{ marginTop: 16 }}>
            <div style={{ marginBottom: 8, opacity: 0.8 }}>
              <small>
                Modelo: {askResult.debug_info?.active_model} · Contexto: {askResult.debug_info?.context_found} · top_k: {askResult.params?.top_k} · min_rel: {askResult.params?.min_relevance}
              </small>
            </div>
            <div className="answer" style={{ padding: 12, border: '1px solid var(--border, rgba(255,255,255,0.1))', borderRadius: 8 }}>
              <h4 style={{ marginTop: 0 }}>Resposta</h4>
              <p style={{ whiteSpace: 'pre-wrap' }}>{askResult.answer}</p>
            </div>
            <div style={{ marginTop: 16 }}>
              <h4>Fontes</h4>
              <div style={{ display: 'grid', gap: 12 }}>
                {(askResult.sources || []).map((s) => (
                  <div key={s.id} className="card" style={{ padding: 12, border: '1px solid var(--border, rgba(255,255,255,0.1))', borderRadius: 8 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                      <strong>{s.title}</strong>
                      <span style={{ fontSize: 12, opacity: 0.8 }}>Relevância: {(s.relevance ?? 0).toFixed(2)}</span>
                    </div>
                    <div style={{ fontSize: 13, opacity: 0.85, margin: '4px 0 8px' }}>Categoria: {s.category || 'n/d'}</div>
                    <div style={{ fontSize: 13, opacity: 0.9 }}>{(s.content_preview || '').slice(0, 240)}</div>
                    <div style={{ marginTop: 8 }}>
                      <a className="btn btn-sm btn-outline-secondary" href={`/documentos?source=${encodeURIComponent(s.id)}`}>
                        Ver fonte (id: {s.id})
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
