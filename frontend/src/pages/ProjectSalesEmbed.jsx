import React, { useEffect, useState } from 'react';

// Wrapper page to embed the external sales site inside the app shell (Header/Footer preserved via App.js layout)
// Does not modify the original ProjectSales page component.
export default function ProjectSalesEmbed() {
  const [loaded, setLoaded] = useState(false);
  const [showFallback, setShowFallback] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => {
      // If the iframe hasn't fired onLoad yet after a delay, show a fallback link
      if (!loaded) setShowFallback(true);
    }, 6000);
    return () => clearTimeout(t);
  }, [loaded]);

  // Height calculation: full viewport minus header (~4rem) and bottom reserved space (~80px) for compact footer
  const iframeHeight = 'calc(100vh - 4rem - 80px)';

  return (
    <div
      className="embed-wrapper"
      style={{
        paddingTop: '4rem', // push content below fixed header
        flex: '1 1 auto',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'stretch',
        minHeight: 0,
      }}
    >
      {/* Optional subtle top info for debugging - hidden by default */}
      <div style={{ display: 'none' }} aria-hidden="true">
        {!loaded && 'Carregando página externa…'}
      </div>

      <iframe
        title="JuSimples - Apresentação e Vendas"
        src="https://jusimplespagesale.netlify.app/"
        style={{
          width: '100%',
          height: iframeHeight,
          border: 'none',
          background: 'transparent',
          borderRadius: 0,
          flex: '0 0 auto',
        }}
        allow="clipboard-read; clipboard-write; fullscreen"
        allowFullScreen
        referrerPolicy="no-referrer-when-downgrade"
        onLoad={() => setLoaded(true)}
      />

      {showFallback && !loaded && (
        <div
          style={{
            marginTop: '1rem',
            textAlign: 'center',
            color: 'var(--text-secondary)'
          }}
          role="status"
        >
          Não foi possível carregar a página incorporada. Abra em uma nova aba:
          {' '}
          <a
            href="https://jusimplespagesale.netlify.app/"
            rel="noopener noreferrer"
            target="_blank"
            style={{ color: 'var(--accent)' }}
          >
            https://jusimplespagesale.netlify.app/
          </a>
        </div>
      )}

      <noscript>
        Habilite JavaScript para visualizar o conteúdo incorporado. Você também pode abrir a página
        {' '}
        <a href="https://jusimplespagesale.netlify.app/" target="_blank" rel="noopener noreferrer">diretamente aqui</a>.
      </noscript>
    </div>
  );
}
