#!/usr/bin/env python3
"""
Proper layer extraction using PyMuPDF's layer control methods.
"""

import sys
import os
import tempfile

def extract_layers_proper():
    """Extract layers using PyMuPDF's layer UI config"""
    
    ai_file = "/Users/sachahurley/Desktop/NOVEL_TEA_SINGLES (1).ai"
    output_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("Proper Layer Extraction - Using PyMuPDF Layer Control")
    print("=" * 70)
    
    try:
        import fitz
    except ImportError:
        os.system(f"{sys.executable} -m pip install PyMuPDF --quiet")
        import fitz
    
    try:
        doc = fitz.open(ai_file)
        page = doc[4]  # Page 5
        
        print(f"\n✓ Opened page 5")
        
        # Get layer configurations
        try:
            layer_configs = doc.layer_ui_configs()
            print(f"\n✓ Found {len(layer_configs)} layer configurations")
            for config in layer_configs:
                print(f"  - Layer {config.get('number')}: {config.get('text')} (on: {config.get('on')})")
        except Exception as e:
            print(f"\n⚠️  layer_ui_configs() not available: {e}")
            print("   Trying alternative method...\n")
        
        # Get OCGs directly
        ocgs = doc.get_ocgs()
        print(f"\n✓ Found {len(ocgs.get('ocgs', {}))} OCGs:")
        for ocg_xref, ocg_info in ocgs.get('ocgs', {}).items():
            print(f"  - OCG {ocg_xref}: {ocg_info.get('name')} (on: {ocg_info.get('on')})")
        
        zoom = 3.0
        mat = fitz.Matrix(zoom, zoom)
        
        print("\n📸 Extracting layers...\n")
        
        # Method 1: Try using layer_ui_configs if available
        try:
            # Create a copy of the document for manipulation
            doc_copy = fitz.open(ai_file)
            
            # Try to set layer visibility
            layer_configs = doc_copy.layer_ui_configs()
            
            # Find TYPE layer and turn it off
            for config in layer_configs:
                if 'TYPE' in config.get('text', '').upper():
                    print(f"  Turning off TYPE layer (config {config.get('number')})")
                    doc_copy.set_layer_ui_config(config.get('number'), 2)  # 2 = OFF
            
            # Render BACKGROUND only
            # Turn off TEXTURE and TYPE, keep BACKGROUND
            for config in layer_configs:
                name = config.get('text', '').upper()
                if 'TEXTURE' in name or 'TYPE' in name:
                    doc_copy.set_layer_ui_config(config.get('number'), 2)
                elif 'BACKGROUND' in name:
                    doc_copy.set_layer_ui_config(config.get('number'), 1)  # 1 = ON
            
            page_copy = doc_copy[4]
            pix_bg = page_copy.get_pixmap(matrix=mat, alpha=True)
            bg_path = os.path.join(output_dir, "special-one-background.png")
            pix_bg.save(bg_path)
            print(f"  ✓ BACKGROUND: {bg_path} ({pix_bg.width}x{pix_bg.height}px)")
            
            doc_copy.close()
            
        except Exception as e:
            print(f"  ⚠️  Layer UI config method failed: {e}")
            print("   Trying direct OCG manipulation...\n")
        
        # Method 2: Direct OCG manipulation by modifying the PDF
        # This is what we were doing before, but let's verify it's working
        import re
        
        with open(ai_file, 'rb') as f:
            pdf_bytes = f.read()
        
        on_pattern = rb'/ON\s*\[9\s+0\s+R\s+10\s+0\s+R\s+11\s+0\s+R\]'
        match = re.search(on_pattern, pdf_bytes)
        
        if match:
            original_on = match.group(0)
            
            # Extract BACKGROUND (9 only)
            new_on_bg = b'/ON[9 0 R]'
            pdf_bg_bytes = pdf_bytes.replace(original_on, new_on_bg)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(pdf_bg_bytes)
                tmp_path = tmp.name
            
            doc_bg = fitz.open(tmp_path)
            page_bg = doc_bg[4]
            pix_bg = page_bg.get_pixmap(matrix=mat, alpha=True)
            bg_path = os.path.join(output_dir, "special-one-background.png")
            pix_bg.save(bg_path)
            print(f"  ✓ BACKGROUND (method 2): {bg_path}")
            
            doc_bg.close()
            os.unlink(tmp_path)
            
            # Extract TEXTURE (11 only)
            new_on_texture = b'/ON[11 0 R]'
            pdf_texture_bytes = pdf_bytes.replace(original_on, new_on_texture)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(pdf_texture_bytes)
                tmp_path = tmp.name
            
            doc_texture = fitz.open(tmp_path)
            page_texture = doc_texture[4]
            pix_texture = page_texture.get_pixmap(matrix=mat, alpha=True)
            texture_path = os.path.join(output_dir, "special-one-texture.png")
            pix_texture.save(texture_path)
            print(f"  ✓ TEXTURE (method 2): {texture_path}")
            
            doc_texture.close()
            os.unlink(tmp_path)
        
        doc.close()
        
        print("\n" + "=" * 70)
        print("✅ Extraction complete")
        print("=" * 70)
        print("\n⚠️  If text is still visible, it may be:")
        print("   1. Embedded within the BACKGROUND/TEXTURE layers")
        print("   2. Rasterized into the layer content")
        print("   3. Controlled by a different mechanism")
        print("\nNext steps: Try image processing or check layer content directly")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = extract_layers_proper()
    sys.exit(0 if success else 1)
