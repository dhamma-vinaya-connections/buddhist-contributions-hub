import os
import yaml
import re
import unicodedata
from pathlib import Path
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup, Comment, NavigableString
import citation_scanner
import author_tools

def clean_filename(stem):
    # 1. Remove Leading numbering
    stem = re.sub(r'^[\d\-\.\_\s]+', '', stem)
    # 2. Remove Trailing "Junk IDs" (Underscore + 4+ digits)
    # Keeps volumes (space + 1 digit), removes IDs (_251013)
    stem = re.sub(r'_[\d]{4,}$', '', stem)
    return stem.strip()

def extract_epub_metadata(book):
    try:
        subjects = book.get_metadata('DC', 'subject')
        descriptions = book.get_metadata('DC', 'description')
        hints = []
        for s in subjects:
            if isinstance(s, tuple): hints.append(s[0])
            else: hints.append(str(s))
        if not hints and descriptions:
            desc = descriptions[0][0] if isinstance(descriptions[0], tuple) else str(descriptions[0])
            if len(desc) < 150: hints.append(desc)
        return ", ".join(hints) if hints else "To_Fill"
    except: return "To_Fill"

def clean_junk_text(text):
    junk_patterns = [
        r"xml version=['\"]1.0['\"].*?\?", r"html #include virtual=.*", r"#include virtual=.*",
        r"________ALL SCRIPTS BELOW HERE________", r"end:content", r"end:container",
        r"Cover end cover", r"#Cover"
    ]
    for pattern in junk_patterns: text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def process_internal_links_and_anchors(soup):
    for tag in soup.find_all(True):
        if tag.has_attr('id') and tag.get_text(strip=True):
            tag.append(f" ^{tag['id']}")

    for a in soup.find_all('a'):
        if a.has_attr('href'):
            href = a['href']
            text = a.get_text()
            if '#' in href and not href.startswith('http'):
                anchor_id = href.split('#')[-1]
                a.replace_with(f"[[#^{anchor_id}|{text}]]")

def html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.find_all('img'): img.decompose() 
    
    process_internal_links_and_anchors(soup)

    for tag in soup(["script", "style", "meta", "link", "title"]): tag.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)): comment.extract()
    
    # DESTROY EXTERNAL LINKS (Unwrap)
    for a in soup.find_all('a'): 
        a.unwrap()
            
    for tag in soup.find_all(['b', 'strong']): tag.replace_with(f"**{tag.get_text()}**")
    for tag in soup.find_all(['i', 'em']): tag.replace_with(f"*{tag.get_text()}*")
    for tag in soup.find_all('h1'): tag.replace_with(f"\n\n# {tag.get_text()}\n\n")
    for tag in soup.find_all('h2'): tag.replace_with(f"\n\n## {tag.get_text()}\n\n")
    for tag in soup.find_all('h3'): tag.replace_with(f"\n\n### {tag.get_text()}\n\n")
    for tag in soup.find_all('h4'): tag.replace_with(f"\n\n#### {tag.get_text()}\n\n")
    for tag in soup.find_all('p'): tag.insert_before("\n"); tag.insert_after("\n")
    for tag in soup.find_all('li'): tag.replace_with(f"- {tag.get_text()}\n")
    
    return soup.get_text(separator="")

def convert_epub_to_md(source_path, dest_root, category="Dhamma", author_override=None):
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

    # --- SUBFOLDER MIRRORING ---
    relative_path = Path("")
    if author_override:
        for parent in source_path.parents:
            if author_tools.normalize(parent.name) == author_tools.normalize(author_override):
                try: relative_path = source_path.parent.relative_to(parent)
                except: pass
                break

    author_folder = dest_root / category / "Books" / author / relative_path
    
    safe_filename = f"{author} - {title}.md".replace("/", "-").replace(":", "-")
    output_path = author_folder / safe_filename

    if output_path.exists():
        print(f"⏩ Skipping: {title} (Exists)")
        return

    print(f"📘 Converting: {title}...")
    try: book = epub.read_epub(source_path)
    except: return

    extracted_theme = extract_epub_metadata(book)
    full_markdown = ""
    for item_id in book.spine:
        item = book.get_item_with_id(item_id[0])
        if item and item.get_type() == ebooklib.ITEM_DOCUMENT:
            raw_html = item.get_content().decode('utf-8')
            md = clean_junk_text(html_to_markdown(raw_html))
            if len(md) > 5: full_markdown += md + "\n\n---\n\n" 

    full_markdown = citation_scanner.inject_wikilinks(full_markdown)
    suttas, vinaya = citation_scanner.extract_citations(full_markdown)
    
    frontmatter = {
        "title": title, "author": author, "category": category,
        "contribution": "book", "theme": extracted_theme, "topic": "To_Fill",
        "sutta_citations": suttas, "vin_citations": vinaya
    }
    
    author_folder.mkdir(parents=True, exist_ok=True)
    final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n\n" + full_markdown
    
    with open(output_path, "w", encoding='utf-8') as f: f.write(final_content)
    print(f"✅ Finished: {output_path}")