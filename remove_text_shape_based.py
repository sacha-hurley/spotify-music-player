#!/usr/bin/env python3
"""
Shape-based text detection - detects text by shape/pattern rather than color.
"""

import sys
import os

def remove_text_shape_based():
    """Remove text using shape-based detection"""
    
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
    print("Shape-Based Text Detection")
    print("=" * 70)
    
    img = Image.open(combined_file).convert('RGBA')
    img_array = np.array(img)
    img_rgb = img_array[:,:,:3]
    img_alpha = img_array[:,:,3]
    img_cv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    print(f"\n✓ Loaded: {img.size[0]}x{img.size[1]}px\n")
    
    # Method: Detect text-like shapes using contours and aspect ratios
    # Text typically has specific characteristics:
    # - Rectangular shapes
    # - Horizontal orientation
    # - Specific size ratios
    
    print("🔍 Detecting text using shape analysis...")
    
    # Use edge detection to find boundaries
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create mask for text-like shapes
    mask = np.zeros(gray.shape, dtype=np.uint8)
    
    text_contours = []
    for contour in contours:
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        
        # Filter for text-like shapes:
        # - Reasonable size (not too small, not too large)
        # - Horizontal orientation (width > height for text)
        # - Specific aspect ratio
        
        if area > 100 and area < 50000:  # Reasonable text size
            aspect_ratio = w / h if h > 0 else 0
            if 1.5 < aspect_ratio < 20:  # Text is typically wider than tall
                # Check if it's roughly horizontal
                if w > h * 1.2:
                    text_contours.append(contour)
                    cv2.drawContours(mask, [contour], -1, 255, -1)
    
    text_pixels = np.sum(mask > 0)
    total_pixels = gray.shape[0] * gray.shape[1]
    print(f"  Found {len(text_contours)} text-like regions")
    print(f"  Mask covers {text_pixels:,} pixels ({(text_pixels/total_pixels)*100:.2f}%)")
    
    if text_pixels < 1000:
        print("\n⚠️  Very few pixels detected - text might be:")
        print("   1. A different color than expected")
        print("   2. Blended with background")
        print("   3. Rasterized into the image")
        print("\nTrying alternative: Detect by color difference from background...")
        
        # Alternative: Detect regions that differ significantly from surrounding area
        # This works if text has different color than background
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        diff = cv2.absdiff(gray, blur)
        _, mask_diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        
        # Morphological operations to connect text parts
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask_diff = cv2.morphologyEx(mask_diff, cv2.MORPH_CLOSE, kernel)
        mask_diff = cv2.dilate(mask_diff, kernel, iterations=2)
        
        text_pixels_diff = np.sum(mask_diff > 0)
        print(f"  Difference method: {text_pixels_diff:,} pixels ({(text_pixels_diff/total_pixels)*100:.2f}%)")
        
        if 0.01 <= (text_pixels_diff/total_pixels) <= 0.20:  # Reasonable range
            mask = mask_diff
            print("  ✓ Using difference-based detection")
        else:
            print("  ⚠️  Difference method also not ideal")
    
    # Save mask
    mask_path = os.path.join(input_dir, "text_mask_shape.png")
    cv2.imwrite(mask_path, mask)
    print(f"\n  ✓ Saved mask: {mask_path}")
    
    # Inpaint
    print("\n🎨 Removing detected regions...")
    inpainted = cv2.inpaint(img_cv, mask, 5, cv2.INPAINT_NS)
    inpainted_rgb = cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)
    result = np.dstack([inpainted_rgb, img_alpha])
    result_img = Image.fromarray(result.astype(np.uint8))
    
    output_file = os.path.join(input_dir, "special-one-background-no-text.png")
    result_img.save(output_file, 'PNG', compress_level=0)
    print(f"  ✓ Saved: {output_file}")
    
    print("\n" + "=" * 70)
    print("✅ Complete!")
    print("=" * 70)
    print("\n⚠️  IMPORTANT: Please check the mask file to see what was detected.")
    print("    If text is still visible or wrong areas were removed,")
    print("    please tell me:")
    print("    1. What color is the text? (white, black, colored?)")
    print("    2. Where is it located? (center, top, bottom?)")
    print("    3. Can you describe the text appearance?")
    
    return True


if __name__ == "__main__":
    success = remove_text_shape_based()
    sys.exit(0 if success else 1)
