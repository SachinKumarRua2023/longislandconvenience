# 📑 Scripts by Website - Complete Index

## 🚀 START HERE

**Before using ANY scripts, read in this order:**

1. ⚠️ **ODOO_CODE_RESTRICTIONS.md** - CRITICAL - Read first!
2. 📖 **README_SCRIPTS.md** - How to use all scripts
3. 🐍 **This file** - Script organization

---

## 📂 Folder Structure

```
SCRIPTS_BY_WEBSITE/
│
├── INDEX.md (This file)
├── README_SCRIPTS.md (Complete guide)
├── ODOO_CODE_RESTRICTIONS.md (⚠️ Must read)
│
├── bulk_operations.py ⭐ (Runs on ALL 14 websites)
│
├── WEBSITE_1/ (Long Island Convenience)
├── WEBSITE_18/ (Balloons)
├── WEBSITE_27/ (Gift Baskets)
├── WEBSITE_29/ (Print & Copy)
├── WEBSITE_33/ (Cards)
├── WEBSITE_36/ (Expansion 1)
├── WEBSITE_37/ (Expansion 2)
├── WEBSITE_38/ (Expansion 3)
├── WEBSITE_39/ (Expansion 4)
├── WEBSITE_40/ (Expansion 5)
├── WEBSITE_41/ (Expansion 6)
├── WEBSITE_42/ (Expansion 7)
├── WEBSITE_45/ (Expansion 8)
└── WEBSITE_46/ (Expansion 9)
```

---

## 🐍 Scripts Overview

### Bulk Operations (ALL 14 websites)

| Script | Purpose | Time | Impact |
|--------|---------|------|--------|
| **bulk_operations.py** | Update logo, prices, status on all websites | 5 min | All 14 websites |

### Website-Specific (Individual websites)

Each WEBSITE_X folder contains:

| Script | Purpose | Time | Impact |
|--------|---------|------|--------|
| **add_products.py** | Add products to one website | 10 min | That website only |
| **add_images.py** | Add logo, product, category images | 10 min | That website only |
| **update_homepage.py** | Update homepage banner and featured | 5 min | That website only |
| **check_status.py** | Check product/image count | 2 min | Read-only |

---

## ✅ Common Tasks

### Task: Update Logo on ALL Websites

```bash
cd SCRIPTS_BY_WEBSITE
python bulk_operations.py
# Edit: logo_path = "C:\\your\\logo.png"
# Time: 5 minutes
```

### Task: Add Products to Website 1

```bash
cd SCRIPTS_BY_WEBSITE/WEBSITE_1
python add_products_website_1.py
# Edit: product names, prices, images
# Time: 10 minutes
```

### Task: Add Images to Website 18 (Balloons)

```bash
cd SCRIPTS_BY_WEBSITE/WEBSITE_18
python add_images_website_18.py
# Edit: image paths
# Time: 10 minutes
```

### Task: Check Status of Website 27

```bash
cd SCRIPTS_BY_WEBSITE/WEBSITE_27
python check_status_website_27.py
# Time: 2 minutes
# Shows: Product count, image count
```

---

## 🌐 All 14 Website IDs

| Folder | ID | Name | Type |
|--------|----|----|------|
| WEBSITE_1 | 1 | Long Island Convenience | Primary |
| WEBSITE_18 | 18 | Country Cove Balloons | Niche |
| WEBSITE_27 | 27 | Country Cove Gift Baskets | Niche |
| WEBSITE_29 | 29 | Long Island Print & Copy | Niche |
| WEBSITE_33 | 33 | Long Island Card Shop | Niche |
| WEBSITE_36 | 36 | Expansion Site 1 | Growth |
| WEBSITE_37 | 37 | Expansion Site 2 | Growth |
| WEBSITE_38 | 38 | Expansion Site 3 | Growth |
| WEBSITE_39 | 39 | Expansion Site 4 | Growth |
| WEBSITE_40 | 40 | Expansion Site 5 | Growth |
| WEBSITE_41 | 41 | Expansion Site 6 | Growth |
| WEBSITE_42 | 42 | Expansion Site 7 | Growth |
| WEBSITE_45 | 45 | Expansion Site 8 | Growth |
| WEBSITE_46 | 46 | Expansion Site 9 | Growth |

---

## 🔄 Workflow

```
1. Read ODOO_CODE_RESTRICTIONS.md
   ↓
2. Read README_SCRIPTS.md
   ↓
3. Gather your images & data
   ↓
4. Choose script (bulk or website-specific)
   ↓
5. Edit script with your data
   ↓
6. Run script on your computer
   ↓
7. Check website to verify
   ↓
8. If OK → Next task
   If ERROR → Fix and re-run
```

---

## 📝 How to Edit Scripts

