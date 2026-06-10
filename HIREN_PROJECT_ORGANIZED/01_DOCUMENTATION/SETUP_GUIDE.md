# Country Cove Inc. — Complete Site Builder
## Setup & Usage Guide

---

## 📋 Overview

This is a complete, production-ready workflow for building the Country Cove Inc. e-commerce website on Odoo, including:

- **Image Processing**: Extract from ZIPs, deduplicate by MD5, organize by category
- **Asset Management**: Organized folder structure in `assets/` with category breakdowns  
- **Odoo Integration**: Auto-upload images, create product categories, manage attachments
- **Website Deployment**: Homepage with carousel, shop page with category filters
- **Reporting**: CSV reports of uploads, duplicates, and category mapping

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Odoo 16+** instance running with website module
3. **ZIP files** with banner/sign/display images in your Downloads folder
4. **Credentials** for Odoo (username, password, database name)

### Step 1: Prepare Environment Variables (Optional)

Edit the scripts or set environment variables:

```powershell
$env:ODOO_URL = "https://country-cove-inc.odoo.com"
$env:ODOO_DB = "country-cove-inc"
$env:ODOO_USER = "countrycoveinc@gmail.com"
$env:ODOO_PASS = "M@nhattan1234"
```

Or edit directly in the script files (lines ~20-25).

### Step 2: Run the Master Orchestrator

```powershell
cd C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask
python RUN_SITE_BUILD.py
```

This will guide you through:
1. ✅ Extracting images from ZIPs  
2. ✅ Deduplicating & organizing into `assets/`
3. ✅ Uploading to Odoo
4. ✅ Deploying website pages

---

## 📁 Folder Structure

After running, you'll have:

```
HirenTask/
├── assets/
│   ├── Banners/
│   │   ├── Step & Repeat/
│   │   │   ├── banner1.jpg
│   │   │   ├── banner2.png
│   │   │   └── ...
│   │   ├── Breakaway/
│   │   ├── Holiday/
│   │   └── ...
│   ├── Stands/
│   │   ├── Retractable Standard/
│   │   ├── Tabletop Retractable/
│   │   └── ...
│   ├── Signs/
│   ├── Decals/
│   ├── Table Covers/
│   ├── Flags/
│   ├── Marketing/
│   ├── upload_report_YYYYMMDD_HHMMSS.csv
│   ├── duplicates_report_YYYYMMDD_HHMMSS.csv
│   └── category_map_YYYYMMDD_HHMMSS.json
│
├── country_cove_site_builder.py    (Extract, dedupe, organize)
├── country_cove_odoo_builder.py    (Deploy website)
├── RUN_SITE_BUILD.py               (Master orchestrator)
└── SETUP_GUIDE.md                  (This file)
```

---

## 🔧 Individual Scripts

### 1. **country_cove_site_builder.py** — Image Processing

**What it does:**
- Finds all banner/sign/display ZIPs in Downloads
- Extracts every image (JPG, PNG, GIF, WebP, BMP, TIFF)
- Removes exact duplicates using MD5 hash
- Auto-categorizes by filename keywords
- Organizes into `assets/by_category/` folder
- Uploads to Odoo ir.attachment records
- Generates CSV reports

**Usage:**

```bash
# Full workflow (extract + organize + upload)
python country_cove_site_builder.py

# Extract & organize only (skip upload)
python country_cove_site_builder.py --no-upload

# Delete ZIPs after successful extraction
python country_cove_site_builder.py --cleanup

# Dry run (shows what would happen, no upload)
python country_cove_site_builder.py --dry-run
```

**Output:**
- `assets/by_category/` — Organized images
- `assets/upload_report_*.csv` — What was uploaded
- `assets/duplicates_report_*.csv` — Removed duplicates
- `assets/category_map_*.json` — Category breakdown

---

### 2. **country_cove_odoo_builder.py** — Website Deployment

**What it does:**
- Connects to Odoo
- Creates QWeb templates for:
  - Homepage with auto-rotating carousel
  - Shop page with category dropdown filters
- Deploys website pages (`/`, `/shop`)
- Links to uploaded images

**Usage:**

```bash
# Deploy website pages
python country_cove_odoo_builder.py
```

**Pages Created:**
- `/` — Homepage with 4-slide carousel + category cards
- `/shop` — Browse all products with dropdown filters

---

### 3. **RUN_SITE_BUILD.py** — Master Orchestrator

**What it does:**
- Guides you through complete workflow step-by-step
- Runs each script in proper order
- Asks for confirmation between steps

**Usage:**

```bash
python RUN_SITE_BUILD.py
```

---

## 📊 Category Rules

Images are auto-categorized by filename. Examples:

| Filename | Category |
|----------|----------|
| `step_repeat_banner.jpg` | Banners / Step & Repeat |
| `breakaway_2x3.png` | Banners / Breakaway |
| `retractable_standard.jpg` | Stands / Retractable Standard |
| `tabletop_booth.png` | Stands / Tabletop Retractable |
| `feather_flag_blue.jpg` | Flags / Feather |
| `yard_sign_pack.png` | Signs / Yard Signs |
| `window_decal.jpg` | Decals / Window |
| `fitted_table_cover.png` | Table Covers / Fitted |

To add more rules, edit `CATEGORY_RULES` in **country_cove_site_builder.py** (line ~60).

---

## 🎨 Website Features

### Homepage
- **Carousel** with 4 rotating slides (auto-cycles every 4 seconds)
- **Category Showcase Cards** with quick links
- **CTA Section** for quote requests
- **Responsive Design** (works on mobile/tablet/desktop)

