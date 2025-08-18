import React, { useState } from 'react';
import { useBackground } from '../context/BackgroundContext';

export default function BackgroundSelector() {
  const [isOpen, setIsOpen] = useState(false);
  const { backgroundType, backgroundColor, changeBackgroundType, changeBackgroundColor } = useBackground();

  const backgroundTypes = [
    { id: 'animated', label: 'Animated', icon: '✨' },
    { id: 'solid', label: 'Solid', icon: '🎨' }
  ];

  const backgroundColors = [
    { id: 'default', label: 'Default', color: '#6366f1' },
    { id: 'purple', label: 'Purple', color: '#9333ea' },
    { id: 'blue', label: 'Blue', color: '#3b82f6' },
    { id: 'green', label: 'Green', color: '#22c55e' },
    { id: 'orange', label: 'Orange', color: '#f97316' }
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
        </div>
      )}
    </div>
  );
}
