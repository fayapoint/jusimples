import React, { useState, useEffect, useRef } from 'react';
import { Send } from 'lucide-react';
import { motion, useAnimation, AnimatePresence } from 'framer-motion';
import marketingPhrases from '../data/marketingPhrases';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [currentPhraseIndex, setCurrentPhraseIndex] = useState(
    Math.floor(Math.random() * marketingPhrases.length)
  );
  const mainTitleControls = useAnimation();
  const mainTitleRef = useRef(null);
  const mainTitleInterval = useRef(null);
  const phraseInterval = useRef(null);
  const [recentSearches, setRecentSearches] = useState([]);
  const [topSearches, setTopSearches] = useState([]);
  const inputRef = useRef(null);

  // Search history helpers
  const updateSearchHistory = (term) => {
    const t = (term || '').trim();
    if (!t) return;
    // Recent searches (unique, most recent first, max 10)
    const existingRecent = JSON.parse(localStorage.getItem('recentSearches') || '[]');
    const newRecent = [t, ...existingRecent.filter((s) => s !== t)].slice(0, 10);
    localStorage.setItem('recentSearches', JSON.stringify(newRecent));
    setRecentSearches(newRecent);

    // Counts for top searches
    const counts = JSON.parse(localStorage.getItem('searchCounts') || '{}');
    counts[t] = (counts[t] || 0) + 1;
    localStorage.setItem('searchCounts', JSON.stringify(counts));

    const sortedTop = Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([term, count]) => ({ term, count }));
    setTopSearches(sortedTop);
  };

  const handleChipClick = (term) => {
    setQuestion(term);
    if (inputRef.current) inputRef.current.focus();
  };

  const handleAskQuestion = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      updateSearchHistory(question);
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

  // Function to randomly animate characters in the main title
  const animateMainTitle = () => {
    if (!mainTitleRef.current) return;
    
    // Select a random character to animate
    const titleText = mainTitleRef.current.textContent;
    const charIndex = Math.floor(Math.random() * titleText.length);
    
    // Create a temporary span for the character
    const charSpan = document.createElement('span');
    charSpan.className = 'animated-char';
    charSpan.textContent = titleText[charIndex];
    
    // Apply animation
    const animationType = Math.floor(Math.random() * 3);
    switch(animationType) {
      case 0:
        charSpan.classList.add('pulse-animation');
        break;
      case 1:
        charSpan.classList.add('glow-animation');
        break;
      case 2:
        charSpan.classList.add('bounce-animation');
        break;
      default:
        charSpan.classList.add('pulse-animation');
    }
  };

  // Change the marketing phrase periodically
  useEffect(() => {
    phraseInterval.current = setInterval(() => {
      setCurrentPhraseIndex(prevIndex => {
        let newIndex;
        do {
          newIndex = Math.floor(Math.random() * marketingPhrases.length);
        } while (newIndex === prevIndex);
        return newIndex;
      });
    }, 10000); // Change every 10 seconds

    return () => clearInterval(phraseInterval.current);
  }, []);

  // Load search history on mount
  useEffect(() => {
    try {
      const recent = JSON.parse(localStorage.getItem('recentSearches') || '[]');
      setRecentSearches(recent);
      const counts = JSON.parse(localStorage.getItem('searchCounts') || '{}');
      const sortedTop = Object.entries(counts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([term, count]) => ({ term, count }));
      setTopSearches(sortedTop);
    } catch (err) {
      // ignore malformed localStorage
    }
  }, []);

  // Setup main title animation interval
  useEffect(() => {
    mainTitleInterval.current = setInterval(() => {
      animateMainTitle();
    }, Math.random() * 10000 + 20000); // Random between 20-30 seconds
    
    // Initial animation
    mainTitleControls.start({
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } // Exponential ease out
    });

    return () => clearInterval(mainTitleInterval.current);
  }, [mainTitleControls]);

  return (
    <main className="main-content">
      <section className="hero">
        <div className="hero-container">
          <motion.h1
            ref={mainTitleRef}
            initial={{ opacity: 0, y: -20 }}
            animate={mainTitleControls}
            className="main-title"
          >
            Resolva questões jurídicas com <motion.span 
              className="accent-text"
              initial={{ scale: 0.9 }}
              animate={{ scale: 1 }}
              transition={{ 
                duration: 1.2, 
                ease: [0.34, 1.56, 0.64, 1] // Spring-like bounce
              }}
            >inteligência artificial</motion.span>
          </motion.h1>
          
          <AnimatePresence mode="wait">
            <motion.p
              key={currentPhraseIndex}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ 
                duration: 0.5, 
                ease: 'easeInOut'
              }}
              className="marketing-phrase"
            >
              {marketingPhrases[currentPhraseIndex]}
            </motion.p>
          </AnimatePresence>

          <div className="chat-interface">
            <div className="chat-input-container">
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Descreva sua questão jurídica..."
                className="chat-input"
                ref={inputRef}
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

        {/* Search Trends Section */}
        <div className="search-trends">
          <div className="trend-panel">
            <div className="trend-header">
              <span className="trend-title">Buscas recentes</span>
            </div>
            <div className="trend-list">
              {recentSearches.length > 0 ? (
                recentSearches.map((t, idx) => (
                  <button key={idx} className="trend-chip" onClick={() => handleChipClick(t)}>
                    {t}
                  </button>
                ))
              ) : (
                <span className="trend-empty">Nenhuma busca recente</span>
              )}
            </div>
          </div>

          <div className="trend-panel">
            <div className="trend-header">
              <span className="trend-title">Mais buscadas</span>
            </div>
            <div className="trend-list">
              {topSearches.length > 0 ? (
                topSearches.map(({ term, count }, idx) => (
                  <button key={idx} className="trend-chip" title={`${count} vezes`} onClick={() => handleChipClick(term)}>
                    {term}
                  </button>
                ))
              ) : (
                <span className="trend-empty">Aguardando buscas</span>
              )}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
