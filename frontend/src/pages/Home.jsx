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
  const [globalPopularSearches, setGlobalPopularSearches] = useState([]);
  const [recentPage, setRecentPage] = useState(0);
  const [popularPage, setPopularPage] = useState(0);
  const [isFlipping, setIsFlipping] = useState({ recent: false, popular: false });
  const [filterCategory] = useState('all');
  const [sortOption] = useState('frequency');
  const inputRef = useRef(null);
  const hoverTimeoutRef = useRef(null);

  const ITEMS_PER_PAGE = 4;

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

  // Categorize search terms
  const categorizeSearch = (term) => {
    const lowerTerm = term.toLowerCase();
    if (lowerTerm.includes('trabalh') || lowerTerm.includes('emprego') || lowerTerm.includes('rescisão') || 
        lowerTerm.includes('férias') || lowerTerm.includes('salário') || lowerTerm.includes('horas extras')) {
      return 'trabalhista';
    }
    if (lowerTerm.includes('consumidor') || lowerTerm.includes('produto') || lowerTerm.includes('serviço') || 
        lowerTerm.includes('compra') || lowerTerm.includes('defeito')) {
      return 'consumidor';
    }
    if (lowerTerm.includes('civil') || lowerTerm.includes('contrato') || lowerTerm.includes('danos morais') || 
        lowerTerm.includes('família') || lowerTerm.includes('divórcio')) {
      return 'civil';
    }
    if (lowerTerm.includes('aposentadoria') || lowerTerm.includes('pensão') || lowerTerm.includes('inss') || 
        lowerTerm.includes('previdência')) {
      return 'previdenciario';
    }
    return 'geral';
  };

  // Sort and filter searches

  // Card navigation functions
  const navigateCard = async (cardType, direction) => {
    const currentPage = cardType === 'recent' ? recentPage : popularPage;
    const items = cardType === 'recent' ? recentSearches : (() => {
      const localSearches = sortAndFilterSearches(topSearches, true);
      const globalSearches = sortAndFilterSearches(globalPopularSearches, false)
        .filter(term => !localSearches.some(local => local.term.toLowerCase() === term.toLowerCase()));
      return [...localSearches.map(({ term, count }) => ({ term, count, type: 'local', badge: `${count}x` })), 
              ...globalSearches.map(term => ({ term, count: 0, type: 'global', badge: 'Popular' }))];
    })();
    
    const totalPages = Math.ceil(items.length / ITEMS_PER_PAGE);
    const newPage = direction === 'next' 
      ? Math.min(currentPage + 1, totalPages - 1)
      : Math.max(currentPage - 1, 0);
    
    if (newPage === currentPage) return;
    
    setIsFlipping(prev => ({ ...prev, [cardType]: true }));
    
    setTimeout(() => {
      if (cardType === 'recent') {
        setRecentPage(newPage);
      } else {
        setPopularPage(newPage);
      }
    }, 300);
    
    setTimeout(() => {
      setIsFlipping(prev => ({ ...prev, [cardType]: false }));
    }, 600);
  };

  const getPageItems = (items, page) => {
    const start = page * ITEMS_PER_PAGE;
    return items.slice(start, start + ITEMS_PER_PAGE);
  };

  const getTotalPages = (items) => Math.ceil(items.length / ITEMS_PER_PAGE);

  // Cleanup timeout on unmount
  useEffect(() => {
    const timeoutRef = hoverTimeoutRef.current;
    return () => {
      if (timeoutRef) {
        clearTimeout(timeoutRef);
      }
    };
  }, []);

  const sortAndFilterSearches = (searches, isLocal = false) => {
    let filtered = searches;
    
    // Apply category filter
    if (filterCategory !== 'all') {
      filtered = searches.filter(search => {
        const term = isLocal ? search.term || search : search;
        return categorizeSearch(term) === filterCategory;
      });
    }
    
    // Apply sorting
    filtered.sort((a, b) => {
      const termA = isLocal ? (a.term || a) : a;
      const termB = isLocal ? (b.term || b) : b;
      const countA = isLocal ? (a.count || 0) : 0;
      const countB = isLocal ? (b.count || 0) : 0;
      
      switch (sortOption) {
        case 'alphabetical':
          return termA.localeCompare(termB);
        case 'recent':
          // For global searches, we don't have timestamps, so keep original order
          return isLocal ? (countB - countA) : 0;
        case 'frequency':
        default:
          return countB - countA;
      }
    });
    
    return filtered;
  };

  // Fetch global popular searches from database (real user searches only)
  const fetchGlobalPopularSearches = async () => {
    try {
      const response = await fetch(`${API_URL}/api/popular-searches`);
      const data = await response.json();
      
      // Use popular searches from database or defaults
      if (data.popular_searches && data.popular_searches.length > 0) {
        setGlobalPopularSearches(data.popular_searches);
        console.log(`Loaded ${data.total_found} popular searches (from ${data.from_database ? 'database' : 'defaults'})`);
      } else {
        setGlobalPopularSearches([]);
        console.log('No popular searches available');
      }
    } catch (error) {
      console.log('Could not fetch popular searches from database');
      setGlobalPopularSearches([]);
    }
  };

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
    
    // Always fetch global popular searches for anonymous users
    fetchGlobalPopularSearches();
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

        {/* Enhanced Search Trends Section */}
        <div className="search-trends">
          {/* Recent Searches Card */}
          <div className="trend-panel recent">
            <div className="trend-header">
              <div className="trend-title">📚 Buscas recentes</div>
              <div className="trend-subtitle">Suas consultas anteriores</div>
              {recentSearches.length > ITEMS_PER_PAGE && (
                <div className="card-nav">
                  <button 
                    className="nav-button"
                    onClick={() => navigateCard('recent', 'prev')}
                    disabled={recentPage === 0}
                    title="Página anterior"
                  >
                    ←
                  </button>
                  <div className="card-pagination">
                    {Array.from({ length: getTotalPages(recentSearches) }, (_, i) => (
                      <div 
                        key={i} 
                        className={`page-dot ${i === recentPage ? 'active' : ''}`}
                        onClick={() => setRecentPage(i)}
                      />
                    ))}
                  </div>
                  <button 
                    className="nav-button"
                    onClick={() => navigateCard('recent', 'next')}
                    disabled={recentPage >= getTotalPages(recentSearches) - 1}
                    title="Próxima página"
                  >
                    →
                  </button>
                </div>
              )}
            </div>
            <div className="card-content">
              <div className="card-stack">
                {recentSearches.length > 0 ? (
                  <>
                    <div className={`card-page ${isFlipping.recent ? 'exiting' : 'active'}`}>
                      {getPageItems(recentSearches, recentPage).map((term, idx) => (
                        <div 
                          key={`${recentPage}-${idx}`} 
                          className="search-item"
                          onClick={() => handleChipClick(term)}
                        >
                          <div className="search-item-content">
                            <span className="search-term">{term}</span>
                            <div className="search-meta">
                              <span className="meta-icon">🔍</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                    {isFlipping.recent && (
                      <div className="card-page entering">
                        {getPageItems(recentSearches, recentPage).map((term, idx) => (
                          <div 
                            key={`${recentPage}-entering-${idx}`} 
                            className="search-item"
                            onClick={() => handleChipClick(term)}
                          >
                            <div className="search-item-content">
                              <span className="search-term">{term}</span>
                              <div className="search-meta">
                                <span className="meta-icon">🔍</span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                ) : (
                  <div className="card-empty-state">
                    <div className="empty-icon">📝</div>
                    <div className="empty-text">Nenhuma busca recente</div>
                    <div className="empty-subtitle">Suas consultas aparecerão aqui</div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Popular Searches Card */}
          <div className="trend-panel popular">
            <div className="trend-header">
              <div className="trend-title">🔥 Mais buscadas</div>
              <div className="trend-subtitle">Consultas populares da comunidade</div>
              {(() => {
                const localSearches = sortAndFilterSearches(topSearches, true);
                const globalSearches = sortAndFilterSearches(globalPopularSearches, false)
                  .filter(term => !localSearches.some(local => local.term.toLowerCase() === term.toLowerCase()));
                const combinedItems = [
                  ...localSearches.map(({ term, count }) => ({ term, count, type: 'local', badge: `${count}x` })), 
                  ...globalSearches.map(term => ({ term, count: 0, type: 'global', badge: 'Popular' }))
                ];
                
                return combinedItems.length > ITEMS_PER_PAGE && (
                  <div className="card-nav">
                    <button 
                      className="nav-button"
                      onClick={() => navigateCard('popular', 'prev')}
                      disabled={popularPage === 0}
                      title="Página anterior"
                    >
                      ←
                    </button>
                    <div className="card-pagination">
                      {Array.from({ length: getTotalPages(combinedItems) }, (_, i) => (
                        <div 
                          key={i} 
                          className={`page-dot ${i === popularPage ? 'active' : ''}`}
                          onClick={() => setPopularPage(i)}
                        />
                      ))}
                    </div>
                    <button 
                      className="nav-button"
                      onClick={() => navigateCard('popular', 'next')}
                      disabled={popularPage >= getTotalPages(combinedItems) - 1}
                      title="Próxima página"
                    >
                      →
                    </button>
                  </div>
                );
              })()}
            </div>
            <div className="card-content">
              <div className="card-stack">
                {(() => {
                  const localSearches = sortAndFilterSearches(topSearches, true);
                  const globalSearches = sortAndFilterSearches(globalPopularSearches, false)
                    .filter(term => !localSearches.some(local => local.term.toLowerCase() === term.toLowerCase()));
                  const combinedItems = [
                    ...localSearches.map(({ term, count }) => ({ term, count, type: 'local', badge: `${count}x` })), 
                    ...globalSearches.map(term => ({ term, count: 0, type: 'global', badge: 'Popular' }))
                  ];

                  return combinedItems.length > 0 ? (
                    <>
                      <div className={`card-page ${isFlipping.popular ? 'exiting' : 'active'}`}>
                        {getPageItems(combinedItems, popularPage).map((item, idx) => (
                          <div 
                            key={`${popularPage}-${idx}`} 
                            className={`search-item ${categorizeSearch(item.term)}`}
                            onClick={() => handleChipClick(item.term)}
                          >
                            <div className="search-item-content">
                              <span className="search-term">{item.term}</span>
                              <div className="search-meta">
                                <span className={`meta-badge ${item.type === 'local' ? 'count' : ''}`}>
                                  {item.badge}
                                </span>
                                <span className="meta-icon">🔍</span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                      {isFlipping.popular && (
                        <div className="card-page entering">
                          {getPageItems(combinedItems, popularPage).map((item, idx) => (
                            <div 
                              key={`${popularPage}-entering-${idx}`} 
                              className={`search-item ${categorizeSearch(item.term)}`}
                              onClick={() => handleChipClick(item.term)}
                            >
                              <div className="search-item-content">
                                <span className="search-term">{item.term}</span>
                                <div className="search-meta">
                                  <span className={`meta-badge ${item.type === 'local' ? 'count' : ''}`}>
                                    {item.badge}
                                  </span>
                                  <span className="meta-icon">🔍</span>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </>
                  ) : (
                    <div className="card-empty-state">
                      <div className="empty-icon">⏳</div>
                      <div className="empty-text">Aguardando buscas</div>
                      <div className="empty-subtitle">As consultas populares aparecerão aqui</div>
                    </div>
                  );
                })()}
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
