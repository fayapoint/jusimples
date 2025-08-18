import React from 'react';
import { useTheme } from '../context/ThemeContext';

const HeroImage = ({ type = 'default', className = '' }) => {
  const { theme } = useTheme();
  
  // Generate SVG patterns based on page type and theme
  const generatePattern = () => {
    // Base colors based on theme
    let mainColor, accentColor, lightColor;
    
    switch(theme) {
      case 'light':
        mainColor = '#3b82f6';
        accentColor = '#818cf8';
        lightColor = '#e0e7ff';
        break;
      case 'dark':
        mainColor = '#4f46e5';
        accentColor = '#6366f1';
        lightColor = '#1e1b4b';
        break;
      case 'original':
        mainColor = '#00b8ff';
        accentColor = '#0088cc';
        lightColor = '#041554';
        break;
      default:
        mainColor = '#6366f1';
        accentColor = '#818cf8';
        lightColor = '#1e1b4b';
    }
    
    // Generate different patterns based on page type
    switch(type) {
      case 'advogados':
        return (
          <svg width="100%" height="100%" viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid slice">
            <defs>
              <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor={mainColor} stopOpacity="0.7" />
                <stop offset="100%" stopColor={accentColor} stopOpacity="0.3" />
              </linearGradient>
              <clipPath id="clip">
                <rect width="100%" height="100%" />
              </clipPath>
            </defs>
            <g clipPath="url(#clip)">
              <path d="M300,200 Q450,50 600,200 T900,300 T600,400 T300,500 T50,350 T300,200" 
                    fill="none" stroke={mainColor} strokeWidth="2" opacity="0.2" />
              <path d="M300,220 Q450,70 600,220 T900,320 T600,420 T300,520 T50,370 T300,220" 
                    fill="none" stroke={accentColor} strokeWidth="3" opacity="0.1" />
              <circle cx="700" cy="200" r="120" fill="url(#grad1)" />
              <path d="M0,150 L1000,20 L1000,180 L0,300 Z" fill={lightColor} opacity="0.05" />
              {/* Scale of justice elements */}
              <circle cx="500" cy="150" r="30" fill={mainColor} opacity="0.2" />
              <rect x="470" y="150" width="60" height="4" fill={mainColor} opacity="0.4" />
              <circle cx="420" cy="220" r="20" fill={mainColor} opacity="0.3" />
              <circle cx="580" cy="220" r="20" fill={mainColor} opacity="0.3" />
            </g>
          </svg>
        );
      
      case 'empresas':
        return (
          <svg width="100%" height="100%" viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid slice">
            <defs>
              <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor={mainColor} stopOpacity="0.5" />
                <stop offset="100%" stopColor={accentColor} stopOpacity="0.2" />
              </linearGradient>
            </defs>
            <g>
              {/* Building-like structures */}
              <rect x="100" y="200" width="80" height="250" fill={mainColor} opacity="0.1" />
              <rect x="200" y="150" width="100" height="300" fill={accentColor} opacity="0.15" />
              <rect x="320" y="180" width="90" height="270" fill={mainColor} opacity="0.1" />
              <rect x="430" y="100" width="120" height="350" fill={accentColor} opacity="0.15" />
              <rect x="570" y="170" width="80" height="280" fill={mainColor} opacity="0.1" />
              <rect x="670" y="120" width="110" height="330" fill={accentColor} opacity="0.12" />
              <rect x="800" y="200" width="90" height="250" fill={mainColor} opacity="0.1" />
              
              {/* Connection lines representing business network */}
              <path d="M100,350 Q300,100 500,350 T900,350" 
                    fill="none" stroke={mainColor} strokeWidth="2" opacity="0.2" />
              <path d="M50,400 Q250,150 450,400 T850,400" 
                    fill="none" stroke={accentColor} strokeWidth="3" opacity="0.15" />
                    
              <circle cx="200" cy="300" r="15" fill={mainColor} opacity="0.3" />
              <circle cx="430" cy="280" r="20" fill={accentColor} opacity="0.25" />
              <circle cx="670" cy="320" r="18" fill={mainColor} opacity="0.3" />
            </g>
          </svg>
        );
        
      case 'consumidores':
        return (
          <svg width="100%" height="100%" viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid slice">
            <defs>
              <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor={mainColor} stopOpacity="0.4" />
                <stop offset="100%" stopColor={accentColor} stopOpacity="0.2" />
              </linearGradient>
            </defs>
            <g>
              {/* Shield shape for consumer protection */}
              <path d="M500,100 L650,150 Q700,300 650,450 T500,550 T350,450 T300,150 Z" 
                    fill="url(#grad3)" opacity="0.15" />
              <path d="M500,120 L630,165 Q670,300 630,430 T500,520 T370,430 T330,165 Z" 
                    fill="none" stroke={mainColor} strokeWidth="2" opacity="0.2" />
                    
              {/* People silhouettes */}
              <circle cx="350" cy="250" r="30" fill={mainColor} opacity="0.2" />
              <rect x="325" y="280" width="50" height="80" rx="20" fill={mainColor} opacity="0.2" />
              
              <circle cx="450" cy="270" r="25" fill={accentColor} opacity="0.2" />
              <rect x="430" y="295" width="40" height="70" rx="15" fill={accentColor} opacity="0.2" />
              
              <circle cx="540" cy="260" r="28" fill={mainColor} opacity="0.2" />
              <rect x="517" y="288" width="46" height="75" rx="18" fill={mainColor} opacity="0.2" />
              
              <path d="M100,400 Q350,200 600,400 T900,450" 
                    fill="none" stroke={accentColor} strokeWidth="3" opacity="0.15" />
            </g>
          </svg>
        );
        
      case 'privacy':
      case 'termos':
        return (
          <svg width="100%" height="100%" viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid slice">
            <defs>
              <linearGradient id="grad4" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor={mainColor} stopOpacity="0.3" />
                <stop offset="100%" stopColor={accentColor} stopOpacity="0.1" />
              </linearGradient>
            </defs>
            <g>
              {/* Document-like patterns */}
              <rect x="300" y="150" width="400" height="300" rx="10" fill={lightColor} opacity="0.1" />
              <rect x="330" y="180" width="340" height="20" rx="4" fill={mainColor} opacity="0.2" />
              <rect x="330" y="220" width="340" height="10" rx="2" fill={mainColor} opacity="0.15" />
              <rect x="330" y="240" width="260" height="10" rx="2" fill={mainColor} opacity="0.15" />
              <rect x="330" y="260" width="300" height="10" rx="2" fill={mainColor} opacity="0.15" />
              <rect x="330" y="280" width="320" height="10" rx="2" fill={mainColor} opacity="0.15" />
              <rect x="330" y="300" width="280" height="10" rx="2" fill={mainColor} opacity="0.15" />
              <rect x="330" y="320" width="310" height="10" rx="2" fill={mainColor} opacity="0.15" />
              <rect x="330" y="340" width="290" height="10" rx="2" fill={mainColor} opacity="0.15" />
              <rect x="330" y="360" width="340" height="10" rx="2" fill={mainColor} opacity="0.15" />
              <rect x="330" y="380" width="250" height="10" rx="2" fill={mainColor} opacity="0.15" />
              <rect x="330" y="400" width="320" height="10" rx="2" fill={mainColor} opacity="0.15" />
              
              {/* Lock icon for privacy/terms */}
              <rect x="620" y="350" width="50" height="40" rx="5" fill={accentColor} opacity="0.3" />
              <rect x="630" y="320" width="30" height="30" rx="15" fill={accentColor} opacity="0.3" />
            </g>
          </svg>
        );
      
      case 'about':
      case 'sobre':
        return (
          <svg width="100%" height="100%" viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid slice">
            <defs>
              <linearGradient id="grad5" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor={mainColor} stopOpacity="0.4" />
                <stop offset="100%" stopColor={accentColor} stopOpacity="0.2" />
              </linearGradient>
            </defs>
            <g>
              {/* Abstract company/team representation */}
              <circle cx="500" cy="250" r="120" fill="url(#grad5)" opacity="0.2" />
              <circle cx="500" cy="250" r="90" fill="none" stroke={mainColor} strokeWidth="2" opacity="0.3" />
              
              {/* Connection lines */}
              <path d="M320,180 L680,320" stroke={accentColor} strokeWidth="2" opacity="0.2" />
              <path d="M320,320 L680,180" stroke={accentColor} strokeWidth="2" opacity="0.2" />
              <path d="M500,130 L500,370" stroke={accentColor} strokeWidth="2" opacity="0.2" />
              <path d="M380,250 L620,250" stroke={accentColor} strokeWidth="2" opacity="0.2" />
              
              {/* People abstractions around the circle */}
              <circle cx="380" cy="180" r="20" fill={mainColor} opacity="0.3" />
              <circle cx="620" cy="180" r="20" fill={mainColor} opacity="0.3" />
              <circle cx="380" cy="320" r="20" fill={mainColor} opacity="0.3" />
              <circle cx="620" cy="320" r="20" fill={mainColor} opacity="0.3" />
            </g>
          </svg>
        );
      
      // Default pattern
      default:
        return (
          <svg width="100%" height="100%" viewBox="0 0 1000 600" preserveAspectRatio="xMidYMid slice">
            <defs>
              <linearGradient id="grad6" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor={mainColor} stopOpacity="0.5" />
                <stop offset="100%" stopColor={accentColor} stopOpacity="0.2" />
              </linearGradient>
            </defs>
            <g>
              <circle cx="500" cy="300" r="150" fill="url(#grad6)" opacity="0.2" />
              <path d="M100,200 Q350,50 600,200 T900,300" 
                   fill="none" stroke={mainColor} strokeWidth="3" opacity="0.2" />
              <path d="M100,300 Q350,150 600,300 T900,400" 
                   fill="none" stroke={accentColor} strokeWidth="2" opacity="0.15" />
              <path d="M100,400 Q350,250 600,400 T900,500" 
                   fill="none" stroke={mainColor} strokeWidth="3" opacity="0.1" />
              <circle cx="350" cy="300" r="30" fill={mainColor} opacity="0.2" />
              <circle cx="650" cy="300" r="25" fill={accentColor} opacity="0.2" />
            </g>
          </svg>
        );
    }
  };
  
  return (
    <div className={`hero-image-container ${className}`}>
      {generatePattern()}
      <div className="hero-overlay"></div>
    </div>
  );
};

export default HeroImage;
