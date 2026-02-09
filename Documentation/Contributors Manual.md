# 🌟 Contributing to the Library

Welcome, and thank you for contributing 🙏  
This library is a **curated, interconnected collection of Dhamma and Vinaya resources**, designed to work as a single, coherent system inside Obsidian.

To keep everything clean, reliable, and link-safe, all contributions are processed through an automated **Gatekeeper** system.

Please follow the sections below carefully.

---

> [!info]+ 🧭 Quick Start: Contributor Checklist  
> **Before you submit, confirm all of the following:**
> 
> -  My file is placed inside the **Inbox** (not Contributions)
>     
> -  I used the **correct folder path** (Dhamma/Vinaya → Format → Author)
>     
> -  The **filename follows “Title First” rules**
>     
> -  The **Author folder name is standardized** (Ven., Ajahn, or Lay)
>     
> -  I did **not** add version numbers or dates to the filename
>     
> -  If updating, I **overwrote** the existing file (same name)
>     
> -  Images (if any) are in the **same folder** as the note
>     
> 
> ✅ If all boxes are checked, your file will be processed correctly.


> [!NOTE]- Folder structure
> 
> - Inbox
> 		- Dhamma 
> 			- pdf
> 				- Folders by author 
> 					- subfolders by type (book, studyguide, canvas, anthologies ets )
> 			- Reference only
> 				- Folders by author 
> 					- subfolders by type (book, studyguide, canvas, anthologies ets )
> 			- epub
> 				- Folders by author 
> 					- subfolders by type (book, studyguide, canvas, anthologies ets )
> 			- obsidian 
> 				- Folders by author 
> 					- subfolders by type (book, studyguide, canvas, anthologies, notes etc )	
> 		- Vinaya
> 			- Pdf
> 					- Folders by author
> 					- subfolders by type (book, studyguide, canvas, anthologies ets )
> 			- Reference only
> 				- Folders by author 
> 					- subfolders by type (book, studyguide, canvas, anthologies ets )
> 			- epub
> 				- Folders by author 
> 					- subfolders by type (book, studyguide, canvas, anthologies ets )
> 			- obsidian 
> 				- Folders by author 
> 					- subfolders by type (book, studyguide, canvas, anthologies ets )		
> 	- Contributions  
> 		- Dhamma
> 			- Folders by author 
> 				subfolders by type (book, studyguide, canvas, anthologies ets )
> 		- Vinaya
> 			- Folders by author 
> 				subfolders by type (book, studyguide, canvas, anthologies ets )


> [!note]+ 📥 1. Where to Put Your Contribution  
> All new work must go into the **Inbox**.  
> **Do not edit the `Contributions` folder directly**—it is fully automated.
> 
> **Required path structure:**
> 
> `Inbox / [Dhamma or Vinaya] / [Format] / [Author] / [Type]`


> [!example]- 📄 2. Supported Formats
> 
> ### PDFs
> 
> **Path:**  
> `.../pdf/Ven. Author/`
> 
> **Use for:**
> - Finished books
> - Essays
> - Study guides
> 
> ---
> 
> ### PDFs (For Reference Only)
> 
> **Path:**  
> `.../for_reference_only_pdf/Author/`
> 
> **Use for:**
> 
> - PDFs that do **not** convert cleanly to Markdown
>     
> 
> **What happens automatically:**
> 
> - Files remain as PDFs
>     
> - All sutta citations are extracted
>     
> - Citations are added as metadata for easy reference
>     
> 
> ---
> 
> ### EPUBs
> 
> **Path:**  
> `.../epub/Ven. Author/`
> 
> **Use for:**
> 
> - Digital books in EPUB format
>     
> 
> ⚠️ Only EPUB is supported (no MOBI, AZW, etc.)
> 
> ---
> 
> ### Obsidian Notes
> 
> **Path:**  
> `.../obsidian/Ven. Author/`
> 
> **Use for:**
> 
> - Markdown notes (`.md`)
>     
> - Canvases
>     
> - Thematic indexes
>     
> - Structured projects or research
>     
> 
> **Tip:**  
> Create subfolders for larger projects:
> 
> `.../obsidian/Ven. Thanissaro/Canvas/`


## File Naming Standards 
> [!warning]+ 🏷️ 3. File Naming Standards (Critical)  
> This is a shared public library.  
> **The automation relies entirely on filenames and folder names.**
> 
> Files that do not follow these rules are **automatically deleted from the Inbox**.


> [!check]- “Title First” Naming Convention  
> Place files inside the **correct Author folder**, using one of the following:
> 
> **Accepted formats:**
> 
> - `Title – Author.pdf`  
>     _Example:_  
>     `Wings to Awakening - Ven. Thanissaro.pdf`
>     
> - `Title.pdf` (inside Author folder)  
>     _Example:_  
>     `Ven. Thanissaro/Wings to Awakening.pdf`
>     
> - `Title only` inside Author folder
>     
>     - Accepted
>         
>     - Renamed automatically by the system
>         

> [!table]- 👤 Author Naming Conventions
> 
> |Category|Rule|Example Folder|Result|
> |---|---|---|---|
> |Ordained|Start with `Ven.`|Ven. Brahmali|Ven. Brahmali - Vinaya Analysis.md|
> |Thai Forest|Start with `Ajahn`|Ajahn Geoff|Ajahn Geoff - The Self.md|
> |Lay|Lastname Firstname|Gethin Rupert|Gethin Rupert - Foundations of Buddhism.md|

> [!danger]- ⛔ Automatic Rejection Policy  
> To keep the library usable and consistent, files that fail validation are **deleted**.
> 
> **Gatekeeper Logic:**
> 
> 1. **Filename contains “ - ”**  
>     → System trusts the filename
>     
>     - Input: `Ven. Sujato - Suttas.pdf`
>         
>     - Output: `Ven. Sujato - Suttas.md`
>         
> 2. **No “ - ” in filename**  
>     → System reads the **Author folder**
>     
>     - Input: `.../Ajahn Brahm/Mindfulness.pdf`
>         
>     - Output: `Ajahn Brahm - Mindfulness.md`
>         
> 3. **Failure mode**
>     
>     - No “ - ”
>         
>     - Not inside an Author folder  
>         → ❌ Rejected / skipped
>         
> 
> **Examples that will be rejected:**
> 
> - `Thanissaro - Wings.pdf` (Author first)
>     
> - `scan_001.pdf` (No metadata)
>     
> - `the_Self_v2_FINAL_EDIT.md` (Non-standard)
>     

> [!refresh]+ 🔄 4. Updating Existing Files  
> **Do not:**
> 
> - Create `v2`, `final`, or dated filenames
>     
> - Rename existing files
>     
> 
> **Correct method:**
> 
> - Overwrite the existing file in the Inbox
>     
> - Keep the **exact same filename**
>     
> 
> **Why:**  
> Git tracks history automatically. Renaming breaks links across the library.

---

> [!image]+ 🖼️ 5. Images & Attachments
> 
> **Obsidian Notes**
> 
> - Keep images in the **same folder** as the note
>     
> - They are copied automatically
>     
> 
> **PDFs & EPUBs**
> 
> - Images and covers are not extracted
>     
> - No action required
>