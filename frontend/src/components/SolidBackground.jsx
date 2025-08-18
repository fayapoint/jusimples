import React from 'react';
import { useBackground } from '../context/BackgroundContext';
import { useTheme } from '../context/ThemeContext';

export default function SolidBackground() {
  const { backgroundType, backgroundColor } = useBackground();
  const { theme } = useTheme();

  // Don't render if background type is not solid
  if (backgroundType !== 'solid') {
    return null;
  }

  // Define solid background colors based on background color and theme
  const getBackgroundStyle = () => {
    const colorMappings = {
      default: {
        light: 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
        dark: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
        original: 'linear-gradient(135deg, #020024 0%, #090979 35%, #00b8ff 100%)',
        normal: 'linear-gradient(135deg, #111827 0%, #1f2937 100%)'
      },
      purple: {
        light: 'linear-gradient(135deg, #faf5ff 0%, #e9d5ff 100%)',
        dark: 'linear-gradient(135deg, #2e1065 0%, #581c87 100%)',
        original: 'linear-gradient(135deg, #2e1065 0%, #581c87 35%, #7c3aed 100%)',
        normal: 'linear-gradient(135deg, #581c87 0%, #7c3aed 100%)'
      },
      blue: {
        light: 'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)',
        dark: 'linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%)',
        original: 'linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 35%, #3b82f6 100%)',
        normal: 'linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%)'
      },
      green: {
        light: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
        dark: 'linear-gradient(135deg, #14532d 0%, #166534 100%)',
        original: 'linear-gradient(135deg, #14532d 0%, #166534 35%, #22c55e 100%)',
        normal: 'linear-gradient(135deg, #166534 0%, #22c55e 100%)'
      },
      orange: {
        light: 'linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%)',
        dark: 'linear-gradient(135deg, #9a3412 0%, #c2410c 100%)',
        original: 'linear-gradient(135deg, #9a3412 0%, #c2410c 35%, #f97316 100%)',
        normal: 'linear-gradient(135deg, #c2410c 0%, #f97316 100%)'
      }
    };

    const colors = colorMappings[backgroundColor] || colorMappings.default;
    return colors[theme] || colors.normal;
  };

  return (
    <div 
      className="solid-background"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        background: getBackgroundStyle(),
        pointerEvents: 'none',
        zIndex: -1,
      }}
    />
  );
}
