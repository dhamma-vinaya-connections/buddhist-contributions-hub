# 🛠️ Developer’s Guide: The Engine Room

> _"Contributors add books. Editors fix typos. Developers upgrade the machinery."_

This guide is for **Python Developers** who want to modify the automation scripts in `scripts/`.

It covers environment setup, the architecture of the pipeline, and how to test your changes locally before pushing to GitHub.

---

> [!abstract]- 🏗️ 1. Architecture Overview
> 
> The system follows a **Hub-and-Spoke** model.
> 
> **The Conductor:**
> 
> - `main.py`: The entry point. It scans the `Inbox/`, identifies file types, and dispatches them to the correct worker.
>     
> 
> **The Workers:**
> 
> - `pdf_converter.py`: Uses `pymupdf4llm` to convert PDFs to Markdown.
>     
> - `epub_converter.py`: Unzips EPUBs, fixes anchors, and patches links.
>     
> - `obsidian_processor.py`: Handles `.md` notes and `.canvas` files.
>     
> - `reference_scanner.py`: Extracts citations from image-heavy PDFs (OCR-lite).
>     
> 
> **The Utilities:**
> 
> - `gatekeeper.py`: Validates quality (word count, citation density). Deletes junk.
>     
> - `citation_scanner.py`: The "Brain". Finds `MN 10` and converts it to `[[MN10]]`.
>     
> - `author_tools.py`: Standardizes names (`Thanissaro` -> `Ven. Thanissaro`) and topics.
>     

> [!info]- 💻 2. Local Setup (Run it on your PC)
> 
> Don't test on the live GitHub repo! Run it on your laptop first.
> 
> **Prerequisites:**
> 
> - Python 3.10+
>     
> - Git
>     
> 
> **Installation:**
> 
> 1. Clone the repository:
>     
>     Bash
>     
>     ```
>     git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
>     cd YOUR-REPO
>     ```
>     
> 2. Create a virtual environment (Optional but recommended):
>     
>     Bash
>     
>     ```
>     python -m venv venv
>     source venv/bin/activate  # Mac/Linux
>     .\venv\Scripts\activate   # Windows
>     ```
>     
> 3. Install dependencies:
>     
>     Bash
>     
>     ```
>     pip install -r scripts/requirements.txt
>     ```
>     

> [!example]- 🧪 3. How to Test Changes
> 
> **The Testing Loop:**
> 
> 4. **Place a Test File:**
>     
>     Drop a PDF or EPUB into `Inbox/Dhamma/pdf/Ven. Test/`.
>     
> 5. **Run the Script:**
>     
>     From the root folder, run:
>     
>     Bash
>     
>     ```
>     python scripts/main.py
>     ```
>     
> 6. **Check the Output:**
>     
>     - Look at the console logs.
>         
>     - Check `Contributions/` to see if the file was created.
>         
>     - Check `Inbox/` to see if the file was deleted.
>         
> 7. **Reset:**
>     
>     Delete the generated file from `Contributions/` and put the source file back in `Inbox/` to try again.
>     

> [!tip]- 🧩 4. Key Libraries & Tools
> 
> We use specific libraries for specific jobs. Please stick to them.
> 
> - **PDF Parsing:** `pymupdf4llm` (Standard) or `fitz` (PyMuPDF).
>     
> - **EPUB Parsing:** `EbookLib` + `BeautifulSoup4`.
>     
> - **Frontmatter:** `PyYAML`.
>     
> - **Regex:** Standard Python `re` module.
>     

> [!warning]- 🛡️ 5. The "Code Owners" Rule
> 
> The `scripts/` folder is **Protected**.
> 
> - You cannot push directly to `main`.
>     
> - You must open a **Pull Request (PR)**.
>     
> - The Administrator (@YourUsername) **must approve** your PR before it can be merged.
>     
> 
> **Before submitting a PR:**
> 
> - [ ] Did you update `requirements.txt` if you added a new library?
>     
> - [ ] Did you run a local test on both a PDF and an EPUB?
>     
> - [ ] Did you follow the existing naming conventions (snake_case)?
>     

---

### 🚀 Quick Command Reference

|**Action**|**Command**|
|---|---|
|**Install Libs**|`pip install -r scripts/requirements.txt`|
|**Run Processor**|`python scripts/main.py`|
|**Check Citations**|_Use the `citation_scanner.py` standalone for debugging regex._|
|**Check Quality**|_Use `gatekeeper.py` to test thresholds._|