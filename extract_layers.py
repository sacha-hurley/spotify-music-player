#!/usr/bin/env python3
"""
Extract BACKGROUND and TEXTURE layers from page 5 of the Illustrator file.
Exports as high-resolution PNG images suitable for animation and video creation.
"""

import sys
import os

def extract_layers():
    """Extract BACKGROUND and TEXTURE layers from page 5"""
    
    ai_file = "/Users/sachahurley/Desktop/NOVEL_TEA_SINGLES (1).ai"
    output_dir = "/Users/sachahurley/spotify-music-player/public/images/special-one-layers"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("Layer Extraction Script")
    print("=" * 60)
    print(f"\nSource file: {ai_file}")
    print(f"Output directory: {output_dir}")
    print(f"\nTarget: Page 5 (Special One artboard)")
    print("Layers to extract: BACKGROUND, TEXTURE")
    print("\n" + "=" * 60)
    
    # Check if file exists
    if not os.path.exists(ai_file):
        print(f"\n❌ ERROR: File not found: {ai_file}")
        return False
    
    # Try to use PyMuPDF (fitz) for PDF layer extraction
    try:
        import fitz  # PyMuPDF
        print("\n✓ PyMuPDF found - attempting layer extraction...")
        
        # Open the PDF
        doc = fitz.open(ai_file)
        
        if len(doc) < 5:
            print(f"\n❌ ERROR: PDF only has {len(doc)} pages, need at least 5")
            doc.close()
            return False
        
        # Get page 5 (0-indexed, so page 4)
        page = doc[4]  # Page 5 is index 4
        
        print(f"\n✓ Opened page 5 (index 4)")
        print(f"  Page dimensions: {page.rect.width} x {page.rect.height} points")
        
        # Set up rendering parameters for high quality
        # Scale factor: 3x for high resolution (good for animation/video)
        # 648pt * 3 = 1944px (good for 30fps video)
        zoom = 3.0
        mat = fitz.Matrix(zoom, zoom)
        
        # Export full page (all layers visible) as reference
        print("\n📸 Rendering page 5 at high resolution...")
        
        # Render full page with all layers visible
        pix_all = page.get_pixmap(matrix=mat, alpha=True)
        full_path = os.path.join(output_dir, "special-one-all-layers-reference.png")
        pix_all.save(full_path)
        print(f"  ✓ Saved reference: {full_path}")
        print(f"    Resolution: {pix_all.width}x{pix_all.height}px")
        print(f"    Format: PNG with transparency")
        
        print("\n" + "=" * 60)
        print("📋 MANUAL EXPORT INSTRUCTIONS")
        print("=" * 60)
        print("\nFor best quality and proper layer separation, please export")
        print("the layers manually from Illustrator:")
        print("\n1. Open: /Users/sachahurley/Desktop/NOVEL_TEA_SINGLES (1).ai")
        print("2. Navigate to Artboard 5 (Special One)")
        print("3. Open the Layers panel (Window > Layers)")
        print("\n4. EXPORT BACKGROUND LAYER:")
        print("   - Hide TYPE layer (click the eye icon)")
        print("   - Hide TEXTURE layer (click the eye icon)")
        print("   - Keep BACKGROUND layer visible")
        print("   - File > Export > Export As...")
        print("   - Format: PNG")
        print("   - Resolution: 300 PPI (or higher)")
        print("   - Save as: special-one-background.png")
        print("   - Location: public/images/special-one-layers/")
        print("\n5. EXPORT TEXTURE LAYER:")
        print("   - Hide TYPE layer")
        print("   - Hide BACKGROUND layer")
        print("   - Keep TEXTURE layer visible")
        print("   - File > Export > Export As...")
        print("   - Format: PNG")
        print("   - Resolution: 300 PPI (or higher)")
        print("   - Save as: special-one-texture.png")
        print("   - Location: public/images/special-one-layers/")
        print("\n💡 TIP: For 30fps video animation, 300 PPI at 648pt gives")
        print("   you ~1944x1944px images, which is excellent quality.")
        print("\n" + "=" * 60)
        
        doc.close()
        return True
        
    except ImportError:
        print("\n⚠️  PyMuPDF not installed")
        print("\nInstalling PyMuPDF...")
        os.system(f"{sys.executable} -m pip install PyMuPDF --quiet")
        
        # Try again
        try:
            import fitz
            return extract_layers()  # Recursive call after install
        except ImportError:
            print("\n❌ Failed to install PyMuPDF")
            print("\nPlease install manually: pip install PyMuPDF")
            return False
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = extract_layers()
    sys.exit(0 if success else 1)
