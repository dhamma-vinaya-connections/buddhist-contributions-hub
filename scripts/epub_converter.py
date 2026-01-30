import os
import yaml
import re
from pathlib import Path
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup, NavigableString, Comment
import citation_scanner  # <--- Module import

def clean_junk_text(text):
    """
    Removes server-side residue (PHP includes, XML headers).
    """
    junk_patterns = [
        r"xml version=['\"]1.0['\"].*?\?",
        r"html #include virtual=.*",
        r"#include virtual=.*",
        r"________ALL SCRIPTS BELOW HERE________",
        r"end:content",
        r"end:container",
        r"Cover end cover",
        r"#Cover",
    ]

    for pattern in junk_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)

    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def html_to_markdown(html_content, img_map):
    """
    Converts HTML to Markdown by replacing tags in-place.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # 0. Clean Junk
    for tag in soup(["script", "style", "meta", "link", "title"]):
        tag.decompose()
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    # 0.5 Unwrap Links (Remove <a href> but keep text to prevent duplication)
    for a in soup.find_all('a'):
        a.unwrap()

    # 1. Handle Images
    for img in soup.find_all('img'):
        src = img.get('src', '')
        filename = os.path.basename(src)
        if filename in img_map:
            img.replace_with(f"\n![[{filename}]]\n")
    
    # 2. Formatting
    for tag in soup.find_all(['b', 'strong']):
        tag.replace_with(f"**{tag.get_text()}**")
    for tag in soup.find_all(['i', 'em']):
        tag.replace_with(f"*{tag.get_text()}*")

    # 3. Headers
    for tag in soup.find_all('h1'): tag.replace_with(f"\n\n# {tag.get_text()}\n\n")
    for tag in soup.find_all('h2'): tag.replace_with(f"\n\n## {tag.get_text()}\n\n")
    for tag in soup.find_all('h3'): tag.replace_with(f"\n\n### {tag.get_text()}\n\n")
    for tag in soup.find_all('h4'): tag.replace_with(f"\n\n#### {tag.get_text()}\n\n")

    # 4. Paragraphs/Lists
    for tag in soup.find_all('p'):
        tag.insert_before("\n")
        tag.insert_after("\n")
    for tag in soup.find_all('li'):
        tag.replace_with(f"- {tag.get_text()}\n")

    return soup.get_text(separator="")

def convert_epub_to_md(source_path, dest_root, category="Dhamma"):
    filename = source_path.stem
    
    try:
        author, title = filename.split(" - ", 1)
    except ValueError:
        author = "Unknown"
        title = filename

    # Setup Folders
    book_folder = dest_root / category / "Books" / author / title
    img_folder = book_folder / "attachments"
    img_folder.mkdir(parents=True, exist_ok=True)
    
    print(f"📘 Converting EPUB: {title}...")

    try:
        book = epub.read_epub(source_path)
    except Exception as e:
        print(f"❌ Failed to read EPUB: {e}")
        return

    # --- 1. EXTRACT IMAGES ---
    img_map = [] 
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_IMAGE:
            img_content = item.get_content()
            original_name = os.path.basename(item.get_name())
            save_path = img_folder / original_name
            with open(save_path, "wb") as f:
                f.write(img_content)
            img_map.append(original_name)

    # --- 2. EXTRACT TEXT ---
    full_markdown = ""
    
    for item_id in book.spine:
        item = book.get_item_with_id(item_id[0])
        if item and item.get_type() == ebooklib.ITEM_DOCUMENT:
            raw_html = item.get_content().decode('utf-8')
            chapter_md = html_to_markdown(raw_html, img_map)
            chapter_md = clean_junk_text(chapter_md)
            
            if len(chapter_md) > 5:
                full_markdown += chapter_md + "\n\n---\n\n" 

    # --- 3. METADATA & LINK INJECTION ---
    full_markdown = citation_scanner.inject_wikilinks(full_markdown)
    suttas, vinaya = citation_scanner.extract_citations(full_markdown)
    
    frontmatter = {
        "title": title,
        "author": author,
        "category": category,
        "contribution": "book",
        "sutta_citations": suttas,
        "vin_citations": vinaya
    }
    
    final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n\n" + full_markdown
    
    # --- 4. SAVE FILE (Named correctly) ---
    safe_filename = f"{author} - {title}.md".replace("/", "-").replace(":", "-")
    output_path = book_folder / safe_filename
    
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"✅ Finished: {output_path}")

if __name__ == "__main__":
    pass