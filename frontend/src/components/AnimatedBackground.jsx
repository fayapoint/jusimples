import React, { useEffect, useRef } from 'react';
import { useTheme } from '../context/ThemeContext';
import { useBackground } from '../context/BackgroundContext';

// Modern animated background component for JuSimples pages
export default function AnimatedBackground() {
  const canvasRef = useRef(null);
  const { theme = 'normal' } = useTheme();
  const { backgroundType, backgroundColor } = useBackground();
  
  useEffect(() => {
    // Don't run animation if background type is not animated
    if (backgroundType !== 'animated') {
      return;
    }
    
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    
    // Set canvas dimensions
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    // Handle window resize
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    
    // Particle configurations based on background color and theme
    let particleColor;
    let connectionColor;
    
    // Color variations based on backgroundColor setting
    const colorMappings = {
      default: {
        light: ['rgba(99, 102, 241, 0.5)', 'rgba(99, 102, 241, 0.1)'],
        dark: ['rgba(139, 92, 246, 0.5)', 'rgba(139, 92, 246, 0.1)'],
        original: ['rgba(0, 184, 255, 0.5)', 'rgba(0, 184, 255, 0.1)'],
        normal: ['rgba(99, 102, 241, 0.5)', 'rgba(99, 102, 241, 0.1)']
      },
      purple: {
        light: ['rgba(147, 51, 234, 0.5)', 'rgba(147, 51, 234, 0.1)'],
        dark: ['rgba(168, 85, 247, 0.5)', 'rgba(168, 85, 247, 0.1)'],
        original: ['rgba(147, 51, 234, 0.5)', 'rgba(147, 51, 234, 0.1)'],
        normal: ['rgba(147, 51, 234, 0.5)', 'rgba(147, 51, 234, 0.1)']
      },
      blue: {
        light: ['rgba(59, 130, 246, 0.5)', 'rgba(59, 130, 246, 0.1)'],
        dark: ['rgba(96, 165, 250, 0.5)', 'rgba(96, 165, 250, 0.1)'],
        original: ['rgba(59, 130, 246, 0.5)', 'rgba(59, 130, 246, 0.1)'],
        normal: ['rgba(59, 130, 246, 0.5)', 'rgba(59, 130, 246, 0.1)']
      },
      green: {
        light: ['rgba(34, 197, 94, 0.5)', 'rgba(34, 197, 94, 0.1)'],
        dark: ['rgba(74, 222, 128, 0.5)', 'rgba(74, 222, 128, 0.1)'],
        original: ['rgba(34, 197, 94, 0.5)', 'rgba(34, 197, 94, 0.1)'],
        normal: ['rgba(34, 197, 94, 0.5)', 'rgba(34, 197, 94, 0.1)']
      },
      orange: {
        light: ['rgba(249, 115, 22, 0.5)', 'rgba(249, 115, 22, 0.1)'],
        dark: ['rgba(251, 146, 60, 0.5)', 'rgba(251, 146, 60, 0.1)'],
        original: ['rgba(249, 115, 22, 0.5)', 'rgba(249, 115, 22, 0.1)'],
        normal: ['rgba(249, 115, 22, 0.5)', 'rgba(249, 115, 22, 0.1)']
      }
    };
    
    const colors = colorMappings[backgroundColor] || colorMappings.default;
    const themeColors = colors[theme] || colors.normal;
    particleColor = themeColors[0];
    connectionColor = themeColors[1];
    
    // Create particles
    const particlesArray = [];
    const numberOfParticles = Math.min(window.innerWidth / 10, 100); // Adjust based on screen size
    
    class Particle {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 3 + 1;
        this.speedX = Math.random() * 1 - 0.5;
        this.speedY = Math.random() * 1 - 0.5;
        this.glow = 0;
        this.glowDirection = Math.random() > 0.5 ? 1 : -1;
      }
      
      update() {
        // Move particles
        this.x += this.speedX;
        this.y += this.speedY;
        
        // Bounce off edges
        if (this.x > canvas.width || this.x < 0) {
          this.speedX = -this.speedX;
        }
        if (this.y > canvas.height || this.y < 0) {
          this.speedY = -this.speedY;
        }
        
        // Pulsate glow
        this.glow += 0.02 * this.glowDirection;
        if (this.glow > 1 || this.glow < 0) {
          this.glowDirection *= -1;
        }
      }
      
      draw() {
        // Draw particle with glow
        ctx.beginPath();
        const gradient = ctx.createRadialGradient(
          this.x, this.y, 0, 
          this.x, this.y, this.size * 3
        );
        gradient.addColorStop(0, particleColor);
        gradient.addColorStop(1, 'transparent');
        
        ctx.fillStyle = gradient;
        ctx.arc(this.x, this.y, this.size * (1 + this.glow), 0, Math.PI * 2);
        ctx.fill();
      }
    }
    
    // Create particles
    const init = () => {
      for (let i = 0; i < numberOfParticles; i++) {
        particlesArray.push(new Particle());
      }
    };
    
    init();
    
    // Connect nearby particles with lines
    const connect = () => {
      const maxDistance = 150;
      
      for (let a = 0; a < particlesArray.length; a++) {
        for (let b = a; b < particlesArray.length; b++) {
          const dx = particlesArray[a].x - particlesArray[b].x;
          const dy = particlesArray[a].y - particlesArray[b].y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < maxDistance) {
            // Draw connection line
            ctx.strokeStyle = connectionColor;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
            ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
            ctx.stroke();
          }
        }
      }
    };
    
    // Animation loop
    const animate = () => {
      // Clear canvas with semi-transparent background for trail effect
      ctx.fillStyle = 'rgba(0, 0, 0, 0.02)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Update and draw particles
      for (let i = 0; i < particlesArray.length; i++) {
        particlesArray[i].update();
        particlesArray[i].draw();
      }
      
      // Connect particles
      connect();
      
      // Continue animation
      animationFrameId = requestAnimationFrame(animate);
    };
    
    animate();
    
    // Cleanup
    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationFrameId);
    };
  }, [theme, backgroundColor]);
  
  // Don't render if background type is not animated
  if (backgroundType !== 'animated') {
    return null;
  }

  return (
    <canvas 
      ref={canvasRef} 
      className="animated-background" 
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        zIndex: -1,
      }}
    />
  );
}
