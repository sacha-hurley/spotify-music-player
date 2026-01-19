'use client';

import { useEffect, useRef } from 'react';
import gsap from 'gsap';

/**
 * Blur Animation Component
 * 
 * Creates a smooth, looping blur animation effect.
 * Perfect for ambient, dreamy visual effects.
 * 
 * HOW IT WORKS:
 * 1. Animates the CSS filter blur property
 * 2. Smoothly transitions from sharp → blurry → sharp
 * 3. Loops seamlessly over the specified duration
 * 
 * FEATURES:
 * - Smooth blur in and blur out
 * - Seamless looping
 * - Starts immediately on page load
 */
interface BlurAnimationProps {
  /**
   * Target element reference to apply blur to
   * If not provided, will apply to the component's container
   */
  targetRef?: React.RefObject<HTMLElement | null>;
  
  /**
   * Maximum blur amount in pixels
   * Higher = more blurry
   */
  blurAmount?: number;
  
  /**
   * Duration of the complete loop in seconds
   */
  loopDuration?: number;
  
  /**
   * Whether to start animation immediately
   */
  autoStart?: boolean;
}

export default function BlurAnimation({ 
  targetRef,
  blurAmount = 4,
  loopDuration = 7,
  autoStart = true
}: BlurAnimationProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const timelineRef = useRef<gsap.core.Timeline | null>(null);

  useEffect(() => {
    // Determine which element to animate
    // Use targetRef if provided, otherwise use containerRef
    const targetElement = targetRef?.current || containerRef.current;
    
    if (!targetElement) return;

    // Create GSAP timeline for seamless looping
    const timeline = gsap.timeline({
      repeat: -1, // Loop forever
      paused: !autoStart // Start immediately if autoStart is true
    });

    // Calculate timing for equal in/out
    // Half the duration for blur in, half for blur out
    const blurInDuration = loopDuration / 2; // 3.5 seconds
    const blurOutDuration = loopDuration / 2; // 3.5 seconds

    // Set initial state (sharp, no blur)
    timeline.set(targetElement, {
      filter: 'blur(0px)',
      willChange: 'filter' // Optimize for animation
    }, 0);

    // Blur in animation (0s → 3.5s)
    // Smoothly transition from sharp to blurry
    timeline.to(targetElement, {
      filter: `blur(${blurAmount}px)`,
      duration: blurInDuration,
      ease: 'sine.inOut' // Smooth, organic easing
    }, 0);

    // Blur out animation (3.5s → 7s)
    // Smoothly transition from blurry back to sharp
    timeline.to(targetElement, {
      filter: 'blur(0px)',
      duration: blurOutDuration,
      ease: 'sine.inOut' // Smooth, organic easing
    }, blurInDuration);

    timelineRef.current = timeline;

    // Cleanup function
    return () => {
      if (timelineRef.current) {
        timelineRef.current.kill();
      }
      // Reset blur on cleanup
      if (targetElement) {
        gsap.set(targetElement, { filter: 'blur(0px)' });
      }
    };
  }, [targetRef, blurAmount, loopDuration, autoStart]);

  // If targetRef is provided, we don't need to render a container
  // The animation will be applied directly to the referenced element
  if (targetRef) {
    return null;
  }

  // Otherwise, render a container that will be animated
  return (
    <div 
      ref={containerRef}
      className="absolute inset-0 pointer-events-none"
      style={{
        zIndex: 1
      }}
    />
  );
}
