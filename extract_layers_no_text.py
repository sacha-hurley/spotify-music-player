#!/usr/bin/env python3
"""
Extract BACKGROUND and TEXTURE layers, ensuring TYPE layer (text) is completely excluded.
"""

import sys
import os
import re
import tempfile

def extract_layers_no_text():
    """Extract layers ensuring TYPE layer is excluded"""
    
    ai_file = "/Users/sachahurley/Desktop/NOVEL_TEA_SINGLES (1).ai"
    output_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("Layer Extraction - Excluding TYPE Layer (Text)")
    print("=" * 70)
    print(f"\nSource: {ai_file}")
    print(f"Output: {output_dir}\n")
    
    try:
        import fitz
    except ImportError:
        os.system(f"{sys.executable} -m pip install PyMuPDF --quiet")
        import fitz
    
    # Read PDF as binary
    with open(ai_file, 'rb') as f:
        pdf_bytes = f.read()
    
    # Find ALL ON arrays - there might be multiple
    on_pattern = rb'/ON\s*\[[^\]]+\]'
    all_matches = list(re.finditer(on_pattern, pdf_bytes))
    
    print(f"Found {len(all_matches)} ON array(s) in PDF")
    
    # Find the main ON array that includes all three layers
    main_on_match = None
    for match in all_matches:
        on_str = match.group(0).decode('latin-1', errors='ignore')
        if '9 0 R' in on_str and '10 0 R' in on_str and '11 0 R' in on_str:
            main_on_match = match
            print(f"✓ Found main ON array: {on_str}")
            break
    
    if not main_on_match:
        print("❌ Could not find main ON array with all three layers")
        return False
    
    original_on = main_on_match.group(0)
    
    # High-quality rendering settings
    zoom = 3.0
    mat = fitz.Matrix(zoom, zoom)
    
    print("\n📸 Extracting layers (excluding TYPE layer 10)...\n")
    
    # Extract BACKGROUND layer (OCG 9 only - explicitly exclude 10 and 11)
    try:
        # Set ON to only BACKGROUND, explicitly exclude TYPE (10) and TEXTURE (11)
        new_on_bg = b'/ON[9 0 R]'
        
        # Replace ALL occurrences of the ON array to ensure consistency
        pdf_bg_bytes = pdf_bytes.replace(original_on, new_on_bg)
        
        # Also check for any other ON arrays that might include TYPE
        # Replace any ON array that includes 10 (TYPE) with one that excludes it
        type_on_pattern = rb'/ON\s*\[[^\]]*10\s+0\s+R[^\]]*\]'
        for match in re.finditer(type_on_pattern, pdf_bg_bytes):
            # Remove 10 from any ON array
            on_with_type = match.group(0)
            on_without_type = re.sub(rb'10\s+0\s+R\s*', b'', on_with_type)
            on_without_type = re.sub(rb',\s*,', b',', on_without_type)  # Clean up double commas
            on_without_type = re.sub(rb'\[\s*,', b'[', on_without_type)  # Clean up leading comma
            on_without_type = re.sub(rb',\s*\]', b']', on_without_type)  # Clean up trailing comma
            pdf_bg_bytes = pdf_bg_bytes.replace(on_with_type, on_without_type)
        
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
        print(f"  ✓ BACKGROUND (no text): {bg_path}")
        print(f"    Size: {pix_bg.width}x{pix_bg.height}px\n")
        
        doc_bg.close()
        os.unlink(tmp_path)
        
    except Exception as e:
        print(f"  ❌ BACKGROUND failed: {e}\n")
        import traceback
        traceback.print_exc()
    
    # Extract TEXTURE layer (OCG 11 only - explicitly exclude TYPE 10)
    try:
        # Set ON to only TEXTURE, explicitly exclude TYPE (10) and BACKGROUND (9)
        new_on_texture = b'/ON[11 0 R]'
        
        # Replace ALL occurrences
        pdf_texture_bytes = pdf_bytes.replace(original_on, new_on_texture)
        
        # Also remove TYPE (10) from any other ON arrays
        type_on_pattern = rb'/ON\s*\[[^\]]*10\s+0\s+R[^\]]*\]'
        for match in re.finditer(type_on_pattern, pdf_texture_bytes):
            on_with_type = match.group(0)
            on_without_type = re.sub(rb'10\s+0\s+R\s*', b'', on_with_type)
            on_without_type = re.sub(rb',\s*,', b',', on_without_type)
            on_without_type = re.sub(rb'\[\s*,', b'[', on_without_type)
            on_without_type = re.sub(rb',\s*\]', b']', on_without_type)
            pdf_texture_bytes = pdf_texture_bytes.replace(on_with_type, on_without_type)
        
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
        print(f"  ✓ TEXTURE (no text): {texture_path}")
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
        print("✅ SUCCESS: Layers extracted without TYPE layer (text)")
        print("=" * 70)
        print(f"\nFiles created:")
        print(f"  ✓ {bg_file}")
        print(f"  ✓ {texture_file}")
        print(f"\n⚠️  IMPORTANT: Please verify the images don't contain any text.")
        print(f"    The TYPE layer (OCG 10) should be completely excluded.")
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
    success = extract_layers_no_text()
    sys.exit(0 if success else 1)
