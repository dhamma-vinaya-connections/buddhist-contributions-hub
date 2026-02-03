import os
import shutil
from pathlib import Path

# --- IMPORT YOUR CONVERTERS ---
import pdf_converter
import epub_converter

# ==========================================
# 🧪 CONFIGURATION (EDIT THIS LINE)
# ==========================================
# Put the full path to the file you want to test here:
TEST_FILE = r"C:\Users\You\Downloads\Analayo - MN comparative 1.pdf" 
# (On Mac/Linux use: "/Users/You/Downloads/File.pdf")

# ==========================================

def run_test():
    source_path = Path(TEST_FILE)
    
    # 1. Validation
    if not source_path.exists():
        print(f"❌ Error: Could not find file at: {source_path}")
        print("   -> Please edit the TEST_FILE line in the script.")
        return

    # 2. Setup a "Sandboxed" Output Folder
    # This creates a folder named "Test_Result" right next to this script
    script_dir = Path(__file__).parent
    output_root = script_dir.parent / "Test_Result"
    
    # Optional: Clear previous tests? (Uncomment to auto-clean)
    # if output_root.exists(): shutil.rmtree(output_root)
    
    output_root.mkdir(parents=True, exist_ok=True)

    print(f"🧪 Starting Test on: {source_path.name}")
    print(f"📂 Output Destination: {output_root}")
    print("-" * 40)

    # 3. Detect Type & Run
    ext = source_path.suffix.lower()
    
    try:
        if ext == ".pdf":
            # We force category="Test" so it goes into a specific folder
            pdf_converter.convert_pdf_to_md(
                source_path, 
                output_root, 
                category="Test_Category", 
                author_override=None
            )
        elif ext == ".epub":
            epub_converter.convert_epub_to_md(
                source_path, 
                output_root, 
                category="Test_Category", 
                author_override=None
            )
        else:
            print(f"⚠️ Unsupported file type: {ext}")
            
    except Exception as e:
        print(f"💥 CRASH: The converter failed.")
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()

    print("-" * 40)
    print("✅ Test run complete. Check the 'Test_Result' folder.")

if __name__ == "__main__":
    run_test()