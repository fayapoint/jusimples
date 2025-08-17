import React, { useState } from 'react';
import { Scale, Send, LogIn, UserPlus } from 'lucide-react';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAskQuestion = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    try {
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
      const response = await fetch(`${apiUrl}/api/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });
      
      const data = await response.json();
      setAnswer(data.answer);
    } catch (error) {
      console.error('Erro ao fazer pergunta:', error);
      setAnswer('Erro ao processar sua pergunta. Tente novamente.');
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !loading) {
      e.preventDefault();
      handleAskQuestion();
    }
  };

  return (
    <div className="App">
      <div className="bg-gradient"></div>
      
      {/* Header */}
      <header className="header">
        <nav className="nav-container">
          <a href="/" className="logo">
            <Scale size={24} />
            JuSimples
          </a>
          <div className="nav-buttons">
            <button className="btn btn-outline" onClick={() => console.log('Cadastrar clicked')}>
              <UserPlus size={16} />
              Cadastrar
            </button>
            <button className="btn btn-primary" onClick={() => console.log('Login clicked')}>
              <LogIn size={16} />
              Login
            </button>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Hero Section */}
        <section className="hero">
          <div className="hero-container">
            <h1>
              Resolva questões jurídicas com <span className="accent-text">inteligência artificial</span>
            </h1>
            <p>
              Democratizando o acesso à justiça através de IA avançada. 
              Obtenha orientações jurídicas precisas em segundos.
            </p>
            
            {/* Chat Interface */}
            <div className="chat-interface">
              <div className="chat-input-container">
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Descreva sua questão jurídica..."
                  className="chat-input"
                  rows="1"
                />
                <button
                  onClick={handleAskQuestion}
                  disabled={loading || !question.trim()}
                  className="chat-send-btn"
                >
                  <Send size={16} />
                </button>
              </div>
              
              {loading && (
                <div className="typing-indicator">
                  <span>Analisando sua questão</span>
                  <div className="typing-dots">
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                </div>
              )}
              
              {answer && (
                <div className="chat-response">
                  <h4>Orientação Jurídica</h4>
                  <p>{answer}</p>
                </div>
              )}
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-container">
          <p className="footer-disclaimer">
            O JuSimples utiliza inteligência artificial para fornecer orientações jurídicas baseadas na legislação brasileira. 
            As informações são de caráter informativo. Para casos complexos, consulte um advogado especializado.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

