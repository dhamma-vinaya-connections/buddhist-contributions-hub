import os
import re
import pymupdf4llm
import fitz
import yaml
import unicodedata
from pathlib import Path
import citation_scanner
import author_tools 
import gatekeeper 

def clean_and_format_title(text):
    text = str(Path(text).stem)
    text = re.sub(r'^[\d\-\.\_\s]+', '', text)
    text = re.sub(r'[_.\s-]*\d{4,}[_.\s-]*$', '', text) 
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    text = text.replace("_", " ").replace("-", " ")
    return text.strip().title()

def determine_author_and_title(source_path, author_override):
    original_stem = source_path.stem
    if " - " in original_stem:
        file_title_part, file_author_part = original_stem.split(" - ", 1)
        final_author = author_tools.normalize_author(file_author_part)
        final_title = clean_and_format_title(file_title_part)
    elif author_override:
        final_author = author_tools.normalize_author(author_override)
        final_title = clean_and_format_title(original_stem)
    else:
        final_author = "Unknown"
        final_title = clean_and_format_title(original_stem)
    return final_author, final_title

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
        if "indesign" in combined.lower() or "microsoft" in combined.lower(): return "to_fill"
        return combined if combined else "to_fill"
    except: return "to_fill"

def convert_pdf_to_md(source_path, dest_root, category="dhamma", author_override=None):
    author, title = determine_author_and_title(source_path, author_override)

    relative_path = Path("Books") 
    contribution_type = "book"
    if author_override:
        for parent in source_path.parents:
            if author_tools.clean_text(parent.name) == author_tools.clean_text(author_override):
                try: 
                    full_rel = source_path.parent.relative_to(parent)
                    if str(full_rel) == "." or author_tools.clean_text(full_rel.name) == author_tools.clean_text(author):
                         relative_path = Path("Books")
                         contribution_type = "book"
                    else:
                        relative_path = full_rel
                        contribution_type = author_tools.normalize_type(full_rel.name)
                except: pass
                break

    storage_author = author_tools.normalize_author(author_override) if author_override else author
    final_folder = dest_root / "Contributions" / author_tools.make_singular(category) / storage_author / relative_path
    
    safe_filename = f"{title} - {author}.md".replace("/", "-").replace(":", "-")
    output_path = final_folder / safe_filename

    if output_path.exists():
        print(f"⏩ Skipping: {title} (Exists)")
        return

    print(f"📖 Converting: {title}...")
    try: doc = fitz.open(source_path)
    except: return

    extracted_theme = extract_pdf_metadata(doc)
    doc.close()

    try:
        md_text = pymupdf4llm.to_markdown(source_path, write_images=False) 
    except: return

    if len(md_text.strip()) < 50:
        gatekeeper.reject_and_delete(source_path, "Empty text (Likely Image Scan)")
        return

    md_text = repair_pali_fractures(md_text)
    md_text = re.sub(r'!\[.*?\]\(.*?\)', '', md_text)
    md_text = citation_scanner.inject_wikilinks(md_text)
    
    word_count = citation_scanner.count_words(md_text)
    citation_count = citation_scanner.get_citation_count(md_text)
    required_citations = gatekeeper.get_quality_threshold(word_count)
    
    if citation_count < required_citations:
        gatekeeper.reject_and_delete(source_path, f"Low Quality (Words: {word_count}, Refs: {citation_count}/{required_citations})")
        return 

    # 🌟 SINGULAR TOPICS
    if extracted_theme and extracted_theme != "to_fill":
        topic_list = [author_tools.make_singular(t) for t in extracted_theme.split(',')]
        final_topic = ", ".join(topic_list)
    else:
        final_topic = "to_fill"

    frontmatter = {
        "title": title, 
        "author": author, 
        "category": author_tools.make_singular(category),
        "contribution": contribution_type,
        "topic": final_topic
    }
    
    final_folder.mkdir(parents=True, exist_ok=True)
    final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n\n" + md_text
    
    with open(output_path, "w", encoding='utf-8') as f: f.write(final_content)
    print(f"✅ Finished: {output_path}")