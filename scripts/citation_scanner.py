import re
import json
from pathlib import Path

# --- LOAD DATA ---
SCRIPTS_DIR = Path(__file__).parent
PTS_MAP = {}
VALID_IDS = set()

try:
    with open(SCRIPTS_DIR / "pts_map.json", 'r') as f:
        PTS_MAP = json.load(f)
    with open(SCRIPTS_DIR / "valid_ids.json", 'r') as f:
        VALID_IDS = set(json.load(f))
except Exception as e:
    print(f"⚠️ citation_scanner warning: Could not load maps. {e}")

# --- CONFIGURATION ---
CODE_MAP = {
    # Nikayas
    'dn': 'DN', 'mn': 'MN', 'sn': 'SN', 'an': 'AN',
    'kp': 'KP', 'khp': 'KP', 'dhp': 'DHP', 'snp': 'SNP',
    'ud': 'UD', 'iti': 'ITI', 'vv': 'VV', 'pv': 'PV',
    'thag': 'THAG', 'thig': 'THIG', 'ja': 'JA',
    
    # Agamas (Accented & Plain)
    'ma': 'MA', 'mā': 'MA', 
    'da': 'DA', 'dā': 'DA',
    'sa': 'SA', 'sā': 'SA',
    'ea': 'EA', 'eā': 'EA',
    
    # Vinaya
    'parajika': 'BU-PJ', 'par': 'BU-PJ', 'pj': 'BU-PJ',
    'sanghadisesa': 'BU-SS', 'sang': 'BU-SS', 'ss': 'BU-SS',
    'nissaggiya': 'BU-NP', 'np': 'BU-NP',
    'pacittiya': 'BU-PC', 'pac': 'BU-PC', 'pc': 'BU-PC',
    'patidesaniya': 'BU-PD', 'pd': 'BU-PD',
    'sekhiya': 'BU-SK', 'sek': 'BU-SK', 'sk': 'BU-SK',
    'adhikarana': 'BU-AS', 'adh': 'BU-AS', 'as': 'BU-AS',
    'mv': 'VIN-MV', 'mahavagga': 'VIN-MV',
    'cv': 'VIN-CV', 'cullavagga': 'VIN-CV',
    'vin': 'VIN',
}

# Regex Keys (Included accented characters for Agamas)
SUTTA_KEYS = r"dn|mn|sn|an|kp|khp|dhp|snp|ud|iti|vv|pv|thag|thig|ja|ma|mā|da|dā|sa|sā|ea|eā"
VIN_KEYS = r"vin|pvr|mv|cv|mahavagga|cullavagga|parajika|par|pj|sanghadisesa|ss|nissaggiya|np|pacittiya|pac|pc|patidesaniya|pd|sekhiya|sk|adhikarana|as"

