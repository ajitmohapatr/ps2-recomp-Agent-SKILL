import sys
import argparse
import os

try:
    import fitz  # PyMuPDF
except ImportError:
    print("CRITICAL: PyMuPDF is required but not installed.")
    print("Agent, you must run: pip install PyMuPDF")
    sys.exit(1)

def extract_page_as_image(pdf_path, page_num, output_path, dpi=300):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return False

    # Adjust for 0-indexed internal structure vs 1-indexed user input
    # Most users/agents say "Page 112" referencing what's on the page.
    # We will assume page_num is 0-indexed as passed by the script arguments.
    if page_num < 0 or page_num >= len(doc):
        print(f"Error: Page number {page_num} is out of bounds for document with {len(doc)} pages.")
        doc.close()
        return False

    try:
        page = doc.load_page(page_num)
        
        # Set zoom matrix for high resolution (default 300 DPI)
        zoom = dpi / 72.0 
        mat = fitz.Matrix(zoom, zoom)
        
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        pix.save(output_path)
        print(f"✅ Successfully extracted page {page_num} to {output_path} at {dpi} DPI.")
        return True
    except Exception as e:
        print(f"Error extracting image: {e}")
        return False
    finally:
        doc.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract a specific PDF page as a high-res image for Multimodal Vision.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("page_num", type=int, help="0-based page index to extract (e.g. 0 for the first page)")
    parser.add_argument("output_path", help="Path to save the resulting .png file (WARNING: ALWAYS USE 'png/' DIRECTORY TO PRESERVE ROOT CLEANLINESS)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for the output image (default: 300)")
    
    args = parser.parse_args()
    extract_page_as_image(args.pdf_path, args.page_num, args.output_path, args.dpi)
