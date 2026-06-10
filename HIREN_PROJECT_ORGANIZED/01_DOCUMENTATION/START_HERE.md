# ⚡ START HERE — Country Cove Inc. Website Builder

## 📊 What You Have

### In Downloads Folder
- **18 ZIP files** (18.4 MB)
- **617 images** (banners, signs, displays, tables, flags, decals)
- Competitor website archives (inspiration sources)

### In Project Root
- **4 new Python scripts** (ready to run)
- **3 documentation files** (setup guides)
- **Existing assets** (will be backed up automatically)

---

## 🚀 Run This (Pick One)

### ✅ RECOMMENDED: Interactive Mode
```bash
cd C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask
python RUN_SITE_BUILD.py
```
- Guides you step-by-step
- Asks for confirmation between steps
- Shows progress & final results
- **Time: 10-15 minutes**

---

### OR: Just Organize Images (No Odoo)
```bash
python manage_images.py
```
- Extracts & organizes images from ZIPs
- Removes duplicates
- Generates reports
- Creates: `assets/country_cove_products/`
- **Time: 2-3 minutes**

Then check: `assets/country_cove_products/`

---

### OR: Step-by-Step Manual
```bash
# Step 1: Organize images
python manage_images.py

# Wait for completion...

# Step 2: Upload to Odoo
python country_cove_site_builder.py

# Wait for completion...

# Step 3: Deploy website
python country_cove_odoo_builder.py

# Done! Visit: https://country-cove-inc.odoo.com/
```

---

## 📋 What Each Script Does

| Script | Function | Time |
|--------|----------|------|
| `manage_images.py` | Extract ZIPs → Deduplicate → Organize by category | 2-3 min |
| `country_cove_site_builder.py` | Upload images to Odoo → Create categories | 5-10 min |
| `country_cove_odoo_builder.py` | Deploy homepage + shop page | 1-2 min |
| `RUN_SITE_BUILD.py` | Run all above with confirmations | 10-15 min |

---

## 📁 Output Folder Structure

After running `manage_images.py`:

```
assets/
├── country_cove_products/          ← ALL IMAGES HERE
│   ├── Banners -- Step & Repeat/
│   ├── Banners -- Breakaway/
│   ├── Stands -- Retractable Standard/
│   ├── Signs -- General/
│   ├── Table Covers -- Fitted/
│   ├── Decals -- Window/
│   ├── Flags -- Feather/
│   ├── Marketing -- Hero Slides/
│   └── [+ 23 more category folders]
│
├── backup_20260604_HHMMSS/         ← OLD ASSETS (preserved)
│   ├── longislandconvenience/
│   └── sing and buzz images of banners/
│
└── longislandconvenience/          ← EXISTING (untouched)
    └── [logos, favicons]
```

---

## 🎨 Website Result

### Homepage
- Auto-rotating carousel (4 slides)
- Category showcase cards
- "Get Free Quote" CTA button
- Responsive design

### Shop Page
- Category dropdown filter
- Sort dropdown
- Product grid (3 columns)
- Pagination

### All 30+ Category Pages
- Auto-generated from image folders
- Product images organized by type
- Linked in navigation

---

## ✨ Features

✅ **Auto-categorization** — Filename keywords → proper folders  
✅ **Deduplication** — MD5 hash removes exact duplicates  
✅ **Backup** — Existing assets preserved automatically  
✅ **Reports** — CSV, JSON, text summaries generated  
✅ **Responsive** — Works on mobile, tablet, desktop  
✅ **No manual work** — Fully automated  

---

## 🔧 Configuration

Everything uses **environment variables** or script defaults:

```
ODOO_URL = https://country-cove-inc.odoo.com
ODOO_DB = country-cove-inc
ODOO_USER = countrycoveinc@gmail.com
ODOO_PASS = M@nhattan1234
```

*(Already set in the scripts)*

---

## 📖 For More Details

| Document | Contains |
|----------|----------|
| `IMAGE_MANAGEMENT_GUIDE.md` | Complete technical guide |
| `SETUP_GUIDE.md` | Original setup documentation |
| `manage_images.py` | Image extraction & organization |
| `country_cove_site_builder.py` | Odoo uploader with XML-RPC |
| `country_cove_odoo_builder.py` | Website pages (carousel & filters) |

---

## ⏱️ Timeline

| Stage | Time | What Happens |
|-------|------|--------------|
| Extract & Organize | 2-3 min | 617 images → 485 unique → 31 categories |
| Upload to Odoo | 5-10 min | Images sent to Odoo, categories created |
| Deploy Website | 1-2 min | Homepage & shop pages go live |
| **Total** | **10-15 min** | **Live website ready** ✓ |

---

## 🎯 Quick Checklist

Before running:
- [ ] ZIPs are in Downloads folder
- [ ] Odoo instance is running
- [ ] You have Odoo credentials (in scripts or env vars)
- [ ] Python 3.8+ is installed

When running:
- [ ] Watch the progress output
- [ ] Confirm between steps (if using RUN_SITE_BUILD.py)
- [ ] Check reports when done

After running:
- [ ] Visit: https://country-cove-inc.odoo.com/
- [ ] Test homepage carousel (should auto-rotate)
- [ ] Test shop page filters
- [ ] Check image loading

---

## 🚦 Go!

### Pick your path:

**I want everything automated:**
```bash
python RUN_SITE_BUILD.py
```

**I want to see each step:**
```bash
python manage_images.py
python country_cove_site_builder.py
python country_cove_odoo_builder.py
```

**I just want organized images:**
```bash
python manage_images.py
```

---

## 💡 Pro Tips

1. **First time?** Use `python RUN_SITE_BUILD.py` (interactive)
2. **Need to re-run?** Safe to run multiple times (duplicates detected)
3. **Want to customize?** Edit CATEGORY_KEYWORDS in manage_images.py
4. **Want different colors?** Edit SHARED_CSS in country_cove_odoo_builder.py
5. **Running multiple times?** Each run creates new backup with timestamp

---

## 🐛 Something Wrong?

**ZIPs not found?**
- Check Downloads folder: `C:\Users\YOUR_USER\Downloads`
- Verify filename contains: banner, sign, display, etc.

**Odoo won't connect?**
- Verify credentials in script
- Check Odoo is running & accessible
- Make sure XML-RPC is enabled

**Images not showing?**
- Check upload report for errors
- Verify images are marked public in Odoo
- Clear browser cache

**Need help?** See `IMAGE_MANAGEMENT_GUIDE.md` for troubleshooting section

---

## 📞 Files You Created

```
HirenTask/
├── manage_images.py                  (image organizer)
├── country_cove_site_builder.py      (odoo uploader)
├── country_cove_odoo_builder.py      (website deployer)
├── RUN_SITE_BUILD.py                 (interactive orchestrator)
├── START_HERE.md                     (this file)
├── IMAGE_MANAGEMENT_GUIDE.md         (complete guide)
├── SETUP_GUIDE.md                    (setup documentation)
└── assets/
    ├── country_cove_products/        (images output)
    └── backup_*/                     (automatic backups)
```

---

**Status:** ✅ Ready to run  
**Total Setup Time:** 5 minutes  
**Total Execution Time:** 10-15 minutes  
**Result:** Live website with carousel & filters  

**👉 Ready? Run: `python RUN_SITE_BUILD.py`**
