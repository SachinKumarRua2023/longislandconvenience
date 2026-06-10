# 🔧 Website Setup - Smart Folder Organization

## Overview

This script automatically:
1. ✅ Checks your Odoo instance for all websites
2. ✅ Finds Long Island Cards website ID
3. ✅ Creates a properly named folder: `WEBSITE_[ID]_[NAME]`
4. ✅ Copies all scripts to the new folder
5. ✅ Updates scripts with correct Website ID
6. ✅ Ready to deploy!

---

## Quick Start

### Run Setup Script

```bash
python setup_website_folder.py
```

**This will:**
1. Connect to Odoo
2. List all websites in your Odoo instance
3. Find Long Island Cards
4. Create new folder with correct ID and name
5. Copy and update all scripts
6. Show you exactly what to do next

---

## What Happens Step-by-Step

### Step 1: Connect to Odoo
```
[1/4] Connecting to Odoo...
[OK] Connected
```

### Step 2: List All Websites
```
Available Websites in Odoo:
────────────────────────────────────────────────────────────────────────────────
1. ID: 1 | Name: Long Island Cards | Domain: longislandcards.com
2. ID: 2 | Name: Dave & Adams | Domain: dacardworld.com
3. ID: 3 | Name: Another Store | Domain: othersite.com
```

### Step 3: Find Long Island Cards
```
✓ Found: Long Island Cards
  - ID: 1
  - Domain: longislandcards.com
```

### Step 4: Create New Folder
```
Creating folder: WEBSITE_1_LONG_ISLAND_CARDS

✓ Copied 16 files to new folder
```

### Final: Update Scripts
```
Updating scripts with correct Website ID...
  ✓ Updated deploy_homepage_odoo.py (WEBSITE_ID = 1)
  ✓ Updated add_images_homepage.py (WEBSITE_ID = 1)
```

---

## Example Output

```
================================================================================
LONG ISLAND CARDS - Smart Website Setup
================================================================================

[1/4] Connecting to Odoo...
[OK] Connected

[2/4] Checking all websites...

Available Websites in Odoo:
────────────────────────────────────────────────────────────────────────────────
1. ID: 1 | Name: Long Island Cards | Domain: longislandcards.com
2. ID: 2 | Name: Another Site | Domain: anothersite.com

[3/4] Finding Long Island Cards website...

✓ Found: Long Island Cards
  - ID: 1
  - Domain: longislandcards.com

[4/4] Organizing folder structure...

Creating folder: WEBSITE_1_LONG_ISLAND_CARDS

  ✓ homepage.html
  ✓ deploy_homepage_odoo.py
  ✓ add_images_homepage.py
  ✓ add_images_homepage_configurable.py
  ✓ add_images_website_1.py
  ✓ add_images_website_1_configurable.py
  ✓ check_websites.py
  ✓ homepage_config.json
  ✓ category_config.json
  ✓ README_homepage_images.md
  ✓ README_add_images.md
  ✓ QUICKSTART.md
  ✓ SCRIPTS_OVERVIEW.md
  ✓ DEPLOYMENT_GUIDE.md
  ✓ HOMEPAGE_DEPLOYMENT_CHECKLIST.md

Updating scripts with correct Website ID...

  ✓ Updated deploy_homepage_odoo.py (WEBSITE_ID = 1)
  ✓ Updated add_images_homepage.py (WEBSITE_ID = 1)

================================================================================
SETUP COMPLETE!
================================================================================

Website: Long Island Cards
Website ID: 1
Domain: longislandcards.com

New Folder: WEBSITE_1_LONG_ISLAND_CARDS
Location: c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\...

✅ All scripts moved and updated!

NEXT STEPS:

1. Navigate to the new folder:
   cd "c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\..."

2. Deploy the homepage:
   python deploy_homepage_odoo.py

3. Verify on website:
   Go to https://longislandcards.com
```

---

## New Folder Structure

After running the script, you'll have:

