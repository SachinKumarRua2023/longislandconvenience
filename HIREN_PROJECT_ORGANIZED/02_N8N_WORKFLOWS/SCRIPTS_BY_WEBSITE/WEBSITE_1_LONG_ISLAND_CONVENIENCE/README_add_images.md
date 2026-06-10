# Long Island Cards - Category Image Updater

## Overview
This script automatically fetches **free, copyright-free** images from Unsplash for each product category in the Long Island Cards Odoo store and updates them in real-time.

## What It Does
✓ Connects to your Odoo instance  
✓ Searches Unsplash for images matching each category  
✓ Downloads images and converts to Odoo format (base64)  
✓ Updates category icons with real product images  
✓ Supports all 15 Long Island Cards categories  

## Supported Categories
The script updates images for these categories:
- **Sports Cards**: Baseball, Basketball, Football, Hockey, Soccer
- **Other Collectibles**: Gaming, Racing, Entertainment, Vintage, Singles
- **Special Sections**: Live Box Breaks, Reed Buys, Daily Deals, Best Deals List, Hit Parade

## Requirements
```bash
pip install requests xmlrpc-client
```

## Installation

1. **Save the script** to your n8n workflows directory:
   ```
   WEBSITE_1/add_images_website_1.py
   ```

2. **Install dependencies**:
   ```bash
   pip install requests
   ```

3. **Verify Odoo credentials** in the script:
   - `URL`: Your Odoo instance URL
   - `DB`: Your Odoo database name
   - `EMAIL`: Admin email
   - `PASSWORD`: Admin password

## Usage

### Run Manually
```bash
python add_images_website_1.py
```

### Expected Output
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
  ...
  
================================================================================
SUMMARY
================================================================================
Category Images:   15/15 added

NEXT STEPS:
  1. Check website: https://longislandcards.com
  2. Verify images appear on category pages
  3. Test on mobile view
```

## How It Works

### Step 1: Image Search
For each category, the script searches Unsplash with a relevant keyword:
- **Baseball** → "baseball card collection"
- **Pokemon** → "pokemon card collection"
- **Magic** → "magic card collection"
- etc.

### Step 2: Image Download
Once found, the script:
1. Gets the image URL from Unsplash
2. Downloads the full-size image
3. Converts it to base64 format (Odoo's native format)

### Step 3: Odoo Update
Finally, it:
1. Searches Odoo for the matching category by name
2. Updates the category's icon (image_128) with the new image

## Customizing Search Keywords

To change what images are fetched for a category, edit the `category_images` list:

```python
category_images = [
    {'category_name': 'Baseball', 'search_keyword': 'your-keyword-here'},
    # ... more categories
]
```

**Tips for better results:**
- Include relevant terms: "card", "collection", "trading"
- Be specific: "vintage baseball card" finds better images than just "baseball"
- Try alternative keywords if the first attempt doesn't work well

## Image Sources
All images are sourced from **Unsplash**, which provides:
- ✓ Completely free for commercial use
- ✓ No copyright restrictions
- ✓ No photographer credit required
- ✓ High-quality images
- ✓ Millions of options

**Attribution:** While not required, it's good practice to link back to Unsplash.

## Troubleshooting

### Issue: "No image found on Unsplash"
**Solution:** The search keyword didn't return results. Try:
- Being more specific: "vintage pokemon card" instead of "pokemon"
- Using different keywords: "trading cards" instead of "cards"
- Checking Unsplash.com manually for that keyword

### Issue: "Category not found in Odoo"
**Solution:** The category name doesn't match in Odoo. Verify:
1. Go to Odoo → Products → Categories
2. Check exact spelling of category names
3. Update the `category_name` in the script to match exactly

### Issue: "Could not download image"
**Solution:** Network or timeout issue. Try:
- Running the script again (usually temporary)
- Checking your internet connection
- Verifying Unsplash is accessible from your location

### Issue: Images don't appear on website
**Solution:** Clear cache and refresh:
1. Browser: Ctrl+Shift+Delete (clear cache) → Ctrl+Shift+R (hard refresh)
2. Odoo: Refresh browser after 5-10 minutes
3. CDN: Images may take 1-5 minutes to cache

## Scheduling (Optional)

To run this automatically, add to an n8n workflow:
1. Create a new workflow in n8n
2. Add a **Schedule** trigger (e.g., weekly)
3. Add an **Execute Command** node:
   ```bash
   python /path/to/add_images_website_1.py
   ```
4. Deploy the workflow

## Notes
- **First run**: May take 1-2 minutes (downloading 15 images)
- **Subsequent runs**: Same images refresh with new ones
- **Rate limits**: Unsplash allows 50 requests/hour for free API use
- **Odoo connection**: Requires admin credentials; keep password secure

## Support
If you need to:
- **Update more categories**: Add entries to the `category_images` list
- **Use different image sources**: Modify `get_unsplash_image()` function
- **Change image size**: Edit the `image_128` field (options: image_128, image_256, image_1024, etc.)

---

**Last Updated**: 2026-06-07  
**Maintained by**: Long Island Cards Team
