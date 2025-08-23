import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Scale, LogIn, UserPlus, Search, Sun, Moon, Monitor, Presentation } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export default function Header() {
  const { user, logout } = useAuth();
  const { theme, changeTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="header">
      <nav className="nav-container">
        <Link to="/" className="logo">
          <Scale size={24} />
          JuSimples
        </Link>
        <div className="nav-buttons">
          <div className="theme-buttons">
            <button
              className={`theme-btn ${theme === 'normal' ? 'active' : ''}`}
              onClick={() => changeTheme('normal')}
              title="Tema Normal"
            >
              <Monitor size={16} />
            </button>
            <button
              className={`theme-btn ${theme === 'light' ? 'active' : ''}`}
              onClick={() => changeTheme('light')}
              title="Tema Claro"
            >
              <Sun size={16} />
            </button>
            <button
              className={`theme-btn ${theme === 'dark' ? 'active' : ''}`}
              onClick={() => changeTheme('dark')}
              title="Tema Escuro"
            >
              <Moon size={16} />
            </button>
          </div>
          <Link className="btn btn-outline" to="/projeto">
            <Presentation size={16} />
            Projeto
          </Link>
          <button
            className="btn btn-outline"
            onClick={() => window.dispatchEvent(new Event('open-command-palette'))}
            title="Abrir comandos (Ctrl/⌘+K)"
          >
            <Search size={16} />
            Comandos
            <span className="kbd-badge">Ctrl K</span>
          </button>
          {!user ? (
            <>
              <Link className="btn btn-outline" to="/register">
                <UserPlus size={16} />
                Cadastrar
              </Link>
              <Link className="btn btn-primary" to="/login">
                <LogIn size={16} />
                Login
              </Link>
            </>
          ) : (
            <>
              <span style={{ color: '#a1a1aa', marginRight: 8 }}>Olá, <strong style={{ color: '#fff' }}>{user.name}</strong></span>
              <button className="btn btn-outline" onClick={handleLogout}>Sair</button>
              <Link className="btn btn-primary" to="/dashboard">Dashboard</Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
