import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await register(name, email, password);
      navigate('/dashboard');
    } catch (_) {
      setError('Falha no cadastro. Tente outro e-mail.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="main-content" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <form onSubmit={handleSubmit} style={{ width: 420, background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 16, padding: 24 }}>
        <h2 style={{ marginBottom: 16 }}>Criar conta</h2>
        {error && <div style={{ color: '#ef4444', marginBottom: 12 }}>{error}</div>}
        <div style={{ display: 'grid', gap: 12 }}>
          <input type="text" placeholder="Nome" value={name} onChange={e => setName(e.target.value)} required style={{ padding: 12, borderRadius: 8, border: '1px solid var(--border)', background: 'var(--surface-light)', color: '#fff' }} />
          <input type="email" placeholder="E-mail" value={email} onChange={e => setEmail(e.target.value)} required style={{ padding: 12, borderRadius: 8, border: '1px solid var(--border)', background: 'var(--surface-light)', color: '#fff' }} />
          <input type="password" placeholder="Senha (mín. 6 caracteres)" value={password} onChange={e => setPassword(e.target.value)} required minLength={6} style={{ padding: 12, borderRadius: 8, border: '1px solid var(--border)', background: 'var(--surface-light)', color: '#fff' }} />
          <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? 'Cadastrando...' : 'Cadastrar'}</button>
        </div>
        <div style={{ marginTop: 12, color: 'var(--text-secondary)' }}>
          Já tem conta? <Link to="/login" style={{ color: 'var(--accent)' }}>Entrar</Link>
        </div>
      </form>
    </main>
  );
}
