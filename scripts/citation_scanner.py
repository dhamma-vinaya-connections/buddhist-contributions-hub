import re
import json
from pathlib import Path

# --- LOAD THE ROSETTA STONE ---
PTS_MAP = {}
try:
    map_path = Path(__file__).parent / "pts_map.json"
    if map_path.exists():
        with open(map_path, 'r') as f:
            PTS_MAP = json.load(f)
        # print(f"Loaded PTS Map with {len(PTS_MAP)} entries.")
except Exception as e:
    print(f"Warning: Could not load pts_map.json: {e}")

# --- CONFIGURATION ---
CODE_MAP = {
    'dn': 'DN', 'mn': 'MN', 'sn': 'SN', 'an': 'AN',
    'kp': 'KP', 'khp': 'KP', 'dhp': 'DHP', 'snp': 'SNP',
    'ud': 'UD', 'iti': 'ITI', 'vv': 'VV', 'pv': 'PV',
    'thag': 'THAG', 'thig': 'THIG', 'ja': 'JA',
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

SUTTA_KEYS = r"dn|mn|sn|an|kp|khp|dhp|snp|ud|iti|vv|pv|thag|thig|ja"
VIN_KEYS = r"vin|pvr|mv|cv|mahavagga|cullavagga|parajika|par|pj|sanghadisesa|ss|nissaggiya|np|pacittiya|pac|pc|patidesaniya|pd|sekhiya|sk|adhikarana|as"

def normalize_citation(code, number):
    """
    1. Generates a 'PTS Key' (e.g. 'an1.1') and checks the Map.
    2. If found, returns the verified ID (e.g. 'AN1.1').
    3. If not, falls back to standard normalization.
    """
    clean_code = code.replace(".", "").replace(" ", "").lower()
    
    # --- STRATEGY 1: PTS LOOKUP ---
    # We try to construct a key: code + vol + . + page
    # Clean the number to get Vol/Page parts
    # Remove Roman prefixes for the lookup logic
    clean_num_str = re.sub(r'^[ixvIXV]+(?=[\.\s\d])[\.\s]*', '', number) # remove 'i '
    clean_num_str = clean_num_str.replace(":", ".").replace(" ", ".").replace(",", ".").replace(";", ".").strip('.')
    
    # Try to extract Vol from the original number if possible, or just use the cleaned number string
    # "i 1" -> Vol=1, Page=1. "1.1" -> Vol=1, Page=1.
    # Simple Heuristic: If we have "Code Vol.Page", the key is "codeVol.Page"
    
    # We need to detect the volume. 
    # If the input was "A i 1", 'number' is "i 1".
    # We extract the roman part.
    vol_match = re.match(r'^([ixvIXV]+)[\.\s]+(\d+)', number)
    
    lookup_key = None
    if vol_match:
        # We have explicit Roman Volume: "i 1"
        roman = vol_match.group(1).lower()
        page = vol_match.group(2)
        roman_map = {'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5', 'vi': '6'}
        vol = roman_map.get(roman, roman)
        lookup_key = f"{clean_code}{vol}.{page}"
        
    elif "." in clean_num_str:
        # We have "3.1" -> assume Vol.Page
        lookup_key = f"{clean_code}{clean_num_str}"
        
    # CHECK THE MAP
    if lookup_key and lookup_key in PTS_MAP:
        return PTS_MAP[lookup_key]

    # --- STRATEGY 2: STANDARD FALLBACK ---
    final_code = CODE_MAP.get(clean_code, clean_code.upper())
    return f"{final_code}{clean_num_str}"

def extract_citations(text):
    regex_template = r"(?i)\b({code})[\.\s]*((?:[ivxIVX]+[\.\s]*)?[\d\.\-–:,;]+)"
    vin_matches = re.findall(regex_template.format(code=VIN_KEYS), text)
    sutta_matches = re.findall(regex_template.format(code=SUTTA_KEYS), text)
    
    vin_links = set()
    for code, num in vin_matches:
        c = code.lower()
        if 'maha' in c: c = 'mahavagga'
        elif 'culla' in c: c = 'cullavagga'
        elif 'para' in c: c = 'parajika'
        elif 'niss' in c: c = 'nissaggiya'
        elif 'pac' in c: c = 'pacittiya'
        elif 'patid' in c: c = 'patidesaniya'
        elif 'sekh' in c: c = 'sekhiya'
        elif 'adhi' in c: c = 'adhikarana'
        link_id = normalize_citation(c, num)
        vin_links.add(f"[[{link_id}]]")
        
    sutta_links = set()
    for code, num in sutta_matches:
        link_id = normalize_citation(code, num)
        sutta_links.add(f"[[{link_id}]]")
        
    return sorted(list(sutta_links)), sorted(list(vin_links))

def inject_wikilinks(text):
    regex_template = r"(?i)\b({code})[\.\s]*((?:[ivxIVX]+[\.\s]*)?[\d\.\-–:,;]+)"
    full_pattern = regex_template.format(code=f"{SUTTA_KEYS}|{VIN_KEYS}")
    
    def replace_match(match):
        code = match.group(1)
        number = match.group(2)
        
        c = code.lower()
        if 'maha' in c: c = 'mahavagga'
        elif 'culla' in c: c = 'cullavagga'
        elif 'para' in c: c = 'parajika'
        elif 'niss' in c: c = 'nissaggiya'
        elif 'pac' in c: c = 'pacittiya'
        elif 'patid' in c: c = 'patidesaniya'
        elif 'sekh' in c: c = 'sekhiya'
        elif 'adhi' in c: c = 'adhikarana'
        
        link_id = normalize_citation(c, number)
        return f"[[{link_id}]]"

    return re.sub(full_pattern, replace_match, text)