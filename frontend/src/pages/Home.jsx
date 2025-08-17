import React, { useState } from 'react';
import { Send } from 'lucide-react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAskQuestion = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      const data = await response.json();
      setAnswer(data.answer);
    } catch (e) {
      setAnswer('Erro ao processar sua pergunta. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !loading) {
      e.preventDefault();
      handleAskQuestion();
    }
  };

  return (
    <main className="main-content">
      <section className="hero">
        <div className="hero-container">
          <h1>
            Resolva questões jurídicas com <span className="accent-text">inteligência artificial</span>
          </h1>
          <p>
            Democratizando o acesso à justiça através de IA avançada. Obtenha orientações jurídicas precisas em segundos.
          </p>

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
              <button onClick={handleAskQuestion} disabled={loading || !question.trim()} className="chat-send-btn">
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
  );
}
