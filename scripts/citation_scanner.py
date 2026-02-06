import re
import json
import unicodedata
from pathlib import Path

# --- CONFIGURATION: BRAHMALI ---
FILE_PATTERNS = {
    "VIN-MV": "mv{num}-brahmali-pali",
    "VIN-CV": "cv{num}-brahmali-pali",
}

# --- LOAD DATA ---
SCRIPTS_DIR = Path(__file__).parent
PTS_MAP = {}
VALID_IDS = set()

try:
    if (SCRIPTS_DIR / "pts_map.json").exists():
        with open(SCRIPTS_DIR / "pts_map.json", 'r') as f:
            PTS_MAP = json.load(f)
    if (SCRIPTS_DIR / "valid_ids.json").exists():
        with open(SCRIPTS_DIR / "valid_ids.json", 'r') as f:
            VALID_IDS = set(json.load(f))
except Exception: pass

# --- MAPPING RULES ---
CODE_MAP = {
    'd': 'DN', 'dn': 'DN', 'm': 'MN', 'mn': 'MN', 's': 'SN', 'sn': 'SN', 'a': 'AN', 'an': 'AN',
    'kp': 'KP', 'khp': 'KP', 'dhp': 'DHP', 'snp': 'SNP', 'ud': 'UD', 'iti': 'ITI', 'vv': 'VV', 'pv': 'PV',
    'thag': 'THAG', 'thig': 'THIG', 'ja': 'JA', 'ma': 'MA', 'mā': 'MA', 'da': 'DA', 'dā': 'DA', 'sa': 'SA', 'sā': 'SA', 'ea': 'EA', 'eā': 'EA',
    'parajika': 'BU-PJ', 'par': 'BU-PJ', 'pj': 'BU-PJ',
    'sanghadisesa': 'BU-SS', 'sang': 'BU-SS', 'ss': 'BU-SS',
    'nissaggiya': 'BU-NP', 'np': 'BU-NP',
    'pacittiya': 'BU-PC', 'pac': 'BU-PC', 'pc': 'BU-PC',
    'patidesaniya': 'BU-PD', 'pd': 'BU-PD',
    'sekhiya': 'BU-SK', 'sek': 'BU-SK', 'sk': 'BU-SK',
    'adhikarana': 'BU-AS', 'adh': 'BU-AS', 'as': 'BU-AS',
    'mv': 'VIN-MV', 'mahavagga': 'VIN-MV', 'cv': 'VIN-CV', 'cullavagga': 'VIN-CV',
    'kd': 'VIN-KD', 'khandhaka': 'VIN-KD', 'vin': 'VIN',
}

SUTTA_KEYS = r"d|m|s|a|dn|mn|sn|an|kp|khp|dhp|snp|ud|iti|vv|pv|thag|thig|ja|ma|mā|da|dā|sa|sā|ea|eā"
VIN_KEYS = r"vin|pvr|mv|cv|kd|khandhaka|mahavagga|cullavagga|parajika|par|pj|sanghadisesa|ss|nissaggiya|np|pacittiya|pac|pc|patidesaniya|pd|sekhiya|sk|adhikarana|as"

def resolve_khandhaka(kd_num_str):
    try:
        if "." in kd_num_str:
            main_num = int(kd_num_str.split('.')[0])
            suffix = "." + kd_num_str.split('.', 1)[1]
        else:
            main_num = int(kd_num_str)
            suffix = ""

        if 1 <= main_num <= 10: return f"VIN-MV{main_num}{suffix}"
        elif 11 <= main_num <= 22: return f"VIN-CV{main_num - 10}{suffix}"
        else: return None
    except ValueError: return None

