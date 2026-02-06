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
    stem = re.sub(r'^[\d\-\.\_\s]+', '', stem)
    stem = re.sub(r'_[\d]{4,}$', '', stem)
    return stem.strip()

def determine_author_and_title(source_path, author_override):
    original_stem = source_path.stem
    if " - " in original_stem:
        file_author_part, file_title_part = original_stem.split(" - ", 1)
        final_author = author_tools.normalize(file_author_part)
        final_title = clean_filename(file_title_part)
    elif author_override:
        final_author = author_tools.strip_accents(author_override)
        final_title = clean_filename(original_stem)
    else:
        final_author = "Unknown"
        final_title = clean_filename(original_stem)
    final_title = author_tools.strip_accents(final_title)
    return final_author, final_title

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
    author, title = determine_author_and_title(filepath, author_override)
    ext = filepath.suffix.lower()

    # --- DYNAMIC FOLDER LOGIC ---
    relative_path = Path("Books") 
    contribution_type = "book"

    if author_override:
        for parent in filepath.parents:
            if author_tools.normalize(parent.name) == author_tools.normalize(author_override):
                try: 
                    full_rel = filepath.parent.relative_to(parent)
                    if str(full_rel) == "." or author_tools.normalize(full_rel.name) == author_tools.normalize(author):
                         relative_path = Path("Books")
                         contribution_type = "book"
                    else:
                        relative_path = full_rel
                        contribution_type = str(full_rel).lower().replace("_", " ")
                except: pass
                break

    storage_author = author_tools.strip_accents(author_override) if author_override else author
    author_folder = dest_root / "Contributions" / category / storage_author / relative_path
    
    attachment_folder = author_folder / "attachments"
    attachment_folder.mkdir(parents=True, exist_ok=True)

    print(f"🔍 Reference Stub: {title}...")

    raw_text = ""
    if ext == '.pdf': raw_text = extract_text_from_pdf(filepath)
    elif ext == '.epub': raw_text = extract_text_from_epub(filepath)
    
    suttas, vinaya = citation_scanner.extract_citations(raw_text)
    
    dest_file = attachment_folder / filepath.name
    
    # --- LOGIC: OVERWRITE ATTACHMENT IN LIBRARY, KEEP IN INBOX ---
    if dest_file.exists():
        print(f"   ⚠️ Attachment exists, overwriting: {dest_file.name}")
    
    # Use copy2 (Copy metadata + file) instead of move
    shutil.copy2(str(filepath), str(dest_file))

    frontmatter = {
        "title": title, 
        "author": author, 
        "category": category,
        "contribution": contribution_type, 
        "status": "reference_only",
        "theme": "To_Fill", 
        "topic": "To_Fill",
        "sutta_citations": suttas, 
        "vin_citations": vinaya
    }

    md_content = f"""---
{yaml.dump(frontmatter, sort_keys=False)}---
# {title}

> [!INFO] Reference Only
> This file is available as an attachment below.

![[{filepath.name}]]
"""
    safe_filename = f"{author} - {title}.md".replace("/", "-").replace(":", "-")
    output_path = author_folder / safe_filename
    
    with open(output_path, "w", encoding='utf-8') as f: f.write(md_content)
    print(f"✅ Stub Created: {safe_filename}")