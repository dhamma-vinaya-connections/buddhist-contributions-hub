
# 👑 Administrator’s Manual

> _"The Editors garden the plants. The Admin maintains the greenhouse."_

This guide is for the **Repository Owner** and **System Administrators**.

It covers system maintenance, script updates, user management, and disaster recovery.

---

> [!important]- 🚨 1. Monitoring the Robots (GitHub Actions)
> 
> Your automation runs on "GitHub Actions." Sometimes, it fails.
> 
> **How to Check Status:**
> 
> 1. Click the **Actions** tab at the top of the repo.
>     
> 2. Look at the list on the left:
>     
>     - **Dhamma Processor:** Runs every time a file is uploaded to Inbox.
>         
>     - **Publish Library:** Runs every 15 days (or manually).
>         
> 
> **If you see a Red X (Failure):**
> 
> 1. Click the failed run.
>     
> 2. Click the step that failed (usually "Run Main Script").
>     
> 3. Scroll down to see the error message (e.g., `FileNotFoundError`, `SyntaxError`).
>     
> 4. **Fix:** Usually, this means a user uploaded a corrupt file that crashed the script. Delete the bad file from `Inbox/` and the system will recover.
>     

> [!tip]- 👥 2. User Management (Adding Editors)
> 
> When a contributor asks for "Editor Access" (via an Issue):
> 
> **To Add a User:**
> 
> 1. Go to **Settings** (Top Right) → **Collaborators**.
>     
> 2. Click **Add people**.
>     
> 3. Type their GitHub username or email.
>     
> 4. Select **Write** access (Do not give Admin access unless you trust them with your life).
>     
> 
> **To Remove a User:**
> 
> - Go to the same screen and click the **Trash Icon** next to their name.
>     

> [!settings]- ⚙️ 3. Updating the "Brain" (Adding Authors/Types)
> 
> If a new monk becomes famous, or you want to add a new category (e.g., `Chants`), you need to teach the robots.
> 
> **File to Edit:** `scripts/author_tools.py`
> 
> **To Add a New Author:**
> 
> Look for the `AUTHOR_MAP` dictionary and add a new line:
> 
> Python
> 
> ```
> AUTHOR_MAP = {
>     "thanissaro": "Ven. Thanissaro",
>     "new monk": "Ven. New Monk",  <-- Add this line
> }
> ```
> 
> **To Add a New Folder Type:**
> 
> Look for the `TYPE_MAP` dictionary:
> 
> Python
> 
> ```
> TYPE_MAP = {
>     "manual": "study guide",
>     "chanting": "chant",  <-- Add this line
> }
> ```
> 
> _Note: Changes take effect immediately for all **new** uploads._

> [!bug]- 🚑 4. Disaster Recovery (Reverting Mistakes)
> 
> **Scenario: An Editor accidentally deleted the entire "Sutta" folder.**
> 
> **The Fix (The Time Machine):**
> 
> 1. Go to the **Code** tab.
>     
> 2. Click **Commits** (the clock icon/number on the right).
>     
> 3. Find the "bad commit" (e.g., "Delete Suttas").
>     
> 4. Click the **Copy SHA** button (the little clipboard next to the code `8f3d...`).
>     
> 5. Open your local terminal (or use GitHub Desktop) and run:
>     
>     Bash
>     
>     ```
>     git revert [SHA_CODE]
>     ```
>     
> 6. Push the changes. The folder will reappear as if by magic.
>     

> [!check]- 📦 5. Manual Release (Forcing a Update)
> 
> If you made major changes and don't want to wait for the 15-day schedule:
> 
> 1. Go to **Actions**.
>     
> 2. Click **📦 Publish Library**.
>     
> 3. Click **Run workflow** (Green Button).
>     
> 4. Wait 1 minute.
>     
> 5. A new `.zip` file will appear in the **Releases** section for users to download.
>     

---

### 🛡️ Summary of Responsibilities

|**Role**|**Responsibility**|**Access Level**|
|---|---|---|
|**Contributor**|Uploads new files to Inbox|**Write** (Inbox Only)|
|**Editor**|Fixes typos, tags topics, links notes|**Write** (Contributions)|
|**Admin (You)**|Updates scripts, manages users, fixes crashes|**Admin** (Everything)|