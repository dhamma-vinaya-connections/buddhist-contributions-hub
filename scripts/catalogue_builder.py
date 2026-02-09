import pandas as pd
import json
import re
from pathlib import Path

# --- CONFIGURATION ---
REPO_ROOT = Path(__file__).resolve().parent.parent
CAT_DIR = REPO_ROOT / "Catalogue"
PTS_MAP_FILE = REPO_ROOT / "scripts" / "pts_map.json"
VALID_IDS_FILE = REPO_ROOT / "scripts" / "valid_ids.json" # <--- NEW

# File Names
FILE_SUTTAS = "suttas.tsv"
FILE_PATIMOKKHA = "patimokkha.tsv"
FILE_KD = "kd.tsv"

def clean_key(code, vol, page):
    """ Standardizes PTS Keys (an1.1) """
    code = code.lower().strip().replace(".", "")
    if code in ['a', 'an']: code = 'an'
    elif code in ['d', 'dn']: code = 'dn'
    elif code in ['m', 'mn']: code = 'mn'
    elif code in ['s', 'sn']: code = 'sn'
    elif code == 'vin': code = 'vin'
    
    vol_str = str(vol).lower().strip()
    roman_map = {'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5', 'vi': '6'}
    vol_num = roman_map.get(vol_str, vol_str) 
    
    page_num = str(page).strip()
    # Handle page ranges in key if necessary? Usually lookup is exact start page.
    # For now, simplistic.
    return f"{code}{vol_num}.{page_num}"

def build_map():
    print("🏗️  Building Maps...")
    pts_map = {}
    valid_ids = set() # <--- Collects all real IDs (AN1.1, MN10, etc.)
    
    # --- 1. PROCESS SUTTAS ---
    try:
        df = pd.read_csv(CAT_DIR / FILE_SUTTAS, sep='\t', encoding='utf-8', on_bad_lines='skip')
        print(f"📖 Loaded Suttas: {len(df)} rows")
        
        for _, row in df.iterrows():
            if pd.isna(row['suttacode']): continue
            
            sutta_id = str(row['suttacode']).strip()
            valid_ids.add(sutta_id) # Add to Guest List
            
            # PTS Mapping
            pts = str(row['pts'])
            if not pd.isna(row['pts']) and pts.lower() != 'nan':
                parts = pts.split()
                if len(parts) >= 3:
                    key = clean_key(parts[0], parts[1], parts[2])
                    pts_map[key] = sutta_id
                
    except Exception as e:
        print(f"⚠️ Error processing Suttas: {e}")

    # --- 2. PROCESS VINAYA ---
    def process_vinaya_row(row, code_col, pts_col):
        if pd.isna(row[code_col]): return
        
        target_id = str(row[code_col]).strip()
        valid_ids.add(target_id) # Add to Guest List
        
        pts_raw = str(row[pts_col])
        if pd.isna(row[pts_col]): return
        
        # Regex for "Vin.3.1–40"
        match = re.match(r"Vin\.(\d+)\.(\d+)(?:[-–](\d+))?", pts_raw, re.IGNORECASE)
        if match:
            vol = match.group(1)
            start_page = int(match.group(2))
            end_page = int(match.group(3)) if match.group(3) else start_page
            
            for p in range(start_page, end_page + 1):
                key = f"vin{vol}.{p}"
                if key not in pts_map:
                    pts_map[key] = target_id

    try:
        df_pat = pd.read_csv(CAT_DIR / FILE_PATIMOKKHA, sep='\t', encoding='utf-8', on_bad_lines='skip')
        print(f"📙 Loaded Patimokkha: {len(df_pat)} rows")
        for _, row in df_pat.iterrows():
            if str(row['vincode']).startswith('BU'): 
                process_vinaya_row(row, 'vincode', 'pts_ref')

        df_kd = pd.read_csv(CAT_DIR / FILE_KD, sep='\t', encoding='utf-8', on_bad_lines='skip')
        print(f"📗 Loaded Khandhakas: {len(df_kd)} rows")
        for _, row in df_kd.iterrows():
            process_vinaya_row(row, 'vincode', 'pts_ref')
            
    except Exception as e:
        print(f"⚠️ Error processing Vinaya: {e}")

    # --- 3. SAVE FILES ---
    with open(PTS_MAP_FILE, 'w') as f:
        json.dump(pts_map, f, indent=2)
        
    with open(VALID_IDS_FILE, 'w') as f:
        json.dump(sorted(list(valid_ids)), f, indent=2)
    
    print(f"✅ Maps Built!")
    print(f"   PTS Keys: {len(pts_map)}")
    print(f"   Valid IDs: {len(valid_ids)}")

if __name__ == "__main__":
    build_map()