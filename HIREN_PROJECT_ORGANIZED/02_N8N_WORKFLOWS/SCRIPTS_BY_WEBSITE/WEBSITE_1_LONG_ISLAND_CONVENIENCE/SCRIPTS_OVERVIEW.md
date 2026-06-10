# Long Island Cards - Image Update Scripts Overview

## Quick Reference

You have **2 main use cases** with multiple script options:

### 🏠 Homepage Update
Update the 5 main homepage categories: Sports, Pokemon, MTG, Yu-Gi-Oh!, Graded

| Script | Type | Use When |
|--------|------|----------|
| `add_images_homepage.py` | Simple | Quick test, no customization needed |
| `add_images_homepage_configurable.py` | Advanced | Need to customize search keywords |

**Config File**: `homepage_config.json`

**Get Started**: `python add_images_homepage.py`

---

### 🎯 All Categories Update
Update all 15 product categories for shop pages

| Script | Type | Use When |
|--------|------|----------|
| `add_images_website_1.py` | Simple | Quick test, no customization needed |
| `add_images_website_1_configurable.py` | Advanced | Need to customize search keywords |

**Config File**: `category_config.json`

**Get Started**: `python add_images_website_1.py`

---

## Which Script Should I Use?

### Scenario 1: Update Homepage Only
```bash
python add_images_homepage.py
```
✓ Quickest way to update the 5 homepage categories  
✓ No setup needed beyond `pip install requests`

### Scenario 2: Update Homepage + Shop Categories
```bash
# First update homepage
python add_images_homepage.py

# Then update all categories
python add_images_website_1.py
```
✓ Complete image update for entire site

### Scenario 3: Customize Image Searches
```bash
# Edit homepage_config.json and/or category_config.json
nano homepage_config.json  # Change search keywords
nano category_config.json

# Run configurable versions
python add_images_homepage_configurable.py
python add_images_website_1_configurable.py
```
✓ Full control over what images are fetched

---

## Available Scripts

### Homepage Scripts

#### `add_images_homepage.py` (Simple)
- Updates: Sports, Pokemon, MTG, Yu-Gi-Oh!, Graded
- Keywords: Hardcoded in Python
- Config needed: None
- Best for: Quick homepage update

#### `add_images_homepage_configurable.py` (Advanced)
- Updates: Same categories (from config)
- Keywords: Read from `homepage_config.json`
- Config needed: Yes (`homepage_config.json`)
- Best for: Ongoing customization

### Category Scripts

#### `add_images_website_1.py` (Simple)
- Updates: 15 all categories (Baseball, Basketball, Football, Hockey, Soccer, Gaming, Racing, Entertainment, Vintage, Singles, Live Box Breaks, Reed Buys, Daily Deals, Best Deals List, Hit Parade)
- Keywords: Hardcoded in Python
- Config needed: None
- Best for: Quick full-site update

#### `add_images_website_1_configurable.py` (Advanced)
- Updates: Same categories (from config)
- Keywords: Read from `category_config.json`
- Config needed: Yes (`category_config.json`)
- Best for: Ongoing customization

---

## Config Files

### `homepage_config.json`
Controls image search for 5 homepage categories.

Example:
```json
{
  "homepage_categories": [
    {
      "name": "Sports",
      "keyword": "baseball basketball football hockey cards",
      "enabled": true
    }
  ]
}
```

Edit the `"keyword"` field to change what Unsplash searches for.

### `category_config.json`
Controls image search for 15 product categories.

Same structure as homepage config.

---

## Step-by-Step: Update Homepage Now

### 1️⃣ Install Dependencies
```bash
pip install requests
```

### 2️⃣ Run Homepage Update
```bash
python add_images_homepage.py
```

### 3️⃣ Verify on Website
- Go to https://longislandcards.com
- Check if category images appear
- Clear cache if needed (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R)

### 4️⃣ (Optional) Customize Keywords
Edit `homepage_config.json` and run:
```bash
python add_images_homepage_configurable.py
```

---

## Documentation Files

| File | Purpose |
|------|---------|
| `SCRIPTS_OVERVIEW.md` | This file - script guide |
| `QUICKSTART.md` | Quick 3-step start guide |
| `README_homepage_images.md` | Homepage script details |
| `README_add_images.md` | Category script details |

---

## Security Notes

✓ **No code execution in Odoo** - Only image data written  
✓ **Image field hardcoded** - `image_128` only, no injection possible  
✓ **Binary data only** - Base64 encoded image content only  
✓ **Credentials secure** - Keep in a safe location  

---

## Recommended Workflow

### First Time
```bash
# 1. Install
pip install requests

# 2. Update homepage
python add_images_homepage.py

# 3. Check website
# → Go to https://longislandcards.com
# → Verify images appear

# 4. Update all categories
python add_images_website_1.py
```

### Ongoing (Weekly/Monthly)
```bash
# Edit config if keywords need changing
nano homepage_config.json
nano category_config.json

# Run configurable versions
python add_images_homepage_configurable.py
python add_images_website_1_configurable.py
```

### Troubleshooting
```bash
# If categories not found:
# 1. Check Odoo category names match config
# 2. Verify Odoo credentials are correct
# 3. Check admin permissions

# If images don't show:
# 1. Clear browser cache (Ctrl+Shift+Delete)
# 2. Hard refresh (Ctrl+Shift+R)
# 3. Wait 1-2 minutes
# 4. Check other site images work
```

---

**Ready?** Start with: `python add_images_homepage.py`

---

**Last Updated**: 2026-06-07
