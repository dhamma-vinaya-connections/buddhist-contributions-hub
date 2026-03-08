If you work with **Find / Replace in VSCode, Obsidian, or regex tools**, there are a handful of patterns you end up using all the time. the ones that actually save time when editing texts, suttas, markdown, etc.

---

## 1. Find a word

Exact word only:


\bword\b


Example:


\bMN\b


Matches `MN` but not `MND` or `AMN`

---

## 2. Find any number


\d+


Examples matched:


1
23
456


Number with decimal:


\d+\.\d+


Matches:


12.3
4.56


Good for suttas:


sn\d+\.\d+


---

## 3. Find anything between two things


start.*end


Example:


\[\[.*\]\]


Matches:


[[MN1]]
[[SN12.3]]


Non-greedy (very important):


start.*?end


Example:


\[\[.*?\]\]


Use this almost always.

---

## 4. Find a full line


^.*$


Line starting with:


^SN


Line ending with:


pali$


Empty line:


^$


Line with spaces only:


^\s*$


---

## 5. Find a paragraph

Paragraph = text until empty line


(.|\n)*?\n\s*\n


Very useful when cleaning notes.

---

## 6. Find multiple possible words


word1|word2|word3


Example:


MN|SN|AN|DN


Example:


pali|bodhi|thanissaro


---

## 7. Find words separated by space / comma / anything

Any space:


\s+


Comma or space:


[,\s]+


Example:


MN41, MN42 MN43


Pattern:


MN\d+[,\s]+MN\d+


---

## 8. Find inside brackets

Double brackets:


\[\[.*?\]\]


Parentheses:


\(.*?\)


Curly:


\{.*?\}


---

## 9. Find Markdown links


\[\[.*?\]\]


With number:


\[\[[A-Z]+\d+(\.\d+)?\]\]


Matches:


[[MN1]]
[[SN12.3]]
[[AN4.23]]


Very useful for sutta vault.

---

## 10. Find headings

H1 H2 H3 etc


^#+ .*


Only H1:


^# .*


Only H2:


^## .*


---

## 11. Find everything after something


start.*


Example:


SN.*


Everything before something:


.*end


---

## 12. Find notes / footnotes / refs (very useful for Thanissaro cleaning)


\[\d+\]


Footnote refs like:


[1]
[23]


With anchors:


\[\d+\]\(#\^.*?\)


---

## 13. Find repeated spaces


 {2,}


Replace with:

Good for cleaning text.

---

## 14. Find lines containing something but not something else

Find MN but not MN1:


MN(?!1)


Find lines without word:


^(?!.*note).*


Very powerful.

---

## 15. Find across multiple lines (VSCode / Obsidian regex)


[\s\S]*?


Example:


START[\s\S]*?END


Best pattern for multiline.

---

## If you want, I can give you next:

- regex for **sutta names**
    
- regex for **file names**
    
- regex for **Obsidian links**
    
- regex for **Thanissaro notes cleaning**
    
- regex for **SN / AN / MN parsing**
    

Those are the ones you actually use every day in your project.