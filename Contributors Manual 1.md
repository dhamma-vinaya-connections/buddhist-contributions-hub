# 🌟 Contributing to the Library 

Welcome! This library is a curated, interconnected collection of Dhamma resources. To keep the quality high and the connections strong, we use an automated **Gatekeeper** system.

### Where do I put my Contribution files?
All new work goes into the **Inbox**. 
Don't edit the **Contributions** folder directly.

Navigate to: **Inbox / [Dhamma or Vinaya] / [Format] / [Author] / [type]**

Formats
- **PDFs:** Go to .../pdf/Ven. Author/
    - _Use for:_ Finished books, essays, or scans.
- **PDFs For Reference Only** /for_reference_only_pdf/Author/
	- These are pdf that when converted is more difficult to read as md file because of style. 
	- Therefore it is preferable to keep them in pdf.
	- The when the pdfs are in this folder the system extracts all the sutta citation links and include them as properties for easy reference 
- **Epubs:** Go to .../epub/Ven. Author/
    - _Use for:_ Digital books. 
    - The system automaticali convert epubs but not other files like mobi, etc.  
- **Obsidian/Notes:** Go to .../obsidian/Ven. Author/
    - _Use for:_ Your markdown notes (.md), Canvases, MOCS, Bases, etc. that you would like to share
    - _Subfolders:_ For ease of reference create a subfolder if it's a specific project (e.g., .../obsidian/Ven. Thanissaro/Canvas/).



###  File Naming Standards
As this is a public project for the benefit of many we try to keep it as organized as possible when we contribute for ease of reference for the users. 
The automation script relies on the filename to organize the library. 
If you break these rules, the **system will automatically delete your file** from the Inbox and won't include it in the contributions folder. Every contribution **must** follow this format and conventions:

#### "Title First" convention. 
Please put the file into the correct Author name. There are 2 options: 
* Title - Author.pdf 
	* Example: Wings to Awakening - Ven. Thanissaro.pdf
	* In the right
* Title. pdf   
	* Only the title in the Author folder 
	* Example. Ven. Thanissaro/Wings to Awakening.pd
*  Title only into a Autor folder with the title will be accepted & renamed automatically according to the folder 

#### Author Title Conventions:
We standardize names to respect lineages and status.

|**Category**|**Rule**|**Example Folder Name**|**Resulting Filename**|
|---|---|---|---|
|**Ordained (General)**|Start with Ven.|Ven. Brahmali|Ven. Brahmali - Vinaya Analysis.md|
|**Thai Forest**|Start with Ajahn|Ajahn Geoff|Ajahn Geoff - The Self.md|
|**Lay Person**|Lastname Name|Gethin Rupert|Gethin Rupert - Foundations of Buddhism.md|

#### ⛔ Automatic "Rejection" Policy 
To keep a beneficial library it has to be as organized and clean as possible.
Therefore any file that does not follow these rules will be deleted from inbox and not included in convention folder.

**The Filter Logic:**
1. **If the file has " - ":** The script trusts the filename.
    - _Input:_ Ven. Sujato - Suttas.pdf $\rightarrow$ _Output:_ Ven. Sujato - Suttas.md
2. **If the file has NO " - ":** The script looks at the **Parent Folder**.
    - _Input:_ .../Ajahn Brahm/Mindfulness.pdf $\rightarrow$ _Output:_ Ajahn Brahm - Mindfulness.md
3. **FAILURE MODE:** If the file has NO " - " **AND** is not in an Author folder (it's loose in the pdf folder).
    - _Result:_ **REJECTED / SKIPPED.** The script cannot determine the author, so it will not process the file.
* **❌ DON'T:** Thanissaro - Wings.pdf (Author first) 
* **❌ DON'T:** scan_001.pdf (No info)
* **❌ DON'T:** he_Self_v2_FINAL_EDIT.md (Junk text)


### 3. Version Control (Updating Files)

- **Do not** create new files for updates (e.g., Essay_v2.md).
    
- **Do not** rename the file to add dates.
    
- **Action:** Simply overwrite the existing file in the Inbox with your new version. Keep the **exact same filename**.
    
- **Why?** The system uses Git to track history. If you rename the file, you break the links in our library.
    

### 4. Images & Attachments

- **For Obsidian Notes:** If your note uses images, keep the image file **in the same folder** as your note. The script will copy it automatically.
    
- **For PDFs/Epubs:** We do not extract images from books. Do not worry about covers.