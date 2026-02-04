import os
import shutil
import fitz
import yaml
import re
from pathlib import Path
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import citation_scanner
import author_tools 

def clean_filename(stem):
    # 1. Remove Leading numbering
    stem = re.sub(r'^[\d\-\.\_\s]+', '', stem)
    # 2. Remove Trailing "Junk IDs" (Underscore + 4+ digits)
    stem = re.sub(r'_[\d]{4,}$', '', stem)
    return stem.strip()

def extract_text_from_pdf(filepath):
    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc: text += page.get_text() + " "
        return text
    except: return ""

def extract_text_from_epub(filepath):
    try:
        book = epub.read_epub(filepath)
        text = ""
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text += soup.get_text() + " "
        return text
    except: return ""

def process_reference_file(filepath, dest_root, category, author_override=None):
    original_stem = filepath.stem
    ext = filepath.suffix.lower()
    
    if author_override:
        author = author_tools.strip_accents(author_override)
        title = clean_filename(original_stem)
    else:
        if " - " in original_stem:
            raw_author, raw_title = original_stem.split(" - ", 1)
            author = author_tools.normalize(raw_author)
            title = raw_title
        else:
            author = "Unknown"
            title = clean_filename(original_stem)
    
    title = author_tools.strip_accents(title)

    # --- SUBFOLDER MIRRORING ---
    relative_path = Path("")
    if author_override:
        for parent in filepath.parents:
            if author_tools.normalize(parent.name) == author_tools.normalize(author_override):
                try: relative_path = filepath.parent.relative_to(parent)
                except: pass
                break

    author_folder = dest_root / category / "Books" / author / relative_path
    attachment_folder = author_folder / "attachments"
    attachment_folder.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Reference Stub: {title}...")

    raw_text = ""
    if ext == '.pdf': raw_text = extract_text_from_pdf(filepath)
    elif ext == '.epub': raw_text = extract_text_from_epub(filepath)
    
    suttas, vinaya = citation_scanner.extract_citations(raw_text)
    
    dest_file = attachment_folder / filepath.name
    shutil.move(str(filepath), str(dest_file))

    frontmatter = {
        "title": title, "author": author, "category": category,
        "contribution": "book", "status": "reference_only",
        "theme": "To_Fill", "topic": "To_Fill",
        "sutta_citations": suttas, "vin_citations": vinaya
    }

    md_content = f"""---
{yaml.dump(frontmatter, sort_keys=False)}---
# {title}

> [!INFO] Reference Only
> This file is available as an attachment below.

![[{filepath.name}]]
"""

    safe_filename = f"{author} - {title}.md".replace("/", "-").replace(":", "-")
    with open(author_folder / safe_filename, "w", encoding='utf-8') as f: f.write(md_content)

    print(f"✅ Stub Created: {safe_filename}")