# 🌿 The Gardener’s Guide: Editing & Curation

> _"The robots build the library structure. Humans build the meaning."_

Welcome to the **Editor's Team**.

While general contributors add files to the Inbox, **Editors** are responsible for polishing, connecting, and perfecting the files inside the `Contributions/` folder.

This guide covers how to request access, how to edit metadata safely, and how to curate the library without breaking the automation.

---

> [!abstract]- 🔐 1. How to Become an Editor By default, the `Contributions/` folder is **read-only** to the public to prevent accidental deletions. To modify these files, you need **Trusted Editor Access**.
> 
> ### Step 1: Request Access
> 
> 1. Open an [Issue](https://www.google.com/search?q=../../issues) in this repository.
>     
> 2. Title it: **"Request: Editor Access"**.
>     
> 3. In the body, briefly state why you want to help (e.g., _"I want to tag all the Thai Forest talks with correct topics"_).
>     
> 4. Wait for the Administrator to add you as a **Collaborator**.
>     
> 
> ### Step 2: Accept Invitation
> 
> Check your email or GitHub notifications. Once you accept, you will have the ability to:
> 
> - Edit files directly in `Contributions/`.
>     
> - Merge Pull Requests.
>     
> - Manage library organization.
>     

> [!info]- 🛠️ 2. The Editor’s Workflow (Safe vs. Dangerous) Your primary job is **Curation**. You are not moving files; you are improving them.
> 
> ### ✅ Safe Tasks (Do These!)
> 
> - **Update Topics:** Change `topic: to_fill` to `topic: meditation, breath`.
>     
> - **Fix Typos:** Correct spelling errors in the Markdown text.
>     
> - **Add Links:** Connect a Sutta reference like `MN 10` to `[[MN10]]`.
>     
> - **Add Notes:** Insert callouts or summaries at the top of a file.
>     
> 
> ### ⛔ Dangerous Tasks (Avoid!)
> 
> - **❌ RENAMING FILES:** > * _Why?_ The automation tracks files by name. Renaming breaks history and kills links.
>     
>     - _Exception:_ If a filename is horribly wrong (e.g., `Scan_001.md`), delete it and re-upload properly to Inbox.
>         
> - **❌ MOVING FILES:** > * _Why?_ The folder structure is auto-generated based on Author/Category. Moving a file manually confuses the robots.
>     

> [!example]- 🏷️ 3. Managing Topics (The Most Important Job) The automated script makes a "best guess" at topics, but it often fails. Humans are needed here.
> 
> ### How to Edit Topics
> 
> 1. Navigate to the file in `Contributions/`.
>     
> 2. Click the **Pencil Icon** ✏️ (Edit file).
>     
> 3. Look at the **Frontmatter** (the block between `---` at the top).
>     
> 
> **Bad Example (Breaks the Library 💥):**
> 
> YAML
> 
> ```
> topic:meditation,Ethics  <-- No space after colon, Capital letters
> ```
> 
> **Good Example (Perfect ✅):**
> 
> YAML
> 
> ```
> topic: meditation, ethics
> ```
> 
> ### The Rules of Topic Tagging
> 
> 4. **Lowercase Only:** Always use `metta`, never `Metta`.
>     
> 5. **Singular Only:** Use `precept`, never `precepts`.
>     
> 6. **Space After Colon:** `key: value`.
>     
> 7. **Comma Separated:** `topic: a, b, c`.
>     

> [!tip]- 🔗 4. Fixing Links & Anchors Sometimes the automated conversion leaves "dead links."
> 
> **Problem:**
> 
> > "As the Buddha said in [[MN 10]]..." (Link is not clickable)
> 
> **Fix:**
> 
> > "As the Buddha said in [[MN10]]..." (Remove spaces in citation codes)
> 
> ---
> 
> **Problem:**
> 
> > "See the section on [[#^part1]]..." (Anchor missing)
> 
> **Fix:**
> 
> > You can manually add an anchor to any paragraph by adding `^part1` at the end of it.
> 
> > _Example:_ "This is the paragraph I want to link to. ^part1"

> [!bug]- 🚑 5. Troubleshooting **"I broke the YAML!"** If you save a file and the Frontmatter looks broken (no color highlighting), you likely forgot a space or used a forbidden character (like `:` inside a tag).
> 
> - **Fix:** Open the file, check for red highlights, and ensure the format matches the **Good Example** above.
>     
> 
> **"I accidentally deleted a file!"**
> 
> - **Fix:** Don't panic. Go to the "Commits" history, find the deletion, and click "Revert."
>     

> [!quote] 🌟 The Golden Rule **"Leave the campsite cleaner than you found it."**
> 
> If you open a file to read it, and you spot a typo or a missing tag—fix it right then and there. This is how the library grows.