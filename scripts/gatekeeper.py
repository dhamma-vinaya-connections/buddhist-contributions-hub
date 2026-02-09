import os
from pathlib import Path

# ==========================================
# 🛡️ SECURITY & QUALITY CONFIGURATION
# ==========================================
MAX_FILE_SIZE_MB = 25   

# Book Rules (Dynamic Density)
ESSAY_WORD_LIMIT = 15000 
MIN_CITATIONS_ESSAY = 5   
MIN_CITATIONS_BOOK = 20   

# Obsidian Note Rules
MIN_WIKILINKS_NOTE = 5  # Must link to 5 things to be accepted
# ==========================================

def get_file_size_mb(filepath):
    return os.path.getsize(filepath) / (1024 * 1024)

def check_malware(filepath, extension):
    """
    Checks magic bytes to prevent renamed .exe files.
    """
    try:
        with open(filepath, 'rb') as f:
            header = f.read(4)
        
        if extension == '.pdf': return header.startswith(b'%PDF')
        if extension == '.epub': return header.startswith(b'PK')
        if extension == '.md': 
            if b'\x00' in header: return False 
            return True
            
        return True # Default safe for others (Canvas, JSON, etc.)
    except: return False

def get_quality_threshold(word_count):
    """
    Returns the minimum citations required based on text length.
    """
    if word_count < ESSAY_WORD_LIMIT:
        return MIN_CITATIONS_ESSAY
    else:
        return MIN_CITATIONS_BOOK

def reject_and_delete(filepath, reason):
    """
    Deletes the file from Inbox and logs the reason.
    """
    print(f"🗑️  DELETING: {filepath.name}")
    print(f"   ↳ Reason: {reason}")
    try:
        os.remove(filepath)
        print("   ✅ File removed from Inbox.")
    except Exception as e:
        print(f"   ⚠️ Could not delete: {e}")

def audit_file_structure(filepath, author_name_from_folder):
    """
    Basic checks (Size, Name, Malware).
    Returns: (Passed (bool), Reason (str))
    """
    filename = filepath.name
    ext = filepath.suffix.lower()

    # 1. PLUGIN BLOCKER
    if ".obsidian" in str(filepath):
        return False, "⛔ SECURITY: Plugins/Settings not allowed."

    # 2. ORPHAN CHECK
    if author_name_from_folder is None:
        if " - " not in filename and "obsidian" not in str(filepath):
            return False, "⛔ ORPHAN: No author in filename or folder."

    # 3. SIZE CHECK
    if ext in ['.pdf', '.epub']:
        size = get_file_size_mb(filepath)
        if size > MAX_FILE_SIZE_MB:
            return False, f"⛔ TOO BIG: {size:.1f}MB (Limit: {MAX_FILE_SIZE_MB}MB)"

    # 4. MALWARE CHECK
    if not check_malware(filepath, ext):
        return False, "☣️  MALWARE SUSPICION: File signature mismatch."

    return True, "OK"