#!/usr/bin/env python3
"""
Working layer extraction - modifies OCProperties to control layer visibility.
"""

import sys
import os

def extract_layers_working():
    """Extract layers by modifying OCProperties ON array"""
    
    ai_file = "/Users/sachahurley/Desktop/NOVEL_TEA_SINGLES (1).ai"
    output_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("Layer Extraction - Artboard 5 (Special One)")
    print("=" * 70)
    
    try:
        import fitz
    except ImportError:
        os.system(f"{sys.executable} -m pip install PyMuPDF --quiet")
        import fitz
    
    try:
        # Open PDF
        doc = fitz.open(ai_file)
        page = doc[4]  # Page 5
        
        print(f"✓ Opened page 5 ({page.rect.width}x{page.rect.height}pt)\n")
        
        # OCG xrefs: 9=BACKGROUND, 10=TYPE, 11=TEXTURE
        bg_xref = 9
        type_xref = 10
        texture_xref = 11
        
        # Get OCProperties
        catalog_xref = doc.pdf_catalog()
        oc_props_key = doc.xref_get_key(catalog_xref, "OCProperties")
        
        if oc_props_key[0] != "dict":
            print("❌ Could not find OCProperties")
            doc.close()
            return False
        
        oc_props_xref = oc_props_key[1]
        print(f"✓ Found OCProperties at xref {oc_props_xref}\n")
        
        # Get the D (default) dictionary which contains ON array
        oc_props_obj = doc.xref_object(oc_props_xref)
        d_dict_xref = oc_props_obj.get("/D", {}).get("xref", None)
        
        if not d_dict_xref:
            # Try to get it differently
            d_key = doc.xref_get_key(oc_props_xref, "D")
            if d_key[0] == "dict":
                d_dict_xref = d_key[1]
        
        if not d_dict_xref:
            print("❌ Could not find D dictionary")
            doc.close()
            return False
        
        print(f"✓ Found D dictionary at xref {d_dict_xref}\n")
        
        # Get the ON array (which OCGs are visible)
        d_dict_obj = doc.xref_object(d_dict_xref)
        on_array = d_dict_obj.get("/ON", [])
        
        print(f"✓ Current ON array: {on_array}")
        print(f"  (All layers currently visible)\n")
        
        # Save original ON array
        original_on = on_array.copy() if isinstance(on_array, list) else on_array
        
        # High-quality rendering
        zoom = 3.0
        mat = fitz.Matrix(zoom, zoom)
        
        print("📸 Extracting layers...\n")
        
        # Extract BACKGROUND layer
        try:
            # Set ON to only BACKGROUND
            new_on = [bg_xref]
            doc.update_object(d_dict_xref, {"/ON": new_on})
            
            # Render
            pix_bg = page.get_pixmap(matrix=mat, alpha=True)
            bg_path = os.path.join(output_dir, "special-one-background.png")
            pix_bg.save(bg_path)
            print(f"  ✓ BACKGROUND: {bg_path} ({pix_bg.width}x{pix_bg.height}px)")
            
        except Exception as e:
            print(f"  ❌ BACKGROUND extraction failed: {e}")
        
        # Extract TEXTURE layer
        try:
            # Set ON to only TEXTURE
            new_on = [texture_xref]
            doc.update_object(d_dict_xref, {"/ON": new_on})
            
            # Render
            pix_texture = page.get_pixmap(matrix=mat, alpha=True)
            texture_path = os.path.join(output_dir, "special-one-texture.png")
            pix_texture.save(texture_path)
            print(f"  ✓ TEXTURE: {texture_path} ({pix_texture.width}x{pix_texture.height}px)")
            
        except Exception as e:
            print(f"  ❌ TEXTURE extraction failed: {e}")
        
        # Restore original ON array
        try:
            doc.update_object(d_dict_xref, {"/ON": original_on})
        except:
            pass
        
        doc.close()
        
        # Check if files were created
        bg_file = os.path.join(output_dir, "special-one-background.png")
        texture_file = os.path.join(output_dir, "special-one-texture.png")
        
        if os.path.exists(bg_file) and os.path.exists(texture_file):
            print("\n" + "=" * 70)
            print("✅ SUCCESS: Both layers extracted!")
            print("=" * 70)
            return True
        else:
            print("\n" + "=" * 70)
            print("⚠️  PARTIAL SUCCESS")
            print("=" * 70)
            print("\nSome layers may not have been extracted.")
            print("Files created:")
            if os.path.exists(bg_file):
                print(f"  ✓ {bg_file}")
            if os.path.exists(texture_file):
                print(f"  ✓ {texture_file}")
            return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = extract_layers_working()
    sys.exit(0 if success else 1)
