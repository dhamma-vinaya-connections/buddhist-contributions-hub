import unicodedata

def strip_accents(text):
    if not text: return ""
    text = unicodedata.normalize('NFD', text)
    text = "".join([c for c in text if unicodedata.category(c) != 'Mn'])
    return unicodedata.normalize('NFC', text)

def normalize(name):
    if not name: return "Unknown"
    return strip_accents(name).strip()