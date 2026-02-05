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

def parse_existing_frontmatter(text):
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try: return yaml.safe_load(match.group(1)), match.group(2)
        except: return {}, text
    return {}, text

def process_obsidian_file(source_path, dest_root, category="Dhamma", author_override=None):
    author, title = determine_author_and_title(source_path, author_override)

    # --- MIRROR SUBFOLDER LOGIC ---
    relative_path = Path("")
    if author_override:
        for parent in source_path.parents:
            if author_tools.normalize(parent.name) == author_tools.normalize(author_override):
                try: 
                    full_rel = source_path.parent.relative_to(parent)
                    if author_tools.normalize(full_rel.name) == author_tools.normalize(author):
                        relative_path = Path("")
                    else:
                        relative_path = full_rel
                except: pass
                break

    storage_author = author_tools.strip_accents(author_override) if author_override else author
    final_folder = dest_root / "Contributions" / category / storage_author / relative_path
    
    ext = source_path.suffix.lower()
    
    # CASE A: MARKDOWN
    if ext == '.md':
        safe_filename = f"{author} - {title}.md".replace("/", "-").replace(":", "-")
        output_path = final_folder / safe_filename
        
        if output_path.exists():
            print(f"⏩ Skipping: {title} (Exists)")
            return

        print(f"📝 Processing MD: {title}...")
        try:
            with open(source_path, 'r', encoding='utf-8') as f: raw_content = f.read()
        except: return

        existing_meta, body_text = parse_existing_frontmatter(raw_content)
        
        # Inject Links (Minimal Metadata)
        clean_body = citation_scanner.inject_wikilinks(body_text)
        
        frontmatter = existing_meta.copy()
        frontmatter.update({
            "title": title, "author": author, "category": category,
            "contribution": frontmatter.get("contribution", "text") 
        })
        
        final_folder.mkdir(parents=True, exist_ok=True)
        final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n" + clean_body
        
        with open(output_path, "w", encoding='utf-8') as f: f.write(final_content)
        print(f"✅ Finished: {output_path}")

    # CASE B: CANVAS / OTHERS
    else:
        safe_filename = f"{author} - {title}{ext}".replace("/", "-").replace(":", "-")
        output_path = final_folder / safe_filename
        
        if output_path.exists():
            print(f"⏩ Skipping: {safe_filename} (Exists)")
            return

        print(f"📦 Moving {ext}: {safe_filename}...")
        final_folder.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(source_path), str(output_path))
        print(f"✅ Finished: {output_path}")