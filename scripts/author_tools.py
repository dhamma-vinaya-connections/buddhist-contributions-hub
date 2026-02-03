import json
import os
import unicodedata
from pathlib import Path

# Load map once when imported
SCRIPT_DIR = Path(__file__).parent
MAP_FILE = SCRIPT_DIR / "authors.json"
AUTHOR_MAP = {}

try:
    if MAP_FILE.exists():
        with open(MAP_FILE, 'r', encoding='utf-8') as f:
            AUTHOR_MAP = json.load(f)
except Exception as e:
    print(f"⚠️ Warning: Could not load authors.json: {e}")

def strip_accents(text):
    """
    Converts 'Ñāṇananda' -> 'Nanananda'
    """
    if not text: return ""
    # Normalize to NFD form (decomposes characters: ñ -> n + ~)
    nfd_form = unicodedata.normalize('NFD', text)
    # Filter out non-spacing mark characters (category 'Mn')
    return "".join(c for c in nfd_form if unicodedata.category(c) != 'Mn')

def normalize(name):
    """
    Input: "ñāṇananda" -> Output: "Ven. Nanananda"
    Input: "Unknown Ñame" -> Output: "Unknown Name"
    """
    if not name: return "Unknown"
    
    # 1. Clean the input
    clean = name.replace("_", " ").strip()
    
    # 2. Check the Map (Lower case lookup)
    # We strip accents from the lookup key just in case
    lower_name = strip_accents(clean.lower())
    
    if lower_name in AUTHOR_MAP:
        return AUTHOR_MAP[lower_name]
    
    # 3. Fallback: Strip accents and Title Case
    # "unknown ñame" -> "Unknown Name"
    return strip_accents(clean).title()