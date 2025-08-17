import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Command, Home, LayoutDashboard, LogIn, LogOut, Search, Settings, UserPlus } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function CommandPalette() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const inputRef = useRef(null);

  // Open with Ctrl/Cmd+K or custom event
  useEffect(() => {
    const onKey = (e) => {
      const isMac = navigator.platform.toUpperCase().includes('MAC');
      if ((isMac ? e.metaKey : e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setOpen(true);
      }
      if (e.key === 'Escape') setOpen(false);
    };
    const onOpen = () => setOpen(true);
    window.addEventListener('keydown', onKey);
    window.addEventListener('open-command-palette', onOpen);
    return () => {
      window.removeEventListener('keydown', onKey);
      window.removeEventListener('open-command-palette', onOpen);
    };
  }, []);

  useEffect(() => {
    if (open) setTimeout(() => inputRef.current?.focus(), 0);
    if (!open) setQuery('');
  }, [open]);

  const run = (fn) => {
    setOpen(false);
    setTimeout(fn, 0);
  };

  const commands = useMemo(() => {
    const items = [
      { icon: <Home size={16} />, label: 'Ir para Início', hint: 'Home', action: () => navigate('/') },
      { icon: <Search size={16} />, label: 'Perguntar à IA', hint: 'Abrir chat na Home', action: () => navigate('/') },
      { icon: <LayoutDashboard size={16} />, label: 'Abrir Dashboard', hint: 'Área do usuário', action: () => navigate('/dashboard'), requireAuth: true },
      { icon: <Settings size={16} />, label: 'Preferências (em breve)', hint: 'Personalize sua experiência', action: () => {} },
    ];
    if (!user) {
      items.push(
        { icon: <LogIn size={16} />, label: 'Login', hint: 'Entrar na conta', action: () => navigate('/login') },
        { icon: <UserPlus size={16} />, label: 'Cadastrar', hint: 'Criar conta', action: () => navigate('/register') },
      );
    } else {
      items.push(
        { icon: <LogOut size={16} />, label: 'Sair', hint: user.email, action: () => logout() },
      );
    }
    return items;
  }, [user, navigate, logout]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return commands.filter(c => {
      if (c.requireAuth && !user) return false;
      if (!q) return true;
      return c.label.toLowerCase().includes(q) || c.hint?.toLowerCase().includes(q);
    });
  }, [commands, query, user]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="cmdp-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setOpen(false)}
          aria-modal="true"
          role="dialog"
        >
          <motion.div
            className="cmdp-panel"
            initial={{ opacity: 0, y: 20, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.98 }}
            transition={{ type: 'spring', stiffness: 260, damping: 22 }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="cmdp-input-row">
              <Command size={18} />
              <input
                ref={inputRef}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Buscar comandos, páginas e ações... (Ctrl/⌘+K)"
                className="cmdp-input"
              />
              <kbd className="kbd">Esc</kbd>
            </div>
            <div className="cmdp-list">
              {filtered.map((c, idx) => (
                <button key={idx} className="cmdp-item" onClick={() => run(c.action)}>
                  <span className="cmdp-icon">{c.icon}</span>
                  <span className="cmdp-label">{c.label}</span>
                  {c.hint && <span className="cmdp-hint">{c.hint}</span>}
                </button>
              ))}
              {filtered.length === 0 && (
                <div className="cmdp-empty">Nenhum resultado. Tente outros termos.</div>
              )}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
