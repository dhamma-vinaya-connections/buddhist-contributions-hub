**Target Audience:** You (the Maintainer). You are the Librarian.

### Phase 1: The "Garbage Check" (Before Running Scripts)

Before you run anything, look at the **Inbox**.

1. **Filenames:** Are they clean? (`Author - Title`). Rename them now if they are messy.
    
2. **Locations:** Is a PDF sitting in the `obsidian` folder? Move it to `pdf`.
    
3. **Typos:** Did someone write `Ven. Thanissaro` as `Ven. Thannisaro`? Fix it, or you'll get two separate author folders.
    

### Phase 2: Run the Processor

1. Open your terminal.
    
2. Navigate to `repo/scripts`.
    
3. Run the master script:
    
    Bash
    
    ```
    python main.py
    ```
    
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
    
    Bash
    
    ```
    git add .
    git commit -m "Library Update: Added 3 books by Ven. Brahmali, updated notes on Vinaya."
    git push
    ```
    
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


Here is the visual logic of how the system decides:

### 1. The "Safe Zone" (Inside an Author Folder)

If a file is inside `Inbox/Dhamma/pdf/Ven. Thanissaro/`, the filename **does not matter**.

- `Wings to Awakening.pdf` -> **ACCEPTED**.
    
    - _System thinks:_ "The user didn't write the author in the filename, but they put it in the 'Ven. Thanissaro' folder. I will rename it to `Ven. Thanissaro - Wings to Awakening.md` automatically."
        

### 2. The "Danger Zone" (Loose Files)

If a file is sitting directly in `Inbox/Dhamma/pdf/` (no subfolder):

- `Ven. Thanissaro - Wings to Awakening.pdf` -> **ACCEPTED**.
    
    - _System thinks:_ "It's a loose file, but the filename has 'Ven. Thanissaro - '. I can read the author. Processing..."
        
- `Wings to Awakening.pdf` -> **REJECTED**.
    
    - _System thinks:_ "It's loose, and there is no Author Name in the filename. I don't know who wrote this. **SKIP.**"