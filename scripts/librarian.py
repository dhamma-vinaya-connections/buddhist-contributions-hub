import os
import shutil
import logging
from pathlib import Path
import yaml
import re

# Import our specialized tools
import pdf_converter
import citation_scanner

# --- CONFIGURATION ---
# Define the Root Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
INBOX = REPO_ROOT / "Inbox"
LIBRARY = REPO_ROOT / "Buddhist_Hub" / "Library"
CONTRIBUTIONS = REPO_ROOT / "Buddhist_Hub" / "Contributions"

# Setup Logging (So we know what happened)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_category(path):
    """
    Determines if file is 'Dhamma' or 'Vinaya' based on folder structure.
    Expects path like: .../Inbox/Vinaya/pdf/Book.pdf
    """
    parts = path.parts
    if "Vinaya" in parts:
        return "Vinaya"
    elif "Dhamma" in parts:
        return "Dhamma"
    return "Dhamma" # Default

def process_markdown(filepath):
    """
    Moves Markdown files from Inbox -> Contributions
    Injects: split citations + category
    """
    category = get_category(filepath)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Parse Existing Metadata (if any)
        meta = {}
        body = content
        # Regex to separate YAML frontmatter from body
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if match:
            try:
                meta = yaml.safe_load(match.group(1)) or {}
                body = match.group(2)
            except yaml.YAMLError:
                logging.warning(f"⚠️ Broken YAML in {filepath.name}. Overwriting.")

        # 2. Extract Data
        filename = filepath.stem
        # If user didn't provide Author/Title, try to guess from filename "Author - Title"
        if " - " in filename and "author" not in meta:
            guessed_author, guessed_title = filename.split(" - ", 1)
            meta['author'] = meta.get('author', guessed_author)
            meta['title'] = meta.get('title', guessed_title)
        
        # Defaults
        meta['title'] = meta.get('title', filename)
        meta['author'] = meta.get('author', 'Unknown')
        meta['category'] = category
        meta['contribution'] = meta.get('contribution', 'essay') # Default for MD is essay

        # 3. Inject Citations (The Nexus)
        suttas, vinaya = citation_scanner.extract_citations(body)
        meta['sutta_citations'] = suttas
        meta['vin_citations'] = vinaya

        # 4. Rebuild File
        new_yaml = yaml.dump(meta, sort_keys=False, allow_unicode=True)
        final_content = f"---\n{new_yaml}---\n\n{body}"

        # 5. Save to Destination
        # Logic: Contributions/{Category}/Essays/{Author}/{Title}.md
        dest_folder = CONTRIBUTIONS / category / "Essays" / meta['author']
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        # Clean filename for saving
        safe_filename = "".join(c for c in meta['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        dest_path = dest_folder / f"{safe_filename}.md"

        with open(dest_path, "w", encoding='utf-8') as f:
            f.write(final_content)
        
        logging.info(f"✅ Processed Essay: {meta['title']} -> {category}")

    except Exception as e:
        logging.error(f"❌ Failed to process MD {filepath.name}: {e}")

def main():
    logging.info("🤖 Librarian: Starting Scan...")

    # Walk through the Inbox
    for root, _, files in os.walk(INBOX):
        for file in files:
            if file.startswith("."): continue # Skip .DS_Store
            
            filepath = Path(root) / file
            ext = filepath.suffix.lower()
            category = get_category(filepath)

            # --- ROUTING LOGIC ---
            
            # 1. PDF Handling (Books)
            if ext == '.pdf':
                # Check if already exists in Library to avoid re-processing
                # (Simple check: does the folder exist?)
                # Note: This is a loose check. For now, we overwrite.
                try:
                    pdf_converter.convert_pdf_to_md(filepath, LIBRARY, category)
                except Exception as e:
                    logging.error(f"❌ PDF Error {file}: {e}")

            # 2. Markdown Handling (Essays)
            elif ext == '.md':
                process_markdown(filepath)

            # 3. EPUB Handling (Coming Soon)
            elif ext == '.epub':
                logging.info(f"⏳ EPUB detected (Converter not ready): {file}")
            
            else:
                logging.debug(f"Skipping unknown file: {file}")

    logging.info("💤 Librarian: Scan Complete.")

if __name__ == "__main__":
    main()