import os
import shutil
import logging
from pathlib import Path
import yaml
import re

# Import our specialized tools
import pdf_converter
import citation_scanner
import epub_converter  # <--- NEW: Import the EPUB tool

# --- CONFIGURATION ---
REPO_ROOT = Path(__file__).resolve().parent.parent
INBOX = REPO_ROOT / "Inbox"
LIBRARY = REPO_ROOT / "Buddhist_Hub" / "Library"
CONTRIBUTIONS = REPO_ROOT / "Buddhist_Hub" / "Contributions"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_category(path):
    parts = path.parts
    if "Vinaya" in parts:
        return "Vinaya"
    elif "Dhamma" in parts:
        return "Dhamma"
    return "Dhamma"

def process_markdown(filepath):
    category = get_category(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        meta = {}
        body = content
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if match:
            try:
                meta = yaml.safe_load(match.group(1)) or {}
                body = match.group(2)
            except yaml.YAMLError:
                logging.warning(f"⚠️ Broken YAML in {filepath.name}. Overwriting.")

        filename = filepath.stem
        if " - " in filename and "author" not in meta:
            guessed_author, guessed_title = filename.split(" - ", 1)
            meta['author'] = meta.get('author', guessed_author)
            meta['title'] = meta.get('title', guessed_title)
        
        meta['title'] = meta.get('title', filename)
        meta['author'] = meta.get('author', 'Unknown')
        meta['category'] = category
        meta['contribution'] = meta.get('contribution', 'essay')

        suttas, vinaya = citation_scanner.extract_citations(body)
        meta['sutta_citations'] = suttas
        meta['vin_citations'] = vinaya

        new_yaml = yaml.dump(meta, sort_keys=False, allow_unicode=True)
        final_content = f"---\n{new_yaml}---\n\n{body}"

        dest_folder = CONTRIBUTIONS / category / "Essays" / meta['author']
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        safe_filename = "".join(c for c in meta['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        dest_path = dest_folder / f"{safe_filename}.md"

        with open(dest_path, "w", encoding='utf-8') as f:
            f.write(final_content)
        
        logging.info(f"✅ Processed Essay: {meta['title']} -> {category}")

    except Exception as e:
        logging.error(f"❌ Failed to process MD {filepath.name}: {e}")

def main():
    logging.info("🤖 Librarian: Starting Scan...")

    for root, _, files in os.walk(INBOX):
        for file in files:
            if file.startswith("."): continue
            
            filepath = Path(root) / file
            ext = filepath.suffix.lower()
            category = get_category(filepath)

            # 1. PDF Handling
            if ext == '.pdf':
                try:
                    pdf_converter.convert_pdf_to_md(filepath, LIBRARY, category)
                except Exception as e:
                    logging.error(f"❌ PDF Error {file}: {e}")

            # 2. Markdown Handling
            elif ext == '.md':
                process_markdown(filepath)

            # 3. EPUB Handling (NOW ACTIVE)
            elif ext == '.epub':
                try:
                    # <--- This is the new line that does the work
                    epub_converter.convert_epub_to_md(filepath, LIBRARY, category)
                except Exception as e:
                    logging.error(f"❌ EPUB Error {file}: {e}")
            
            else:
                logging.debug(f"Skipping unknown file: {file}")

    logging.info("💤 Librarian: Scan Complete.")

if __name__ == "__main__":
    main()