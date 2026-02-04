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
    # 1. Remove Leading numbering
    stem = re.sub(r'^[\d\-\.\_\s]+', '', stem)
    # 2. Remove Trailing "Junk IDs" (Underscore + 4+ digits)
    stem = re.sub(r'_[\d]{4,}$', '', stem)
    return stem.strip()

def repair_pali_fractures(text):
    """
    Fixes words broken by font switches in PDFs.
    Example: "_Majjhima-nik_ ā _ya_" -> "_Majjhima-nikāya_"
    """
    # Regex explanation:
    # 1. Matches italicized text ending in _ (_abc_)
    # 2. Matches a single Pali char floating in space ( ā )
    # 3. Matches italicized text starting in _ (_xyz_)
    # We stitch them together into one italicized block: _abcāxyz_
    
    pattern = r'_([a-zA-Z\-]+)_\s*([āīūḍḷṃṅṇṭñĀĪŪḌḶṂṄṆṬÑ])\s*_([a-zA-Z\-]+)_'
    
    # Run it twice to catch multiple fractures in one word
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

def convert_pdf_to_md(source_path, dest_root, category="Dhamma", author_override=None):
    original_stem = source_path.stem
    
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

    # --- SMART FLATTENING ---
    relative_path = Path("")
    if author_override:
        for parent in source_path.parents:
            if author_tools.normalize(parent.name) == author_tools.normalize(author_override):
                try: 
                    candidate_rel = source_path.parent.relative_to(parent)
                    folder_name = candidate_rel.name.lower().replace(" ", "").replace("_", "")
                    book_name = title.lower().replace(" ", "").replace("_", "")
                    
                    if folder_name == book_name:
                        relative_path = Path("") 
                    else:
                        relative_path = candidate_rel
                except: pass
                break

    final_folder = dest_root / category / "Books" / author / relative_path
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

    # 1. CONVERT
    md_text = pymupdf4llm.to_markdown(source_path, write_images=False) 
    
    # 2. REPAIR FRACTURES (Fix the spacing issues)
    md_text = repair_pali_fractures(md_text)

    # 3. CLEANUP
    md_text = re.sub(r'!\[.*?\]\(.*?\)', '', md_text)
    
    # 4. INJECT LINKS (Using Strict Scanner)
    md_text = citation_scanner.inject_wikilinks(md_text)
    suttas, vinaya = citation_scanner.extract_citations(md_text)
    
    frontmatter = {
        "title": title, "author": author, "category": category,
        "contribution": "book", "theme": extracted_theme, "topic": "To_Fill",
        "sutta_citations": suttas, "vin_citations": vinaya
    }
    
    final_folder.mkdir(parents=True, exist_ok=True)
    final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n\n" + md_text
    
    with open(output_path, "w", encoding='utf-8') as f: f.write(final_content)
    print(f"✅ Finished: {output_path}")