### Shop Page
- **Category Dropdown Filter** (Banners, Stands, Signs, Flags, Table Covers)
- **Sort Dropdown** (Popular, Price Low-to-High, etc.)
- **Product Grid** (responsive, 3 columns on desktop)
- **Product Cards** with:
  - Product image
  - Title & rating
  - Price
  - "Customize Now" button
- **Pagination** (1, 2, 3...)

---

## 🔐 Odoo Connection Details

The scripts use XML-RPC to connect to Odoo:

```python
ODOO_URL = "https://country-cove-inc.odoo.com"
ODOO_DB = "country-cove-inc"
ODOO_USER = "countrycoveinc@gmail.com"
ODOO_PASS = "M@nhattan1234"
```

**Make sure:**
- Odoo instance is accessible from your computer
- User has permissions to:
  - Create/edit `product.category`
  - Create/upload `ir.attachment`
  - Create/edit `ir.ui.view`
  - Create/edit `website.page`

---

## 📈 Troubleshooting

### Issue: "No ZIP files found"
- **Solution**: Move banner/sign/display ZIPs to your Downloads folder
- Download folder location: `C:\Users\YOUR_USER\Downloads`

### Issue: "Odoo authentication failed"
- **Solution**: Check credentials in the script
  - Verify username/password are correct
  - Ensure database name matches Odoo instance
  - Make sure XML-RPC is enabled in Odoo settings

### Issue: "Bad ZIP file"
- **Solution**: The ZIP may be corrupted
  - Try opening it manually in Windows
  - Re-download if possible
  - Script will skip corrupted ZIPs and continue

### Issue: "Image upload failed"
- **Solution**: Check Odoo logs
  - Make sure product.category exists
  - Verify user has attachment creation permissions
  - Check disk space on Odoo server

### Issue: "Categories not showing on website"
- **Solution**: Images need to be uploaded first
  1. Run `country_cove_site_builder.py` with `--upload` flag
  2. Wait for upload to complete
  3. Then run `country_cove_odoo_builder.py`

---

## 🎯 Next Steps

After initial setup:

1. **Customize Product Pages**
   - In Odoo, go to each product category
   - Add detailed descriptions
   - Set pricing
   - Add product variants

2. **Add More Images**
   - Place new ZIPs in Downloads
   - Re-run `country_cove_site_builder.py`
   - Images will be added to existing categories

3. **Customize Homepage**
   - Edit carousel images in `country_cove_odoo_builder.py`
   - Update category cards
   - Change prices/descriptions

4. **Setup Contact Form**
   - In Odoo website, add contact page
   - Setup email notifications
   - Link "Get Quote" buttons to contact form

5. **Go Live**
   - Update domain DNS to point to Odoo
   - Enable SSL/HTTPS
   - Test all pages on mobile
   - Setup Google Analytics

---

## 📝 CSV Reports

### upload_report_*.csv
Shows what was uploaded to Odoo:

```
filename,category,status,hash
banner1.jpg,Banners / Step & Repeat,UPLOADED,a1b2c3d4
banner2.png,Banners / Breakaway,EXISTS,e5f6g7h8
banner3.jpg,Uncategorized,SKIP,i9j0k1l2
```

**Status values:**
- `UPLOADED` — Successfully uploaded to Odoo
- `EXISTS` — Already on Odoo (skipped)
- `SKIP` — File not found or error
- `ERROR` — Upload failed (see error message)

### duplicates_report_*.csv
Shows what was removed as duplicates:

```
filename,src_zip,duplicate_of
banner_copy.jpg,banners.zip,banner.jpg
image_2.png,signs.zip,image.png
```

### category_map_*.json
Shows all images organized by category:

```json
{
  "Banners / Step & Repeat": [
    "banner1.jpg",
    "banner2.jpg"
  ],
  "Banners / Breakaway": [
    "breakaway1.png"
  ],
  "Uncategorized": [
    "random_image.jpg"
  ]
}
```

---

## 🔄 Workflow Diagram

```
Downloads Folder (ZIPs)
        ↓
   Extract Images
        ↓
  Remove Duplicates (MD5)
        ↓
Auto-Categorize by Filename
        ↓
assets/ Folder (organized by category)
        ↓
      Upload to Odoo
        ↓
Deploy Website Pages
        ↓
LIVE SITE!
```

---

## 💡 Pro Tips

1. **Naming Convention**
   - Use clear, descriptive filenames
   - Include category keywords (e.g., `step_repeat_banner_4x8.jpg`)
   - Use underscores instead of spaces
   - This ensures correct auto-categorization

2. **Bulk Uploads**
   - Process ZIPs in batches (5-10 at a time)
   - Monitor RAM usage for large ZIPs (100MB+)
   - Can re-run script multiple times safely (duplicates detected)

3. **Image Quality**
   - Use high-resolution images (1200x900px minimum)
   - JPG for photos, PNG for graphics
   - Keep file size under 5MB for web

4. **Backup**
   - Keep original ZIPs in Downloads
   - Keep `assets/` folder as backup
   - Save CSV reports in version control

---

## 📞 Support

For issues:
1. Check the **Troubleshooting** section above
2. Review script output messages (they're verbose)
3. Check CSV reports for details
4. Verify Odoo logs in `/admin/logs`

---

## 📜 License

Internal use only. Country Cove Inc.

---

**Last Updated**: 2026-06-04  
**Version**: 2.0
