import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useTheme } from '../context/ThemeContext';
import { Github, Instagram, Linkedin } from 'lucide-react';

export default function Footer() {
  const [expanded, setExpanded] = useState(false);
  const { theme } = useTheme();
  const expandTimerRef = useRef(null);
  const collapseTimerRef = useRef(null);
  const closingClassTimerRef = useRef(null);
  const footerRef = useRef(null);
  
  const clearExpandTimer = useCallback(() => {
    if (expandTimerRef.current) {
      clearTimeout(expandTimerRef.current);
      expandTimerRef.current = null;
    }
  }, []);

  const clearCollapseTimer = useCallback(() => {
    if (collapseTimerRef.current) {
      clearTimeout(collapseTimerRef.current);
      collapseTimerRef.current = null;
    }
  }, []);

  const scheduleCollapse = useCallback((delay = 1200) => {
    clearCollapseTimer();
    const root = document.documentElement;
    // Mark closing for CSS to apply a slightly longer, softer transition
    root.classList.add('footer-closing');
    if (closingClassTimerRef.current) {
      clearTimeout(closingClassTimerRef.current);
    }
    closingClassTimerRef.current = setTimeout(() => {
      root.classList.remove('footer-closing');
      closingClassTimerRef.current = null;
    }, delay + 800); // remove after collapse begins and animation completes

    collapseTimerRef.current = setTimeout(() => {
      setExpanded(false);
      clearCollapseTimer();
    }, delay);
  }, [clearCollapseTimer]);

  const handleMouseEnter = () => {
    // Cancel any pending collapse and schedule expand
    clearCollapseTimer();
    clearExpandTimer();
    expandTimerRef.current = setTimeout(() => {
      setExpanded(true);
      clearExpandTimer();
    }, 600);
  };
  
  const handleMouseLeave = (e) => {
    // If moving into the background selector, keep expanded
    const toEl = e?.relatedTarget;
    if (toEl && (toEl.closest && toEl.closest('.background-selector'))) {
      return; // don't collapse
    }
    clearExpandTimer();
    // Delay the collapse for a more organic feel
    scheduleCollapse(1200);
  };
  
  // Sync a root-level class so CSS can animate things (e.g., BackgroundSelector) on expand/collapse
  useEffect(() => {
    const root = document.documentElement;
    if (expanded) {
      root.classList.add('footer-expanded');
      // If expanding again, ensure 'closing' flag is cleared
      root.classList.remove('footer-closing');
    } else {
      root.classList.remove('footer-expanded');
    }

    return () => {
      // Clean up timer and ensure class removed on unmount
      clearExpandTimer();
      clearCollapseTimer();
      if (closingClassTimerRef.current) {
        clearTimeout(closingClassTimerRef.current);
        closingClassTimerRef.current = null;
      }
      root.classList.remove('footer-expanded');
      root.classList.remove('footer-closing');
    };
  }, [expanded, clearExpandTimer, clearCollapseTimer]);

  // Ensure moving into the Background Selector keeps the footer expanded
  useEffect(() => {
    const selector = document.querySelector('.background-selector');
    if (!selector) return;

    const onEnter = () => { clearCollapseTimer(); setExpanded(true); };
    const onMouseDown = () => { clearCollapseTimer(); setExpanded(true); };
    const onLeave = (e) => {
      const toEl = e?.relatedTarget;
      const footerEl = footerRef.current;
      if (toEl && footerEl && (toEl === footerEl || (toEl.closest && toEl.closest('footer')))) {
        return; // moving back into footer
      }
      // Schedule a delayed collapse when leaving selector to outside
      scheduleCollapse(1200);
    };

    selector.addEventListener('mouseenter', onEnter);
    selector.addEventListener('mouseleave', onLeave);
    selector.addEventListener('mousedown', onMouseDown);

    return () => {
      selector.removeEventListener('mouseenter', onEnter);
      selector.removeEventListener('mouseleave', onLeave);
      selector.removeEventListener('mousedown', onMouseDown);
    };
  }, [scheduleCollapse, clearCollapseTimer]);
  
  return (
    <footer 
      className={`footer footer-${theme} ${expanded ? 'expanded-footer' : 'compact-footer'}`}
      ref={footerRef}
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

              {/* Socials separate right column */}
              <div className="footer-section socials-section">
                <div className="socials">
                  <a
                    href="https://linkedin.com/company/jusimples"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="social-link linkedin"
                    aria-label="LinkedIn JuSimples"
                  >
                    <Linkedin size={18} />
                  </a>
                  <a
                    href="https://instagram.com/jusimples"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="social-link instagram"
                    aria-label="Instagram JuSimples"
                  >
                    <Instagram size={18} />
                  </a>
                  <a
                    href="https://github.com/jusimples"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="social-link github"
                    aria-label="GitHub JuSimples"
                  >
                    <Github size={18} />
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
