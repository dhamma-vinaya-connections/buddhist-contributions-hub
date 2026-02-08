import unicodedata
import re

# ==========================================
# 👤 AUTHOR DICTIONARY (Specific Overrides)
# ==========================================
# Use this for names that don't follow standard rules
# or for people with multiple names (e.g., Ajaan Geoff -> Thanissaro)
AUTHOR_MAP = {
    # Thai Forest Nicknames
    "ajaan geoff": "Ven. Thanissaro",
    "ajahn geoff": "Ven. Thanissaro",
    "thanissaro": "Ven. Thanissaro",
    
    # Specific Spellings
    "bhikkhu bodhi": "Ven. Bodhi",
    "analayo": "Ven. Analayo",
    
    # Lay Scholars
    "gombrich": "Gombrich Richard",
    "richard gombrich": "Gombrich Richard",
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
    Standardizes Author Names with Rules & Dictionary.
    """
    if not raw_name: return "Unknown"
    
    # 1. Clean input
    clean = clean_text(raw_name)
    
    # 2. DICTIONARY CHECK (Highest Priority)
    if clean in AUTHOR_MAP:
        return AUTHOR_MAP[clean]
        
    # 3. RULE ENGINE (General Logic)
    
    # Rule A: "Bhikkhu" -> "Ven."
    # Handles: "Bhikkhu Sujato", "Sujato Bhikkhu" -> "Ven. Sujato"
    if "bhikkhu" in clean and "bhikkhuni" not in clean:
        name_part = re.sub(r'\bbhikkhu\b', '', clean).strip().title()
        return f"Ven. {name_part}"
        
    # Rule B: "Bhikkhuni" -> "Ayya"
    # Handles: "Bhikkhuni Vimala" -> "Ayya Vimala"
    if "bhikkhuni" in clean:
        name_part = re.sub(r'\bbhikkhuni\b', '', clean).strip().title()
        return f"Ayya {name_part}"

    # Rule C: "Thera" -> "Ven."
    if "thera" in clean:
        name_part = re.sub(r'\bthera\b', '', clean).strip().title()
        return f"Ven. {name_part}"

    # Rule D: "Ajahn" (Ensure it is always at the front)
    # Handles: "Chah Ajahn" -> "Ajahn Chah"
    if "ajahn" in clean or "ajaan" in clean:
        name_part = re.sub(r'\ba[jz]a[a]?hn\b', '', clean).strip().title()
        return f"Ajahn {name_part}"

    # Rule E: "Sayadaw" (Ensure it is always at the front)
    if "sayadaw" in clean:
        name_part = re.sub(r'\bsayadaw\b', '', clean).strip().title()
        return f"Sayadaw {name_part}"

    # 4. Fallback
    return raw_name.strip().title()