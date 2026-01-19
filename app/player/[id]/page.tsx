'use client';

import { use, useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { getSongById, getAlbumById, getArtist } from '@/lib/data';
import MusicPlayer from '@/components/MusicPlayer';
import AnimatedAlbumCover from '@/components/AnimatedAlbumCover';
import TwinklingStarsOverlay from '@/components/TwinklingStarsOverlay';
import BlurAnimation from '@/components/BlurAnimation';
import { notFound } from 'next/navigation';

interface PlayerPageProps {
  params: Promise<{ id: string }>;
}

/**
 * Music Player Page - Now Playing Screen
 * 
 * Pixel-perfect recreation of the Figma design showing:
 * - Top section with dismiss icon and "Novel tea" text
 * - Large middle content area for album art
 * - Bottom section with song info, progress bar, and playback controls
 * - Bottom gesture bar matching home page exactly
 * 
 * Route: /player/[id]
 */
export default function PlayerPage({ params }: PlayerPageProps) {
  const router = useRouter();
  const { id } = use(params);
  const song = getSongById(id);

  // If song not found, show 404
  if (!song) {
    notFound();
  }

  const album = getAlbumById(song.albumId);


  // Audio playback state
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(song.duration);
  const audioRef = useRef<HTMLAudioElement>(null);
  
  // UI visibility toggle state
  const [isUIVisible, setIsUIVisible] = useState(true);
  
  const playerRef = useRef<HTMLDivElement>(null);
  const specialOneBackgroundRef = useRef<HTMLDivElement>(null);

  // Initialize audio element
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleLoadedMetadata = () => {
      const audioDuration = audio.duration;
      if (audioDuration && !isNaN(audioDuration) && audioDuration > 0) {
        setDuration(audioDuration);
      } else {
        setDuration(song.duration);
      }
    };

    const handleTimeUpdate = () => {
      setCurrentTime(audio.currentTime);
    };

    const handleEnded = () => {
      setIsPlaying(false);
      setCurrentTime(0);
    };

    setDuration(song.duration);

    audio.addEventListener('loadedmetadata', handleLoadedMetadata);
    audio.addEventListener('timeupdate', handleTimeUpdate);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
      audio.removeEventListener('timeupdate', handleTimeUpdate);
      audio.removeEventListener('ended', handleEnded);
    };
  }, [song.audioUrl, song.duration]);

  // Handle play/pause
  const togglePlayPause = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
    } else {
      audio.play().catch((error) => {
        console.error('Error playing audio:', error);
      });
      setIsPlaying(true);
    }
  };

  // Format time from seconds to MM:SS
  const formatTime = (seconds: number): string => {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Calculate progress percentage
  const progressPercentage = duration > 0 ? (currentTime / duration) * 100 : 0;
  const remainingTime = Math.max(0, duration - currentTime);

  // Handle dismiss - navigate to home screen
  const handleDismiss = () => {
    if (audioRef.current) {
      audioRef.current.pause();
    }
    // Navigate back to home
    router.replace('/');
  };
  
  // Toggle UI visibility
  const toggleUIVisibility = () => {
    setIsUIVisible(!isUIVisible);
  };

  // Get list of songs from artist's popular songs
  const artist = getArtist();
  const songList = artist.popularSongs;
  const currentIndex = songList.findIndex(s => s.id === song.id);

  // Handle previous song
  const handlePrevious = () => {
    if (currentIndex > 0) {
      const previousSong = songList[currentIndex - 1];
      // Stop current audio
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
      setIsPlaying(false);
      // Navigate to previous song
      router.push(`/player/${previousSong.id}`);
    }
  };

  // Handle next song
  const handleNext = () => {
    if (currentIndex < songList.length - 1) {
      const nextSong = songList[currentIndex + 1];
      // Stop current audio
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0;
      }
      setIsPlaying(false);
      // Navigate to next song
      router.push(`/player/${nextSong.id}`);
    }
  };

  return (
    <div className="fixed inset-0 z-40">
      {/* Backdrop overlay - not needed for full-screen page */}
      
      {/* Player page - full screen */}
      <div 
        ref={playerRef}
        className={`fixed inset-0 z-50 w-full max-w-[375px] mx-auto overflow-x-hidden ${
          song.id === 'song-1' ? '' : 'bg-[#111]'
        }`}
        style={{
          position: 'relative', // Ensure background layers can position relative to this
        }}
      >
      {/* Background Layer for Special One (song-1) */}
      {/* Full-screen background using special-one-all.png - shifted 100px right to show hand */}
      {song.id === 'song-1' && (
        <>
          <div 
            ref={specialOneBackgroundRef}
            className="absolute inset-0 w-full h-full"
            style={{
              backgroundImage: 'url(/images/special-one-layers/special-one-all.png)',
              backgroundSize: 'cover',
              backgroundPosition: 'calc(50% + 50px) center',
              backgroundRepeat: 'no-repeat',
              zIndex: 0,
              pointerEvents: 'none',
            }}
          />
          {/* Blur Animation - 7 second looping blur in/out */}
          <BlurAnimation 
            targetRef={specialOneBackgroundRef} 
            blurAmount={4} 
            loopDuration={7} 
            autoStart={true} 
          />
          {/* Noise/Grain Animation Overlay - 7 second looping animation */}
          <div 
            className="absolute inset-0 w-full h-full special-one-noise-overlay"
            style={{
              zIndex: 1,
              pointerEvents: 'none',
            }}
          />
        </>
      )}
      
      {/* Top Section - Close Icon and Title */}
      {isUIVisible && (
      <div className="absolute flex items-center justify-between left-0 top-0 w-full pt-[50px] px-[16px] pb-[16px] z-10">
        {/* Close Icon (X) */}
        <button
          onClick={handleDismiss}
          className="relative shrink-0 w-[24px] h-[24px] flex items-center justify-center"
          aria-label="Close"
        >
          <svg 
            width="24" 
            height="24" 
            viewBox="0 0 24 24" 
            fill="none" 
            xmlns="http://www.w3.org/2000/svg"
            className="text-white"
          >
            <path 
              d="M18 6L6 18M6 6L18 18" 
              stroke="currentColor" 
              strokeWidth="2" 
              strokeLinecap="round" 
              strokeLinejoin="round"
            />
          </svg>
        </button>

        {/* Novel tea Text - Centered */}
        <p 
          className="absolute left-1/2 -translate-x-1/2 text-white text-[18px] font-medium leading-[22px]"
          style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
        >
          Novel tea
        </p>

        {/* Spacer to balance the layout */}
        <div className="w-[24px]" />
      </div>
      )}

      {/* Middle Content Area - Album Art Space */}
      {song.id === 'song-6' ? (
        /* Dream Song V2 - Full screen centered, clipped to viewport (same as Special One) */
        <div className="absolute inset-0 w-full h-full flex items-center justify-center z-0 overflow-hidden relative">
          <AnimatedAlbumCover isPlaying={isPlaying} svgPath="/assets/novel-tea-final-v2.svg" fullScreen={true} />
          {/* Twinkling Stars Overlay - Gentle ambient animation */}
          <TwinklingStarsOverlay starCount={30} starSize={3} loopDuration={7} />
        </div>
      ) : (
        /* This fills the space between top section and bottom controls for other songs */
        <div className="absolute left-0 top-[100px] right-0 bottom-[400px] w-full flex items-center justify-center z-10">
          {/* Show SVG art for Dream Song (song-2) */}
          {song.id === 'song-2' ? (
            <div className="relative w-full flex items-center justify-center px-4" style={{ maxWidth: '375px' }}>
              <AnimatedAlbumCover isPlaying={isPlaying} svgPath="/assets/novel-tea-final.svg" />
            </div>
          ) : (
            // Placeholder for other songs - each will have their own unique asset
            <div className="relative w-full flex items-center justify-center px-4" style={{ maxWidth: '375px' }}>
              <div className="w-full h-full flex items-center justify-center bg-gray-800 rounded-lg">
                {/* Placeholder - will be replaced with unique asset for each song */}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Bottom Section - Song Info and Controls */}
      {/* Positioned above the gesture bar with proper spacing */}
      {isUIVisible && (
      <div className="fixed bottom-[60px] left-1/2 -translate-x-1/2 w-full max-w-[375px] px-[16px] z-10">
        {/* Song Title */}
        <p 
          className="text-white text-[24px] font-bold mb-0 leading-[28px]"
          style={{ fontFamily: 'SF Pro Display, -apple-system, BlinkMacSystemFont, sans-serif' }}
        >
          {song.title}
        </p>

        {/* Artist Name and Plus Icon Row */}
        <div className="flex items-center justify-between mb-[16px]">
          <p 
            className="text-white text-[16px] opacity-90 leading-[20px]"
            style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
          >
            {album?.artist || 'Artist'}
          </p>
          
          {/* Plus Icon in Circle */}
          <button
            className="relative shrink-0 w-[32px] h-[32px] flex items-center justify-center opacity-90"
            aria-label="Add to playlist"
          >
            <Image 
              src="/icons/plus-icon.svg" 
              alt="Add" 
              width={24} 
              height={24} 
              className="w-full h-full" 
            />
          </button>
        </div>

        {/* Progress Bar Section */}
        <div className="mb-[24px]">
          {/* Progress Bar */}
          <div className="relative w-full h-[4px] bg-white/30 rounded-full mb-[6px]">
            <div 
              className="absolute left-0 top-0 h-full bg-white rounded-full transition-all"
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
          
          {/* Timestamps */}
          <div className="flex justify-between">
            <span 
              className="text-white text-[12px] opacity-70 leading-[14px]"
              style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
            >
              {formatTime(currentTime)}
            </span>
            <span 
              className="text-white text-[12px] opacity-70 leading-[14px]"
              style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
            >
              -{formatTime(remainingTime)}
            </span>
          </div>
        </div>

        {/* Main Playback Controls */}
        <div className="flex items-center justify-between mb-[24px]">
          {/* Shuffle */}
          <button
            className="relative shrink-0 w-[24px] h-[24px] opacity-70"
            aria-label="Shuffle"
          >
            <Image 
              src="/icons/shuffle-icon.svg" 
              alt="Shuffle" 
              width={24} 
              height={24} 
              className="w-full h-full" 
            />
          </button>

          {/* Previous */}
          <button
            onClick={handlePrevious}
            disabled={currentIndex === 0}
            className={`relative shrink-0 w-[36px] h-[36px] transition-opacity ${
              currentIndex === 0 ? 'opacity-30 cursor-not-allowed' : 'hover:opacity-80'
            }`}
            aria-label="Previous"
          >
            <Image 
              src="/icons/previous-icon.svg" 
              alt="Previous" 
              width={36} 
              height={36} 
              className="w-full h-full" 
            />
          </button>

          {/* Play/Pause Button (Center, Larger) */}
          <button
            onClick={togglePlayPause}
            className="relative shrink-0 w-[64px] h-[64px] rounded-full bg-white flex items-center justify-center shadow-lg"
            aria-label={isPlaying ? 'Pause' : 'Play'}
          >
            <div className="w-[32px] h-[32px] flex items-center justify-center">
              {isPlaying ? (
                // Pause icon
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="6" y="4" width="4" height="16" fill="black"/>
                  <rect x="14" y="4" width="4" height="16" fill="black"/>
                </svg>
              ) : (
                // Play icon
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M8 5v14l11-7z" fill="black"/>
                </svg>
              )}
            </div>
          </button>

          {/* Next */}
          <button
            onClick={handleNext}
            disabled={currentIndex === songList.length - 1}
            className={`relative shrink-0 w-[36px] h-[36px] transition-opacity ${
              currentIndex === songList.length - 1 ? 'opacity-30 cursor-not-allowed' : 'hover:opacity-80'
            }`}
            aria-label="Next"
          >
            <Image 
              src="/icons/next-icon.svg" 
              alt="Next" 
              width={36} 
              height={36} 
              className="w-full h-full" 
            />
          </button>

          {/* More Options */}
          <button
            className="relative shrink-0 w-[24px] h-[24px] opacity-70"
            aria-label="More options"
          >
            <Image 
              src="/icons/more-options-icon.svg" 
              alt="More options" 
              width={24} 
              height={24} 
              className="w-full h-full" 
            />
          </button>
        </div>

        {/* Utility Icons Row */}
        <div className="flex items-center justify-between px-[60px]">
          {/* Bluetooth Icon */}
          <button
            className="relative shrink-0 w-[24px] h-[24px]"
            aria-label="Connect to Bluetooth"
          >
            <Image 
              src="/icons/speaker-icon.svg" 
              alt="Bluetooth" 
              width={24} 
              height={24} 
              className="w-full h-full" 
            />
          </button>

          {/* Share Icon */}
          <button
            className="relative shrink-0 w-[24px] h-[24px]"
            aria-label="Share"
          >
            <Image 
              src="/icons/share-icon.svg" 
              alt="Share" 
              width={24} 
              height={24} 
              className="w-full h-full" 
            />
          </button>
        </div>
      </div>
      )}

      {/* Eye Icon - Always visible, centered */}
      <div className="fixed bottom-[52px] left-1/2 -translate-x-1/2 z-50 w-full max-w-[375px] flex justify-center px-[16px] pointer-events-none">
        <button
          onClick={toggleUIVisibility}
          className={`relative shrink-0 w-[32px] h-[32px] pointer-events-auto flex items-center justify-center ${isUIVisible ? 'opacity-100' : 'opacity-10'}`}
          aria-label="Toggle UI visibility"
          style={{ backgroundColor: 'rgba(255, 255, 255, 0.1)', borderRadius: '50%' }}
        >
          {/* Simple eye icon using SVG */}
          <svg 
            width="24" 
            height="24" 
            viewBox="0 0 24 24" 
            fill="none" 
            xmlns="http://www.w3.org/2000/svg"
            className="text-white"
          >
            {isUIVisible ? (
              // Eye slash (hide)
              <>
                <path d="M3 3L21 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                <path d="M10.5 10.677a2 2 0 002.823 2.823" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                <path d="M7.362 7.561C5.68 8.74 4.279 10.42 3 12c1.889 2.991 5.282 6 9 6 1.55 0 3.043-.523 4.395-1.35M12 6c3.6 0 6.991 2.807 9 6a15.7 15.7 0 01-2.808 3.374" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </>
            ) : (
              // Eye (show)
              <>
                <path d="M12 5C7.5 5 3.73 7.61 1 12c2.73 4.39 6.5 7 11 7s8.27-2.61 11-7c-2.73-4.39-6.5-7-11-7z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/>
              </>
            )}
          </svg>
        </button>
      </div>

      {/* Home Indicator - Fixed to bottom (EXACTLY matching home page) */}
      <div className="fixed bottom-0 flex flex-col items-center justify-center left-1/2 -translate-x-1/2 pb-[9px] pt-[20px] px-[120px] w-full max-w-[375px]">
        <div className="bg-white h-[5px] rounded-[5px] shrink-0 w-[134px]" />
      </div>

      {/* Hidden audio element */}
      <audio 
        ref={audioRef} 
        src={song.audioUrl} 
        preload="metadata"
      />
      </div>
    </div>
  );
}
