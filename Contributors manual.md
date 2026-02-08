# 🌟 Contributing to the Library 

Welcome! This library is a curated, interconnected collection of Dhamma resources. To keep the quality high and the connections strong, we use an automated **Gatekeeper** system.

### 1. Where do I put my files?

All new work goes into the **Inbox**. 
Never edit the `Contributions` folder directly.

Navigate to: `Inbox / [Dhamma or Vinaya] / [Format] / [Author] / [Subfolder]`

- **PDFs:** Go to `.../pdf/Ven. Author/`
    - _Use for:_ Finished books, essays, or scans.
- **PDFs For Reference Only**
	- These are pdf that when converted is more difficult to read as md file becasue of style so it is preferable to keep them in pdf but extract all the sutta links and include the properties for easy reference /for_reference_only_pdf/Author

- **Epubs:** Go to `.../epub/Ven. Author/`
    - _Use for:_ Digital books.

- **Obsidian/Notes:** Go to `.../obsidian/Ven. Author/`
    - _Use for:_ Your markdown notes (`.md`), Canvases, or MOCS, Bases, etc.
    - _Subfolders:_ You **must** create a subfolder if it's a specific project (e.g., `.../obsidian/Ven. Thanissaro/Canvas/`).
        

### 2. The Golden Rule: Naming Files

The automation script relies on the filename to organize the library. You **must** follow this format:
If you break these rules, the **Gatekeeper will automatically delete your file** from the Inbox. 

### 1. File Naming Standards
We use a **"Title First"** convention. 
* **✅ DO:** `Wings to Awakening - Ven. Thanissaro.pdf` 
* **✅ DO:** `Mindfulness in Plain English - Ven. Gunaratana.epub` 
* **❌ DON'T:** `Thanissaro - Wings.pdf` (Author first) 
* **❌ DON'T:** `scan_001.pdf` (No info)
* he_Self_v2_FINAL_EDIT.md` (Junk text)

> **Pro Tip:** If you are lazy, just drop the file into a named folder! > `Inbox/Dhamma/pdf/Ven. Thanissaro/Wings to Awakening.pdf` -> **Accepted & Renamed automatically.**

**The Automation:** If you organize your Inbox folders correctly, the system will do this for you.

**Author Title Conventions:**

We standardize names to respect lineages and status.

|**Category**|**Rule**|**Example Folder Name**|**Resulting Filename**|
|---|---|---|---|
|**Ordained (General)**|Start with `Ven.`|`Ven. Brahmali`|`Ven. Brahmali - Vinaya Analysis.md`|
|**Thai Forest**|Start with `Ajahn`|`Ajahn Geoff`|`Ajahn Geoff - The Self.md`|
|**Lay Person**|`Lastname Name`|`Gethin Rupert`|`Gethin Rupert - Foundations of Buddhism.md`|

#### ⛔ The "Rejection" Policy (The Gatekeeper)

Any file that does not follow these rules will fail the audit.

**The Filter Logic:**

1. **If the file has " - ":** The script trusts the filename.
    
    - _Input:_ `Ven. Sujato - Suttas.pdf` $\rightarrow$ _Output:_ `Ven. Sujato - Suttas.md`
        
2. **If the file has NO " - ":** The script looks at the **Parent Folder**.
    
    - _Input:_ `.../Ajahn Brahm/Mindfulness.pdf` $\rightarrow$ _Output:_ `Ajahn Brahm - Mindfulness.md`
        
3. **FAILURE MODE:** If the file has NO " - " **AND** is not in an Author folder (it's loose in the `pdf` folder).
    
    - _Result:_ **REJECTED / SKIPPED.** The script cannot determine the author, so it will not process the file.




### 3. Version Control (Updating Files)

- **Do not** create new files for updates (e.g., `Essay_v2.md`).
    
- **Do not** rename the file to add dates.
    
- **Action:** Simply overwrite the existing file in the Inbox with your new version. Keep the **exact same filename**.
    
- **Why?** The system uses Git to track history. If you rename the file, you break the links in our library.
    

### 4. Images & Attachments

- **For Obsidian Notes:** If your note uses images, keep the image file **in the same folder** as your note. The script will copy it automatically.
    
- **For PDFs/Epubs:** We do not extract images from books. Do not worry about covers.