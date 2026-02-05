import os
import re
import pymupdf4llm
import fitz
import yaml
import unicodedata
from pathlib import Path
import citation_scanner
import author_tools 

def clean_filename(stem):
    stem = re.sub(r'^[\d\-\.\_\s]+', '', stem)
    stem = re.sub(r'_[\d]{4,}$', '', stem)
    return stem.strip()

def repair_pali_fractures(text):
    pattern = r'_([a-zA-Z\-]+)_\s*([āīūḍḷṃṅṇṭñĀĪŪḌḶṂṄṆṬÑ])\s*_([a-zA-Z\-]+)_'
    text = re.sub(pattern, r'_\1\2\3_', text)
    text = re.sub(pattern, r'_\1\2\3_', text)
    return text

def extract_pdf_metadata(doc):
    try:
        meta = doc.metadata
        candidates = []
        if meta.get('subject'): candidates.append(meta['subject'])
        if meta.get('keywords'): candidates.append(meta['keywords'])
        combined = ", ".join(candidates)
        if "indesign" in combined.lower() or "microsoft" in combined.lower(): return "To_Fill"
        return combined if combined else "To_Fill"
    except: return "To_Fill"

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

def convert_pdf_to_md(source_path, dest_root, category="Dhamma", author_override=None):
    author, title = determine_author_and_title(source_path, author_override)

    # --- DYNAMIC SUBFOLDER & CONTRIBUTION LOGIC ---
    relative_path = Path("Books") # Default folder
    contribution_type = "book"    # Default metadata

    if author_override:
        for parent in source_path.parents:
            if author_tools.normalize(parent.name) == author_tools.normalize(author_override):
                try: 
                    full_rel = source_path.parent.relative_to(parent)
                    
                    # If file is directly in author folder, or redundant folder
                    if str(full_rel) == "." or author_tools.normalize(full_rel.name) == author_tools.normalize(author):
                         relative_path = Path("Books")
                         contribution_type = "book"
                    else:
                        relative_path = full_rel
                        # Use the folder name as the type (e.g. "Study Guides" -> "study guides")
                        contribution_type = str(full_rel).lower().replace("_", " ")
                except: pass
                break

    storage_author = author_tools.strip_accents(author_override) if author_override else author
    final_folder = dest_root / "Contributions" / category / storage_author / relative_path
    
    safe_filename = f"{author} - {title}.md".replace("/", "-").replace(":", "-")
    output_path = final_folder / safe_filename

    if output_path.exists():
        print(f"⏩ Skipping: {title} (Exists)")
        return

    print(f"📖 Converting: {title}...")
    try: doc = fitz.open(source_path)
    except: return

    extracted_theme = extract_pdf_metadata(doc)
    doc.close()

    md_text = pymupdf4llm.to_markdown(source_path, write_images=False) 
    md_text = repair_pali_fractures(md_text)
    md_text = re.sub(r'!\[.*?\]\(.*?\)', '', md_text)
    
    # Inject Text Links (No YAML extraction)
    md_text = citation_scanner.inject_wikilinks(md_text)
    
    frontmatter = {
        "title": title, 
        "author": author, 
        "category": category,
        "contribution": contribution_type, # <--- DYNAMIC LOWERCASE
        "theme": extracted_theme, 
        "topic": "To_Fill"
    }
    
    final_folder.mkdir(parents=True, exist_ok=True)
    final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n\n" + md_text
    
    with open(output_path, "w", encoding='utf-8') as f: f.write(final_content)
    print(f"✅ Finished: {output_path}")