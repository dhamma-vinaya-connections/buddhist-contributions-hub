import re

# --- CONFIGURATION: The Mapping Rules ---
# Maps abbreviations found in PDF text -> Your Repo B standard codes
CODE_MAP = {
    # --- SUTTAS (Standard -> UPPERCASE) ---
    'dn': 'DN', 'mn': 'MN', 'sn': 'SN', 'an': 'AN',
    'kp': 'KP', 'khp': 'KP', 'dhp': 'DHP', 'snp': 'SNP',
    'ud': 'UD', 'iti': 'ITI', 'vv': 'VV', 'pv': 'PV',
    'thag': 'THAG', 'thig': 'THIG', 'ja': 'JA',
    
    # --- VINAYA: BHIKKHU PATIMOKKHA (Specific mappings) ---
    # Parajika -> BU-PJ
    'parajika': 'BU-PJ', 'par': 'BU-PJ', 'pj': 'BU-PJ',
    
    # Sanghadisesa -> BU-SS (Assuming BU-SS based on pattern, or let me know if different)
    'sanghadisesa': 'BU-SS', 'sang': 'BU-SS', 'ss': 'BU-SS',
    
    # Nissaggiya Pacittiya -> BU-NP
    'nissaggiya': 'BU-NP', 'np': 'BU-NP',
    
    # Pacittiya -> BU-PC
    'pacittiya': 'BU-PC', 'pac': 'BU-PC', 'pc': 'BU-PC',
    
    # Patidesaniya -> BU-PD
    'patidesaniya': 'BU-PD', 'pd': 'BU-PD',
    
    # Sekhiya -> BU-SK
    'sekhiya': 'BU-SK', 'sek': 'BU-SK', 'sk': 'BU-SK',
    
    # Adhikarana Samatha -> BU-AS
    'adhikarana': 'BU-AS', 'adh': 'BU-AS', 'as': 'BU-AS',
    
    # --- VINAYA: KHANDHAKAS ---
    'mv': 'VIN-MV', 'mahavagga': 'VIN-MV',
    'cv': 'VIN-CV', 'cullavagga': 'VIN-CV',
    'vin': 'VIN',
}

def normalize_citation(code, number):
    """
    Transforms raw text into Repo B standard link.
    Input:  ('Parajika', '1')     -> [[BU-PJ1]]
    Input:  ('M.V.', '1.1')       -> [[VIN-MV1.1]]
    Input:  ('D N', 'i 12')       -> [[DN12]]
    """
    
    # 1. Clean the Code
    clean_code = code.replace(".", "").replace(" ", "").lower()
    
    # Map to your Repo B standard
    # If the exact key isn't found, it defaults to uppercase (e.g. unknown code)
    final_code = CODE_MAP.get(clean_code, clean_code.upper())
    
    # 2. Clean the Number (Strict Formatting)
    # Remove Roman Numerals at the start (e.g. 'i 12' -> '12')
    clean_number = re.sub(r'^[ixvIXV]+[\.\s]+', '', number)
    
    # Remove all spaces and trailing dots
    clean_number = clean_number.replace(" ", "").strip('.')
    
    return f"[[{final_code}{clean_number}]]"

def extract_citations(text):
    """
    Scans text and returns sorted lists of normalized WikiLinks.
    """
    
    # --- REGEX KEYWORDS ---
    
    # Sutta Keys
    sutta_keys = r"dn|mn|sn|an|kp|khp|dhp|snp|ud|iti|vv|pv|thag|thig|ja"
    
    # Vinaya Keys (Includes full names to catch "Parajika 1")
    vin_keys = r"vin|pvr|mv|cv|mahavagga|cullavagga|parajika|par|pj|sanghadisesa|ss|nissaggiya|np|pacittiya|pac|pc|patidesaniya|pd|sekhiya|sk|adhikarana|as"
    
    # --- THE MASTER REGEX ---
    # Matches: Code + (Optional Roman) + Number
    regex_template = r"(?i)\b({code})[\.\s]*((?:[ivxIVX]+[\.\s]+)?[\d\.\-–]+)"
    
    vin_matches = re.findall(regex_template.format(code=vin_keys), text)
    sutta_matches = re.findall(regex_template.format(code=sutta_keys), text)
    
    # --- PROCESS ---
    vin_links = set()
    for code, num in vin_matches:
        # Pre-cleaning for map lookup
        c = code.lower()
        if 'maha' in c: c = 'mahavagga'
        elif 'culla' in c: c = 'cullavagga'
        elif 'para' in c: c = 'parajika'
        elif 'niss' in c: c = 'nissaggiya'
        elif 'pac' in c: c = 'pacittiya'
        elif 'patid' in c: c = 'patidesaniya'
        elif 'sekh' in c: c = 'sekhiya'
        elif 'adhi' in c: c = 'adhikarana'
        
        vin_links.add(normalize_citation(c, num))
        
    sutta_links = set()
    for code, num in sutta_matches:
        sutta_links.add(normalize_citation(code, num))
        
    return sorted(list(sutta_links)), sorted(list(vin_links))