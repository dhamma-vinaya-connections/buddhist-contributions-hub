import unicodedata
import re

# ==========================================
# 👤 AUTHOR DICTIONARY
# ==========================================
AUTHOR_MAP = {
    "thanissaro": "Ven. Thanissaro",
    "bhikkhu bodhi": "Ven. Bodhi",
    "analayo": "Ven. Analayo",
    "sujato": "Ven. Sujato",
    "brahmali": "Ven. Brahmali",
    "gombrich": "Gombrich Richard",
}

# ==========================================
# 📚 FOLDER TYPE DICTIONARY
# ==========================================
TYPE_MAP = {
    "manual": "study guide",
    "handbook": "study guide",
    "textbook": "study guide",
    "talk": "dhamma talk",
    "transcript": "dhamma talk",
    "paper": "essay",
    "article": "essay",
    "canon": "sutta translation",
}
# ==========================================

def clean_text(text):
    if not text: return ""
    text = unicodedata.normalize('NFD', text)
    text = "".join([c for c in text if unicodedata.category(c) != 'Mn'])
    return text.lower().strip()

def make_singular(text):
    """
    Smartly converts plural to singular without a map.
    Logic: Lowercase -> Check endings -> Strip 's'.
    """
    if not text: return "to_fill"
    clean = text.lower().strip()
    
    # 1. Protect words ending in 'ss' (Mindfulness, Glass)
    if clean.endswith('ss'): return clean
    
    # 2. Protect words ending in 'is' (Analysis, Basis)
    if clean.endswith('is'): return clean
    
    # 3. Protect words ending in 'us' (Status, Consensus)
    if clean.endswith('us'): return clean
    
    # 4. Standard Strip: If it ends in 's', remove it.
    if clean.endswith('s'):
        return clean[:-1]
        
    return clean

def normalize_type(folder_name):
    """Standardizes 'Study_Guides' -> 'study guide'."""
    if not folder_name: return "book"
    
    clean = re.sub(r'^\d+[\.\-_]\s*', '', folder_name)
    clean = re.sub(r'[\-_]', ' ', clean).strip().lower()
    
    # Apply Singular Logic
    singular = make_singular(clean)

    if singular in TYPE_MAP: return TYPE_MAP[singular]
    
    return singular

def normalize_author(raw_name):
    if not raw_name: return "Unknown"
    
    clean = clean_text(raw_name)
    
    if clean in AUTHOR_MAP: return AUTHOR_MAP[clean]
        
    if "bhikkhu" in clean and "bhikkhuni" not in clean:
        name_part = re.sub(r'\bbhikkhu\b', '', clean).strip().title()
        return f"Ven. {name_part}"
        
    if "bhikkhuni" in clean:
        name_part = re.sub(r'\bbhikkhuni\b', '', clean).strip().title()
        return f"Ayya {name_part}"

    if "thera" in clean:
        name_part = re.sub(r'\bthera\b', '', clean).strip().title()
        return f"Ven. {name_part}"

    if "ajahn" in clean or "ajaan" in clean:
        name_part = re.sub(r'\ba[jz]a[a]?hn\b', '', clean).strip().title()
        return f"Ajahn {name_part}"

    if "sayadaw" in clean:
        name_part = re.sub(r'\bsayadaw\b', '', clean).strip().title()
        return f"Sayadaw {name_part}"

    return raw_name.strip().title()