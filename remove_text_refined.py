#!/usr/bin/env python3
"""
Refined text removal - better detection parameters for precise text removal.
"""

import sys
import os

def remove_text_refined():
    """Remove text with refined detection"""
    
    input_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    combined_file = os.path.join(input_dir, "special-one-all-layers-reference.png")
    
    try:
        from PIL import Image
        import numpy as np
        import cv2
    except ImportError:
        os.system(f"{sys.executable} -m pip install Pillow numpy opencv-python --quiet")
        from PIL import Image
        import numpy as np
        import cv2
    
    print("=" * 70)
    print("Refined Text Removal - Multiple Detection Methods")
    print("=" * 70)
    
    img = Image.open(combined_file).convert('RGBA')
    img_array = np.array(img)
    img_rgb = img_array[:,:,:3]
    img_alpha = img_array[:,:,3]
    img_cv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    print(f"\n✓ Loaded: {img.size[0]}x{img.size[1]}px\n")
    
    # Try multiple detection methods and save each for comparison
    methods = []
    
    # Method 1: Very bright text (white/light) - threshold 250
    _, mask1 = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    text_pixels1 = np.sum(mask1 > 0)
    methods.append(("Very bright (250)", mask1, text_pixels1))
    
    # Method 2: Bright text - threshold 240
    _, mask2 = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    text_pixels2 = np.sum(mask2 > 0)
    methods.append(("Bright (240)", mask2, text_pixels2))
    
    # Method 3: Medium bright - threshold 220
    _, mask3 = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
    text_pixels3 = np.sum(mask3 > 0)
    methods.append(("Medium bright (220)", mask3, text_pixels3))
    
    # Method 4: Adaptive threshold (handles varying backgrounds)
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, 11, 2)
    # Invert to get bright regions
    adaptive = 255 - adaptive
    text_pixels4 = np.sum(adaptive > 0)
    methods.append(("Adaptive", adaptive, text_pixels4))
    
    print("Detection results:")
    for name, mask, pixels in methods:
        percent = (pixels / (gray.shape[0] * gray.shape[1])) * 100
        print(f"  {name}: {pixels:,} pixels ({percent:.2f}%)")
    
    # Use the most reasonable mask (not too much, not too little)
    # Prefer method with 1-10% of image (likely text region)
    best_mask = None
    best_name = None
    total_pixels = gray.shape[0] * gray.shape[1]
    
    for name, mask, pixels in methods:
        percent = pixels / total_pixels
        if 0.01 <= percent <= 0.15:  # 1-15% of image is reasonable for text
            best_mask = mask
            best_name = name
            break
    
    # If no mask in reasonable range, use the one with least pixels (most selective)
    if best_mask is None:
        methods_sorted = sorted(methods, key=lambda x: x[2])
        best_mask = methods_sorted[0][1]
        best_name = methods_sorted[0][0]
        print(f"\n⚠️  No mask in ideal range, using most selective: {best_name}")
    else:
        print(f"\n✓ Using: {best_name}")
    
    # Refine mask with morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    refined_mask = cv2.morphologyEx(best_mask, cv2.MORPH_CLOSE, kernel)
    refined_mask = cv2.morphologyEx(refined_mask, cv2.MORPH_OPEN, kernel)
    
    # Dilate slightly to ensure full text coverage
    kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    final_mask = cv2.dilate(refined_mask, kernel_dilate, iterations=2)
    
    text_pixels_final = np.sum(final_mask > 0)
    print(f"  Final mask: {text_pixels_final:,} pixels ({(text_pixels_final/total_pixels)*100:.2f}%)")
    
    # Save mask for inspection
    mask_path = os.path.join(input_dir, "text_mask_refined.png")
    cv2.imwrite(mask_path, final_mask)
    print(f"  ✓ Saved mask: {mask_path}\n")
    
    # Inpaint with both algorithms
    print("🎨 Removing text...")
    
    # TELEA (faster)
    inpainted_telea = cv2.inpaint(img_cv, final_mask, 5, cv2.INPAINT_TELEA)
    inpainted_telea_rgb = cv2.cvtColor(inpainted_telea, cv2.COLOR_BGR2RGB)
    result_telea = np.dstack([inpainted_telea_rgb, img_alpha])
    result_telea_img = Image.fromarray(result_telea.astype(np.uint8))
    
    output_telea = os.path.join(input_dir, "special-one-background-no-text.png")
    result_telea_img.save(output_telea, 'PNG', compress_level=0)
    print(f"  ✓ TELEA: {output_telea}")
    
    # NS (higher quality)
    inpainted_ns = cv2.inpaint(img_cv, final_mask, 5, cv2.INPAINT_NS)
    inpainted_ns_rgb = cv2.cvtColor(inpainted_ns, cv2.COLOR_BGR2RGB)
    result_ns = np.dstack([inpainted_ns_rgb, img_alpha])
    result_ns_img = Image.fromarray(result_ns.astype(np.uint8))
    
    output_ns = os.path.join(input_dir, "special-one-background-no-text-ns.png")
    result_ns_img.save(output_ns, 'PNG', compress_level=0)
    print(f"  ✓ NS: {output_ns}")
    
    print("\n" + "=" * 70)
    print("✅ Complete! Check the mask file to verify text detection.")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    success = remove_text_refined()
    sys.exit(0 if success else 1)
