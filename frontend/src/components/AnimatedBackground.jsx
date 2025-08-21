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
      },
      black: {
        light: ['rgba(0, 0, 0, 0.3)', 'rgba(0, 0, 0, 0.1)'],
        dark: ['rgba(255, 255, 255, 0.3)', 'rgba(255, 255, 255, 0.1)'],
        original: ['rgba(0, 0, 0, 0.5)', 'rgba(0, 0, 0, 0.1)'],
        normal: ['rgba(0, 0, 0, 0.5)', 'rgba(0, 0, 0, 0.1)']
      },
      white: {
        light: ['rgba(0, 0, 0, 0.3)', 'rgba(0, 0, 0, 0.1)'],
        dark: ['rgba(0, 0, 0, 0.3)', 'rgba(0, 0, 0, 0.1)'],
        original: ['rgba(255, 255, 255, 0.5)', 'rgba(255, 255, 255, 0.1)'],
        normal: ['rgba(0, 0, 0, 0.3)', 'rgba(0, 0, 0, 0.1)']
      },
      red: {
        light: ['rgba(239, 68, 68, 0.5)', 'rgba(239, 68, 68, 0.1)'],
        dark: ['rgba(248, 113, 113, 0.5)', 'rgba(248, 113, 113, 0.1)'],
        original: ['rgba(239, 68, 68, 0.5)', 'rgba(239, 68, 68, 0.1)'],
        normal: ['rgba(239, 68, 68, 0.5)', 'rgba(239, 68, 68, 0.1)']
      },
      gray: {
        light: ['rgba(107, 114, 128, 0.5)', 'rgba(107, 114, 128, 0.1)'],
        dark: ['rgba(156, 163, 175, 0.5)', 'rgba(156, 163, 175, 0.1)'],
        original: ['rgba(107, 114, 128, 0.5)', 'rgba(107, 114, 128, 0.1)'],
        normal: ['rgba(107, 114, 128, 0.5)', 'rgba(107, 114, 128, 0.1)']
      },
      matrix: {
        light: ['rgba(0, 255, 0, 0.5)', 'rgba(0, 255, 0, 0.1)'],
        dark: ['rgba(0, 255, 0, 0.7)', 'rgba(0, 255, 0, 0.2)'],
        original: ['rgba(0, 255, 0, 0.8)', 'rgba(0, 255, 0, 0.2)'],
        normal: ['rgba(0, 255, 0, 0.6)', 'rgba(0, 255, 0, 0.1)']
      },
      waves: {
        light: ['rgba(34, 197, 94, 0.4)', 'rgba(59, 130, 246, 0.1)'],
        dark: ['rgba(34, 197, 94, 0.6)', 'rgba(59, 130, 246, 0.2)'],
        original: ['rgba(34, 197, 94, 0.5)', 'rgba(59, 130, 246, 0.2)'],
        normal: ['rgba(34, 197, 94, 0.5)', 'rgba(59, 130, 246, 0.1)']
      },
      particles: {
        light: ['rgba(139, 92, 246, 0.4)', 'rgba(99, 102, 241, 0.1)'],
        dark: ['rgba(139, 92, 246, 0.6)', 'rgba(99, 102, 241, 0.2)'],
        original: ['rgba(139, 92, 246, 0.5)', 'rgba(99, 102, 241, 0.2)'],
        normal: ['rgba(139, 92, 246, 0.5)', 'rgba(99, 102, 241, 0.1)']
      },
      spiral: {
        light: ['rgba(249, 115, 22, 0.4)', 'rgba(249, 115, 22, 0.1)'],
        dark: ['rgba(249, 115, 22, 0.6)', 'rgba(249, 115, 22, 0.2)'],
        original: ['rgba(249, 115, 22, 0.5)', 'rgba(249, 115, 22, 0.2)'],
        normal: ['rgba(249, 115, 22, 0.5)', 'rgba(249, 115, 22, 0.1)']
      },
      pulse: {
        light: ['rgba(239, 68, 68, 0.4)', 'rgba(239, 68, 68, 0.1)'],
        dark: ['rgba(239, 68, 68, 0.6)', 'rgba(239, 68, 68, 0.2)'],
        original: ['rgba(239, 68, 68, 0.5)', 'rgba(239, 68, 68, 0.2)'],
        normal: ['rgba(239, 68, 68, 0.5)', 'rgba(239, 68, 68, 0.1)']
      }
    };
    
    const colors = colorMappings[backgroundColor] || colorMappings.default;
    const themeColors = colors[theme] || colors.normal;
    particleColor = themeColors[0];
    connectionColor = themeColors[1];
    
    // Create particles with different behaviors based on animation type
    const particlesArray = [];
    let numberOfParticles = Math.min(window.innerWidth / 10, 100);
    
    // Adjust particle count based on animation type
    if (backgroundColor === 'matrix') numberOfParticles = Math.min(window.innerWidth / 8, 120);
    if (backgroundColor === 'particles') numberOfParticles = Math.min(window.innerWidth / 6, 150);
    
    class Particle {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 3 + 1;
        this.glow = 0;
        this.glowDirection = Math.random() > 0.5 ? 1 : -1;
        this.angle = Math.random() * Math.PI * 2;
        this.pulsePhase = Math.random() * Math.PI * 2;
        
        // Animation-specific properties
        switch(backgroundColor) {
          case 'matrix':
            this.speedX = 0;
            this.speedY = Math.random() * 2 + 1;
            this.char = String.fromCharCode(0x30A0 + Math.random() * 96);
            break;
          case 'waves':
            this.speedX = Math.random() * 0.5 - 0.25;
            this.speedY = Math.random() * 0.5 - 0.25;
            this.amplitude = Math.random() * 50 + 20;
            this.frequency = Math.random() * 0.02 + 0.01;
            break;
          case 'particles':
            this.speedX = Math.random() * 2 - 1;
            this.speedY = Math.random() * 2 - 1;
            this.life = 1;
            this.decay = Math.random() * 0.02 + 0.01;
            break;
          case 'spiral':
            this.distance = Math.random() * 200 + 50;
            this.angleSpeed = Math.random() * 0.02 + 0.01;
            this.centerX = canvas.width / 2;
            this.centerY = canvas.height / 2;
            break;
          case 'pulse':
            this.speedX = Math.random() * 0.3 - 0.15;
            this.speedY = Math.random() * 0.3 - 0.15;
            this.pulseSpeed = Math.random() * 0.1 + 0.05;
            break;
          default:
            this.speedX = Math.random() * 1 - 0.5;
            this.speedY = Math.random() * 1 - 0.5;
        }
      }
      
      update() {
        switch(backgroundColor) {
          case 'matrix':
            this.y += this.speedY;
            if (this.y > canvas.height) {
              this.y = -this.size;
              this.x = Math.random() * canvas.width;
            }
            break;
            
          case 'waves':
            this.x += this.speedX;
            this.y += this.speedY + Math.sin(this.x * this.frequency) * this.amplitude * 0.01;
            if (this.x > canvas.width || this.x < 0) this.speedX = -this.speedX;
            if (this.y > canvas.height || this.y < 0) this.speedY = -this.speedY;
            break;
            
          case 'particles':
            this.x += this.speedX;
            this.y += this.speedY;
            this.life -= this.decay;
            if (this.life <= 0) {
              this.x = Math.random() * canvas.width;
              this.y = Math.random() * canvas.height;
              this.life = 1;
              this.speedX = Math.random() * 2 - 1;
              this.speedY = Math.random() * 2 - 1;
            }
            break;
            
          case 'spiral':
            this.angle += this.angleSpeed;
            this.x = this.centerX + Math.cos(this.angle) * this.distance;
            this.y = this.centerY + Math.sin(this.angle) * this.distance;
            break;
            
          case 'pulse':
            this.x += this.speedX;
            this.y += this.speedY;
            this.pulsePhase += this.pulseSpeed;
            this.size = (Math.sin(this.pulsePhase) * 2 + 3);
            if (this.x > canvas.width || this.x < 0) this.speedX = -this.speedX;
            if (this.y > canvas.height || this.y < 0) this.speedY = -this.speedY;
            break;
            
          default:
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x > canvas.width || this.x < 0) this.speedX = -this.speedX;
            if (this.y > canvas.height || this.y < 0) this.speedY = -this.speedY;
        }
        
        // Pulsate glow
        this.glow += 0.02 * this.glowDirection;
        if (this.glow > 1 || this.glow < 0) {
          this.glowDirection *= -1;
        }
      }
      
      draw() {
        // Special drawing for matrix animation
        if (backgroundColor === 'matrix') {
          ctx.fillStyle = particleColor;
          ctx.font = `${this.size * 4}px monospace`;
          ctx.fillText(this.char, this.x, this.y);
          return;
        }
        
        // Special drawing for particles animation with opacity
        if (backgroundColor === 'particles') {
          ctx.globalAlpha = this.life;
        }
        
        // Draw particle with glow
        ctx.beginPath();
        const gradient = ctx.createRadialGradient(
          this.x, this.y, 0, 
          this.x, this.y, this.size * 3
        );
        gradient.addColorStop(0, particleColor);
        gradient.addColorStop(1, 'transparent');
        
        ctx.fillStyle = gradient;
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        
        // Reset global alpha for particles animation
        if (backgroundColor === 'particles') {
          ctx.globalAlpha = 1;
        }
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
  }, [theme, backgroundColor, backgroundType]);
  
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
