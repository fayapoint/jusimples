import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Home, LayoutDashboard, LogIn, LogOut, Search, UserPlus } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function QuickDock() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const openPalette = () => window.dispatchEvent(new Event('open-command-palette'));

  const items = [
    { key: 'home', label: 'Início', icon: <Home size={18} />, onClick: () => navigate('/') },
    { key: 'search', label: 'Comandos', icon: <Search size={18} />, onClick: openPalette },
    user
      ? { key: 'dash', label: 'Dashboard', icon: <LayoutDashboard size={18} />, onClick: () => navigate('/dashboard') }
      : { key: 'login', label: 'Login', icon: <LogIn size={18} />, onClick: () => navigate('/login') },
    user
      ? { key: 'logout', label: 'Sair', icon: <LogOut size={18} />, onClick: () => logout() }
      : { key: 'register', label: 'Cadastrar', icon: <UserPlus size={18} />, onClick: () => navigate('/register') },
  ];

  return (
    <AnimatePresence>
      <motion.nav
        className="quick-dock"
        initial={{ y: 80, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 80, opacity: 0 }}
        transition={{ type: 'spring', stiffness: 160, damping: 18 }}
        aria-label="Navegação rápida"
      >
        {items.map((item) => (
          <button key={item.key} className="quick-dock-btn" onClick={item.onClick} aria-label={item.label}>
            {item.icon}
            <span className="quick-dock-label">{item.label}</span>
          </button>
        ))}
      </motion.nav>
    </AnimatePresence>
  );
}
