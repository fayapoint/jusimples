import React, { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && !user) navigate('/login');
  }, [loading, user, navigate]);

  if (loading || !user) return null;

  return (
    <main className="main-content" style={{ padding: '6rem 2rem 2rem' }}>
      <div style={{ maxWidth: 900, margin: '0 auto' }}>
        <h2 style={{ marginBottom: 16 }}>Bem-vindo, {user.name}</h2>
        <p style={{ color: 'var(--text-secondary)' }}>Este é o seu painel. Em breve: histórico de perguntas, favoritos, preferências e acesso rápido.</p>
        <div style={{ marginTop: 24, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 16 }}>
          <div style={{ border: '1px solid var(--border)', borderRadius: 12, padding: 16 }}>
            <div style={{ fontWeight: 600, marginBottom: 8 }}>Status da Conta</div>
            <div style={{ color: 'var(--text-secondary)' }}>E-mail: {user.email}</div>
          </div>
          <div style={{ border: '1px solid var(--border)', borderRadius: 12, padding: 16 }}>
            <div style={{ fontWeight: 600, marginBottom: 8 }}>Acesso Rápido</div>
            <div style={{ color: 'var(--text-secondary)' }}>Pergunte à IA diretamente da página inicial.</div>
          </div>
        </div>
      </div>
    </main>
  );
}
