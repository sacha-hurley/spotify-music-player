'use client';

import { useState } from 'react';
import { getArtist, getFirstSong } from '@/lib/data';
import Image from 'next/image';
import MusicPlayerModal from '@/components/MusicPlayerModal';

/**
 * Homepage Component - Artist Page
 * 
 * Pixel-perfect recreation of the Figma design showing:
 * - Artist header with name and monthly listeners
 * - Following button and options
 * - Shuffle and Play buttons
 * - Popular songs list
 * - Bottom navigation bar
 */
export default function Home() {
  const artistData = getArtist();
  const firstSong = getFirstSong();
  const [selectedSongId, setSelectedSongId] = useState<string | null>(null);
  const [isModalVisible, setIsModalVisible] = useState(false);

  // Format number with commas
  const formatNumber = (num: number): string => {
    return num.toLocaleString('en-US');
  };

  // Handle play button click - open modal with first song
  const handlePlayClick = () => {
    if (firstSong) {
      setSelectedSongId(firstSong.id);
      setIsModalVisible(true);
    }
  };

  // Handle song click - open modal with selected song
  const handleSongClick = (songId: string) => {
    setSelectedSongId(songId);
    setIsModalVisible(true);
  };

  // Handle modal close
  const handleCloseModal = () => {
    setIsModalVisible(false);
    // Small delay to allow fade-out animation to complete
    setTimeout(() => {
      setSelectedSongId(null);
    }, 300);
  };

  // Handle song change in modal (for previous/next buttons)
  const handleSongChange = (songId: string) => {
    setSelectedSongId(songId);
    // Keep modal visible when changing songs
    setIsModalVisible(true);
  };

  return (
    <div className="bg-[#111] relative min-h-screen w-full max-w-[375px] mx-auto overflow-x-hidden">
      {/* Header Image Section - Square container to match SVG 1:1 aspect ratio */}
      <div className="absolute aspect-square left-0 overflow-hidden shadow-[0px_4px_28px_15px_rgba(27,99,229,0.12)] top-0 w-full">
        {/* SVG Background - fills container perfectly with matching aspect ratio */}
        <div className="absolute inset-0 w-full h-full">
          <Image 
            src="/assets/novel-tea-final.svg" 
            alt="" 
            width={375} 
            height={375} 
            className="w-full h-full object-cover"
          />
        </div>
        {/* Shadow overlay */}
        <div className="absolute bg-black blur-[100px] h-[53px] left-0 bottom-0 w-full" />
        {/* Artist Name - Overlaid on SVG */}
        <p 
          className="absolute font-bold leading-[48px] left-[16px] text-[56px] text-nowrap text-white bottom-[61px] tracking-[-2.52px] z-10"
          style={{ fontFamily: 'SF Pro Display, -apple-system, BlinkMacSystemFont, sans-serif' }}
        >
          {artistData.name}
        </p>
      </div>

      {/* Monthly Listeners */}
      <div className="absolute flex gap-[2px] items-start left-[16px] text-[14px] text-nowrap text-white top-[393px]">
        <p className="opacity-50 relative shrink-0 tracking-[0.07px]" style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}>
          {formatNumber(artistData.monthlyListeners)}
        </p>
        <p className="opacity-50 relative shrink-0 tracking-[-0.42px]" style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}>
          monthly listeners
        </p>
      </div>

      {/* Following Button */}
      <div className="absolute border border-solid border-white h-[34px] left-[16px] overflow-hidden rounded-[32px] top-[425px] w-[91px]">
        <p 
          className="absolute font-medium leading-[14px] left-[14px] text-[14px] text-nowrap text-white top-[9px] tracking-[-0.21px]"
          style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif', fontWeight: 510 }}
        >
          Following
        </p>
      </div>

      {/* Options Button (three dots) */}
      <div className="absolute flex gap-[4px] items-start left-[131px] opacity-50 top-[440px]">
        <div className="relative shrink-0 w-[4px] h-[4px]">
          <Image src="/icons/dots-icon.svg" alt="" width={4} height={4} className="w-full h-full" />
        </div>
        <div className="relative shrink-0 w-[4px] h-[4px]">
          <Image src="/icons/dots-icon.svg" alt="" width={4} height={4} className="w-full h-full" />
        </div>
        <div className="relative shrink-0 w-[4px] h-[4px]">
          <Image src="/icons/dots-icon.svg" alt="" width={4} height={4} className="w-full h-full" />
        </div>
      </div>

      {/* Shuffle Icon */}
      <div className="absolute h-[24px] left-[266px] opacity-50 top-[430px] w-[26.769px]">
        <Image src="/icons/shuffle-icon.svg" alt="Shuffle" width={27} height={24} className="w-full h-full" />
      </div>

      {/* Play Button */}
      <button
        onClick={handlePlayClick}
        className="absolute bg-[#66d46f] left-[311px] overflow-hidden rounded-[48px] w-[48px] h-[48px] top-[418px] flex items-center justify-center"
        aria-label="Play"
      >
        <div className="flex items-center justify-center w-[24px] h-[24px]">
          <div className="rotate-90">
            <Image src="/icons/play-icon.svg" alt="Play" width={24} height={24} className="w-full h-full" />
          </div>
        </div>
      </button>

      {/* Popular Section Title */}
      <p 
        className="absolute font-bold leading-[14px] left-[16px] text-[18px] text-nowrap text-white top-[482px]"
        style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
      >
        Popular
      </p>

      {/* Song List */}
      <div className="absolute left-1/2 -translate-x-1/2 w-[343px] top-[520px] pb-[120px]">
        <div className="flex flex-col gap-[16px]">
          {artistData.popularSongs.map((song, index) => (
            <div
              key={song.id}
              onClick={() => handleSongClick(song.id)}
              className="h-[48px] relative cursor-pointer ml-[8px]"
            >
            {/* Track Number */}
            <p 
              className="absolute leading-[14px] left-0 text-[14px] text-nowrap text-white top-[17px]"
              style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
            >
              {index + 1}
            </p>

            {/* Song Container */}
            <div className="absolute flex gap-[12px] items-center left-[23px] top-0">
              {/* Cover Art */}
              {song.id === 'song-1' ? (
                // Special One - Use special-one-all.png
                <div className="relative shrink-0 w-[48px] h-[48px] rounded overflow-hidden">
                  <Image 
                    src="/images/special-one-layers/special-one-all.png" 
                    alt="" 
                    width={48} 
                    height={48} 
                    className="w-full h-full object-cover"
                  />
                </div>
              ) : song.id === 'song-2' || song.id === 'song-6' ? (
                // Dream Song and Dream Song v2 - Use SVG with aspect ratio maintained
                <div className="relative shrink-0 w-[48px] h-[48px] rounded overflow-hidden">
                  <Image 
                    src="/assets/novel-tea-final.svg" 
                    alt="" 
                    width={48} 
                    height={48} 
                    className="w-full h-full object-contain"
                  />
                </div>
              ) : (
                // Other rows - Placeholder
                <div className="relative shrink-0 w-[48px] h-[48px] bg-gray-700 rounded">
                  {/* Placeholder square - same size as broken image */}
                </div>
              )}

              {/* Song Details */}
              <div className="flex flex-col items-start relative shrink-0 text-nowrap text-white">
                <p 
                  className="relative shrink-0 text-[16px] tracking-[0.08px] leading-[16px] mb-[6px]"
                  style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
                >
                  {song.title}
                </p>
                {song.playCount && (
                  <p 
                    className="relative shrink-0 text-[14px] leading-[14px]"
                    style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
                  >
                    {formatNumber(song.playCount)}
                  </p>
                )}
              </div>
            </div>

            {/* Options Icon - 16px right margin */}
            <div className="absolute h-[4px] right-[16px] opacity-50 top-[22px] w-[18px] flex gap-[7px]">
              <Image src="/icons/options-icon.svg" alt="" width={4} height={4} className="w-full h-full" />
              <Image src="/icons/options-icon.svg" alt="" width={4} height={4} className="w-full h-full" />
              <Image src="/icons/options-icon.svg" alt="" width={4} height={4} className="w-full h-full" />
            </div>
          </div>
          ))}
        </div>
      </div>

      {/* Navigation Bar - Fixed to bottom */}
      <div className="fixed bottom-[34px] backdrop-blur-[20px] backdrop-filter flex gap-[42px] items-center justify-center left-1/2 overflow-hidden px-[33px] py-[9px] -translate-x-1/2 w-full max-w-[375px] bg-gradient-to-b from-[rgba(17,17,17,0.81)] to-[#111]">
        {/* Home */}
        <div className="flex flex-col gap-[6px] items-center relative shrink-0">
          <div className="relative shrink-0 w-[24px] h-[24px]">
            <Image src="/icons/home-icon.svg" alt="Home" width={24} height={24} className="w-full h-full" />
          </div>
          <p 
            className="leading-[12px] relative shrink-0 text-[11px] text-nowrap text-white tracking-[-0.055px]"
            style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
          >
            Home
          </p>
        </div>

        {/* Search */}
        <div className="flex flex-col gap-[6px] items-center relative shrink-0 opacity-60">
          <div className="relative shrink-0 w-[24px] h-[24px]">
            <Image src="/icons/search-icon.svg" alt="Search" width={24} height={24} className="w-full h-full" />
          </div>
          <p 
            className="leading-[12px] relative shrink-0 text-[11px] text-nowrap text-white tracking-[-0.055px]"
            style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
          >
            Search
          </p>
        </div>

        {/* Your Library */}
        <div className="flex flex-col gap-[6px] items-center relative shrink-0 opacity-60">
          <div className="relative shrink-0 w-[24px] h-[24px]">
            <Image src="/icons/library-icon.svg" alt="Your Library" width={24} height={24} className="w-full h-full" />
          </div>
          <p 
            className="leading-[12px] relative shrink-0 text-[11px] text-nowrap text-white tracking-[-0.055px]"
            style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
          >
            Your Library
          </p>
        </div>

        {/* Premium */}
        <div className="flex flex-col gap-[6px] items-center relative shrink-0 opacity-60">
          <div className="opacity-60 overflow-hidden relative shrink-0 w-[24px] h-[24px]">
            <Image src="/icons/spotify-icon.svg" alt="Premium" width={24} height={24} className="w-full h-full" />
          </div>
          <p 
            className="leading-[12px] relative shrink-0 text-[11px] text-nowrap text-white tracking-[-0.055px]"
            style={{ fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif' }}
          >
            Premium
          </p>
        </div>
      </div>

      {/* Home Indicator - Fixed to bottom */}
      <div className="fixed bottom-0 flex flex-col items-center justify-center left-1/2 -translate-x-1/2 pb-[9px] pt-[20px] px-[120px] w-full max-w-[375px]">
        <div className="bg-white h-[5px] rounded-[5px] shrink-0 w-[134px]" />
      </div>

      {/* Music Player Modal - Always render if songId exists, control visibility separately */}
      {selectedSongId && (
        <MusicPlayerModal 
          songId={selectedSongId} 
          isVisible={isModalVisible}
          onClose={handleCloseModal} 
          onSongChange={handleSongChange} 
        />
      )}
    </div>
  );
}
