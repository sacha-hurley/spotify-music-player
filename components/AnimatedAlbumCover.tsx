'use client';

import Image from 'next/image';

interface AnimatedAlbumCoverProps {
  isPlaying?: boolean; // Kept for compatibility but not used
  svgPath?: string; // Optional SVG path, defaults to original
  fullScreen?: boolean; // If true, makes the image fill the viewport
}

/**
 * Album Cover Component
 * 
 * Displays the static SVG album cover image.
 */
export default function AnimatedAlbumCover({ isPlaying, svgPath = '/assets/novel-tea-final.svg', fullScreen = false }: AnimatedAlbumCoverProps) {
  return (
    <div 
      className="relative flex items-center justify-center"
      style={{ 
        width: fullScreen ? '100%' : '100%',
        height: fullScreen ? '100%' : 'auto',
        maxWidth: '100%',
        maxHeight: fullScreen ? '100%' : 'none',
        overflow: fullScreen ? 'hidden' : 'visible'
      }}
    >
      {/* The Album Cover Image */}
      <Image
        src={svgPath}
        alt="Novel tea Album Cover"
        width={864}
        height={864}
        className={fullScreen ? "w-full h-full object-cover block" : "w-full h-auto object-contain block"}
        loading="eager"
        priority
        style={{
          width: fullScreen ? '100%' : undefined,
          height: fullScreen ? '100%' : undefined,
          maxWidth: '100%',
          maxHeight: fullScreen ? '100%' : 'none',
          objectFit: fullScreen ? 'cover' : 'contain',
          objectPosition: fullScreen ? 'center' : 'center',
          transform: fullScreen ? 'scale(1.12)' : 'none'
        }}
      />
    </div>
  );
}
