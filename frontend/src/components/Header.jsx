import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Scale, LogIn, UserPlus, Search } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Header() {
  const { user, logout } = useAuth();
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
