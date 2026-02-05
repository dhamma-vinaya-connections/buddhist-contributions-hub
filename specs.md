# Project Specifications: Buddhist Contributions Hub

## Overview
A community-curated, "Digital Garden" style library of Dhamma and Vinaya Contributions. It is designed to be downloaded and dropped directly into Early Buddhis Connections interconnecting with the Pali Canon (Suttas).

**Goal:** Automated processing of Buddhist works (PDF, Epub, Markdown) from a staging "Inbox" into a clean, interconnected Obsidian library ("Contributions").

**Core Principles:**

- **Unified Destination:** All processed files land in `Buddhist_hub/Contributions`, organized by Category $\rightarrow$ Author $\rightarrow$ Type.
    
- **Minimalist Metadata:** Citations are injected as clickable links in the text. They are _only_ listed in the YAML frontmatter for "Reference Only" files (where text is hidden).
    
- **Dynamic Structure:** The system mirrors the subfolders you use in the Inbox (e.g., "Study Guides", "Anthologies") directly into the Library structure and metadata.

##  2. Folder Architecture

#### **Source: The Inbox**

The entry point for all files. `Inbox / {Category} / {Format} / {Author} / {Type/Subfolder} / File`

- **Category:** `Dhamma` or `Vinaya`.
    
- **Format:** `pdf`, `epub`, `reference only`, `obsidian` (includes .md, .canvas).
    
- **Author:** `Ven. Thanissaro`, `Ven. Brahmali`, etc.
    
- **Type:** `Books` (default), `Study Guides`, `Anthologies`, `Canvas`, etc.
    

#### **Destination: The Hub**

The target structure after processing. `Buddhist_hub / Contributions / {Category} / {Author} / {Type} / File.md`

> **Note:** The "Format" folder (pdf/epub) is removed. Files are organized purely by Content and Author.

- repo e
	- scrips
	- inbox
		- Dhamma 
			- pdf
				- Folders by author 
					- books
					- study guides 
					- etc
			- Reference only pdf
				- Folders by author 
			- epub
				- Folders by author 
			- md
				- Folders by author 
			- others (bases canvas, etc)
		- Vinaya
			- Pdf
					- Folders by author 
			- Reference only
				- Folders by author 
			- epub
				- Folders by author 
			- md
				- Folders by author 
			- others (bases canvas, etc)
	- Buddhist _hub
		- Library 
			- Dhamma
				- Folders by author 
			- Vinaya
				- Folders by author 
		- Contributions 
			- Dhamma 
				- Folders by author 
			- Vinaya
				- Folders by author 

## 3. The Automation Pipeline (`main.py`)

The system scans the Inbox and dispatches files based on their **Format** folder.

|**Format Folder**|**Handler Script**|**Action**|
|---|---|---|
|`pdf`|`pdf_converter.py`|Converts text to Markdown. Injects links. Moves to Contributions.|
|`epub`|`epub_converter.py`|extracts text. Cleans HTML junk. Injects links. Moves to Contributions.|
|`reference only`|`reference_scanner.py`|Moves original file to `attachments`. Creates a wrapper `.md` file. Scans citations into YAML.|
|`obsidian`|`obsidian_processor.py`|**.md:** Cleans links, updates YAML. **.canvas:** Moves directly.|

---

## 4. Handling Rules

#### **A. Citation & Linking Logic**

- **Regex:** Detects citations like `MN 10`, `VIN-MV8.15.3`.
    
- **Truncation:** Deep paragraphs are truncated to the **Section** level for the link target to ensure validity.
    
    - _Source:_ `VIN-MV8.15.3` (Para 3)
        
    - _Link:_ `[[mv8-brahmali-pali#^15|VIN-MV8.15.3]]` (Links to Section 15)
        
- **Cullavagga Offset:** Applies `+10` to Book Numbers for CV citations.
    
    - _Source:_ `VIN-CV1.x`
        
    - _Link:_ `[[cv11-brahmali-pali...]]`
        
- **Formatting:** Injects WikiLinks (`[[...]]`) into the body text automatically.
    

#### **B. Metadata (YAML Frontmatter)**

The scripts enforce a **Force Update** on 4 core fields but preserve all other user data (tags, dates, notes).

- **Core Fields (Overwritten):**
    
    1. `title`: Cleaned from filename.
        
    2. `author`: From filename (priority) or folder name.
        
    3. `category`: `Dhamma` or `Vinaya`.
        
    4. `contribution`: derived from **Subfolder Name**.
        
        - Folder `Study Guides` $\rightarrow$ YAML `contribution: study guides` (Lowercase).
            
        - No folder $\rightarrow$ YAML `contribution: book` (PDF/Epub) or `text` (Obsidian).
            
- **Citation Fields (`sutta_citations`, `vin_citations`):**
    
    - **PDF/Epub/MD:** **REMOVED**. Links are in the text.
        
    - **Reference Only:** **INCLUDED**. Needed for search since text is hidden.
        

#### **C. File Collision Logic**

- **Safe Mode:** If a file with the exact same name exists in the destination, the script **SKIPS** it. It never overwrites your notes.
    
- **Reference Exception:** If an attachment (PDF) inside the `attachments` folder exists, it is **OVERWRITTEN** (assuming you are updating the scan quality).
    

---

## 5. Script Inventory

1. **`main.py`**: The Orchestrator. Scans Inbox, detects types, runs workers.
    
2. **`citation_scanner.py`**: The Brain. Handles regex, Pāli offsets, and link generation.
    
3. **`author_tools.py`**: Utility. Cleans names and removes accents.
    
4. **`pdf_converter.py`**: Worker. Uses PyMuPDF4LLM. Smart subfolder detection.
    
5. **`epub_converter.py`**: Worker. Uses EbookLib. Smart subfolder detection.
    
6. **`reference_scanner.py`**: Worker. Creates stubs. **Extracts full YAML metadata.**
    
7. **`obsidian_processor.py`**: Worker. Handles `.md` text polishing and `.canvas` moving.
    

This spec is now fully implemented in the code provided in the previous turn. You are ready to run `python main.py`!