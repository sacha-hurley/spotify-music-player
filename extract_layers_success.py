#!/usr/bin/env python3
"""
Successfully extract layers by modifying PDF ON array directly.
"""

import sys
import os
import re
import tempfile
import shutil

def extract_layers_success():
    """Extract layers by modifying PDF ON array"""
    
    ai_file = "/Users/sachahurley/Desktop/NOVEL_TEA_SINGLES (1).ai"
    output_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("Layer Extraction - Artboard 5 (Special One)")
    print("=" * 70)
    print(f"\nSource: {ai_file}")
    print(f"Output: {output_dir}\n")
    
    if not os.path.exists(ai_file):
        print("❌ File not found")
        return False
    
    try:
        import fitz
    except ImportError:
        os.system(f"{sys.executable} -m pip install PyMuPDF --quiet")
        import fitz
    
    # Read PDF as binary
    with open(ai_file, 'rb') as f:
        pdf_bytes = f.read()
    
    # Find the ON array pattern
    # Pattern: /ON[9 0 R 10 0 R 11 0 R]
    on_pattern = rb'/ON\s*\[9\s+0\s+R\s+10\s+0\s+R\s+11\s+0\s+R\]'
    match = re.search(on_pattern, pdf_bytes)
    
    if not match:
        print("❌ Could not find ON array in PDF")
        return False
    
    print(f"✓ Found ON array at position {match.start()}")
    original_on = match.group(0)
    print(f"  Original: {original_on.decode('latin-1', errors='ignore')}\n")
    
    # High-quality rendering settings
    zoom = 3.0
    mat = fitz.Matrix(zoom, zoom)
    
    print("📸 Extracting layers...\n")
    
    # Extract BACKGROUND layer (OCG 9 only)
    try:
        # Modify ON array to show only BACKGROUND
        new_on_bg = b'/ON[9 0 R]'
        pdf_bg_bytes = pdf_bytes.replace(original_on, new_on_bg)
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(pdf_bg_bytes)
            tmp_path = tmp.name
        
        # Open and render
        doc_bg = fitz.open(tmp_path)
        page_bg = doc_bg[4]  # Page 5
        pix_bg = page_bg.get_pixmap(matrix=mat, alpha=True)
        
        bg_path = os.path.join(output_dir, "special-one-background.png")
        pix_bg.save(bg_path)
        print(f"  ✓ BACKGROUND: {bg_path}")
        print(f"    Size: {pix_bg.width}x{pix_bg.height}px\n")
        
        doc_bg.close()
        os.unlink(tmp_path)
        
    except Exception as e:
        print(f"  ❌ BACKGROUND failed: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Extract TEXTURE layer (OCG 11 only)
    try:
        # Modify ON array to show only TEXTURE
        new_on_texture = b'/ON[11 0 R]'
        pdf_texture_bytes = pdf_bytes.replace(original_on, new_on_texture)
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(pdf_texture_bytes)
            tmp_path = tmp.name
        
        # Open and render
        doc_texture = fitz.open(tmp_path)
        page_texture = doc_texture[4]  # Page 5
        pix_texture = page_texture.get_pixmap(matrix=mat, alpha=True)
        
        texture_path = os.path.join(output_dir, "special-one-texture.png")
        pix_texture.save(texture_path)
        print(f"  ✓ TEXTURE: {texture_path}")
        print(f"    Size: {pix_texture.width}x{pix_texture.height}px\n")
        
        doc_texture.close()
        os.unlink(tmp_path)
        
    except Exception as e:
        print(f"  ❌ TEXTURE failed: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Verify files were created
    bg_file = os.path.join(output_dir, "special-one-background.png")
    texture_file = os.path.join(output_dir, "special-one-texture.png")
    
    print("=" * 70)
    if os.path.exists(bg_file) and os.path.exists(texture_file):
        print("✅ SUCCESS: Both layers extracted!")
        print("=" * 70)
        print(f"\nFiles created:")
        print(f"  ✓ {bg_file}")
        print(f"  ✓ {texture_file}")
        print(f"\nThese layers are now ready for animation!")
        return True
    else:
        print("⚠️  PARTIAL SUCCESS")
        print("=" * 70)
        if os.path.exists(bg_file):
            print(f"  ✓ {bg_file}")
        if os.path.exists(texture_file):
            print(f"  ✓ {texture_file}")
        return False


if __name__ == "__main__":
    success = extract_layers_success()
    sys.exit(0 if success else 1)
