## Part 1: Instructions for Contributors

**Target Audience:** Monks, students, or editors adding files to the repository.

### 1. Where do I put my files?

All new work goes into the **Inbox**. Never edit the `Contributions` folder directly.

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

1 
`Ven. Author Name - The Title of the Work.ext`

| **✅ DO THIS**                              | **❌ DO NOT DO THIS**                             |
| ------------------------------------------ | ------------------------------------------------ |
| `Ven. Thanissaro - Wings to Awakening.pdf` | `wings-to-awakening-final.pdf` (No Author)       |
| `Ven. Brahmali - Vinaya Analysis.md`       | `Vinaya Analysis - Ven. Brahmali.md` (Backwards) |
| `Ajahn Geoff - The Self.md`                | `The_Self_v2_FINAL_EDIT.md` (Junk text)          |

#### Naming Standards

**The Rule:** Every file in the final library **must** start with the Author's Name.

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