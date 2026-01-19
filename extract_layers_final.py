#!/usr/bin/env python3
"""
Final layer extraction script - modifies OCG visibility to extract individual layers.
"""

import sys
import os
import copy

def extract_layers_final():
    """Extract BACKGROUND and TEXTURE layers by controlling OCG visibility"""
    
    ai_file = "/Users/sachahurley/Desktop/NOVEL_TEA_SINGLES (1).ai"
    output_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 70)
    print("Layer Extraction - Artboard 5 (Special One)")
    print("=" * 70)
    print(f"\nSource: {ai_file}")
    print(f"Output: {output_dir}\n")
    
    if not os.path.exists(ai_file):
        print(f"❌ ERROR: File not found")
        return False
    
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("⚠️  Installing PyMuPDF...")
        os.system(f"{sys.executable} -m pip install PyMuPDF --quiet")
        import fitz
    
    try:
        # Open the PDF
        doc = fitz.open(ai_file)
        print(f"✓ Opened PDF: {len(doc)} pages")
        
        if len(doc) < 5:
            print(f"❌ ERROR: Need at least 5 pages")
            doc.close()
            return False
        
        page = doc[4]  # Page 5
        print(f"✓ Loaded page 5")
        print(f"  Dimensions: {page.rect.width} x {page.rect.height} points\n")
        
        # Get OCGs
        ocgs_info = doc.get_ocgs()
        print(f"✓ Found {len(ocgs_info.get('ocgs', {}))} Optional Content Groups")
        
        # Find OCG xrefs by name
        # Based on our analysis: 9=BACKGROUND, 10=TYPE, 11=TEXTURE
        background_xref = None
        texture_xref = None
        type_xref = 10  # We know this exists
        
        # Verify OCG names
        for ocg_xref, ocg_dict in ocgs_info.get('ocgs', {}).items():
            ocg_name = None
            try:
                # Try to get name from OCG object
                ocg_obj = doc.xref_object(ocg_xref)
                if "/Name" in ocg_obj:
                    ocg_name = ocg_obj["/Name"]
                    print(f"  - OCG {ocg_xref}: {ocg_name}")
                    if "BACKGROUND" in str(ocg_name).upper():
                        background_xref = ocg_xref
                    elif "TEXTURE" in str(ocg_name).upper():
                        texture_xref = ocg_xref
            except Exception as e:
                # Try alternative method
                try:
                    name_key = doc.xref_get_key(ocg_xref, "Name")
                    if name_key[0] == "name":
                        ocg_name = name_key[1].strip("()")
                        if "BACKGROUND" in ocg_name.upper():
                            background_xref = ocg_xref
                        elif "TEXTURE" in ocg_name.upper():
                            texture_xref = ocg_xref
                except:
                    pass
        
        # Fallback: use known xrefs
        if not background_xref:
            background_xref = 9
            print(f"  ✓ Using OCG 9 for BACKGROUND")
        if not texture_xref:
            texture_xref = 11
            print(f"  ✓ Using OCG 11 for TEXTURE")
        
        # High-quality rendering
        zoom = 3.0
        mat = fitz.Matrix(zoom, zoom)
        target_size = (int(page.rect.width * zoom), int(page.rect.height * zoom))
        print(f"\n📸 Rendering at {zoom}x ({target_size[0]}x{target_size[1]}px)\n")
        
        # Method: Create a temporary document with modified OCG visibility
        # We'll create copies and modify OCG states
        
        # Get the OCProperties to understand the structure
        try:
            oc_props = doc.xref_get_key(doc.pdf_catalog(), "OCProperties")
            if oc_props[0] == "dict":
                oc_props_xref = oc_props[1]
                print(f"✓ Found OCProperties at xref {oc_props_xref}")
        except:
            oc_props_xref = None
        
        # Approach: Modify OCG Usage dictionaries to control visibility
        # Get OCG objects and modify their visibility
        
        def set_ocg_visibility(ocg_xref, visible):
            """Set OCG visibility by modifying its Usage dictionary"""
            try:
                ocg_obj = doc.xref_object(ocg_xref)
                # OCGs have a Usage dictionary that controls visibility
                # We need to modify the /ON array in the Usage/View
                # This is complex, so let's try a simpler approach
                return True
            except:
                return False
        
        # Alternative: Use OCMD (Optional Content Membership Dictionary)
        # Create OCMDs that control which OCGs are visible
        
        print("Attempting layer extraction via OCG control...\n")
        
        # Try Method 1: Render with OCMD
        try:
            # Create OCMD for BACKGROUND only
            bg_ocmd_xref = doc.set_ocmd(
                ocgs=[background_xref],
                policy="AllOn"  # All specified OCGs must be on
            )
            
            pix_bg = page.get_pixmap(matrix=mat, alpha=True, oc=bg_ocmd_xref)
            bg_path = os.path.join(output_dir, "special-one-background.png")
            pix_bg.save(bg_path)
            print(f"  ✓ Saved BACKGROUND: {bg_path} ({pix_bg.width}x{pix_bg.height}px)")
            
            # Create OCMD for TEXTURE only
            texture_ocmd_xref = doc.set_ocmd(
                ocgs=[texture_xref],
                policy="AllOn"
            )
            
            pix_texture = page.get_pixmap(matrix=mat, alpha=True, oc=texture_ocmd_xref)
            texture_path = os.path.join(output_dir, "special-one-texture.png")
            pix_texture.save(texture_path)
            print(f"  ✓ Saved TEXTURE: {texture_path} ({pix_texture.width}x{pix_texture.height}px)")
            
            doc.close()
            print("\n" + "=" * 70)
            print("✅ SUCCESS: Layers extracted!")
            print("=" * 70)
            return True
            
        except Exception as e:
            print(f"  ⚠️  OCMD method failed: {e}")
            print("  Trying alternative approach...\n")
        
        # Method 2: Modify document OCG states, render, restore
        print("Trying document modification approach...\n")
        
        # Save original OCG states
        original_states = {}
        for ocg_xref in [background_xref, texture_xref, type_xref]:
            try:
                ocg_obj = doc.xref_object(ocg_xref)
                original_states[ocg_xref] = copy.deepcopy(ocg_obj)
            except:
                pass
        
        # Render BACKGROUND only
        try:
            # Hide TYPE and TEXTURE, show BACKGROUND
            # Modify OCG Usage/View/ON
            for ocg_xref in [background_xref, texture_xref, type_xref]:
                try:
                    ocg_obj = doc.xref_object(ocg_xref)
                    # OCG visibility is controlled by the /ON key in Usage/View
                    # This is nested, so we need to modify it carefully
                    # For now, let's try a different approach
                except:
                    pass
            
            # Actually, modifying OCGs in-place is risky
            # Let's try using the OCProperties D dictionary
            
        except Exception as e:
            print(f"  ⚠️  Modification approach failed: {e}\n")
        
        # Method 3: Use PDF content stream filtering
        # This is very complex and may not work perfectly
        
        # For now, let's render what we can and provide guidance
        print("Rendering full page as reference...\n")
        pix_full = page.get_pixmap(matrix=mat, alpha=True)
        full_path = os.path.join(output_dir, "special-one-all-layers-reference.png")
        pix_full.save(full_path)
        print(f"  ✓ Saved reference: {full_path}")
        
        doc.close()
        
        print("\n" + "=" * 70)
        print("⚠️  CHALLENGE")
        print("=" * 70)
        print("\nProgrammatic layer extraction from Illustrator PDFs is complex.")
        print("The OCG visibility control requires deep PDF manipulation.")
        print("\nLet me try one more approach using a different tool...\n")
        
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = extract_layers_final()
    sys.exit(0 if success else 1)
