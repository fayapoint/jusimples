import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default function Footer() {
  const { user } = useAuth();
  const [news, setNews] = useState([]);
  const [ads, setAds] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const [n, a] = await Promise.all([
          fetch(`${API_URL}/api/news`).then(r => r.json()).catch(() => ({ news: [] })),
          fetch(`${API_URL}/api/ads`).then(r => r.json()).catch(() => ({ ads: [] })),
        ]);
        setNews(n.news || []);
        setAds(a.ads || []);
      } catch (_) {}
    })();
  }, []);

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-top">
          <section className="footer-section">
            <h4>Notícias Jurídicas</h4>
            <div className="news-list">
              {news.map((item) => (
                <a key={item.id} href={item.url} target="_blank" rel="noreferrer" className="news-item">
                  <img className="news-thumb" src={item.thumbnail} alt={item.title} width={88} height={60} />
                  <div>
                    <div className="news-title">{item.title}</div>
                    <div className="news-summary">{item.summary}</div>
                  </div>
                </a>
              ))}
            </div>
          </section>

          <section className="footer-section">
            <h4>Patrocinado</h4>
            <div className="ads-list">
              {ads.map((ad) => (
                <a key={ad.id} href={ad.url} target="_blank" rel="noreferrer">
                  <img className="ad-card" src={ad.image} alt={ad.title} />
                  <div className="ad-title">{ad.title}</div>
                </a>
              ))}
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
