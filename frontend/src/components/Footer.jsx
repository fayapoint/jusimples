import React, { useState, useRef, useEffect } from 'react';
import { useTheme } from '../context/ThemeContext';

export default function Footer() {
  const [expanded, setExpanded] = useState(false);
  const { theme } = useTheme();
  const timerRef = useRef(null);
  
  const handleMouseEnter = () => {
    timerRef.current = setTimeout(() => {
      setExpanded(true);
    }, 1000);
  };
  
  const handleMouseLeave = () => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    setExpanded(false);
  };
  
  // Clean up timer on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
    };
  }, []);
  
  return (
    <footer 
      className={`footer footer-${theme} ${expanded ? 'expanded-footer' : 'compact-footer'}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className={`footer-container ${expanded ? 'expanded' : 'compact'}`}>
        {expanded ? (
          <>
            <div className="footer-top">
              {/* Brand & About */}
              <div className="footer-section brand-section">
                <img src="/logotipojusimples.png" alt="Logo JuSimples" className="footer-logo" />
                <p className="footer-description">
                  O JuSimples é uma plataforma online que simplifica demandas jurídicas de menor complexidade por meio de IA e automação,
                  tornando o acesso à justiça mais rápido e acessível para todos.
                </p>
                <p className="footer-small-text">
                  As informações fornecidas pela plataforma são de caráter informativo. Em casos complexos, consulte um advogado especializado.
                </p>
              </div>

              {/* Useful Links */}
              <div className="footer-section">
                <h4>Links Úteis</h4>
                <ul className="link-list">
                  <li><a href="/sobre">Sobre o JuSimples</a></li>
                  <li><a href="/faq">FAQ</a></li>
                  <li><a href="/privacidade">Política de Privacidade</a></li>
                  <li><a href="/termos">Termos de Uso</a></li>
                  <li><a href="mailto:contato@jusimples.com">Contato</a></li>
                </ul>
              </div>

              {/* Solutions */}
              <div className="footer-section">
                <h4>Soluções</h4>
                <ul className="link-list">
                  <li><a href="/consumidores">Para Consumidores</a></li>
                  <li><a href="/empresas">Para Pequenas Empresas</a></li>
                  <li><a href="/advogados">Para Advogados</a></li>
                  <li><a href="/documentos">Documentos Automáticos</a></li>
                </ul>
              </div>

              {/* Socials */}
              <div className="footer-section social-section">
                <h4>Redes Sociais</h4>
                <div className="socials">
                  <a href="https://linkedin.com/company/jusimples" target="_blank" rel="noopener noreferrer" className="social-link linkedin">
                    <span className="social-icon">🔗</span>
                  </a>
                  <a href="https://instagram.com/jusimples" target="_blank" rel="noopener noreferrer" className="social-link instagram">
                    <span className="social-icon">📸</span>
                  </a>
                  <a href="https://github.com/jusimples" target="_blank" rel="noopener noreferrer" className="social-link github">
                    <span className="social-icon">💻</span>
                  </a>
                </div>
              </div>
            </div>

            <div className="footer-bottom">
              <p className="copyright">© 2025 JuSimples. Todos os direitos reservados.</p>
              {/* Quick Links replicated from compact footer */}
              <div className="footer-links">
                <a href="https://github.com/juximplex" target="_blank" rel="noreferrer">GitHub</a>
                <span className="footer-separator">•</span>
                <a href="/">Início</a>
                <span className="footer-separator">•</span>
                <a href="/dashboard">Dashboard</a>
                <span className="footer-separator">•</span>
                <a href="mailto:contato@jusimples.com">Contato</a>
              </div>
            </div>
          </>
        ) : (
          <div className="compact-footer-content">
            <div className="footer-disclaimer">
              O JuSimples utiliza inteligência artificial para fornecer orientações jurídicas baseadas na legislação brasileira. 
              Para casos complexos, consulte um advogado especializado.
            </div>
            <div className="footer-links">
              <a href="https://github.com/juximplex" target="_blank" rel="noreferrer">GitHub</a>
              <span className="footer-separator">•</span>
              <a href="/">Início</a>
              <span className="footer-separator">•</span>
              <a href="/dashboard">Dashboard</a>
              <span className="footer-separator">•</span>
              <a href="mailto:contato@jusimples.com">Contato</a>
            </div>
          </div>
        )}
      </div>
    </footer>
  );
}
