import pandas as pd
import json
import re
from pathlib import Path

# --- CONFIGURATION ---
REPO_ROOT = Path(__file__).resolve().parent.parent
CAT_DIR = REPO_ROOT / "Catalogue"
OUTPUT_FILE = REPO_ROOT / "scripts" / "pts_map.json"

# File Names (Must match your TSV files in Catalogue/ folder)
FILE_SUTTAS = "suttas.tsv"
FILE_PATIMOKKHA = "patimokkha.tsv"
FILE_KD = "kd.tsv"

def clean_key(code, vol, page):
    """
    Generates a standardized key for lookup.
    Ex: Code='A', Vol='i', Page='1' -> 'an1.1'
    """
    # 1. Standardize Code
    code = code.lower().strip().replace(".", "")
    if code in ['a', 'an']: code = 'an'
    elif code in ['d', 'dn']: code = 'dn'
    elif code in ['m', 'mn']: code = 'mn'
    elif code in ['s', 'sn']: code = 'sn'
    elif code == 'vin': code = 'vin'
    
    # 2. Standardize Vol (Roman to Int)
    vol_str = str(vol).lower().strip()
    roman_map = {'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5', 'vi': '6'}
    vol_num = roman_map.get(vol_str, vol_str) 
    
    # 3. Standardize Page
    page_num = str(page).strip()
    
    return f"{code}{vol_num}.{page_num}"

def build_map():
    print("Example Key Generation: 'A i 1' -> 'an1.1'")
    pts_map = {}
    
    # --- 1. PROCESS SUTTAS (TSV) ---
    try:
        # sep='\t' is the magic switch for TSV
        df = pd.read_csv(CAT_DIR / FILE_SUTTAS, sep='\t', encoding='utf-8', on_bad_lines='skip')
        print(f"📖 Loaded Suttas: {len(df)} rows")
        
        for _, row in df.iterrows():
            pts = str(row['pts'])
            sutta_id = str(row['suttacode'])
            
            if pd.isna(row['pts']) or pd.isna(row['suttacode']) or pts.lower() == 'nan': continue
            
            # Handling "A i 1"
            parts = pts.split()
            if len(parts) >= 3:
                key = clean_key(parts[0], parts[1], parts[2])
                pts_map[key] = sutta_id
            # Handling "D I 1" (Roman attached or weird spacing)
            # You can add more parsing logic here if needed
                
    except Exception as e:
        print(f"⚠️ Error processing Suttas: {e}")

    # --- 2. PROCESS VINAYA (TSV + Ranges) ---
    def process_vinaya_row(row, code_col, pts_col):
        pts_raw = str(row[pts_col])
        target_id = str(row[code_col])
        
        if pd.isna(row[pts_col]) or pd.isna(row[code_col]): return
        
        # Regex for "Vin.3.1–40" or "Vin.3.1"
        match = re.match(r"Vin\.(\d+)\.(\d+)(?:[-–](\d+))?", pts_raw, re.IGNORECASE)
        
        if match:
            vol = match.group(1)
            start_page = int(match.group(2))
            end_page = int(match.group(3)) if match.group(3) else start_page
            
            # Map every page in the range to this rule
            for p in range(start_page, end_page + 1):
                key = f"vin{vol}.{p}"
                if key not in pts_map:
                    pts_map[key] = target_id

    try:
        # Patimokkha
        df_pat = pd.read_csv(CAT_DIR / FILE_PATIMOKKHA, sep='\t', encoding='utf-8', on_bad_lines='skip')
        print(f"📙 Loaded Patimokkha: {len(df_pat)} rows")
        for _, row in df_pat.iterrows():
            # Check for Monk rules (BU) or Nun rules (BNI)
            if str(row['vincode']).startswith('BU'): 
                process_vinaya_row(row, 'vincode', 'pts_ref')

        # Khandhakas
        df_kd = pd.read_csv(CAT_DIR / FILE_KD, sep='\t', encoding='utf-8', on_bad_lines='skip')
        print(f"📗 Loaded Khandhakas: {len(df_kd)} rows")
        for _, row in df_kd.iterrows():
            process_vinaya_row(row, 'vincode', 'pts_ref')
            
    except Exception as e:
        print(f"⚠️ Error processing Vinaya: {e}")

    # --- 3. SAVE ---
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(pts_map, f, indent=2)
    
    print(f"✅ Map Built! Saved {len(pts_map)} keys to {OUTPUT_FILE.name}")
    # print(json.dumps(pts_map, indent=2)) # Debug print

if __name__ == "__main__":
    build_map()