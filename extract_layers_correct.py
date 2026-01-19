#!/usr/bin/env python3
"""
Correct layer extraction using PyMuPDF's layer_ui_configs properly.
"""

import sys
import os
import tempfile

def extract_layers_correct():
    """Extract layers using proper layer UI config"""
    
    ai_file = "/Users/sachahurley/Desktop/NOVEL_TEA_SINGLES (1).ai"
    output_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("Correct Layer Extraction Using Layer UI Configs")
    print("=" * 70)
    
    try:
        import fitz
    except ImportError:
        os.system(f"{sys.executable} -m pip install PyMuPDF --quiet")
        import fitz
    
    zoom = 3.0
    mat = fitz.Matrix(zoom, zoom)
    
    print("\n📸 Extracting layers with proper layer control...\n")
    
    # Extract BACKGROUND layer
    try:
        doc_bg = fitz.open(ai_file)
        configs = doc_bg.layer_ui_configs()
        
        print("Layer configurations:")
        for config in configs:
            print(f"  {config.get('number')}: {config.get('text')} (currently: {'ON' if config.get('on') else 'OFF'})")
        
        # Turn OFF TEXTURE (0) and TYPE (1), keep BACKGROUND (2) ON
        print("\nSetting up for BACKGROUND extraction:")
        for config in configs:
            num = config.get('number')
            name = config.get('text', '').upper()
            if 'BACKGROUND' in name:
                print(f"  ✓ Keeping {name} (layer {num}) ON")
                doc_bg.set_layer_ui_config(num, 1)  # ON
            else:
                print(f"  ✗ Turning OFF {name} (layer {num})")
                doc_bg.set_layer_ui_config(num, 2)  # OFF
        
        page_bg = doc_bg[4]
        pix_bg = page_bg.get_pixmap(matrix=mat, alpha=True)
        bg_path = os.path.join(output_dir, "special-one-background.png")
        pix_bg.save(bg_path)
        print(f"\n  ✓ BACKGROUND saved: {bg_path} ({pix_bg.width}x{pix_bg.height}px)")
        
        doc_bg.close()
        
    except Exception as e:
        print(f"  ❌ BACKGROUND failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Extract TEXTURE layer
    try:
        doc_texture = fitz.open(ai_file)
        configs = doc_texture.layer_ui_configs()
        
        # Turn OFF BACKGROUND (2) and TYPE (1), keep TEXTURE (0) ON
        print("\nSetting up for TEXTURE extraction:")
        for config in configs:
            num = config.get('number')
            name = config.get('text', '').upper()
            if 'TEXTURE' in name:
                print(f"  ✓ Keeping {name} (layer {num}) ON")
                doc_texture.set_layer_ui_config(num, 1)  # ON
            else:
                print(f"  ✗ Turning OFF {name} (layer {num})")
                doc_texture.set_layer_ui_config(num, 2)  # OFF
        
        page_texture = doc_texture[4]
        pix_texture = page_texture.get_pixmap(matrix=mat, alpha=True)
        texture_path = os.path.join(output_dir, "special-one-texture.png")
        pix_texture.save(texture_path)
        print(f"\n  ✓ TEXTURE saved: {texture_path} ({pix_texture.width}x{pix_texture.height}px)")
        
        doc_texture.close()
        
    except Exception as e:
        print(f"  ❌ TEXTURE failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Verify they're different
    try:
        from PIL import Image
        import numpy as np
        
        bg_img = Image.open(bg_path)
        texture_img = Image.open(texture_path)
        
        bg_array = np.array(bg_img)
        texture_array = np.array(texture_img)
        
        if np.array_equal(bg_array, texture_array):
            print("\n" + "=" * 70)
            print("⚠️  WARNING: Images are still IDENTICAL!")
            print("=" * 70)
            print("\nThis suggests the PDF layers may not be properly separated,")
            print("or the content is structured differently than expected.")
            print("\nPossible reasons:")
            print("  1. Layers might be nested/flattened in the PDF")
            print("  2. Content might be shared between layers")
            print("  3. OCG control might not work as expected for this PDF")
            print("\nNext steps:")
            print("  - Check if layers are visible separately in Illustrator")
            print("  - Try manual export if possible")
            print("  - Consider if layers are actually separate in the source file")
        else:
            diff = np.sum(np.abs(bg_array.astype(int) - texture_array.astype(int)) > 0)
            print(f"\n✓ Images are DIFFERENT ({diff:,} different pixels)")
            
    except Exception as e:
        print(f"\n⚠️  Could not verify difference: {e}")
    
    print("\n" + "=" * 70)
    return True


if __name__ == "__main__":
    success = extract_layers_correct()
    sys.exit(0 if success else 1)
