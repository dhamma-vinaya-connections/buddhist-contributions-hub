import os
import pymupdf4llm
import fitz
import yaml
from pathlib import Path
import citation_scanner  # <--- Changed to module import

def convert_pdf_to_md(source_path, dest_root, category="Dhamma"):
    """
    Converts PDF using 'pymupdf4llm' to preserve Headers, Tables, and formatting.
    """
    
    filename = source_path.stem
    
    # Try to parse Author/Title
    try:
        author, title = filename.split(" - ", 1)
    except ValueError:
        author = "Unknown"
        title = filename

    # Define Output Structure
    book_folder = dest_root / category / "Books" / author / title
    img_folder = book_folder / "attachments"
    
    # Create folders
    img_folder.mkdir(parents=True, exist_ok=True)
    
    print(f"📖 Converting (Structure Aware): {title}...")

    # --- 1. CONVERT TO MARKDOWN ---
    md_text = pymupdf4llm.to_markdown(source_path, write_images=False) 
    
    # --- 2. IMAGE EXTRACTION ---
    doc = fitz.open(source_path)
    for page_index, page in enumerate(doc):
        image_list = page.get_images()
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            image_name = f"p{page_index+1}_{img_index+1}.{image_ext}"
            image_path = img_folder / image_name
            with open(image_path, "wb") as f_img:
                f_img.write(image_bytes)

    # --- 3. METADATA & LINK INJECTION ---
    
    # A. Inject Links (Rewrite "AN 6:63" -> "[[AN6.63]]")
    md_text = citation_scanner.inject_wikilinks(md_text)

    # B. Extract Citations
    suttas, vinaya = citation_scanner.extract_citations(md_text)
    
    frontmatter = {
        "title": title,
        "author": author,
        "category": category,
        "contribution": "book",
        "sutta_citations": suttas,
        "vin_citations": vinaya
    }
    
    # Combine
    final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n\n" + md_text
    
    # --- 4. SAVE FILE (Named correctly) ---
    # Sanitize filename (remove colons or slashes that break filesystems)
    safe_filename = f"{author} - {title}.md".replace("/", "-").replace(":", "-")
    output_path = book_folder / safe_filename
    
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"✅ Finished: {output_path}")

if __name__ == "__main__":
    pass