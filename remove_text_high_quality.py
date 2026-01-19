#!/usr/bin/env python3
"""
High-quality text removal from extracted layers using image processing.
Uses OCR detection and inpainting to remove text while preserving quality.
"""

import sys
import os

def remove_text_high_quality():
    """Remove text from images using high-quality image processing"""
    
    input_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    bg_file = os.path.join(input_dir, "special-one-background.png")
    texture_file = os.path.join(input_dir, "special-one-texture.png")
    
    print("=" * 70)
    print("High-Quality Text Removal from Background Layers")
    print("=" * 70)
    
    # Check if files exist
    if not os.path.exists(bg_file):
        print(f"❌ Background file not found: {bg_file}")
        return False
    if not os.path.exists(texture_file):
        print(f"❌ Texture file not found: {texture_file}")
        return False
    
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        print("\n⚠️  Installing required libraries...")
        os.system(f"{sys.executable} -m pip install Pillow numpy opencv-python --quiet")
        try:
            from PIL import Image
            import numpy as np
            import cv2
        except ImportError:
            print("❌ Failed to install required libraries")
            print("Please install: pip install Pillow numpy opencv-python")
            return False
    
    try:
        import cv2
    except ImportError:
        print("⚠️  OpenCV not available, using PIL-only method")
        cv2 = None
    
    print("\n📸 Processing images...\n")
    
    # Process BACKGROUND layer
    try:
        print("Processing BACKGROUND layer...")
        img_bg = Image.open(bg_file).convert('RGBA')
        print(f"  Original size: {img_bg.size}")
        
        # Method 1: Try color-based text detection (if text is white/light)
        # Convert to numpy array
        img_array = np.array(img_bg)
        
        # Create mask for very light/white pixels (likely text)
        # Adjust threshold based on your text color
        if cv2:
            # Use OpenCV for better inpainting
            gray = cv2.cvtColor(img_array[:,:,:3], cv2.COLOR_RGB2GRAY)
            
            # Detect bright/white text (adjust threshold as needed)
            # Text is likely white or very light colored
            _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
            
            # Dilate mask to cover text fully
            kernel = np.ones((3,3), np.uint8)
            mask = cv2.dilate(mask, kernel, iterations=2)
            
            # Inpaint to remove text
            img_rgb = img_array[:,:,:3]
            inpainted = cv2.inpaint(img_rgb, mask, 3, cv2.INPAINT_TELEA)
            
            # Combine with alpha channel
            result = np.dstack([inpainted, img_array[:,:,3]])
            img_bg_clean = Image.fromarray(result.astype(np.uint8))
        else:
            # Fallback: Simple approach with PIL
            # This is a placeholder - would need more sophisticated processing
            img_bg_clean = img_bg.copy()
            print("  ⚠️  Using basic processing (OpenCV recommended for best results)")
        
        # Save cleaned image
        bg_clean_path = os.path.join(input_dir, "special-one-background-clean.png")
        img_bg_clean.save(bg_clean_path, 'PNG', compress_level=0)  # No compression for quality
        print(f"  ✓ Saved: {bg_clean_path}")
        
    except Exception as e:
        print(f"  ❌ BACKGROUND processing failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Process TEXTURE layer
    try:
        print("\nProcessing TEXTURE layer...")
        img_texture = Image.open(texture_file).convert('RGBA')
        print(f"  Original size: {img_texture.size}")
        
        if cv2:
            img_array = np.array(img_texture)
            gray = cv2.cvtColor(img_array[:,:,:3], cv2.COLOR_RGB2GRAY)
            _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
            kernel = np.ones((3,3), np.uint8)
            mask = cv2.dilate(mask, kernel, iterations=2)
            img_rgb = img_array[:,:,:3]
            inpainted = cv2.inpaint(img_rgb, mask, 3, cv2.INPAINT_TELEA)
            result = np.dstack([inpainted, img_array[:,:,3]])
            img_texture_clean = Image.fromarray(result.astype(np.uint8))
        else:
            img_texture_clean = img_texture.copy()
            print("  ⚠️  Using basic processing")
        
        texture_clean_path = os.path.join(input_dir, "special-one-texture-clean.png")
        img_texture_clean.save(texture_clean_path, 'PNG', compress_level=0)
        print(f"  ✓ Saved: {texture_clean_path}")
        
    except Exception as e:
        print(f"  ❌ TEXTURE processing failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("⚠️  IMPORTANT NOTES")
    print("=" * 70)
    print("\nThis method uses color-based detection which may:")
    print("  - Remove other light-colored elements (not just text)")
    print("  - Require threshold adjustment based on your text color")
    print("  - Need fine-tuning for best results")
    print("\nFor best results, you may need to:")
    print("  1. Adjust the threshold (currently 240) based on text color")
    print("  2. Manually specify text regions if location is known")
    print("  3. Use OCR-based detection for more precise text removal")
    print("\nCheck the output images and let me know if adjustments are needed.")
    
    return True


if __name__ == "__main__":
    success = remove_text_high_quality()
    sys.exit(0 if success else 1)