```
SCRIPTS_BY_WEBSITE/
├── WEBSITE_1_LONG_ISLAND_CARDS/     ← New folder (properly named)
│   ├── homepage.html
│   ├── deploy_homepage_odoo.py       ← Website ID updated
│   ├── add_images_homepage.py        ← Website ID updated
│   ├── add_images_homepage_configurable.py
│   ├── add_images_website_1.py
│   ├── add_images_website_1_configurable.py
│   ├── homepage_config.json
│   ├── category_config.json
│   ├── check_websites.py
│   ├── README_homepage_images.md
│   ├── README_add_images.md
│   ├── QUICKSTART.md
│   ├── SCRIPTS_OVERVIEW.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── HOMEPAGE_DEPLOYMENT_CHECKLIST.md
│   └── SETUP_INSTRUCTIONS.md          ← This file
│
└── WEBSITE_1/                        ← Old folder (can delete later)
    └── [original files]
```

---

## What Gets Updated Automatically

### Website ID in Scripts

The script updates the `WEBSITE_ID` variable in:
- `deploy_homepage_odoo.py`
- `add_images_homepage.py`

**Before:**
```python
WEBSITE_ID = 1
```

**After (if your Long Island Cards ID is 2):**
```python
WEBSITE_ID = 2
```

---

## Next Steps After Setup

Once the script completes:

### Step 1: Navigate to New Folder
```bash
cd "WEBSITE_1_LONG_ISLAND_CARDS"
```

### Step 2: Deploy Homepage
```bash
python deploy_homepage_odoo.py
```

### Step 3: Verify
Go to your website (e.g., https://longislandcards.com)
- Clear cache: Ctrl+Shift+Delete
- Hard refresh: Ctrl+Shift+R
- Homepage should be updated!

### Step 4: Add Images (Optional)
```bash
python add_images_homepage.py
```

---

## Troubleshooting

### "Connection failed" Error
- **Check:** Odoo URL and credentials are correct
- **Verify:** Odoo server is running and accessible

### "Long Island Cards not found" Error
The script will ask you to select from the list:
```
Please select from the list above:
Enter the number (1-3): 
```
Just type the number (1, 2, or 3) and press Enter

### "Could not copy files" Error
- **Check:** You have read/write permissions
- **Verify:** Files in WEBSITE_1 folder exist
- **Try:** Run as Administrator

### Files in wrong folder
- Don't worry! The setup script copies files (doesn't delete)
- You can manually delete WEBSITE_1 folder later if needed
- Or keep it as backup

---

## What's Inside the New Folder

| File | Purpose |
|------|---------|
| `homepage.html` | Complete custom homepage design |
| `deploy_homepage_odoo.py` | Deploy to Odoo (Website ID already set!) |
| `add_images_homepage.py` | Add category images |
| `add_images_homepage_configurable.py` | Advanced image configuration |
| `add_images_website_1.py` | Add all category images |
| `add_images_website_1_configurable.py` | Advanced all-category config |
| `check_websites.py` | Check website list |
| `homepage_config.json` | Category image settings |
| `category_config.json` | All categories settings |
| `README_homepage_images.md` | Homepage documentation |
| `README_add_images.md` | Image scripts documentation |
| `QUICKSTART.md` | Quick start guide |
| `SCRIPTS_OVERVIEW.md` | All scripts reference |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment help |
| `HOMEPAGE_DEPLOYMENT_CHECKLIST.md` | Deployment checklist |
| `SETUP_INSTRUCTIONS.md` | This file |

---

## Customization

### Change Website Name in Folder
If the folder name isn't perfect, you can manually rename:
```
WEBSITE_1_LONG_ISLAND_CARDS  →  WEBSITE_1_LONGISLAND_CARDS
```

Just remember to update any batch scripts or references.

### Add More Websites
Just run the setup script again for a different website!

---

## Clean Up (Optional)

After confirming new folder works, you can delete the old folder:

```bash
# Delete old WEBSITE_1 folder (keep if unsure!)
rmdir "WEBSITE_1" /s /q
```

---

## Automation Benefit

Instead of manually:
1. ❌ Finding Website ID
2. ❌ Creating new folder
3. ❌ Moving files
4. ❌ Updating scripts with correct ID
5. ❌ Figuring out folder naming

You just run ONE script and it's all done! ✅

---

## Summary

**Before:**
- Folder: `WEBSITE_1` (generic name)
- Scripts: All have `WEBSITE_ID = 1` hardcoded
- Manual work needed

**After:**
- Folder: `WEBSITE_1_LONG_ISLAND_CARDS` (specific, organized)
- Scripts: Website ID auto-updated
- Ready to deploy immediately!

---

## Ready?

Run this ONE command:

```bash
python setup_website_folder.py
```

Everything else happens automatically! 🚀

---

**Last Updated:** 2026-06-07
