# 🐍 Scripts by Website - Complete Guide
**Bulk Operations & Website-Specific Scripts for All 14 Odoo Websites**

---

## 📂 Folder Structure

```
SCRIPTS_BY_WEBSITE/
│
├── README_SCRIPTS.md (this file)
├── bulk_operations.py (runs on ALL 14 websites)
│
├── WEBSITE_1/
│   ├── add_products_website_1.py
│   ├── add_images_website_1.py
│   ├── update_homepage_website_1.py
│   └── check_status_website_1.py
│
├── WEBSITE_18/
│   ├── add_products_website_18.py
│   ├── add_images_website_18.py
│   └── update_homepage_website_18.py
│
├── WEBSITE_27/
├── WEBSITE_29/
├── WEBSITE_33/
├── WEBSITE_36/ ... WEBSITE_46/
│   (Same structure for each website)
│
└── [More website folders]
```

---

## 🎯 When to Use Each Script

### Use `bulk_operations.py` When You Want To:
✅ **Update logo on all 14 websites** at once  
✅ **Get status** of all websites  
✅ **Update product prices** (affects all websites sharing product DB)  
✅ **Assign products** to multiple websites  
✅ **Bulk operations** on all 14 websites

**Time**: 5 minutes per operation  
**Impact**: All 14 websites updated

---

### Use `WEBSITE_X/` Scripts When You Want To:
✅ **Add products** to ONE specific website only  
✅ **Upload images** for ONE website  
✅ **Update homepage** for ONE website  
✅ **Website-specific configuration**  
✅ **Test on one website** before bulk operations

**Time**: 10-20 minutes per website  
**Impact**: Only that website affected

---

## 🚀 Quick Start

### Quick Start 1: Update Logo On All 14 Websites

```bash
# 1. Edit the file
notepad bulk_operations.py

# 2. Change this line:
logo_path = "C:\\path\\to\\your\\logo.png"  # ← Update path

# 3. Run the script
python bulk_operations.py

# 4. Check results in console output
```

**Result**: Logo appears on all 14 websites in 5 minutes

---

### Quick Start 2: Add Products to Website 1 Only

```bash
# 1. Go to Website 1 folder
cd WEBSITE_1

# 2. Edit the script
notepad add_products_website_1.py

# 3. Modify product details:
products = [
    {
        'name': 'Your Product Name',
        'price': 49.99,
        'image_path': 'C:\\path\\to\\image.jpg'
    }
]

# 4. Run the script
python add_products_website_1.py

# 5. Check website: https://longislandconvenience.com
```

**Result**: Products appear only on Website 1

---

### Quick Start 3: Add Images to Website 18 (Balloons)

```bash
# 1. Go to Website 18 folder
cd WEBSITE_18

# 2. Edit the script
notepad add_images_website_18.py

# 3. Update image paths:
logo_path = "C:\\path\\to\\logo.png"
product_images = [
    {
        'product_id': 100,
        'image_path': 'C:\\path\\to\\balloon_image.jpg'
    }
]

# 4. Run the script
python add_images_website_18.py

# 5. Check website: https://longislandballoonsdecor.com
```

**Result**: Logo and images on Website 18 only

---

## 📋 Bulk Operations Script Details

### What `bulk_operations.py` Does

```python
# OPERATION 1: Add logo to all 14 websites
logo_path = "C:\\path\\to\\logo.png"
# → Updates: Website [1, 18, 27, 29, 33, 36-46]

# OPERATION 2: Update product price
product_id = 100
new_price = 79.99
# → Updates: Product (affects all websites with that product)

# OPERATION 3: Check status
# → Reports: Which websites are active

# OPERATION 4: Get counts
# → Shows: Products, Images, Categories count

# OPERATION 5: Assign product to websites
product_id = 100
assign_to = [1, 18, 27]
# → Assigns: Product to 3 specific websites
```

### Running Bulk Operations

