import os
import shutil
import re
import yaml
from pathlib import Path
import citation_scanner
import author_tools 

def clean_filename(stem):
    stem = re.sub(r'^[\d\-\.\_\s]+', '', stem)
    stem = re.sub(r'_[\d]{4,}$', '', stem)
    return stem.strip()

def determine_author_and_title(source_path, author_override):
    original_stem = source_path.stem
    if " - " in original_stem:
        # SWAPPED: Title - Author
        file_title_part, file_author_part = original_stem.split(" - ", 1)
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

def parse_existing_frontmatter(text):
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try: return yaml.safe_load(match.group(1)), match.group(2)
        except: return {}, text
    return {}, text

def transfer_attachments(body_text, source_path, dest_folder):
    wiki_matches = re.findall(r'!\[\[(.*?)(?:\|.*?)?\]\]', body_text)
    md_matches = re.findall(r'!\[.*?\]\((.*?)\)', body_text)
    all_images = set(wiki_matches + md_matches)

    for img_name in all_images:
        img_name = img_name.strip()
        src_img = source_path.parent / img_name
        if src_img.exists() and src_img.is_file():
            dest_img = dest_folder / img_name
            dest_img.parent.mkdir(parents=True, exist_ok=True)
            if not dest_img.exists():
                print(f"   🖼️ Copying attachment: {img_name}")
                shutil.copy2(str(src_img), str(dest_img))

def process_obsidian_file(source_path, dest_root, category="Dhamma", author_override=None):
    author, title = determine_author_and_title(source_path, author_override)

    relative_path = Path("") 
    contribution_type = "text" 
    if author_override:
        for parent in source_path.parents:
            if author_tools.normalize(parent.name) == author_tools.normalize(author_override):
                try: 
                    full_rel = source_path.parent.relative_to(parent)
                    if author_tools.normalize(full_rel.name) == author_tools.normalize(author) or str(full_rel) == ".":
                        relative_path = Path("")
                        contribution_type = "text"
                    else:
                        relative_path = full_rel
                        contribution_type = str(full_rel).lower().replace("_", " ")
                except: pass
                break

    storage_author = author_tools.strip_accents(author_override) if author_override else author
    final_folder = dest_root / "Contributions" / category / storage_author / relative_path
    ext = source_path.suffix.lower()
    
    # CASE A: MARKDOWN
    if ext == '.md':
        # OUTPUT: Title - Author.md
        safe_filename = f"{title} - {author}.md".replace("/", "-").replace(":", "-")
        output_path = final_folder / safe_filename
        
        action_msg = "📝 Creating"
        if output_path.exists(): action_msg = "♻️ Updating (Overwrite)"
        print(f"{action_msg}: {title}...")

        try:
            with open(source_path, 'r', encoding='utf-8') as f: raw_content = f.read()
        except: return

        existing_meta, body_text = parse_existing_frontmatter(raw_content)
        clean_body = citation_scanner.inject_wikilinks(body_text)
        
        frontmatter = existing_meta.copy()
        
        # 1. DELETE TOPIC if exists
        if "topic" in frontmatter:
            del frontmatter["topic"]
            
        # 2. ENSURE THEME exists
        if "theme" not in frontmatter:
            frontmatter["theme"] = "To_Fill"
            
        frontmatter.update({
            "title": title, "author": author, 
            "category": category, "contribution": contribution_type 
        })
        
        final_folder.mkdir(parents=True, exist_ok=True)
        transfer_attachments(clean_body, source_path, final_folder)
        
        final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n" + clean_body
        with open(output_path, "w", encoding='utf-8') as f: f.write(final_content)
        print(f"✅ Finished: {output_path}")

    # CASE B: CANVAS / OTHERS
    else:
        # OUTPUT: Title - Author.ext
        safe_filename = f"{title} - {author}{ext}".replace("/", "-").replace(":", "-")
        output_path = final_folder / safe_filename
        
        action_msg = "📦 Moving"
        if output_path.exists(): action_msg = "♻️ Updating (Overwrite)"
        print(f"{action_msg}: {safe_filename}...")
        
        final_folder.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(source_path), str(output_path))
        print(f"✅ Finished: {output_path}")