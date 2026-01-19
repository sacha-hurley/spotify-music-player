#!/usr/bin/env python3
"""
High-quality text removal from the combined "all layers" image.
Uses advanced image processing to detect and remove text while preserving quality.
"""

import sys
import os

def remove_text_high_quality():
    """Remove text from combined image using high-quality inpainting"""
    
    input_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    combined_file = os.path.join(input_dir, "special-one-all-layers-reference.png")
    output_dir = input_dir
    
    print("=" * 70)
    print("High-Quality Text Removal from Combined Image")
    print("=" * 70)
    
    if not os.path.exists(combined_file):
        print(f"❌ Combined image not found: {combined_file}")
        return False
    
    try:
        from PIL import Image
        import numpy as np
        import cv2
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
    
    print(f"\n📸 Processing: {combined_file}\n")
    
    try:
        # Load image
        img = Image.open(combined_file).convert('RGBA')
        print(f"✓ Loaded image: {img.size[0]}x{img.size[1]}px")
        
        # Convert to numpy array
        img_array = np.array(img)
        img_rgb = img_array[:,:,:3]
        img_alpha = img_array[:,:,3]
        
        # Convert to OpenCV format (BGR)
        img_cv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        print("\n🔍 Detecting text regions...")
        
        # Method 1: Detect bright/white text (common for overlays)
        # Text is likely white or very light colored
        _, mask_white = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        
        # Method 2: Detect text using morphological operations
        # This helps find text-like shapes
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morph = cv2.morphologyEx(mask_white, cv2.MORPH_CLOSE, kernel)
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
        
        # Method 3: Use edge detection to find text boundaries
        edges = cv2.Canny(gray, 50, 150)
        edges_dilated = cv2.dilate(edges, kernel, iterations=2)
        
        # Combine masks
        combined_mask = cv2.bitwise_or(mask_white, morph)
        combined_mask = cv2.bitwise_or(combined_mask, edges_dilated)
        
        # Dilate mask to ensure full text coverage
        kernel_large = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        final_mask = cv2.dilate(combined_mask, kernel_large, iterations=3)
        
        # Count text pixels
        text_pixels = np.sum(final_mask > 0)
        total_pixels = gray.shape[0] * gray.shape[1]
        print(f"  Detected {text_pixels:,} potential text pixels ({text_pixels/total_pixels*100:.2f}%)")
        
        # Save mask for inspection
        mask_path = os.path.join(output_dir, "text_mask_debug.png")
        cv2.imwrite(mask_path, final_mask)
        print(f"  ✓ Saved detection mask: {mask_path}")
        
        print("\n🎨 Removing text using inpainting...")
        
        # Use high-quality inpainting algorithm
        # INPAINT_TELEA is fast and good quality
        # INPAINT_NS is slower but higher quality
        inpainted = cv2.inpaint(img_cv, final_mask, 5, cv2.INPAINT_TELEA)
        
        # Convert back to RGB
        inpainted_rgb = cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)
        
        # Combine with original alpha channel
        result_array = np.dstack([inpainted_rgb, img_alpha])
        result_img = Image.fromarray(result_array.astype(np.uint8))
        
        # Save cleaned image
        output_file = os.path.join(output_dir, "special-one-background-no-text.png")
        result_img.save(output_file, 'PNG', compress_level=0)  # No compression for max quality
        print(f"  ✓ Saved cleaned image: {output_file}")
        print(f"    Size: {result_img.size[0]}x{result_img.size[1]}px")
        
        # Also try NS algorithm for comparison (higher quality but slower)
        print("\n🎨 Trying higher-quality inpainting algorithm...")
        inpainted_ns = cv2.inpaint(img_cv, final_mask, 5, cv2.INPAINT_NS)
        inpainted_ns_rgb = cv2.cvtColor(inpainted_ns, cv2.COLOR_BGR2RGB)
        result_ns_array = np.dstack([inpainted_ns_rgb, img_alpha])
        result_ns_img = Image.fromarray(result_ns_array.astype(np.uint8))
        
        output_file_ns = os.path.join(output_dir, "special-one-background-no-text-ns.png")
        result_ns_img.save(output_file_ns, 'PNG', compress_level=0)
        print(f"  ✓ Saved NS version: {output_file_ns}")
        
        print("\n" + "=" * 70)
        print("✅ Text removal complete!")
        print("=" * 70)
        print(f"\nFiles created:")
        print(f"  1. {output_file} (TELEA algorithm - faster)")
        print(f"  2. {output_file_ns} (NS algorithm - higher quality)")
        print(f"  3. {mask_path} (text detection mask - for verification)")
        print("\n⚠️  Please check both versions and let me know which looks better.")
        print("    The mask file shows what was detected as text.")
        print("    If text is still visible, we can adjust the detection parameters.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = remove_text_high_quality()
    sys.exit(0 if success else 1)