```bash
# Basic run
python bulk_operations.py

# Expected output:
# ✓ Website 1: Logo updated
# ✓ Website 18: Logo updated
# ✓ Website 27: Logo updated
# ... (all 14 websites)
```

---

## 📖 Website-Specific Scripts Details

### Website 1 Scripts

#### `add_products_website_1.py`
```python
# Adds products visible ONLY on Website 1
# Includes: Logo, product images, product data
# Time: 10 minutes
```

```bash
python add_products_website_1.py
```

#### `add_images_website_1.py`
```python
# Adds images to products on Website 1
# Includes: Logo, product images, category images
# Time: 5 minutes
```

```bash
python add_images_website_1.py
```

#### `update_homepage_website_1.py`
```python
# Updates homepage for Website 1 only
# Includes: Hero banner, featured products, categories
# Time: 5 minutes
```

```bash
python update_homepage_website_1.py
```

#### `check_status_website_1.py`
```python
# Shows status of Website 1
# Includes: Product count, image count, logo status
# Time: 1 minute
```

```bash
python check_status_website_1.py
```

---

## 🔧 How to Edit Scripts

### Step 1: Open Script File

```bash
# Using Notepad
notepad WEBSITE_1/add_products_website_1.py

# Or in VS Code
code WEBSITE_1/add_products_website_1.py
```

### Step 2: Find & Edit Configuration

```python
# Look for this section:
products = [
    {
        'name': 'Premium Gift Basket Deluxe',      # ← Change product name
        'category_id': 74,                         # ← Change category
        'price': 89.99,                            # ← Change price
        'cost': 45.00,                             # ← Change cost
        'description': 'Luxury gift basket...',    # ← Change description
        'image_path': 'C:\\path\\to\\product1.jpg' # ← Change image path
    }
]
```

### Step 3: Save & Run

```bash
# Save file (Ctrl+S)
# Run script
python add_products_website_1.py
```

---

## 💡 Common Tasks

### Task 1: Add Same Logo to All Websites

```bash
# Edit bulk_operations.py
logo_path = "C:\\images\\company_logo.png"

# Run
python bulk_operations.py

# Time: 5 minutes
# Impact: All 14 websites get same logo
```

---

### Task 2: Add Different Products to Each Website

```bash
# Website 1: All products
python WEBSITE_1/add_products_website_1.py

# Website 18: Balloons only
python WEBSITE_18/add_products_website_18.py

# Website 27: Gift baskets only
python WEBSITE_27/add_products_website_27.py

# Time: 30 minutes (10 min per website)
# Impact: Each website has specific products
```

---

### Task 3: Update Images for Website 18 Only

```bash
# Go to Website 18
cd WEBSITE_18

# Edit image paths
notepad add_images_website_18.py

# Update all image paths to balloon images

# Run
python add_images_website_18.py

# Time: 10 minutes
# Impact: Only Website 18 (Balloons) gets new images
```

---

### Task 4: Add Category Images to All Websites

```bash
# Option A: Bulk (all websites at once)
python bulk_operations.py
# Edit to add category images for all

# Option B: Per website (customize per site)
python WEBSITE_1/add_images_website_1.py
python WEBSITE_18/add_images_website_18.py
python WEBSITE_27/add_images_website_27.py
# ... etc for each website

# Time: Option A: 5 min, Option B: 50 min (10 each)
```

---

## 📝 Script Templates Provided

### Template 1: bulk_operations.py
- ✅ Logo update for all websites
- ✅ Product price update
- ✅ Status check
- ✅ Product count
- ✅ Assign to websites

### Template 2: WEBSITE_X/add_products_website_X.py
- ✅ Add 3 sample products
- ✅ Assign to website
- ✅ Add product images
- ✅ Set prices
- ✅ Assign to categories

### Template 3: WEBSITE_X/add_images_website_X.py
- ✅ Add logo
- ✅ Add product images
- ✅ Add category images
- ✅ Update branding

---

## 🔑 Important Variables to Edit

### In `bulk_operations.py`

