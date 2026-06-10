# Long Island Cards - Homepage Image Updater

## Overview
This script updates the **5 homepage category sections** with real card images from Unsplash:
- Sports
- Pokemon
- MTG
- Yu-Gi-Oh!
- Graded

All images are **free, copyright-free**, and automatically downloaded from Unsplash.

## Quick Start

### Option 1: Simple (Hardcoded)
```bash
python add_images_homepage.py
```

### Option 2: Configurable (Recommended)
```bash
python add_images_homepage_configurable.py
```
Then edit `homepage_config.json` to customize keywords without touching Python code.

## Installation

```bash
pip install requests
```

## Expected Output

```
================================================================================
LONG ISLAND CARDS - Update Homepage Categories
================================================================================

[1/2] Connecting to Odoo...
[OK] Connected

[2/2] Updating Homepage Categories...

  → Sports... ✓ (photo-abc123xyz...)
  → Pokemon... ✓ (photo-def456uvw...)
  → MTG... ✓ (photo-ghi789rst...)
  → Yu-Gi-Oh!... ✓ (photo-jkl012mno...)
  → Graded... ✓ (photo-pqr345stu...)

================================================================================
SUMMARY
================================================================================
Homepage Categories Updated: 5/5

✓ All homepage categories updated successfully!

NEXT STEPS:
  1. Go to https://longislandcards.com
  2. Clear browser cache (Ctrl+Shift+Delete)
  3. Hard refresh (Ctrl+Shift+R)
  4. Check if homepage category images appear
```

## Customizing Keywords (Option 2 Only)

Edit `homepage_config.json` to change what images are searched:

```json
{
  "name": "Sports",
  "keyword": "baseball basketball football hockey cards",  // ← Change this
  "enabled": true
}
```

**Tips for better results:**
- Include multiple related terms: "sports card collection" works better than just "sports"
- Be specific: "magic the gathering card" finds better MTG images
- Test on Unsplash.com manually first to see available images

## Troubleshooting

### "Not found in Odoo"
The category name doesn't match in Odoo. Check:
1. Go to Odoo → Products → Categories
2. Find the exact category name spelling
3. Update the `"name"` field in `homepage_config.json` to match exactly

### Images not showing on website
1. Clear browser cache: Ctrl+Shift+Delete
2. Hard refresh: Ctrl+Shift+R
3. Wait 1-2 minutes for cache to propagate
4. Check if other images on site work (rules out Odoo issue)

### Connection errors
- Verify Odoo credentials in the script are correct
- Check that user has admin permissions
- Verify Odoo server is running and accessible

## Files

| File | Purpose |
|------|---------|
| `add_images_homepage.py` | Simple version (hardcoded) |
| `add_images_homepage_configurable.py` | Advanced version (config-based) |
| `homepage_config.json` | Configuration for keywords |
| `README_homepage_images.md` | This file |

## Security

✓ Only image data written to Odoo (no code execution)  
✓ Image field hardcoded - no injection possible  
✓ Binary image data only - completely safe  

## Image Source

All images from **Unsplash** - 100% free and copyright-free for commercial use.

---

**Last Updated**: 2026-06-07
