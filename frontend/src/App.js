import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';
import CommandPalette from './components/CommandPalette';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';

function App() {
  // Add theme-specific CSS variables to the document
  useEffect(() => {
    // Add global CSS for themes
    const style = document.createElement('style');
    style.innerHTML = `
      :root[data-theme="light"] {
        --bg-primary: #f8fafc;
        --bg-secondary: #f1f5f9;
        --text-primary: #0f172a;
        --text-secondary: #334155;
        --accent-primary: #3b82f6;
        --accent-secondary: #60a5fa;
      }
      
      :root[data-theme="dark"] {
        --bg-primary: #0f172a;
        --bg-secondary: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --accent-primary: #3b82f6;
        --accent-secondary: #60a5fa;
      }
      
      :root[data-theme="normal"] {
        --bg-primary: #111827;
        --bg-secondary: #1f2937;
        --text-primary: #ffffff;
        --text-secondary: #e5e7eb;
        --accent-primary: #3b82f6;
        --accent-secondary: #60a5fa;
      }
      
      body {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        transition: background-color 0.3s ease, color 0.3s ease;
      }

      /* Theme-specific background gradients */
      :root[data-theme="normal"] .bg-gradient {
        background: radial-gradient(ellipse at top, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom right, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
      }
      
      :root[data-theme="light"] .bg-gradient {
        background: radial-gradient(ellipse at top, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom right, rgba(79, 70, 229, 0.05) 0%, transparent 50%);
      }
      
      :root[data-theme="dark"] .bg-gradient {
        background: radial-gradient(ellipse at top, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom right, rgba(139, 92, 246, 0.08) 0%, transparent 50%);
      }
    `;
    document.head.appendChild(style);
    
    return () => {
      document.head.removeChild(style);
    };
  }, []);

  return (
    <div className="App">
      <div className="bg-gradient"></div>
      <BrowserRouter>
        <AuthProvider>
          <ThemeProvider>
            <div className="layout">
              <Header />
              <div className="content">
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                </Routes>
              </div>
              <Footer />
            </div>
            <CommandPalette />
          </ThemeProvider>
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;

