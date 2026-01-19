# Layer Export Guide for "Special One" Animation

## Overview
This guide explains how to export the BACKGROUND and TEXTURE layers from the Illustrator file for use in the "Special One" music player page.

## Export Settings for Animation/Video

**Best Format: PNG**
- ✅ Lossless quality (no compression artifacts)
- ✅ Supports transparency (alpha channel)
- ✅ Perfect for compositing and animation
- ✅ Works great for 30fps MP4 video creation

**Recommended Resolution:**
- **300 PPI** (or higher) for crisp quality
- At 648pt artboard size, this gives you **~1944x1944px** images
- This resolution is excellent for smooth 30fps video animation

## Step-by-Step Export Instructions

### 1. Open the Illustrator File
- File: `/Users/sachahurley/Desktop/NOVEL_TEA_SINGLES (1).ai`
- Open in Adobe Illustrator

### 2. Navigate to Artboard 5
- Go to **Artboard 5** (the "Special One" artboard)
- You can use the Artboards panel (Window > Artboards) to navigate

### 3. Open Layers Panel
- Go to **Window > Layers** (or press `F7`)
- You should see 3 layers:
  - **BACKGROUND** (bottom layer)
  - **TYPE** (middle layer - we'll skip this)
  - **TEXTURE** (top layer)

### 4. Export BACKGROUND Layer

1. **Hide other layers:**
   - Click the eye icon 👁️ next to **TYPE** layer to hide it
   - Click the eye icon 👁️ next to **TEXTURE** layer to hide it
   - Keep **BACKGROUND** layer visible (eye icon should be visible)

2. **Export the layer:**
   - Go to **File > Export > Export As...**
   - Choose format: **PNG**
   - Set resolution: **300 PPI** (or higher)
   - Save location: `/Users/sachahurley/spotify-music-player/public/images/special-one-layers/`
   - File name: `special-one-background.png`
   - Click **Export**

### 5. Export TEXTURE Layer

1. **Hide other layers:**
   - Click the eye icon 👁️ next to **TYPE** layer to hide it
   - Click the eye icon 👁️ next to **BACKGROUND** layer to hide it
   - Keep **TEXTURE** layer visible (eye icon should be visible)

2. **Export the layer:**
   - Go to **File > Export > Export As...**
   - Choose format: **PNG**
   - Set resolution: **300 PPI** (or higher)
   - Save location: `/Users/sachahurley/spotify-music-player/public/images/special-one-layers/`
   - File name: `special-one-texture.png`
   - Click **Export**

## File Structure

After exporting, you should have:
```
public/images/special-one-layers/
├── special-one-background.png  (BACKGROUND layer)
├── special-one-texture.png      (TEXTURE layer)
└── special-one-all-layers-reference.png  (reference image)
```

## Implementation

The code has already been set up in `/app/player/[id]/page.tsx` to:
- ✅ Display BACKGROUND layer as the bottom background
- ✅ Display TEXTURE layer on top of BACKGROUND
- ✅ Only show these layers for "Special One" (song-1)
- ✅ Position them full-screen underneath all UI and text

## Animation Tips

For creating smooth 30fps MP4 animations:
1. **Use PNG format** - maintains quality through animation
2. **300 PPI resolution** - ensures crisp details even when scaled
3. **Keep layers separate** - allows independent animation of each layer
4. **Export at artboard size** - maintains proper aspect ratio

## Next Steps

Once you've exported the layers:
1. The images will automatically appear on the "Special One" player page
2. You can then animate these layers using CSS animations or GSAP
3. Export individual frames for video creation if needed

## Troubleshooting

**If layers don't appear:**
- Check that files are saved in the correct location
- Verify file names match exactly: `special-one-background.png` and `special-one-texture.png`
- Check browser console for any image loading errors

**If quality looks low:**
- Increase export resolution to 300 PPI or higher
- Ensure you're exporting at the full artboard size (648x648pt)
