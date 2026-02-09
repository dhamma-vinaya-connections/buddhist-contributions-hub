

## 1. GATEKEEPER_MANUAL.md
*The "Policy Document" explaining the logic behind the automated decisions.*

### 🛡️ The Gatekeeper Protocol

The Gatekeeper is an automated script that protects the integrity of the library. It enforces strict security, quality, and organizational standards.

## 1. Security Gates

### A. Malware Protection (Magic Bytes)
The system ignores file extensions and reads the file header (Magic Numbers).
* **PDF:** Must start with `%PDF`
* **EPUB:** Must start with `PK` (Zip container)
* **Markdown:** Must be valid text (no binary null bytes)
* **Action:** If a file is an `.exe` renamed to `.pdf`, it is **IMMEDIATELY DELETED**

### B. Size Limits
* **Threshold:** 25 MB.
* **Logic:** Prevents repository bloat. Git struggles with files >100MB; we keep a safety buffer.
* **Action:** Files > 25MB are **DELETED**.

### C. Plugin Blocker
* **Target:** `.obsidian` folder and plugin files.
* **Logic:** Protects users from malicious scripts in shared vaults.
* **Action:** Ignored / Blocked.

---

## 2. Quality Gates (The Density Curve)

We use a "Dynamic Threshold" to ensure content relevance.

| Content Type    | Definition     | Requirement         | Failure Action |     |
| --------------- | -------------- | ------------------- | -------------- | --- |
| **Short Essay** | < 15,000 words | **Min 5 Citations** | **DELETE**     |     
| **Book** | > 15,000 words | **Min 20 Citations** | **DELETE** | 
|**Personal Note** | Markdown (`.md`) | **Min 5 WikiLinks** | **DELETE** |


* **Zero-Text Policy:** If a PDF yields < 50 characters of text (Image Scan), it is treated as having 0 citations and is **DELETED**.

---

## 3. Organizational Gates

### A. The Orphan Check
A file must have an identifiable author.
1.  **Check Filename:** Does it have ` - `? (e.g., `Title - Author.pdf`)
2.  **Check Folder:** Is it inside a named folder? (e.g., `Ven. Bodhi/`)
3.  **Result:** If BOTH are missing -> **DELETE**.

### B. Standardization
The Gatekeeper normalizes metadata on entry.
* **Authors:** `Bhikkhu Bodhi` -> `Ven. Bodhi`.
* **Types:** `manuals` / `guides` -> `Study Guide`.

## Manual check 
### Phase 1: The "Garbage Check" (Before Running Scripts)

Before you run anything, look at the **Inbox**.

1. **Filenames:** Are they clean? (`Author - Title`). Rename them now if they are messy.
    
2. **Locations:** Is a PDF sitting in the `obsidian` folder? Move it to `pdf`.
    
3. **Typos:** Did someone write `Ven. Thanissaro` as `Ven. Thannisaro`? Fix it, or you'll get two separate author folders.
    

### Phase 2: Run the Processor

1. Open your terminal.
2. Navigate to `repo/scripts`.
3. Run the master script: python main.py
4. **Read the Output:** Watch the terminal.
    - ✅ `Finished` means it worked.
    - ⏩ `Skipping` means a book already existed (Safe Mode).
    - ♻️ `Updating` means an Obsidian note was updated (Version Control).

### Phase 3: The "Garden Walk" (Quality Control)

Go to the **Contributions** folder.

1. **Check for Duplicates:** Do you see `Ven. Thanissaro - Essay.md` AND `Ven. Thanissaro - Essay v2.md`?
    - _Action:_ Delete the old one manually.
2. **Check Reference Stubs:** Open a "Reference Only" file. Does the link work? Is the metadata correct?

### Phase 4: Git Commit & Release

1. **Status Check:**
    Bash
    ```
    git status
    ```
    - Look at what is being added. Does it look right?
2. **Commit:**

    git add .
    git commit -m "Library Update: Added 3 books by Ven. Brahmali, updated notes on Vinaya."
    git push
    
3. **Release (Optional):**
    
    - Zip the `Contributions` folder -> `contributions.zip` (For distribution).
    - Zip the `Inbox` folder -> `inbox.zip` (For backup).


---

### 🚨 Troubleshooting Cheat Sheet

|**Problem**|**Solution**|
|---|---|
|**"The script didn't move my PDF!"**|Check if the file already exists in `Contributions`. The script skips duplicates to protect notes. Delete the old one in `Contributions` if you really want to replace it.|
|**"My Canvas links are broken!"**|Did you rename the file linked in the Canvas? Never rename files once they are linked. Restore the old name.|
|**"I have two folders for the same author."**|Check spelling. `Ven. Thanissaro` vs `Ven. Thanissaro` (trailing space). Merge them manually in `Contributions` and fix the Inbox folder name.|
|**"Images are missing in my Note."**|Ensure the image file (`image.png`) was inside the `Inbox/.../Author/Project` folder _alongside_ the `.md` file before running the script.|

This documentation makes your system robust. It tells humans how to behave so the robots can do their job perfectly.

