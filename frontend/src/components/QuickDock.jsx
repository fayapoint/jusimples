import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import {
  HomeIcon,
  DashboardIcon,
  AboutIcon,
  ContactIcon,
  EmailIcon,
  LightThemeIcon,
  DarkThemeIcon,
  NormalThemeIcon
} from './icons/NavigationIcons';


export default function QuickDock() {
  const { user, logout } = useAuth();
  const { theme, changeTheme } = useTheme();
  const navigate = useNavigate();

  const openPalette = () => window.dispatchEvent(new Event('open-command-palette'));

  const items = [
    { key: 'home', label: 'Início', icon: <HomeIcon />, onClick: () => navigate('/') },
    { key: 'about', label: 'Sobre', icon: <AboutIcon />, onClick: () => navigate('/about') },
    user
      ? { key: 'dash', label: 'Dashboard', icon: <DashboardIcon />, onClick: () => navigate('/dashboard') }
      : { key: 'contact', label: 'Contato', icon: <ContactIcon />, onClick: () => navigate('/contact') },
    { 
      key: 'theme', 
      label: theme === 'light' ? 'Claro' : theme === 'dark' ? 'Escuro' : 'Normal', 
      icon: theme === 'light' ? <LightThemeIcon /> : theme === 'dark' ? <DarkThemeIcon /> : <NormalThemeIcon />,
      onClick: () => {
        // Cycle through themes: normal -> light -> dark -> normal
        const nextTheme = theme === 'normal' ? 'light' : theme === 'light' ? 'dark' : 'normal';
        changeTheme(nextTheme);
      }
    },
  ];

  return (
    <AnimatePresence>
      <motion.nav
        className={`quick-dock ${theme === 'dark' ? 'quick-dock-dark' : theme === 'light' ? 'quick-dock-light' : ''}`}
        initial={{ y: 80, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 80, opacity: 0 }}
        transition={{ type: 'spring', stiffness: 160, damping: 18 }}
        aria-label="Navegação rápida"
        style={{
          background: theme === 'dark' ? 'rgba(17, 24, 39, 0.8)' : 
                     theme === 'light' ? 'rgba(255, 255, 255, 0.8)' : 
                     'rgba(15, 23, 42, 0.8)',
          borderColor: theme === 'dark' ? 'rgba(75, 85, 99, 0.3)' : 
                        theme === 'light' ? 'rgba(203, 213, 225, 0.5)' : 
                        'rgba(59, 130, 246, 0.3)',
          backdropFilter: 'blur(10px)',
          boxShadow: theme === 'dark' ? '0 10px 25px -5px rgba(0, 0, 0, 0.3)' : 
                      theme === 'light' ? '0 10px 25px -5px rgba(0, 0, 0, 0.1)' : 
                      '0 10px 25px -5px rgba(0, 0, 0, 0.2)',
          position: 'fixed',
          bottom: '1rem',
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          borderRadius: '0.75rem',
          padding: '0.5rem',
          zIndex: 50,
          gap: '0.25rem'
        }}
      >
        {items.map((item) => (
          <button 
            key={item.key} 
            className={`quick-dock-btn ${theme === 'dark' ? 'quick-dock-btn-dark' : theme === 'light' ? 'quick-dock-btn-light' : ''}`} 
            onClick={item.onClick} 
            aria-label={item.label}
            style={{
              color: theme === 'dark' ? 'rgba(229, 231, 235, 0.9)' : 
                     theme === 'light' ? 'rgba(31, 41, 55, 0.9)' : 
                     'rgba(255, 255, 255, 0.9)',
              background: 'transparent',
              border: 'none',
              borderRadius: '0.5rem',
              padding: '0.5rem 0.75rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '0.75rem',
              fontWeight: 500,
              gap: '0.375rem',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
          >
            <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              {item.icon}
            </span>
            <span className="quick-dock-label" style={{
              fontSize: '0.7rem',
              fontWeight: 500,
              marginTop: '0.125rem'  
            }}>{item.label}</span>
          </button>
        ))}
      </motion.nav>
    </AnimatePresence>
  );
}