### Step 1: Open in Text Editor
```bash
notepad WEBSITE_1/add_products_website_1.py
```

### Step 2: Find Configuration Section
```python
products = [
    {
        'name': 'Your Product Name',        # ← Change this
        'category_id': 74,                  # ← Change this
        'price': 89.99,                     # ← Change this
        'image_path': 'C:\\path\\image.jpg' # ← Change this
    }
]
```

### Step 3: Save & Run
```bash
python add_products_website_1.py
```

---

## ⚠️ Important Rules

### DO ✅

- ✅ Run Python scripts on YOUR computer
- ✅ Call Odoo via XML-RPC API
- ✅ Use JavaScript in Odoo (free)
- ✅ Use HTML/CSS in Odoo (free)
- ✅ Create unlimited external scripts
- ✅ Update data unlimited times

### DON'T ❌

- ❌ Put Python code in Odoo UI
- ❌ Create Python modules in Odoo
- ❌ Use paid Odoo features without license
- ❌ Put API keys in Odoo directly

---

## 🎯 Script Selection Guide

```
Do you need to...

Update MANY websites?
  → Use: bulk_operations.py
  → Time: 5 minutes

Add products to ONE website?
  → Use: WEBSITE_X/add_products_website_X.py
  → Time: 10 minutes

Add images to ONE website?
  → Use: WEBSITE_X/add_images_website_X.py
  → Time: 10 minutes

Check status of ONE website?
  → Use: WEBSITE_X/check_status_website_X.py
  → Time: 2 minutes

Update homepage ONE website?
  → Use: WEBSITE_X/update_homepage_website_X.py
  → Time: 5 minutes
```

---

## 🐍 Python Scripts Features

### All Scripts Include

- ✅ Pre-configured Odoo credentials
- ✅ Error handling
- ✅ Progress indicators
- ✅ Status messages
- ✅ Ready-to-edit templates
- ✅ Zero additional cost

### What You Customize

- Website ID (already set in folder name)
- Product names, prices, categories
- Image file paths
- Logo paths
- Category information

---

## 🔐 Security

All scripts:
- ✅ Run locally on YOUR computer
- ✅ Connect via secure HTTPS API
- ✅ No credentials hardcoded (config inside)
- ✅ No data leaves your computer
- ✅ Full audit trail via Odoo

---

## 📚 Documentation Files

| File | Purpose | Read When |
|------|---------|-----------|
| **ODOO_CODE_RESTRICTIONS.md** | Python in Odoo restrictions | FIRST |
| **README_SCRIPTS.md** | Complete usage guide | SECOND |
| **INDEX.md** | This file - Quick reference | ANYTIME |

---

## ✨ What You Get

- 1 bulk operations script (runs on all 14)
- 56 website-specific scripts (4 per website × 14)
- Complete documentation
- Ready-to-use templates
- Zero setup required
- Zero additional cost

---

## 🚀 Quick Start in 3 Steps

### Step 1: Read
```
ODOO_CODE_RESTRICTIONS.md (2 min)
README_SCRIPTS.md (5 min)
```

### Step 2: Prepare
```
Gather your images
Collect product data
Organize files
```

### Step 3: Run
```
Edit script with your data
python script_name.py
Check website for results
```

**Total time: 30 minutes to get started**

---

## 📞 Quick Commands

```bash
# Go to scripts folder
cd C:\...\HIREN_PROJECT_ORGANIZED\02_N8N_WORKFLOWS\SCRIPTS_BY_WEBSITE

# Update all websites
python bulk_operations.py

# Go to specific website
cd WEBSITE_1

# Add products to Website 1
python add_products_website_1.py

# Add images to Website 1
python add_images_website_1.py

# Check Website 1 status
python check_status_website_1.py
```

---

## 🎓 Learning Path

1. **Beginner**: Read README_SCRIPTS.md
2. **Intermediate**: Edit and run bulk_operations.py
3. **Advanced**: Edit website-specific scripts
4. **Expert**: Customize scripts for your needs

---

## ✅ Verification Checklist

- ☐ Read ODOO_CODE_RESTRICTIONS.md
- ☐ Read README_SCRIPTS.md
- ☐ Python installed on your computer
- ☐ Images ready (correct size/format)
- ☐ Product data prepared
- ☐ Can access Odoo website
- ☐ Ready to run first script

---

## 🎯 Next Steps

1. Read: ODOO_CODE_RESTRICTIONS.md
2. Read: README_SCRIPTS.md
3. Choose: Bulk or website-specific script
4. Prepare: Your data and images
5. Edit: Script configuration
6. Run: Python script
7. Verify: Check website
8. Repeat: For other websites/tasks

---

**All scripts ready to use!**  
**Zero setup required!**  
**Zero additional cost!**

---

*Last Updated: June 7, 2026*  
*Status: Complete & Ready*
