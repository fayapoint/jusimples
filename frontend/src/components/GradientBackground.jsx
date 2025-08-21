import React from 'react';
import { useBackground } from '../context/BackgroundContext';

export default function GradientBackground() {
  const { backgroundType, backgroundColor } = useBackground();

  // Don't render if background type is not gradient
  if (backgroundType !== 'gradient') {
    return null;
  }

  // Define gradient mappings
  const gradientMappings = {
    sunset: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    ocean: 'linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)',
    cosmic: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
    aurora: 'linear-gradient(135deg, #00c6ff 0%, #0072ff 100%)',
    fire: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%)',
    forest: 'linear-gradient(135deg, #134e5e 0%, #71b280 100%)',
    neon: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    royal: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    tropical: 'linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%)',
    midnight: 'linear-gradient(135deg, #2c3e50 0%, #3498db 100%)',
    candy: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    volcano: 'linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)'
  };

  const selectedGradient = gradientMappings[backgroundColor] || gradientMappings.sunset;

  return (
    <div 
      className="gradient-background"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: selectedGradient,
        pointerEvents: 'none',
        zIndex: -1,
      }}
    />
  );
}
