import os
import fitz  # PyMuPDF
import yaml
from pathlib import Path
from citation_scanner import extract_citations

def convert_pdf_to_md(source_path, dest_root, category="Dhamma"):
    """
    Converts a PDF to a folder containing markdown + images.
    
    Args:
        source_path (Path): Path to the input PDF.
        dest_root (Path): The 'Library' or 'Contributions' folder.
        category (str): 'Dhamma' or 'Vinaya'.
    """
    
    filename = source_path.stem  # "Ajahn Chah - Food for the Heart"
    
    # Try to parse Author/Title from filename
    try:
        author, title = filename.split(" - ", 1)
    except ValueError:
        author = "Unknown"
        title = filename

    # Define Output Structure
    # Buddhist_Hub/Library/Dhamma/Books/Ajahn Chah/Food for the Heart/
    book_folder = dest_root / category / "Books" / author / title
    img_folder = book_folder / "attachments"
    
    # Create folders
    img_folder.mkdir(parents=True, exist_ok=True)
    
    print(f"📖 Converting: {title}...")

    # --- PDF PROCESSING ---
    doc = fitz.open(source_path)
    full_text = ""
    markdown_body = ""
    
    for page_index, page in enumerate(doc):
        # 1. Get Text
        text = page.get_text()
        full_text += text
        markdown_body += text + "\n\n"
        
        # 2. Extract Images
        image_list = page.get_images()
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Naming: Page_ImgIndex.png (Keeps it unique per book)
            image_name = f"p{page_index+1}_{img_index+1}.{image_ext}"
            image_path = img_folder / image_name
            
            # Save Image
            with open(image_path, "wb") as f_img:
                f_img.write(image_bytes)
                
            # Insert Markdown Link at bottom of page text (Approximation)
            # Link format: ![[attachments/image.png]]
            markdown_body += f"\n![[{image_name}]]\n"

    # --- METADATA INJECTION ---
    suttas, vinaya = extract_citations(full_text)
    
    frontmatter = {
        "title": title,
        "author": author,
        "category": category,
        "contribution": "book",
        "sutta_citations": suttas,
        "vin_citations": vinaya  # <--- As requested
    }
    
    # Combine YAML + Content
    final_content = "---\n" + yaml.dump(frontmatter, sort_keys=False) + "---\n\n" + markdown_body
    
    # Save Markdown
    with open(book_folder / "content.md", "w", encoding='utf-8') as f:
        f.write(final_content)
        
    print(f"✅ Finished: {book_folder}")

# --- TEST RUNNER (Remove later) ---
if __name__ == "__main__":
    # Test with a dummy file if you have one
    # convert_pdf_to_md(Path("Inbox/Dhamma/pdf/Test.pdf"), Path("Buddhist_Hub/Library"))
    pass