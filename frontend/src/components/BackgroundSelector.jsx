import React, { useState } from 'react';
import { useBackground } from '../context/BackgroundContext';

export default function BackgroundSelector() {
  const [isOpen, setIsOpen] = useState(false);
  const { backgroundType, backgroundColor, changeBackgroundType, changeBackgroundColor } = useBackground();

  const backgroundTypes = [
    { id: 'animated', label: 'Animated', icon: '✨' },
    { id: 'solid', label: 'Solid', icon: '🎨' },
    { id: 'gradient', label: 'Gradient', icon: '🌈' }
  ];

  const backgroundColors = [
    { id: 'default', label: 'Default', color: '#6366f1' },
    { id: 'purple', label: 'Purple', color: '#9333ea' },
    { id: 'blue', label: 'Blue', color: '#3b82f6' },
    { id: 'green', label: 'Green', color: '#22c55e' },
    { id: 'orange', label: 'Orange', color: '#f97316' },
    { id: 'black', label: 'Black', color: '#000000' },
    { id: 'white', label: 'White', color: '#ffffff' },
    { id: 'red', label: 'Red', color: '#ef4444' },
    { id: 'gray', label: 'Gray', color: '#6b7280' }
  ];

  const backgroundGradients = [
    { id: 'sunset', label: 'Sunset', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
    { id: 'ocean', label: 'Ocean', gradient: 'linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)' },
    { id: 'cosmic', label: 'Cosmic', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)' },
    { id: 'aurora', label: 'Aurora', gradient: 'linear-gradient(135deg, #00c6ff 0%, #0072ff 100%)' },
    { id: 'fire', label: 'Fire', gradient: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%)' },
    { id: 'forest', label: 'Forest', gradient: 'linear-gradient(135deg, #134e5e 0%, #71b280 100%)' },
    { id: 'neon', label: 'Neon', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
    { id: 'royal', label: 'Royal', gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
    { id: 'tropical', label: 'Tropical', gradient: 'linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%)' },
    { id: 'midnight', label: 'Midnight', gradient: 'linear-gradient(135deg, #2c3e50 0%, #3498db 100%)' },
    { id: 'candy', label: 'Candy', gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)' },
    { id: 'volcano', label: 'Volcano', gradient: 'linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)' }
  ];

  const animationTypes = [
    { id: 'default', label: 'Default', description: 'Gentle floating particles' },
    { id: 'matrix', label: 'Matrix', description: 'Digital rain effect' },
    { id: 'waves', label: 'Waves', description: 'Flowing wave patterns' },
    { id: 'particles', label: 'Particles', description: 'Dynamic particle system' },
    { id: 'spiral', label: 'Spiral', description: 'Rotating spiral motion' },
    { id: 'pulse', label: 'Pulse', description: 'Rhythmic pulsing effect' }
  ];

  return (
    <div className="background-selector">
      <button
        className="bg-selector-toggle"
        onClick={() => setIsOpen(!isOpen)}
        title="Background Settings"
      >
        🎭
      </button>
      
      {isOpen && (
        <div className="bg-selector-panel">
          <div className="bg-selector-section">
            <h4>Background Type</h4>
            <div className="bg-type-options">
              {backgroundTypes.map(type => (
                <button
                  key={type.id}
                  className={`bg-type-btn ${backgroundType === type.id ? 'active' : ''}`}
                  onClick={() => changeBackgroundType(type.id)}
                >
                  <span className="bg-type-icon">{type.icon}</span>
                  {type.label}
                </button>
              ))}
            </div>
          </div>

          {backgroundType === 'solid' && (
            <div className="bg-selector-section">
              <h4>Background Color</h4>
              <div className="bg-color-options">
                {backgroundColors.map(color => (
                  <button
                    key={color.id}
                    className={`bg-color-btn ${backgroundColor === color.id ? 'active' : ''}`}
                    onClick={() => changeBackgroundColor(color.id)}
                    title={color.label}
                  >
                    <div 
                      className="bg-color-swatch"
                      style={{ backgroundColor: color.color }}
                    />
                    <span className="bg-color-label">{color.label}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {backgroundType === 'gradient' && (
            <div className="bg-selector-section">
              <h4>Gradient Style</h4>
              <div className="bg-gradient-options">
                {backgroundGradients.map(gradient => (
                  <button
                    key={gradient.id}
                    className={`bg-gradient-btn ${backgroundColor === gradient.id ? 'active' : ''}`}
                    onClick={() => changeBackgroundColor(gradient.id)}
                    title={gradient.label}
                  >
                    <div 
                      className="bg-gradient-swatch"
                      style={{ background: gradient.gradient }}
                    />
                    <span className="bg-gradient-label">{gradient.label}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {backgroundType === 'animated' && (
            <div className="bg-selector-section">
              <h4>Animation Style</h4>
              <div className="bg-animation-options">
                {animationTypes.map(animation => (
                  <button
                    key={animation.id}
                    className={`bg-animation-btn ${backgroundColor === animation.id ? 'active' : ''}`}
                    onClick={() => changeBackgroundColor(animation.id)}
                    title={animation.description}
                  >
                    <span className="bg-animation-label">{animation.label}</span>
                    <span className="bg-animation-desc">{animation.description}</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
