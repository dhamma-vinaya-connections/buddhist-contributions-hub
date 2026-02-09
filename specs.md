# Project Specifications: Buddhist Contributions Hub

## Overview
A community-curated, high qualityk "Digital Garden" style library of Dhamma and Vinaya Contributions. It is designed to be downloaded and dropped directly into Early Buddhis Connections interconnecting with the Pali Canon (Suttas).

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

The target structure after processing. `Contributions / {Category} / {Author} / {Type} / File.md`

> **Note:** The "Format" folder (pdf/epub) is removed. Files are organized purely by Content and Author.

- Buddhist Contributions Hub 
	- scrips
	- inbox
		- Dhamma 
			- pdf
				- Folders by author 
					- subfolders by type (book, studyguide, canvas, anthologies ets )
			- Reference only
				- Folders by author 
					- subfolders by type (book, studyguide, canvas, anthologies ets )
			- epub
				- Folders by author 
					- subfolders by type (book, studyguide, canvas, anthologies ets )
			- obsidian 
				- Folders by author 
					- subfolders by type (book, studyguide, canvas, anthologies, notes etc )	
		- Vinaya
			- Pdf
					- Folders by author
					- subfolders by type (book, studyguide, canvas, anthologies ets )
			- Reference only
				- Folders by author 
					- subfolders by type (book, studyguide, canvas, anthologies ets )
			- epub
				- Folders by author 
					- subfolders by type (book, studyguide, canvas, anthologies ets )
			- obsidian 
				- Folders by author 
					- subfolders by type (book, studyguide, canvas, anthologies ets )		
	- Contributions  
		- Dhamma
			- Folders by author 
				subfolders by type (book, studyguide, canvas, anthologies ets )
		- Vinaya
			- Folders by author 
				subfolders by type (book, studyguide, canvas, anthologies ets )

## 3. The Automation Pipeline
## System Architecture
The pipeline consists of one Supervisor (`gatekeeper.py`) and four Workers, orchestrated by `main.py`.

```mermaid
graph TD
    Inbox[Inbox] --> Main[main.py]
    Main --> GK{Gatekeeper}
    GK -- "Audit Failed" --> Delete[DELETE File]
    GK -- "Passed" --> Router[Worker Router]
    
    Router -- PDF --> PDFWorker[pdf_converter.py]
    Router -- EPUB --> EPUBWorker[epub_converter.py]
    Router -- Ref --> RefWorker[reference_scanner.py]
    Router -- MD --> MDWorker[obsidian_processor.py]
    
    PDFWorker --> QualityCheck{Density Check}
    EPUBWorker --> QualityCheck
    
    QualityCheck -- "Low Value" --> Delete
    QualityCheck -- "High Value" --> Library[Contributions/]
````

## Script Modules

### 1. gatekeeper.py
- **Role:** Policy Engine.
- **Key Functions:**
    - `audit_file_structure()`: Checks Size, Malware, Orphans.
    - `get_quality_threshold(word_count)`: Returns 5 or 20 based on length.
    - `reject_and_delete()`: The destructive action.

### 2. citation_scanner.py
- **Role:** The "Brain" for content analysis.
- **Capabilities:**
    - **Regex:** Detects `DN 1.1`, `M i 10`, `Vin.iii.45`.
    - **PTS Conversion:** Uses `pts_map.json` to convert `M.i.10` -> `MN 2`.
    - **DHP Routing:** Converts `Dhp 42` -> `[[DHP|DHP 42]]`.
    - **Counting:** Returns total citations for Quality Checks.

### 3. author_tools.py
- **Role:** Standardization Engine.
- **Dictionaries:**
    - `AUTHOR_MAP`: Maps `ajaan geoff` -> `Ven. Thanissaro`.
    - `TYPE_MAP`: Maps `manuals` -> `Study Guide`.
- **Logic:**
    - Detects titles: `Bhikkhu X` -> `Ven. X`.
    - Detects titles: `Bhikkhuni Y` -> `Ayya Y`.

### 4. Workers (pdf_converter`, `epub_converter`, etc.)
- **Role:** Format conversion and metadata injection.
- **Input:** `Title - Author.ext` OR `Author/Title.ext`.
- **Output:** `Title - Author.md` (Standardized).
- **Frontmatter:** Adds `theme`, `category`, `contribution` (Standardized).

|**Format Folder**|**Handler Script**|**Action**|
|---|---|---|
|`pdf`|`pdf_converter.py`|Converts text to Markdown. Injects links. Moves to Contributions.|
|`epub`|`epub_converter.py`|extracts text. Cleans HTML junk. Injects links. Moves to Contributions.|
|`reference only`|`reference_scanner.py`|Moves original file to `attachments`. Creates a wrapper `.md` file. Scans citations into YAML.|
|`obsidian`|`obsidian_processor.py`|**.md:** Cleans links, updates YAML. **.canvas:** Moves directly.|

## Data Files
- `scripts/pts_map.json`: 20,000+ mappings of PTS volume/page to Sutta IDs.
- `scripts/valid_ids.json`: List of valid SuttaCentral IDs for validation.

## 4. Handling Rules

#### **A. Citation & Linking Logic**
- **Regex:** Detects citations like `MN 10`, `VIN-MV8.15.3`.
- **Truncation:** Deep paragraphs are truncated to the **Section** level for the link target to ensure validity.
    - _Source:_ `VIN-MV8.15.3` (Para 3)
    - _Link:_ `[[mv8-brahmali-pali#^15|VIN-MV8.15]].3` (Links to Section 15)
        
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
        - Folder `Study Guides` $\rightarrow$ YAML `contribution: study guides`
        - No folder $\rightarrow$ YAML `contribution: book` (PDF/Epub) or `text` (Obsidian).

- **Citation Fields (`sutta_citations`, `vin_citations`):**
    - **PDF/Epub/MD:** **REMOVED**. Links are in the text.
    - **Reference Only:** **INCLUDED**. Needed for search since text is hidden.

#### **C. File Collision Logic**
- **Safe Mode:** If a file with the exact same name exists in the destination, the script **SKIPS** it. It never overwrites your notes.
- **Reference Exception:** If an attachment (PDF) inside the `attachments` folder exists, it is **OVERWRITTEN** (assuming you are updating the scan quality).

### Version control 
All the files remain in the inbox and only the last version is moved to the contributions folder, specially for obsidian files 

## 5. Script Inventory

1. **`main.py`**: The Orchestrator. Scans Inbox, detects types, runs workers.
2. gatekeeprer.py: remove prevent useless, lowqualiaty or malware files
3. **`citation_scanner.py`**: The Brain. Handles regex, Pāli offsets, and link generation.
4. **`author_tools.py`**: Utility. Cleans names and removes accents.
5. **`pdf_converter.py`**: Worker. Uses PyMuPDF4LLM. Smart subfolder detection.
6. **`epub_converter.py`**: Worker. Uses EbookLib. Smart subfolder detection.
7. **`reference_scanner.py`**: Worker. Creates stubs. **Extracts full YAML metadata.**
8. **`obsidian_processor.py`**: Worker. Handles `.md` text polishing and `.canvas` moving.