def normalize_citation(code, number):
    book_override = None
    if code == "Sn": book_override = "SNP"
    
    clean_code = code.replace(".", "").replace(" ", "").lower()
    clean_code = unicodedata.normalize('NFC', clean_code)
    
    clean_num_str = number.replace(":", ".").replace(";", ".").replace(",", ".")
    clean_num_str = clean_num_str.replace("*", "").replace("_", "")
    clean_num_str = clean_num_str.strip(". ")

    if clean_code in ['kd', 'khandhaka']:
        resolved = resolve_khandhaka(clean_num_str)
        if resolved: return resolved, ""
    
    if "." in clean_num_str:
        possible_key = f"{clean_code}{clean_num_str}"
        parts = possible_key.split('.')
        if len(parts) >= 2 and f"{parts[0]}.{parts[1]}" in PTS_MAP:
            return PTS_MAP[f"{parts[0]}.{parts[1]}"], ""

    if book_override: prefix = book_override
    else: prefix = CODE_MAP.get(clean_code, clean_code.upper())
        
    candidate = f"{prefix}{clean_num_str}"
    if candidate in VALID_IDS: return candidate, ""
    
    parts = clean_num_str.split('.')
    for i in range(len(parts)-1, 0, -1):
        check_id = f"{prefix}{'.'.join(parts[:i])}"
        if check_id in VALID_IDS: return check_id, f".{'.'.join(parts[i:])}"

    return candidate, ""

def generate_smart_link(full_id):
    """
    Handles offsets, truncations, and Index routing.
    """
    
    # 1. DHAMMAPADA ROUTER -> Master Index
    # Input: DHP42
    # Output: [[DHP|DHP42]]
    if full_id.startswith("DHP"):
        return f"[[DHP|{full_id}]]"

    # 2. VINAYA LOGIC
    match = re.match(r"^(VIN-MV|VIN-CV)(\d+)\.(\d+)(?:\.[\d\.]+)?$", full_id)
    if match:
        prefix, book_num, section = match.groups()
        if prefix == "VIN-CV": book_num = str(int(book_num) + 10)
        if prefix in FILE_PATTERNS:
            filename = FILE_PATTERNS[prefix].format(num=book_num)
            return f"[[{filename}#^{section}|{full_id}]]"

    match_chap = re.match(r"^(VIN-MV|VIN-CV)(\d+)$", full_id)
    if match_chap:
        prefix, book_num = match_chap.groups()
        if prefix == "VIN-CV": book_num = str(int(book_num) + 10)
        if prefix in FILE_PATTERNS:
            filename = FILE_PATTERNS[prefix].format(num=book_num)
            return f"[[{filename}|{full_id}]]"

    return f"[[{full_id}]]"

def extract_citations(text):
    regex_template = r"\b({code})[\.\s\*\_]*(\d[\d\.\-–:,;]*)"
    vin_pattern = f"(?i){regex_template.format(code=VIN_KEYS)}"
    sutta_pattern = f"(?i){regex_template.format(code=SUTTA_KEYS)}"
    
    vin_matches = re.findall(vin_pattern, text)
    sutta_matches = re.findall(sutta_pattern, text)
    
    sutta_links = set()
    for code, num in sutta_matches:
        full_id, _ = normalize_citation(code, num)
        sutta_links.add(generate_smart_link(full_id))
        
    vin_links = set()
    for code, num in vin_matches:
        full_id, _ = normalize_citation(code, num)
        vin_links.add(generate_smart_link(full_id))
        
    return sorted(list(sutta_links)), sorted(list(vin_links))

def inject_wikilinks(text):
    regex_template = r"\b({code})[\.\s\*\_]*(\d[\d\.\-–:,;]*)"
    citation_pattern = regex_template.format(code=f"{SUTTA_KEYS}|{VIN_KEYS}")
    combined_pattern = f"(?i)(\\[\\[.*?\\]\\])|({citation_pattern})"
    
    def replace_logic(match):
        if match.group(1): return match.group(1) 
        full_citation_text = match.group(2)
        sub_match = re.match(f"(?i){citation_pattern}", full_citation_text)
        if sub_match:
            code = sub_match.group(1)
            number = sub_match.group(2)
            link_id, suffix = normalize_citation(code, number)
            return f"{generate_smart_link(link_id)}{suffix}"
        return full_citation_text

    return re.sub(combined_pattern, replace_logic, text)