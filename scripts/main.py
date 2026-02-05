import os
from pathlib import Path

# --- IMPORT WORKERS ---
import pdf_converter
import epub_converter
import reference_scanner
import obsidian_processor

# ==========================================
# 🚀 CONFIGURATION
# ==========================================
REPO_ROOT = Path(__file__).parent.parent 
INBOX_ROOT = REPO_ROOT / "Inbox"
DESTINATION_ROOT = REPO_ROOT / "Buddhist_hub"
# ==========================================

def get_category_and_type(path):
    try:
        relative_parts = path.relative_to(INBOX_ROOT).parts
        if len(relative_parts) < 2: return None, None, None 

        category = relative_parts[0] 
        folder_type = relative_parts[1].lower() 
        
        author_override = None
        if len(relative_parts) > 2:
            author_override = relative_parts[2]
            if path.parent.name.lower() == folder_type:
                 author_override = None

        return category, folder_type, author_override

    except ValueError:
        return None, None, None

def process_inbox():
    print(f"🚀 STARTING INBOX PROCESSOR")
    print(f"📂 Inbox: {INBOX_ROOT}")
    print(f"🎯 Dest : {DESTINATION_ROOT}/Contributions")
    print("-" * 50)

    count = 0
    for root, dirs, files in os.walk(INBOX_ROOT):
        for file in files:
            file_path = Path(root) / file
            if file.startswith("."): continue
            
            category, folder_type, author = get_category_and_type(file_path)
            
            if not category or not folder_type: continue 

            try:
                if folder_type == "pdf" and file_path.suffix.lower() == ".pdf":
                    pdf_converter.convert_pdf_to_md(file_path, DESTINATION_ROOT, category, author)
                    count += 1
                
                elif folder_type == "epub" and file_path.suffix.lower() == ".epub":
                    epub_converter.convert_epub_to_md(file_path, DESTINATION_ROOT, category, author)
                    count += 1

                elif "reference" in folder_type:
                    reference_scanner.process_reference_file(file_path, DESTINATION_ROOT, category, author)
                    count += 1

                elif "obsidian" in folder_type:
                    obsidian_processor.process_obsidian_file(file_path, DESTINATION_ROOT, category, author)
                    count += 1
                    
            except Exception as e:
                print(f"💥 ERROR on {file}: {e}")

    print("-" * 50)
    print(f"✅ COMPLETE. Processed {count} files.")

if __name__ == "__main__":
    process_inbox()