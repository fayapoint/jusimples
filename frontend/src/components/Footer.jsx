import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
const LOCAL_FALLBACK = 'http://localhost:5000';

export default function Footer() {
  const { user } = useAuth();
  const [news, setNews] = useState([]);
  const [ads, setAds] = useState([]);
  const [loadingNews, setLoadingNews] = useState(true);
  const [loadingAds, setLoadingAds] = useState(true);
  const [errorNews, setErrorNews] = useState(null);
  const [errorAds, setErrorAds] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchWithFallback(path) {
      // Prefer relative path (works with CRA proxy), then env API, then localhost
      const urls = ['', API_URL, LOCAL_FALLBACK];
      let lastErr = null;
      for (const base of urls) {
        try {
          const controller = new AbortController();
          const t = setTimeout(() => controller.abort(), 7000);
          const url = base ? `${base}${path}` : path; // '' uses relative path
          const res = await fetch(url, { signal: controller.signal });
          clearTimeout(t);
          if (!res.ok) {
            lastErr = new Error(`HTTP ${res.status}`);
            continue;
          }
          return await res.json();
        } catch (e) {
          lastErr = e;
          continue;
        }
      }
      throw lastErr || new Error('Falha ao buscar dados');
    }

    (async () => {
      try {
        setLoadingNews(true);
        const n = await fetchWithFallback('/api/news');
        if (!cancelled) setNews(Array.isArray(n.news) ? n.news : []);
      } catch (e) {
        if (!cancelled) setErrorNews('Não foi possível carregar as notícias.');
      } finally {
        if (!cancelled) setLoadingNews(false);
      }

      try {
        setLoadingAds(true);
        const a = await fetchWithFallback('/api/ads');
        if (!cancelled) setAds(Array.isArray(a.ads) ? a.ads : []);
      } catch (e) {
        if (!cancelled) setErrorAds('Não foi possível carregar os patrocinados.');
      } finally {
        if (!cancelled) setLoadingAds(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-top">
          <section className="footer-section">
            <h4>Notícias Jurídicas</h4>
            <div className="news-list">
              {loadingNews && (
                <>
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="news-item" aria-hidden>
                      <div className="news-thumb skeleton" />
                      <div>
                        <div className="skeleton skeleton-text" style={{ width: '85%' }} />
                        <div className="skeleton skeleton-text" style={{ width: '60%', marginTop: 6 }} />
                      </div>
                    </div>
                  ))}
                </>
              )}

              {!loadingNews && news.slice(0, 3).map((item) => (
                <a key={item.id} href={item.url} target="_blank" rel="noreferrer" className="news-item">
                  <img
                    className="news-thumb"
                    src={item.thumbnail}
                    alt={item.title || 'Notícia jurídica'}
                    onError={(e) => { e.currentTarget.style.display = 'none'; }}
                  />
                  <div>
                    <div className="news-title">{item.title}</div>
                    <div className="news-summary">{item.summary}</div>
                  </div>
                </a>
              ))}

              {!loadingNews && !news.length && !errorNews && (
                <div className="text-muted" role="status">Sem notícias no momento.</div>
              )}
              {errorNews && (
                <div className="text-muted" role="alert">{errorNews}</div>
              )}
            </div>
          </section>

          <section className="footer-section">
            <h4>Patrocinado</h4>
            <div className="ads-list">
              {loadingAds && (
                <>
                  {[...Array(2)].map((_, i) => (
                    <div key={i} className="ad-card skeleton" style={{ height: 80 }} aria-hidden />
                  ))}
                </>
              )}

              {!loadingAds && ads.slice(0, 2).map((ad) => (
                <a key={ad.id} href={ad.url} target="_blank" rel="noreferrer">
                  <img className="ad-card" src={ad.image} alt={ad.title || 'Patrocinado'} onError={(e) => { e.currentTarget.style.visibility = 'hidden'; }} />
                  <div className="ad-title">{ad.title}</div>
                </a>
              ))}

              {!loadingAds && !ads.length && !errorAds && (
                <div className="text-muted" role="status">Nenhum patrocinado no momento.</div>
              )}
              {errorAds && (
                <div className="text-muted" role="alert">{errorAds}</div>
              )}
            </div>
          </section>

          <section className="footer-section">
            <h4>Links</h4>
            <ul className="link-list">
              <li><a href="/">Início</a></li>
              <li><a href="/dashboard">Dashboard</a></li>
              <li><a href="/admin">Admin</a></li>
              <li><a href="https://github.com/juximplex" target="_blank" rel="noreferrer">GitHub</a></li>
            </ul>
          </section>

          <section className="footer-section">
            <h4>Você</h4>
            {user ? (
              <div className="user-card">
                <div><strong>{user.name || 'Usuário'}</strong></div>
                <div className="text-muted">{user.email}</div>
                <a className="btn btn-outline" href="/dashboard">Ir ao Dashboard</a>
              </div>
            ) : (
              <div className="user-card">
                <div className="text-muted">Entre para salvar seu histórico e preferências.</div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <a className="btn btn-outline" href="/login">Login</a>
                  <a className="btn btn-primary" href="/register">Cadastrar</a>
                </div>
              </div>
            )}
          </section>
        </div>

        <div className="footer-bottom">
          <p className="footer-disclaimer">
            O JuSimples utiliza inteligência artificial para fornecer orientações jurídicas baseadas na legislação brasileira. As informações são de caráter informativo. Para casos complexos, consulte um advogado especializado.
          </p>
          <div className="socials">
            <a href="https://github.com/juximplex" target="_blank" rel="noreferrer">GitHub</a>
            <a href="mailto:contato@jusimples.com">Contato</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
