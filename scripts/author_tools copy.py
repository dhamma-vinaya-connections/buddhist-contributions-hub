import unicodedata
import re

# ==========================================
# 👤 AUTHOR SYNONYM DICTIONARY
# ==========================================
# Maps variations (lowercase) -> The Official Folder Name
AUTHOR_MAP = {
    # --- THAI FOREST TRADITION ---
    "thanissaro": "Ven. Thanissaro",
    "thanissaro bhikkhu": "Ven. Thanissaro",
    "bhikkhu thanissaro": "Ven. Thanissaro",
    "ajaan geoff": "Ven. Thanissaro",
    "ajahn geoff": "Ven. Thanissaro",
    
    "ajahn brahm": "Ajahn Brahm",
    "brahmavamso": "Ajahn Brahm",
    "ajahn brahmavamso": "Ajahn Brahm",
    "phra brahmavamso": "Ajahn Brahm",
    
    "ajahn chah": "Ajahn Chah",
    "chah subhaddo": "Ajahn Chah",
    "ven. chah": "Ajahn Chah",
    
    "ajahn sumedho": "Ajahn Sumedho",
    "luang por sumedho": "Ajahn Sumedho",

    # --- SCHOLAR MONKS ---
    "bhikkhu bodhi": "Ven. Bodhi",
    "ven. bodhi": "Ven. Bodhi",
    "acariya bodhi": "Ven. Bodhi",
    
    "bhikkhu analayo": "Ven. Analayo",
    "analayo": "Ven. Analayo",
    
    "bhikkhu sujato": "Ven. Sujato",
    "sujato": "Ven. Sujato",
    "ajahn sujato": "Ven. Sujato",
    
    "bhikkhu brahmali": "Ven. Brahmali",
    "brahmali": "Ven. Brahmali",
    "ajahn brahmali": "Ven. Brahmali",
    
    # --- LAY SCHOLARS ---
    "gombrich": "Gombrich Richard",
    "richard gombrich": "Gombrich Richard",
    "damien keown": "Keown Damien",
}

# ==========================================
# 📚 FOLDER TYPE DICTIONARY
# ==========================================
TYPE_MAP = {
    "guide": "Study Guide",
    "manual": "Study Guide",
    "textbook": "Study Guide",
    "talk": "Dhamma Talk",
    "transcript": "Dhamma Talk",
    "article": "Essay",
    "paper": "Essay",
    "canon": "Sutta Translation",
    "nikaya": "Sutta Translation",
}
# ==========================================

def clean_text(text):
    """Basic lowercase and strip."""
    if not text: return ""
    text = unicodedata.normalize('NFD', text)
    text = "".join([c for c in text if unicodedata.category(c) != 'Mn'])
    return text.lower().strip()

def normalize_type(folder_name):
    """Standardizes 'study_guides' -> 'Study Guide'."""
    if not folder_name: return "Book"
    clean = re.sub(r'^\d+[\.\-_]\s*', '', folder_name)
    clean = re.sub(r'[\-_]', ' ', clean).strip().lower()
    
    if clean.endswith('s') and not clean.endswith('ss'):
        clean_singular = clean[:-1]
    else:
        clean_singular = clean

    if clean in TYPE_MAP: return TYPE_MAP[clean]
    if clean_singular in TYPE_MAP: return TYPE_MAP[clean_singular]
    
    return clean.title()

def normalize_author(raw_name):
    """
    Standardizes Author Names using the AUTHOR_MAP.
    Input: "thanissaro bhikkhu" -> Output: "Ven. Thanissaro"
    """
    if not raw_name: return "Unknown"
    
    # 1. Clean input for lookup
    search_key = clean_text(raw_name)
    
    # 2. Check Dictionary
    if search_key in AUTHOR_MAP:
        return AUTHOR_MAP[search_key]
        
    # 3. Fallback: Formatting Rules
    # If no match, try to respect your "Ven." or "Ajahn" rules automatically
    
    # If Ordained (detected by title), ensure specific format?
    # For now, just Title Case it to be safe.
    # e.g. "somedet" -> "Somedet"
    return raw_name.strip().title()