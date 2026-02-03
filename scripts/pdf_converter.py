import os
import re
import pymupdf4llm
import fitz
import yaml
import unicodedata
from collections import Counter
from pathlib import Path
import citation_scanner
import author_tools 

def clean_filename(stem):
    cleaned = re.sub(r'^[\d\-\.\_\s]+', '', stem)
    return cleaned if cleaned else stem

def identify_footnotes_by_size(doc):
    font_sizes = []
    # Sample first 10 pages for body text size
    for page in doc[:10]:
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                for line in b["lines"]:
                    for span in line["spans"]:
                        font_sizes.append(round(span["size"]))
    
    if not font_sizes: return []
    common_size = Counter(font_sizes).most_common(1)[0][0]
    footnote_threshold = common_size - 1.5 

    footnotes = []
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if "lines" in b:
                try:
                    first_span = b["lines"][0]["spans"][0]
                    if first_span["size"] < footnote_threshold:
                        text = "".join([s["text"] for line in b["lines"] for s in line["spans"]]).strip()
                        if re.match(r'^\d+\.', text) or len(text) > 5:
                            footnotes.append(text)
                except: continue
    return footnotes

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
        author = author_tools.normalize(author_override)
        title = clean_filename(original_stem)
    else:
        if " - " in original_stem:
            raw_author, raw_title = original_stem.split(" - ", 1)
            author = author_tools.normalize(raw_author)
            title = raw_title
        else:
            author = "Unknown"
            title = clean_filename(original_stem)

    # Force ASCII-Safe Unicode Normalization (NFC usually fine, but our tools strip accents)
    author = author_tools.strip_accents(author)
    title = author_tools.strip_accents(title)

    book_folder = dest_root / category / "Books" / author / title
    safe_filename = f"{author} - {title}.md".replace("/", "-").replace(":", "-")
    output_path = book_folder / safe_filename

    if output_path.exists():
        print(f"⏩ Skipping: {title} (Exists)")
        return

    print(f"📖 Converting: {title}...")
    try: doc = fitz.open(source_path)
    except: return

    extracted_footnotes = identify_footnotes_by_size(doc)
    extracted_theme = extract_pdf_metadata(doc)
    doc.close()

    md_text = pymupdf4llm.to_markdown(source_path, write_images=False) 
    md_text = re.sub(r'!\[.*?\]\(.*?\)', '', md_text)
    md_text = citation_scanner.inject_wikilinks(md_text)
    suttas, vinaya = citation_scanner.extract_citations(md_text)
    
    if extracted_footnotes:
        footnote_section = "\n\n---\n\n## Reference Notes (Extracted)\n> [!info] These notes were detected by font size.\n\n"
        for fn in extracted_footnotes:
            fn_formatted = re.sub(r'^(\d+)\.', r'**\1.**', fn)
            footnote_section += f"{fn_formatted}\n\n"
        md_text += footnote_section

    frontmatter = {
        "title": title, "author": author, "category": category,
        "contribution": "book", "theme": extracted_theme, "topic": "To_Fill",
        "sutta_citations": suttas, "vin_citations": vinaya
    }
    
    book_folder.mkdir(parents=True, exist_ok=True)
    final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n\n" + md_text
    
    with open(output_path, "w", encoding='utf-8') as f: f.write(final_content)
    print(f"✅ Finished: {output_path}")