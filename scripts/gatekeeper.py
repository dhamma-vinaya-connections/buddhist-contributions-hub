import os
import shutil
from pathlib import Path

# ==========================================
# 🛡️ GATEKEEPER CONFIGURATION
# ==========================================

# 1. MINIMUM CITATIONS (For PDFs/EPUBs)
# How many Sutta/Vinaya references (e.g., "MN 10") must be found?
MIN_CITATIONS_BOOK = 35       # For big books (> 40k words)
MIN_CITATIONS_ESSAY = 20      # For essays/articles (> 2k words)
MIN_CITATIONS_SHORT = 8       # For very short texts (< 2k words)

# 2. MINIMUM CONNECTIVITY (For Markdown Notes)
# How many wiki-links ([[Link]]) must a note have?
MIN_WIKILINKS_NOTE = 10       # Rejects "orphan" or empty notes

# 3. WORD COUNT THRESHOLDS
# Defines what counts as a "Book" vs "Essay"
THRESHOLD_BOOK_WORDS = 40000
THRESHOLD_ESSAY_WORDS = 2000

# ==========================================

def count_words(text):
    if not text: return 0
    return len(text.split())

def get_quality_threshold(word_count):
    """
    Returns the required number of citations based on text length.
    """
    if word_count >= THRESHOLD_BOOK_WORDS:
        return MIN_CITATIONS_BOOK
    elif word_count >= THRESHOLD_ESSAY_WORDS:
        return MIN_CITATIONS_ESSAY
    else:
        return MIN_CITATIONS_SHORT

def reject_and_delete(file_path, reason):
    """
    Deletes the file and logs the rejection.
    """
    print(f"❌ REJECTED: {file_path.name}")
    print(f"   Reason: {reason}")
    try:
        os.remove(file_path)
        print(f"   🗑️ File deleted from Inbox.")
    except OSError as e:
        print(f"   ⚠️ Error deleting file: {e}")

def validate_note_connectivity(link_count):
    """
    Checks if an Obsidian note has enough connections.
    """
    return link_count >= MIN_WIKILINKS_NOTE