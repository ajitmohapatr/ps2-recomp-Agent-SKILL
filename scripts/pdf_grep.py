import sys
import argparse

try:
    import fitz  # PyMuPDF
    import pymupdf4llm
except ImportError:
    print("CRITICAL: Required mapping libraries are missing.")
    print("Agent, you must run: pip install pymupdf4llm")
    sys.exit(1)

def search_pdf(pdf_path, query, max_pages=3):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return

    query_lower = query.lower()
    matching_pages = []

    print(f"Scanning {pdf_path} for '{query}'...")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        if text and query_lower in text.lower():
            matching_pages.append(page_num)

    doc.close()

    if not matching_pages:
        print(f"No matches found for '{query}' in {pdf_path}")
        return

    print(f"Found matches on {len(matching_pages)} pages: {matching_pages}")
    
    if len(matching_pages) > max_pages:
        print(f"\n[⚠️  CONTEXT PROTECTION TRIGGERED ⚠️]")
        print(f"Query returned too many pages ({len(matching_pages)} pages).")
        print(f"To protect the LLM context window from collapsing, extraction is blocked.")
        print(f"Please refine your search query to be highly specific (e.g., instead of 'DMA', use 'DMA Channel 4').")
        return

    print(f"\nExtracting EXACT Markdown (including tables) for the matching pages...\n")
    
    for page_num in matching_pages:
        print(f"--- START OF PAGE {page_num + 1} (index {page_num}) ---")
        try:
            # pymupdf4llm uses 0-based page indexing
            md_text = pymupdf4llm.to_markdown(pdf_path, pages=[page_num])
            print(md_text.strip())
        except Exception as e:
            print(f"Error extracting markdown for page {page_num}: {e}")
        print(f"--- END OF PAGE {page_num + 1} ---\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standalone PDF Markdown extraction for LLMs. Preserves Tables.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("query", help="Text to search for")
    parser.add_argument("-m", "--max_pages", type=int, default=4, help="Maximum number of pages to extract before triggering context protection limit")
    
    args = parser.parse_args()
    search_pdf(args.pdf_path, args.query, args.max_pages)
