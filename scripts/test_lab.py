import os
import shutil
from pathlib import Path

# --- IMPORT YOUR CONVERTERS ---
import pdf_converter
import epub_converter

# ==========================================
# 🧪 CONFIGURATION
# ==========================================
TEST_FILE = r"buddhist-contributions-hub/Inbox/Dhamma/pdf/Ven. Analayo/Comparative studies/Analayo - MN comparative 1.pdf"
# ==========================================

def get_author_smart(filepath):
    """
    Mimics the Librarian's smart logic.
    Finds 'epub'/'pdf' in path and grabs the folder IMMEDIATELY after it.
    """
    parts = filepath.parts
    anchors = ["pdf", "epub", "md", "reference only"]
    
    for i, part in enumerate(parts):
        if part.lower() in anchors:
            if i + 1 < len(parts) - 1:
                return parts[i+1] # The folder after anchor
            elif i + 1 == len(parts) - 1:
                return parts[i+1] # The folder holding the file
                
    # Fallback: Parent folder
    return filepath.parent.name

def run_test():
    source_path = Path(TEST_FILE).resolve()
    
    if not source_path.exists():
        print(f"❌ Error: Could not find file at: {source_path}")
        return

    # Use Smart Logic
    author_from_folder = get_author_smart(source_path)
    print(f"🧪 Detected Author: '{author_from_folder}'")

    script_dir = Path(__file__).parent
    output_root = script_dir.parent / "Test_Result"
    
    if output_root.exists(): shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    print(f"📂 Output: {output_root}")
    print("-" * 40)

    ext = source_path.suffix.lower()
    
    try:
        if ext == ".pdf":
            pdf_converter.convert_pdf_to_md(
                source_path, output_root, category="Test_Category", author_override=author_from_folder
            )
        elif ext == ".epub":
            epub_converter.convert_epub_to_md(
                source_path, output_root, category="Test_Category", author_override=author_from_folder
            )
        else:
            print(f"⚠️ Unsupported file type: {ext}")
            
    except Exception as e:
        print(f"💥 CRASH: {e}")
        import traceback
        traceback.print_exc()

    print("-" * 40)
    
    found_files = list(output_root.rglob("*.md"))
    if found_files:
        print(f"✅ SUCCESS! Created {len(found_files)} file(s):")
        for f in found_files:
            print(f"   📄 {f}")
    else:
        print("❌ FAILURE: No Markdown files were created.")

if __name__ == "__main__":
    run_test()