```python
logo_path = "C:\\path\\to\\logo.png"              # Logo file path
product_id = 100                                   # Product to update
new_price = 79.99                                  # New price
assign_to = [1, 18, 27]                           # Website IDs
```

### In `WEBSITE_X/add_products_website_X.py`

```python
WEBSITE_ID = 1                                     # Website ID (1, 18, 27, etc.)

products = [
    {
        'name': 'Product Name',                    # Product name
        'category_id': 74,                         # Category ID
        'price': 89.99,                            # Sale price
        'cost': 45.00,                             # Cost price
        'image_path': 'C:\\path\\to\\image.jpg'   # Image file
    }
]
```

### In `WEBSITE_X/add_images_website_X.py`

```python
WEBSITE_ID = 1                                     # Website ID
logo_path = "C:\\path\\to\\logo.png"              # Logo file

product_images = [
    {
        'product_id': 100,                         # Product ID
        'image_path': 'C:\\path\\to\\image.jpg'   # Image file
    }
]

category_images = [
    {
        'category_id': 74,                         # Category ID
        'image_path': 'C:\\path\\to\\icon.png'    # Image file
    }
]
```

---

## ✅ Checklist: Before Running Scripts

- ☐ Image files exist at specified paths
- ☐ Product IDs are correct
- ☐ Website IDs are correct
- ☐ Category IDs are correct
- ☐ All file paths have correct slashes (C:\\path\\to\\file)
- ☐ Odoo credentials are correct
- ☐ Internet connection is stable

---

## 🚨 Troubleshooting

### Error: "File not found"
```
Solution:
1. Check image path is correct
2. Verify file exists at that location
3. Use full absolute path: C:\\Users\\...\\image.jpg
```

### Error: "Product/Website/Category not found"
```
Solution:
1. Verify ID is correct
2. Check if record exists in Odoo
3. Run check_status script first
```

### Error: "Authentication failed"
```
Solution:
1. Verify Odoo credentials
2. Check internet connection
3. Verify Odoo server is running
```

### Images not showing after upload
```
Solution:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+Shift+R)
3. Check image format is JPG or PNG
4. Verify image size is correct
```

---

## 📚 Related Files

- `HOMEPAGE_IMAGE_FIX_GUIDE.md` - Image troubleshooting
- `PRODUCT_UPDATE_GUIDE_BY_WEBSITE.md` - Product update guide
- `ALL_WEBSITES_IMAGE_STATUS.md` - Website status
- `DOCUMENTATION_MAP.md` - Quick reference

---

## 🎯 Usage Examples

### Example 1: Add Logo to All 14 Websites
```bash
cd SCRIPTS_BY_WEBSITE
# Edit: logo_path = "C:\\company_logo.png"
python bulk_operations.py
```

### Example 2: Add Balloon Products to Website 18
```bash
cd SCRIPTS_BY_WEBSITE/WEBSITE_18
# Edit product names, images, etc.
python add_products_website_18.py
```

### Example 3: Update Images on Website 1
```bash
cd SCRIPTS_BY_WEBSITE/WEBSITE_1
# Edit all image paths
python add_images_website_1.py
```

---

## 🔄 Workflow

```
1. Edit script with your data
   ↓
2. Run script
   ↓
3. Check console for ✓ or ✗
   ↓
4. Visit website to verify
   ↓
5. If OK → Move to next website
   If ERROR → Fix and re-run
```

---

## 📞 Quick Reference

| Need | Script | Time |
|------|--------|------|
| Logo on all sites | bulk_operations.py | 5 min |
| Products on Website 1 | WEBSITE_1/add_products.py | 10 min |
| Images on Website 18 | WEBSITE_18/add_images.py | 10 min |
| Status check | WEBSITE_X/check_status.py | 2 min |
| Homepage update | WEBSITE_X/update_homepage.py | 5 min |

---

**Status**: Ready to Use  
**Last Updated**: June 7, 2026  
**Next Step**: Edit and run your first script!
