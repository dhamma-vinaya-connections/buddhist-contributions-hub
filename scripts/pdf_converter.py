import os
import pymupdf4llm  # <--- The secret weapon for structure
import fitz
import yaml
from pathlib import Path
from citation_scanner import extract_citations

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

    # --- 1. CONVERT TO MARKDOWN (With Formatting) ---
    # This function extracts text while keeping # Headers, **Bold**, and Tables.
    # It also extracts images automatically into the dictionary result.
    md_text = pymupdf4llm.to_markdown(source_path, write_images=False) 
    
    # --- 2. IMAGE EXTRACTION (Manual Control) ---
    # We do this manually to ensure our custom naming convention (p1_1.png) matches Obsidian links
    # Note: pymupdf4llm is great at text, but we want strict control over image paths.
    
    doc = fitz.open(source_path)
    
    # We will append images to the bottom or let the user place them. 
    # For now, let's keep the image extraction logic simple:
    for page_index, page in enumerate(doc):
        image_list = page.get_images()
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save Image
            image_name = f"p{page_index+1}_{img_index+1}.{image_ext}"
            image_path = img_folder / image_name
            with open(image_path, "wb") as f_img:
                f_img.write(image_bytes)

    # --- 3. METADATA INJECTION ---
    # Scan the rich markdown for citations
    suttas, vinaya = extract_citations(md_text)
    
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
    
    # Save
    with open(book_folder / "content.md", "w", encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"✅ Finished: {book_folder}")

if __name__ == "__main__":
    pass