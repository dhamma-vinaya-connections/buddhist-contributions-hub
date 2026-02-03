import os
import logging
import author_tools
from pathlib import Path

# --- THE TEAM ---
import pdf_converter
import epub_converter
import reference_scanner

# --- CONFIGURATION ---
REPO_ROOT = Path(__file__).resolve().parent.parent
INBOX = REPO_ROOT / "Inbox"
OUTPUT_ROOT = REPO_ROOT / "Buddhist_Hub"
LIBRARY = OUTPUT_ROOT / "Library"
CONTRIBUTIONS = OUTPUT_ROOT / "Contributions"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def parse_path_context(filepath):
    parts = filepath.parts
    
    # 1. Determine Category
    category = "Dhamma"
    for part in parts:
        if part.lower() == "vinaya":
            category = "Vinaya"
            break
            
    # 2. Determine Author from Folder
    parent_folder = filepath.parent.name
    system_folders = ["pdf", "epub", "md", "reference only", "reference_only", "others", "vinaya", "dhamma", "inbox"]
    
    if parent_folder.lower() not in system_folders:
        author = author_tools.normalize(parent_folder)
    else:
        author = None
        
    return category, author

def main():
    logging.info("🤖 Librarian: Starting Scan...")

    for root, _, files in os.walk(INBOX):
        if "/." in root or "\\." in root: continue

        for file in files:
            if file.startswith("."): continue
            
            filepath = Path(root) / file
            ext = filepath.suffix.lower()
            path_str = str(filepath).lower()
            
            category, author_override = parse_path_context(filepath)

            # LANE 1: REFERENCE ONLY
            if "reference only" in path_str or "reference_only" in path_str:
                try: reference_scanner.process_reference_file(filepath, LIBRARY, category, author_override)
                except Exception as e: logging.error(f"❌ Reference Error {file}: {e}")
                continue

            # LANE 2: PDF
            if ext == '.pdf':
                try: pdf_converter.convert_pdf_to_md(filepath, LIBRARY, category, author_override)
                except Exception as e: logging.error(f"❌ PDF Error {file}: {e}")

            # LANE 3: EPUB
            elif ext == '.epub':
                try: epub_converter.convert_epub_to_md(filepath, LIBRARY, category, author_override)
                except Exception as e: logging.error(f"❌ EPUB Error {file}: {e}")

    logging.info("💤 Librarian: Scan Complete.")

if __name__ == "__main__":
    main()