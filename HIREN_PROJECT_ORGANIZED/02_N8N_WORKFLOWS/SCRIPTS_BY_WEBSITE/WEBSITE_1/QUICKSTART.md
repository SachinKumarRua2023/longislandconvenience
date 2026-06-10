# Quick Start - Long Island Cards Image Updater

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install requests
```

### Step 2: Choose Your Version

**Option A: Simple Version (Recommended for first run)**
```bash
python add_images_website_1.py
```
- Fixed categories hardcoded in Python
- Just run it - everything works automatically
- Best for: Quick testing

**Option B: Configurable Version (Recommended for ongoing use)**
```bash
python add_images_website_1_configurable.py
```
- Edit `category_config.json` to customize categories
- No Python editing needed
- Best for: Regular use and customization

### Step 3: Verify
1. Go to https://longislandcards.com
2. Check category pages - images should appear
3. Clear browser cache if needed (Ctrl+Shift+Delete)

---

## 📊 What Gets Updated

The script will update images for these 15 categories:

| Sports | Gaming & Entertainment | Special |
|--------|------------------------|---------|
| Baseball | Gaming | Live Box Breaks |
| Basketball | Racing | Reed Buys |
| Football | Entertainment | Daily Deals |
| Hockey | Vintage | Best Deals List |
| Soccer | Singles | Hit Parade |

---

## 🎯 Expected Output

```
================================================================================
WEBSITE 1 - Long Island Cards: Add Category Images
================================================================================

[1/2] Connecting to Odoo...
[OK] Connected

[2/2] Adding Category Images from Unsplash...
  → Baseball... ✓ (photo-abc123xyz...)
  → Basketball... ✓ (photo-def456uvw...)
  → Football... ✓ (photo-ghi789rst...)
  → Hockey... ✓ (photo-jkl012mno...)
  → Soccer... ✓ (photo-pqr345stu...)
  → Gaming... ✓ (photo-vwx678yza...)
  → Racing... ✓ (photo-bcd901efg...)
  → Entertainment... ✓ (photo-hij234klm...)
  → Vintage... ✓ (photo-nop567qrs...)
  → Singles... ✓ (photo-tuv890wxy...)
  → Live Box Breaks... ✓ (photo-zab123cde...)
  → Reed Buys... ✓ (photo-fgh456ijk...)
  → Daily Deals... ✓ (photo-lmn789opq...)
  → Best Deals List... ✓ (photo-rst012uvw...)
  → Hit Parade... ✓ (photo-xyz345abc...)

================================================================================
SUMMARY
================================================================================
Category Images:   15/15 added

NEXT STEPS:
  1. Check website: https://longislandcards.com
  2. Verify images appear on category pages
  3. Test on mobile view
```

---

## 🔧 Customizing (Option B Only)

If using the **configurable version**, edit `category_config.json`:

### Change Search Keywords
```json
{
  "name": "Baseball",
  "search_keyword": "vintage baseball cards collection",  // ← Change this
  "enabled": true
}
```

### Disable a Category
```json
{
  "name": "Baseball",
  "search_keyword": "baseball card collection",
  "enabled": false  // ← Set to false to skip
}
```

### Add a New Category
```json
{
  "categories": [
    // ... existing categories ...
    {
      "name": "Pokemon",
      "search_keyword": "pokemon card collection",
      "enabled": true,
      "notes": "Pokémon trading cards"
    }
  ]
}
```

---

## ❓ Troubleshooting

### Images not showing?
```bash
# 1. Clear browser cache (Ctrl+Shift+Delete)
# 2. Hard refresh (Ctrl+Shift+R)
# 3. Wait 1-2 minutes for cache to update
```

### "No image found on Unsplash"
- Try more specific keywords: "vintage pokemon card" instead of "pokemon"
- Check Unsplash.com directly with your keyword
- Ask in the Long Island Cards Slack for suggestions

### "Category not found in Odoo"
- Go to Odoo → Products → Categories
- Verify exact spelling matches in the config file
- Category names are case-sensitive

### Script runs but images don't update
- Verify Odoo credentials in the script are correct
- Check that user has admin permissions
- Look for error messages in the script output

---

## 📝 Files Included

| File | Purpose |
|------|---------|
| `add_images_website_1.py` | Simple version (hardcoded categories) |
| `add_images_website_1_configurable.py` | Advanced version (reads from config) |
| `category_config.json` | Configuration file (categories & keywords) |
| `README_add_images.md` | Detailed documentation |
| `QUICKSTART.md` | This file |

---

## 🎨 Image Sources

All images come from **Unsplash** - 100% free and copyright-free for commercial use.

✓ Free for any use (commercial, personal, etc)  
✓ No attribution required  
✓ No copyright restrictions  
✓ High quality images  

---

## 🔄 Scheduling (Optional)

To run automatically, add to n8n:

1. Create workflow trigger → Schedule (e.g., weekly)
2. Add Execute Command node:
   ```bash
   cd /path/to/scripts && python add_images_website_1.py
   ```
3. Deploy

---

## 📞 Need Help?

- **Check**: README_add_images.md for detailed documentation
- **Edit**: category_config.json to customize (Option B only)
- **Run**: `python add_images_website_1.py` to see detailed output

---

**Next**: Run the script and check https://longislandcards.com! 🎉
