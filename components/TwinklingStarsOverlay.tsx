'use client';

import { useEffect, useRef } from 'react';
import gsap from 'gsap';

/**
 * Twinkling Stars Overlay Component
 * 
 * Creates a subtle, ambient twinkling star effect over an image.
 * Perfect for Spotify Canvas animations.
 * 
 * HOW IT WORKS:
 * 1. Creates multiple small white star elements positioned randomly
 * 2. Each star has its own independent fade in/out animation
 * 3. Different timing for each star creates organic, natural movement
 * 4. All animations loop seamlessly over 7 seconds
 * 
 * FEATURES:
 * - Small white stars scattered across the image
 * - Each twinkles independently at different rates
 * - Very slow, organic timing (subtle and ambient)
 * - Seamless 7-second loop
 */
interface TwinklingStarsOverlayProps {
  /**
   * Number of stars to create
   * More stars = more twinkling, but can be distracting if too many
   */
  starCount?: number;
  
  /**
   * Size of each star in pixels
   * Keep small for subtle effect
   */
  starSize?: number;
  
  /**
   * Duration of the complete loop in seconds
   */
  loopDuration?: number;
}

export default function TwinklingStarsOverlay({ 
  starCount = 25, 
  starSize = 2,
  loopDuration = 7 
}: TwinklingStarsOverlayProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const starsRef = useRef<HTMLDivElement[]>([]);
  const timelineRef = useRef<gsap.core.Timeline | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Clear any existing stars
    starsRef.current.forEach(star => {
      if (star.parentNode) {
        star.parentNode.removeChild(star);
      }
    });
    starsRef.current = [];

    // Create star elements
    for (let i = 0; i < starCount; i++) {
      const star = document.createElement('div');
      
      // Style the star - small white dot with gentle glow
      star.style.position = 'absolute';
      star.style.width = `${starSize}px`;
      star.style.height = `${starSize}px`;
      star.style.borderRadius = '50%';
      star.style.backgroundColor = 'white';
      
      // Add subtle glow effect for ambient feel
      star.style.boxShadow = `
        0 0 ${starSize * 2}px rgba(255, 255, 255, 0.9),
        0 0 ${starSize * 4}px rgba(255, 255, 255, 0.5)
      `;
      
      // Start invisible (will be animated by GSAP)
      star.style.opacity = '0';
      star.style.transform = 'scale(0.7)';
      star.style.willChange = 'opacity, transform'; // Optimize for animation
      
      // Random position across the container
      // Leave some margin around edges for better distribution
      const margin = 5; // 5% margin on all sides
      const x = margin + Math.random() * (100 - margin * 2);
      const y = margin + Math.random() * (100 - margin * 2);
      star.style.left = `${x}%`;
      star.style.top = `${y}%`;
      
      // Add to container
      containerRef.current.appendChild(star);
      starsRef.current.push(star);
    }

    // Create GSAP timeline for seamless looping
    const timeline = gsap.timeline({
      repeat: -1, // Loop forever
      paused: false // Start immediately
    });

    // Animate each star independently with unique timing
    starsRef.current.forEach((star, index) => {
      // Generate unique timing parameters for each star
      // This creates organic, natural variation
      
      // Random fade-in duration (slow and gentle)
      // Between 2 and 3 seconds for very slow, organic feel
      const fadeInDuration = 2 + Math.random() * 1;
      
      // Random fade-out duration (also slow)
      // Between 2 and 3 seconds
      const fadeOutDuration = 2 + Math.random() * 1;
      
      // Random peak opacity (subtle variation)
      // Between 0.5 and 0.8 for ambient, not too bright
      const peakOpacity = 0.5 + Math.random() * 0.3;
      
      // Random hold time at peak (how long star stays bright)
      // Between 0.2 and 0.8 seconds - keeps it subtle
      const holdDuration = 0.2 + Math.random() * 0.6;
      
      // Calculate total animation duration
      const totalDuration = fadeInDuration + holdDuration + fadeOutDuration;
      
      // Ensure cycle fits within loop (with some buffer)
      // If too long, scale it down proportionally
      let adjustedFadeIn = fadeInDuration;
      let adjustedHold = holdDuration;
      let adjustedFadeOut = fadeOutDuration;
      
      if (totalDuration > loopDuration * 0.9) {
        const scale = (loopDuration * 0.9) / totalDuration;
        adjustedFadeIn = fadeInDuration * scale;
        adjustedHold = holdDuration * scale;
        adjustedFadeOut = fadeOutDuration * scale;
      }
      
      // Distribute start times across the loop for continuous twinkling
      // Each star starts at a different phase
      // Add some randomness to make it more organic, but ensure stars are distributed
      const baseStartTime = (index * (loopDuration / starCount)) % loopDuration;
      const randomOffset = (Math.random() - 0.5) * 0.3; // Small random offset
      const startTime = Math.max(0, Math.min(loopDuration - totalDuration, baseStartTime + randomOffset));
      
      // Calculate when fade-out should start
      const fadeOutStart = startTime + adjustedFadeIn + adjustedHold;
      
      // Set initial state (invisible)
      timeline.set(star, {
        opacity: 0,
        scale: 0.7
      }, 0);
      
      // Fade in animation
      timeline.to(star, {
        opacity: peakOpacity,
        scale: 1.3, // Slight scale increase for gentle glow effect
        duration: adjustedFadeIn,
        ease: 'sine.inOut' // Smooth, organic easing
      }, startTime);
      
      // Hold at peak (creates pause at brightest point)
      timeline.to(star, {
        opacity: peakOpacity,
        scale: 1.3,
        duration: adjustedHold,
        ease: 'none'
      }, startTime + adjustedFadeIn);
      
      // Fade out animation
      // Handle wrapping for seamless loop
      if (fadeOutStart + adjustedFadeOut <= loopDuration) {
        // Normal case: fade-out completes within loop
        timeline.to(star, {
          opacity: 0,
          scale: 0.7,
          duration: adjustedFadeOut,
          ease: 'sine.inOut'
        }, fadeOutStart);
      } else {
        // Wrap case: fade-out spans loop boundary
        const fadeOutBeforeWrap = loopDuration - fadeOutStart;
        const fadeOutAfterWrap = adjustedFadeOut - fadeOutBeforeWrap;
        
        // Calculate intermediate opacity/scale at wrap point
        const progressAtWrap = fadeOutBeforeWrap / adjustedFadeOut;
        const opacityAtWrap = peakOpacity * (1 - progressAtWrap);
        const scaleAtWrap = 1.3 - (0.6 * progressAtWrap);
        
        // Fade out before wrap
        timeline.to(star, {
          opacity: opacityAtWrap,
          scale: scaleAtWrap,
          duration: fadeOutBeforeWrap,
          ease: 'sine.inOut'
        }, fadeOutStart);
        
        // Continue fade-out after wrap (at start of loop)
        timeline.to(star, {
          opacity: 0,
          scale: 0.7,
          duration: fadeOutAfterWrap,
          ease: 'sine.inOut'
        }, 0);
      }
    });

    timelineRef.current = timeline;

    // Cleanup function
    return () => {
      // Stop animation
      if (timelineRef.current) {
        timelineRef.current.kill();
      }
      
      // Remove star elements
      starsRef.current.forEach(star => {
        if (star.parentNode) {
          star.parentNode.removeChild(star);
        }
      });
      starsRef.current = [];
    };
  }, [starCount, starSize, loopDuration]);

  return (
    <div 
      ref={containerRef}
      className="absolute inset-0 pointer-events-none"
      style={{
        // Ensure stars appear above the image
        zIndex: 10
      }}
    />
  );
}