def normalize_citation(code, number):
    """
    Returns the Wikilink ID AND any leftover text (suffix).
    Returns: (link_id, suffix)
    Ex: ('MN', '83.20') -> ('MN83', '.20')
    Ex: ('AN', '6.63')  -> ('AN6.63', '')
    """
    clean_code = code.replace(".", "").replace(" ", "").lower()
    
    # ----------------------------------------
    # STRATEGY 1: PTS LOOKUP (Vol/Page)
    # ----------------------------------------
    # Clean roman numerals for lookup key construction
    # Remove Roman prefixes (i, ii, v)
    clean_num_str = re.sub(r'^[ixvIXV]+(?=[\.\s\d])[\.\s]*', '', number)
    # Normalize separators to dots
    clean_num_str = clean_num_str.replace(":", ".").replace(" ", ".").replace(",", ".").replace(";", ".")
    clean_num_str = clean_num_str.strip('.')

    # Try to detect Volume from input string
    vol_match = re.match(r'^([ixvIXV]+)[\.\s]+(\d+)', number)
    lookup_key = None
    
    if vol_match:
        # "A i 1" case
        roman = vol_match.group(1).lower()
        page = vol_match.group(2)
        roman_map = {'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5', 'vi': '6'}
        vol = roman_map.get(roman, roman)
        lookup_key = f"{clean_code}{vol}.{page}"
    elif "." in clean_num_str:
        # "3.1" -> assume Vol.Page for lookup
        # Problem: "6.63" is AN 6.63 (Sutta), not Vol 6 Page 63.
        # So we only trust this lookup if the key exists in PTS_MAP
        # AND if the code is typically referenced by Vol/Page (Vinaya, PTS variants)
        possible_key = f"{clean_code}{clean_num_str}"
        # We strip suffixes like ".20" from the key for lookup
        # e.g. "1.372.20" -> try "1.372"
        parts = possible_key.split('.')
        if len(parts) >= 2:
            base_key = f"{parts[0]}.{parts[1]}" # codeVol.Page
            if base_key in PTS_MAP:
                lookup_key = base_key

    # Check Map
    if lookup_key and lookup_key in PTS_MAP:
        # Found it! Now, calculate suffix.
        # If input was "I 372,20" and we matched "372", suffix is ",20"
        # This is tricky to calculate exactly, so we default to returning the ID and NO suffix 
        # (assuming the map result is the Sutta, and extra bits are inside the sutta).
        # OR: We just assume the map gives the Sutta ID.
        # But wait, if text was "SN I 372,20", the user wants the link to point to the Sutta, 
        # and ",20" to remain as text? Or part of the link?
        # Usually PTS refs point to the WHOLE Sutta.
        return PTS_MAP[lookup_key], "" 

    # ----------------------------------------
    # STRATEGY 2: STANDARD ID CONSTRUCTION + VALIDATION
    # ----------------------------------------
    prefix = CODE_MAP.get(clean_code, clean_code.upper())
    
    # Fully dotted numeric part
    full_id_num = clean_num_str 
    
    # Try the Full ID first: "AN6.63"
    candidate = f"{prefix}{full_id_num}"
    if candidate in VALID_IDS:
        return candidate, ""
        
    # BACKTRACKING for Suffixes (Paragraphs)
    # Split by dots from right to left
    # "MN83.20" -> Try "MN83" (Suffix ".20")
    parts = full_id_num.split('.')
    
    # Try iteratively removing parts from the end
    for i in range(len(parts)-1, 0, -1):
        base_num = ".".join(parts[:i])
        suffix_num = ".".join(parts[i:])
        
        check_id = f"{prefix}{base_num}"
        if check_id in VALID_IDS:
            # We found a valid parent!
            # Reconstruct the original separator (we normalized to dots, so we return dots)
            return check_id, f".{suffix_num}"

    # If nothing matched in VALID_IDS, return the full thing (Best Guess)
    return candidate, ""

def extract_citations(text):
    regex_template = r"(?i)\b({code})[\.\s]*((?:[ivxIVX]+[\.\s]*)?[\d\.\-–:,;]+)"
    vin_matches = re.findall(regex_template.format(code=VIN_KEYS), text)
    sutta_matches = re.findall(regex_template.format(code=SUTTA_KEYS), text)
    
    sutta_links = set()
    for code, num in sutta_matches:
        link_id, _ = normalize_citation(code, num) # Ignore suffix for Metadata list
        sutta_links.add(f"[[{link_id}]]")
        
    vin_links = set()
    for code, num in vin_matches:
        link_id, _ = normalize_citation(code, num)
        vin_links.add(f"[[{link_id}]]")
        
    return sorted(list(sutta_links)), sorted(list(vin_links))

def inject_wikilinks(text):
    regex_template = r"(?i)\b({code})[\.\s]*((?:[ivxIVX]+[\.\s]*)?[\d\.\-–:,;]+)"
    full_pattern = regex_template.format(code=f"{SUTTA_KEYS}|{VIN_KEYS}")
    
    def replace_match(match):
        code = match.group(1)
        number = match.group(2)
        
        link_id, suffix = normalize_citation(code, number)
        return f"[[{link_id}]]{suffix}"

    return re.sub(full_pattern, replace_match, text)