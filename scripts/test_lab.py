import os
import shutil
from pathlib import Path

# --- IMPORT TOOLS ---
import reference_scanner
import pdf_converter
import epub_converter

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================

# 1. FILE TO PROCESS (Path to a specific file in your Inbox)
SOURCE_FILE = r"buddhist-contributions-hub/Inbox/Vinaya/reference_only_pdf/Ven. Anon/Ven. Anon - The_Concise_Buddhist_Monastic_Code_1.pdf"

# 2. MODE SWITCH
# False = Safe Test (Creates copies in 'Test_Result' folder)
# True  = REAL ACTION (Moves file to 'Library' & creates MD)
PRODUCTION_MODE = True

# 3. DESTINATION (Where is your real Library?)
REAL_LIBRARY_ROOT = Path(r"buddhist-contributions-hub/Library")

# 4. CATEGORY (Dhamma, Vinaya, etc.)
CATEGORY = "Dhamma"

# 5. AUTHOR OVERRIDE (Optional, set to None if not needed)
# If the file is in 'Inbox/Dhamma/pdf/Ven. Thanissaro/Book.pdf', set this to "Ven. Thanissaro"
AUTHOR_OVERRIDE = "None"

# ==========================================

def run_manual_process():
    source_path = Path(SOURCE_FILE).resolve()
    
    if not source_path.exists():
        print(f"❌ Error: Could not find file at: {source_path}")
        return

    # --- DETERMINE ROOT & MODE ---
    if PRODUCTION_MODE:
        dest_root = REAL_LIBRARY_ROOT
        target_file = source_path # We work on the REAL file
        print("🚨 PRODUCTION MODE ENABLED 🚨")
        print(f"   Moving file from: {source_path}")
        print(f"   To Library at:    {dest_root}")
    else:
        # Safe Test Setup
        script_dir = Path(__file__).parent
        dest_root = script_dir.parent / "Test_Result"
        fake_inbox = dest_root / "Fake_Inbox"
        
        if dest_root.exists(): shutil.rmtree(dest_root)
        fake_inbox.mkdir(parents=True, exist_ok=True)
        
        # Copy file to fake inbox
        target_file = fake_inbox / source_path.name
        shutil.copy(source_path, target_file)
        
        print("🧪 SAFE TEST MODE")
        print(f"   Working on copy: {target_file}")
        print(f"   Outputting to:   {dest_root}")

    print("-" * 40)

    # --- SELECT TOOL BASED ON FOLDER NAME ---
    # (Or you can manually uncomment the one you want)
    
    try:
        # CHECK: Is it a Reference Scan?
        if "reference" in str(source_path).lower():
            print("🔧 Using: REFERENCE SCANNER")
            reference_scanner.process_reference_file(
                filepath=target_file,
                dest_root=dest_root,
                category=CATEGORY,
                author_override=AUTHOR_OVERRIDE
            )
            
        # CHECK: Is it a PDF?
        elif source_path.suffix.lower() == '.pdf':
            print("🔧 Using: PDF CONVERTER")
            pdf_converter.convert_pdf_to_md(
                source_path=target_file,
                dest_root=dest_root,
                category=CATEGORY,
                author_override=AUTHOR_OVERRIDE
            )
            
        # CHECK: Is it an EPUB?
        elif source_path.suffix.lower() == '.epub':
            print("🔧 Using: EPUB CONVERTER")
            epub_converter.convert_epub_to_md(
                source_path=target_file,
                dest_root=dest_root,
                category=CATEGORY,
                author_override=AUTHOR_OVERRIDE
            )
            
        else:
            print("❌ Unknown file type.")

    except Exception as e:
        print(f"💥 CRASH: {e}")
        import traceback
        traceback.print_exc()

    print("-" * 40)
    print("✅ Done.")

if __name__ == "__main__":
    run_manual_process()