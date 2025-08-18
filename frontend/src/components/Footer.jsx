import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';

// Get API URL from environment or use production URL as fallback
const API_URL = process.env.REACT_APP_API_URL || 'https://jusimples-production.up.railway.app';
const LOCAL_FALLBACK = 'https://jusimples-production.up.railway.app';

// For debugging
console.log('Environment API URL:', process.env.REACT_APP_API_URL);
console.log('Using API URL:', API_URL);

export default function Footer() {
  return (
    <footer className="footer compact-footer">
      <div className="footer-container compact">
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
      </div>
    </footer>
  );
}
