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
    text = text.replace("[[[", "[[").replace("]]]", "]]")
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def process_internal_links_and_anchors(soup):
    """
    Returns a dictionary of {old_id: new_numeric_id} found in this chapter.
    """
    local_map = {}
    
    # --- STEP 1: SCAN & STANDARDIZE ANCHORS ---
    for tag in soup.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'li', 'blockquote']):
        text_content = tag.get_text(strip=True)
        
        # Regex: Start of line, optional §, capture number
        match = re.search(r'^\s*§?\s*(\d+)[\.\s]', text_content)
        
        new_id = None
        current_html_id = tag.get('id')
        
        if match:
            new_id = match.group(1) # e.g. "115"
        
        if current_html_id:
            if new_id:
                # We found a number! Map 'hfifteen' -> '115'
                local_map[current_html_id] = new_id
                tag['id'] = new_id
            else:
                # No number, keep old ID
                local_map[current_html_id] = current_html_id
        elif new_id:
            # No ID existed, but we found a number. Create '115'.
            tag['id'] = new_id
            
        # Append Obsidian Anchor ^115
        if new_id:
            if f"^{new_id}" not in text_content:
                tag.append(NavigableString(f" ^{new_id}"))

    # --- STEP 2: LOCAL LINK FIX (Best Effort) ---
    # We fix what we can see in this chapter immediately
    for a in soup.find_all('a'):
        if a.has_attr('href'):
            href = a['href']
            text = a.get_text()
            
            if text.startswith('[') and text.endswith(']'):
                text = text[1:-1]

            if '#' in href and not href.startswith('http'):
                old_link_id = href.split('#')[-1]
                # Try local map first
                target_id = local_map.get(old_link_id, old_link_id)
                replacement = f"[[#^{target_id}|{text}]]"
                a.replace_with(replacement)
            elif not href.startswith('http'):
                 a.replace_with(text)
                 
    return local_map

def html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.find_all('img'): img.decompose() 
    
    # 🌟 CAPTURE THE MAP 🌟
    chapter_map = process_internal_links_and_anchors(soup)
    
    for tag in soup(["script", "style", "meta", "link", "title"]): tag.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)): comment.extract()
    for a in soup.find_all('a'): a.unwrap()
    for tag in soup.find_all(['b', 'strong']): tag.replace_with(f"**{tag.get_text()}**")
    for tag in soup.find_all(['i', 'em']): tag.replace_with(f"*{tag.get_text()}*")
    
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'div', 'li']):
        tag.insert_before("\n")
        tag.insert_after("\n")

    for tag in soup.find_all('h1'): tag.replace_with(f"# {tag.get_text()}")
    for tag in soup.find_all('h2'): tag.replace_with(f"## {tag.get_text()}")
    for tag in soup.find_all('h3'): tag.replace_with(f"### {tag.get_text()}")
    for tag in soup.find_all('h4'): tag.replace_with(f"#### {tag.get_text()}")
    for tag in soup.find_all('li'): tag.replace_with(f"- {tag.get_text()}")
    
    return soup.get_text(separator=""), chapter_map

def convert_epub_to_md(source_path, dest_root, category="Dhamma", author_override=None):
    author, title = determine_author_and_title(source_path, author_override)

    relative_path = Path("Books") 
    contribution_type = "Book"
    if author_override:
        for parent in source_path.parents:
            if author_tools.clean_text(parent.name) == author_tools.clean_text(author_override):
                try: 
                    full_rel = source_path.parent.relative_to(parent)
                    if str(full_rel) == "." or author_tools.clean_text(full_rel.name) == author_tools.clean_text(author):
                         relative_path = Path("Books")
                         contribution_type = "Book"
                    else:
                        relative_path = full_rel
                        contribution_type = author_tools.normalize_type(full_rel.name)
                except: pass
                break

    storage_author = author_tools.normalize_author(author_override) if author_override else author
    final_folder = dest_root / "Contributions" / category / storage_author / relative_path
    
    safe_filename = f"{title} - {author}.md".replace("/", "-").replace(":", "-")
    output_path = final_folder / safe_filename

    if output_path.exists():
        print(f"⏩ Skipping: {title} (Exists)")
        return
    
    print(f"📘 Converting: {title}...")
    try: book = epub.read_epub(source_path)
    except: return
    extracted_theme = extract_epub_metadata(book)
    
    full_markdown = ""
    GLOBAL_ID_MAP = {} # 🌟 Master list of all renamed IDs
    
    # PASS 1: CONVERT & BUILD MAP
    for item_id in book.spine:
        item = book.get_item_with_id(item_id[0])
        if item and item.get_type() == ebooklib.ITEM_DOCUMENT:
            raw_html = item.get_content().decode('utf-8')
            md, chapter_map = html_to_markdown(raw_html)
            
            md = clean_junk_text(md)
            if len(md) > 5: 
                full_markdown += md + "\n\n---\n\n"
                GLOBAL_ID_MAP.update(chapter_map) # Merge maps

    # PASS 2: GLOBAL PATCHING (Fix cross-chapter links)
    # We look for links pointing to old IDs and update them
    print(f"   🔧 Patching internal links...")
    for old_id, new_id in GLOBAL_ID_MAP.items():
        if old_id != new_id:
            # Replace [[#^hfifteen| with [[#^115|
            full_markdown = full_markdown.replace(f"[[#^{old_id}|", f"[[#^{new_id}|")
            # Replace [[#^hfifteen]] with [[#^115]]
            full_markdown = full_markdown.replace(f"[[#^{old_id}]]", f"[[#^{new_id}]]")

    full_markdown = citation_scanner.inject_wikilinks(full_markdown)

    # --- 🛡️ GATEKEEPER CHECK ---
    word_count = citation_scanner.count_words(full_markdown)
    citation_count = citation_scanner.get_citation_count(full_markdown)
    required_citations = gatekeeper.get_quality_threshold(word_count)
    
    if citation_count < required_citations:
        reason = f"Low Quality (Words: {word_count}, Refs: {citation_count}/{required_citations})"
        gatekeeper.reject_and_delete(source_path, reason)
        return
    # ---------------------------

    frontmatter = {
        "title": title, 
        "author": author, 
        "category": category,
        "contribution": contribution_type,
        "theme": extracted_theme
    }
    
    final_folder.mkdir(parents=True, exist_ok=True)
    final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n\n" + full_markdown
    
    with open(output_path, "w", encoding='utf-8') as f: f.write(final_content)
    print(f"✅ Finished: {output_path}")