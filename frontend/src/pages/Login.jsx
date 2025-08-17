import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (_) {
      setError('E-mail ou senha incorretos');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="main-content" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <form onSubmit={handleSubmit} style={{ width: 380, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 16, padding: 24 }}>
        <h2 style={{ marginBottom: 16 }}>Entrar</h2>
        {error && <div style={{ color: '#ef4444', marginBottom: 12 }}>{error}</div>}
        <div style={{ display: 'grid', gap: 12 }}>
          <input type="email" placeholder="E-mail" value={email} onChange={e => setEmail(e.target.value)} required style={{ padding: 12, borderRadius: 8, border: '1px solid var(--border)', background: 'var(--surface-light)', color: '#fff' }} />
          <input type="password" placeholder="Senha" value={password} onChange={e => setPassword(e.target.value)} required style={{ padding: 12, borderRadius: 8, border: '1px solid var(--border)', background: 'var(--surface-light)', color: '#fff' }} />
          <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? 'Entrando...' : 'Entrar'}</button>
        </div>
        <div style={{ marginTop: 12, color: 'var(--text-secondary)' }}>
          Não tem conta? <Link to="/register" style={{ color: 'var(--accent)' }}>Cadastre-se</Link>
        </div>
      </form>
    </main>
  );
}
