import React, { createContext, useContext, useState, useEffect } from 'react';

const BackgroundContext = createContext();

export function useBackground() {
  return useContext(BackgroundContext);
}

export function BackgroundProvider({ children }) {
  const [backgroundType, setBackgroundType] = useState('animated'); // animated, solid
  const [backgroundColor, setBackgroundColor] = useState('default'); // default, purple, blue, green, orange

  useEffect(() => {
    // Load background settings from localStorage
    const savedBgType = localStorage.getItem('jusimples-bg-type');
    const savedBgColor = localStorage.getItem('jusimples-bg-color');
    
    if (savedBgType) {
      setBackgroundType(savedBgType);
    }
    if (savedBgColor) {
      setBackgroundColor(savedBgColor);
    }
  }, []);

  const changeBackgroundType = (newType) => {
    setBackgroundType(newType);
    localStorage.setItem('jusimples-bg-type', newType);
  };

  const changeBackgroundColor = (newColor) => {
    setBackgroundColor(newColor);
    localStorage.setItem('jusimples-bg-color', newColor);
  };

  return (
    <BackgroundContext.Provider value={{ 
      backgroundType, 
      backgroundColor, 
      changeBackgroundType, 
      changeBackgroundColor 
    }}>
      {children}
    </BackgroundContext.Provider>
  );
}
