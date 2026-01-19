#!/usr/bin/env python3
"""
Advanced layer extraction script for Illustrator PDF files.
Extracts BACKGROUND and TEXTURE layers from page 5 programmatically.
"""

import sys
import os

def extract_layers_advanced():
    """Extract BACKGROUND and TEXTURE layers using PyMuPDF OCG manipulation"""
    
    ai_file = "/Users/sachahurley/Desktop/NOVEL_TEA_SINGLES (1).ai"
    output_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("Advanced Layer Extraction - Artboard 5 (Special One)")
    print("=" * 70)
    print(f"\nSource: {ai_file}")
    print(f"Output: {output_dir}\n")
    
    if not os.path.exists(ai_file):
        print(f"❌ ERROR: File not found: {ai_file}")
        return False
    
    try:
        import fitz  # PyMuPDF
        print("✓ PyMuPDF imported successfully\n")
    except ImportError:
        print("⚠️  Installing PyMuPDF...")
        os.system(f"{sys.executable} -m pip install PyMuPDF --quiet")
        try:
            import fitz
            print("✓ PyMuPDF installed successfully\n")
        except ImportError:
            print("❌ Failed to install PyMuPDF")
            print("Please install manually: pip3 install PyMuPDF")
            return False
    
    try:
        # Open the PDF
        doc = fitz.open(ai_file)
        print(f"✓ Opened PDF: {len(doc)} pages")
        
        if len(doc) < 5:
            print(f"❌ ERROR: PDF only has {len(doc)} pages, need at least 5")
            doc.close()
            return False
        
        # Get page 5 (index 4)
        page = doc[4]
        print(f"✓ Loaded page 5 (index 4)")
        print(f"  Dimensions: {page.rect.width} x {page.rect.height} points\n")
        
        # Get the document's OCG (Optional Content Groups) structure
        # OCGs represent layers in Illustrator files
        ocgs = doc.get_ocgs()
        print(f"✓ Found {len(ocgs)} Optional Content Groups")
        
        # Find layer OCGs by name
        background_ocg = None
        texture_ocg = None
        
        # The OCGs we found earlier were references 9, 10, 11
        # Let's search for them in the OCG structure
        for ocg_id, ocg_dict in ocgs.items():
            ocg_name = None
            # Try to get the name from the OCG dictionary
            if isinstance(ocg_dict, dict):
                if "Name" in ocg_dict:
                    ocg_name = str(ocg_dict["Name"])
                elif "name" in ocg_dict:
                    ocg_name = str(ocg_dict["name"])
            
            # Also check the raw object
            try:
                ocg_obj = doc.xref_get_key(ocg_id, "Name")
                if ocg_obj[0] == "name":
                    ocg_name = ocg_obj[1].strip("()")
            except:
                pass
            
            if ocg_name:
                print(f"  - OCG {ocg_id}: {ocg_name}")
                if "BACKGROUND" in ocg_name.upper():
                    background_ocg = ocg_id
                elif "TEXTURE" in ocg_name.upper():
                    texture_ocg = ocg_id
        
        # Alternative approach: Use the OCG references we know (9, 10, 11)
        # Based on our earlier analysis:
        # 9 = BACKGROUND, 10 = TYPE, 11 = TEXTURE
        if not background_ocg:
            # Try to find OCG by checking the structure
            # OCGs are stored as objects, let's try accessing them directly
            try:
                # Check if OCG 9 exists and is BACKGROUND
                ocg_9_ref = doc.xref_get_key(9, "Name")
                if ocg_9_ref[0] == "name" and "BACKGROUND" in ocg_9_ref[1].upper():
                    background_ocg = 9
                    print(f"  ✓ Found BACKGROUND at OCG reference 9")
            except:
                pass
        
        if not texture_ocg:
            try:
                ocg_11_ref = doc.xref_get_key(11, "Name")
                if ocg_11_ref[0] == "name" and "TEXTURE" in ocg_11_ref[1].upper():
                    texture_ocg = 11
                    print(f"  ✓ Found TEXTURE at OCG reference 11")
            except:
                pass
        
        # Set up high-quality rendering
        zoom = 3.0  # 3x for high resolution (1944x1944px)
        mat = fitz.Matrix(zoom, zoom)
        
        print(f"\n📸 Rendering layers at {zoom}x resolution ({int(page.rect.width * zoom)}x{int(page.rect.height * zoom)}px)...\n")
        
        # Method 1: Try to use OCG visibility control
        if background_ocg and texture_ocg:
            print("Attempting OCG-based layer extraction...")
            
            # Get the OCG configuration
            ocg_config = doc.get_oc_config()
            
            # Try to create custom OCG configs
            try:
                # Render with only BACKGROUND visible
                ocg_config.set_ocg_usage(background_ocg, True)
                ocg_config.set_ocg_usage(texture_ocg, False)
                # Hide TYPE layer (OCG 10) if it exists
                try:
                    ocg_config.set_ocg_usage(10, False)
                except:
                    pass
                
                pix_bg = page.get_pixmap(matrix=mat, alpha=True, oc=ocg_config)
                bg_path = os.path.join(output_dir, "special-one-background.png")
                pix_bg.save(bg_path)
                print(f"  ✓ Saved: {bg_path}")
                
                # Render with only TEXTURE visible
                ocg_config.set_ocg_usage(background_ocg, False)
                ocg_config.set_ocg_usage(texture_ocg, True)
                try:
                    ocg_config.set_ocg_usage(10, False)
                except:
                    pass
                
                pix_texture = page.get_pixmap(matrix=mat, alpha=True, oc=ocg_config)
                texture_path = os.path.join(output_dir, "special-one-texture.png")
                pix_texture.save(texture_path)
                print(f"  ✓ Saved: {texture_path}")
                
                doc.close()
                print("\n" + "=" * 70)
                print("✅ SUCCESS: Layers extracted successfully!")
                print("=" * 70)
                return True
                
            except Exception as e:
                print(f"  ⚠️  OCG method failed: {e}")
                print("  Trying alternative method...\n")
        
        # Method 2: Alternative approach - render full page and use image processing
        # This is a fallback if OCG control doesn't work
        print("Using alternative extraction method...")
        print("⚠️  Note: This method renders the full page.")
        print("    For true layer separation, manual export from Illustrator")
        print("    may be necessary.\n")
        
        # Render full page as reference
        pix_full = page.get_pixmap(matrix=mat, alpha=True)
        full_path = os.path.join(output_dir, "special-one-all-layers-reference.png")
        pix_full.save(full_path)
        print(f"  ✓ Saved reference: {full_path} ({pix_full.width}x{pix_full.height}px)")
        
        # Since we can't easily separate layers programmatically,
        # let's try one more approach: using PDF content stream manipulation
        print("\n" + "=" * 70)
        print("⚠️  LIMITATION REACHED")
        print("=" * 70)
        print("\nProgrammatic layer extraction from Illustrator PDFs is complex.")
        print("The layers are stored as Optional Content Groups (OCGs), but")
        print("controlling their visibility requires deep PDF manipulation.")
        print("\nRECOMMENDED SOLUTION:")
        print("Since you mentioned you cannot do manual export, let me try")
        print("a different approach using image processing or PDF content")
        print("stream analysis...\n")
        
        # Try Method 3: Extract content streams and analyze
        try:
            import io
            from PIL import Image
            
            # Get the page's content stream
            content = page.read_contents()
            
            # Try to find layer-specific content
            # This is complex and may not work perfectly, but let's try
            
            print("Attempting content stream analysis...")
            # This would require parsing the PDF content stream which is very complex
            # For now, let's provide the reference image and instructions
            
        except ImportError:
            print("PIL/Pillow not available for advanced processing")
        
        doc.close()
        
        print("\n" + "=" * 70)
        print("📋 NEXT STEPS")
        print("=" * 70)
        print("\nI've created a reference image showing all layers combined.")
        print("\nFor true layer separation, we have a few options:")
        print("1. Use a PDF tool that supports OCG manipulation (like PDFtk)")
        print("2. Use image processing to separate layers (if they have distinct colors)")
        print("3. Use a service/API that can extract PDF layers")
        print("\nLet me try one more approach using a different method...\n")
        
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = extract_layers_advanced()
    sys.exit(0 if success else 1)
