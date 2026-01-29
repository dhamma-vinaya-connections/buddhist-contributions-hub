# Project Specifications: Buddhist Contributions Hub

## Overview
A community-curated, "Digital Garden" style library of Dhamma books and essays. It is designed to be downloaded and dropped directly into an Obsidian vault, interconnecting with the Pali Canon (Suttas).

## Directory Structure
The repository is divided into two primary domains: **Dhamma** and **Vinaya**

- **Repo Root/**
    - **scripts/** # Automation Logic
    - **Inbox/** # Permanent Archive (Git LFS)
	    - Dhamma
	        - pdf/
	        - epub/
	        - md/
	        - others
		- Vinaya
			- pdf/
	        - epub/
	        - md/
	        - others
    - **Buddhist_Hub/** # The Downloadable Product
        - **Library/** # Authoritative Texts
	        - Dhamma
	            - Books/
	            - Papers/
	            - Essays/
			- Vinaya
				- Books/
	            - Papers/
	            - Essays/
        - **Contributions/** # Community Content
	        - Dhamma
	            - Books/
	            - Papers/
	            - Essays/
			- Vinaya
				- Books/
	            - Papers/
	            - Essays/

## 2. Metadata Standards (YAML)

All files in `Buddhist_Hub` must have standard frontmatter.

**A. User Input**

- `title`: Display title.
    
- `author`: Creator name.
    
- `contribution`: (Optional) `book`, `essay`, `paper`.
    

**B. Automated Injection**

- `category`: `Dhamma` or `Vinaya` (Derived from the parent folder name).
    
- `sutta_citations`: List of WikiLinks to Sutta texts (e.g., `["[[DN1]]"]`).
    
- `vinaya_citations`: List of WikiLinks to Vinaya texts (e.g., `["[[Vin.I.1]]"]`).

## 3. Functional Modules

### 1. The Gatekeeper (`gatekeeper.py`)

- **Trigger:** GitHub Pull Request.
    
- **Function:** Security & Quality Control.
    
- **Logic:**
    
    - Reject filenames not matching `Author - Title`.
        
    - Reject PDFs/EPUBs with < 5 Pali citations.
        
    - Reject Markdown with malicious HTML.
        
- Must validate citations against the specific domain (e.g., a file in `Inbox/Vinaya` _should_ probably have Vinaya citations, though not strictly enforced).

### 2. The Librarian (`librarian.py`)

- **Trigger:** Push to `main`.
    
- **Function:** Orchestrator.
    
- **Logic:**
    
    - Scans `Inbox/`.
        
    - If file exists in `Buddhist_Hub/`, SKIP.
        
    - If new, call specific converter (`pdf_converter`, `epub_converter`).
        
- **Path Routing:**
    
    - Source: `Inbox/Dhamma/md/Essay.md`
        
    - Dest: `Buddhist_Hub/Contributions/Dhamma/Essays/Essay.md`
        
- **Citation Sorting:**
    
    - Scans text for all standard Pali abbreviations.
        
    - Sorts into `sutta_citations` vs `vinaya_citations` based on book code.

### 3. PDF Converter (`pdf_converter.py`)

- **Library:** `pymupdf` (PyMuPDF).
    
- **Logic:**
    
    - Extract text to Markdown.
        
    - Extract images to `attachments/` folder.
        
    - Rewrite image links to `![[attachments/image.jpg]]`.
        
    - Regex scan for Sutta citations (`DN 1.1`, `M ii 45`) -> Normalize to `[[DN1.1]]`.
        
    - Inject YAML Frontmatter.
        

## Release Strategy

- **Frequency:** Automated on every push to `main`.
    
- **Artifacts:**
    
    1. `Buddhist_Hub_Full.zip` (Everything)
        
    2. `Buddhist_Hub_Library.zip` (Books/Papers only)
        
    3. `Buddhist_Hub_Community.zip` (Contributions only)