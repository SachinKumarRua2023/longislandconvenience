# Odoo Python Scripts Setup Guide

## 📋 Overview

Two Python scripts to manage images and products in Odoo:

1. **`odoo_image_upload.py`** - Upload images to Odoo Media Library
2. **`odoo_website_products.py`** - Create/update product records with images

---

## 🔧 Requirements

### Install Python (if not already installed)

**Windows:**
```bash
# Download from https://www.python.org/downloads/
# Or use PowerShell:
winget install Python.Python.3.11
```

**Check Python is installed:**
```bash
python --version
```

### Install Required Python Package

```bash
pip install requests
```

Or for complete XML-RPC support:
```bash
pip install xmlrpc2
```

---

## 📁 File Structure

```
HirenTask/
├── odoo_image_upload.py          # Upload images script
├── odoo_website_products.py       # Create products script
├── images/                        # Image folder
│   ├── sports-cards-center.png
│   ├── cards_left.png
│   ├── cards_right.png
│   ├── giftbasket_center.jpg
│   ├── giftbasket_left.jpg
│   ├── giftbasket_right.jpg
│   ├── BalloonsCenter.png
│   ├── balloon_left.jfif
│   ├── balloon_right.jfif
│   ├── printmail_center.jpeg
│   ├── printmail_left.jpeg
│   ├── printmail_right.jpeg
│   ├── Gemini_Generated_Image...png
│   ├── GreetingCardLeft.png
│   └── GreetingCardRight.png
```

---

## ⚙️ Script Configuration

Both scripts use these Odoo details (already configured):

```python
ODOO_URL = "https://country-cove-inc.odoo.com"
ODOO_DB = "country-cove-inc"
ODOO_USER = "countrycoveinc@gmail.com"
ODOO_PASSWORD = "M@nhattan1234"
```

**Change if different**, located at top of each script.

---

## 🚀 Running the Scripts

### Method 1: Command Line (Easiest)

**Step 1: Open PowerShell or Command Prompt**

```bash
# Navigate to project folder
cd c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask
```

**Step 2: Run Image Upload Script**

```bash
python odoo_image_upload.py
```

**Output:**
```
============================================================
ODOO IMAGE UPLOAD & PRODUCT SETUP
============================================================

Step 1: Connecting to Odoo...
✓ Connected successfully! User ID: 2

Step 2: Uploading images and creating product categories...

Processing: Sports Cards
  ✓ Uploaded: sports-cards-center.png (ID: 123)
  ✓ Uploaded: cards_left.png (ID: 124)
  ✓ Uploaded: cards_right.png (ID: 125)
  ✓ Created category: Sports Cards (ID: 45)

... (continues for all categories)

============================================================
✓ UPLOAD COMPLETE!
============================================================
```

**Step 3: Run Products Script**

```bash
python odoo_website_products.py
```

**Output:**
```
============================================================
ODOO WEBSITE PRODUCTS SETUP
============================================================

Step 1: Connecting to Odoo...
✓ Connected successfully! User ID: 2

Step 2: Creating/updating products...

  ✓ Created product: Sports Cards (ID: 234)
  ✓ Created product: Gift Baskets (ID: 235)
  ✓ Created product: Balloons & Décor (ID: 236)
  ... (continues)

============================================================
✓ SETUP COMPLETE!
============================================================

Created/Updated 6 products
```

---

### Method 2: Python IDE (PyCharm/VS Code)

**PyCharm:**
1. Open `odoo_image_upload.py`
2. Right-click > **Run**
3. View output in console

**VS Code:**
1. Open terminal
2. Run: `python odoo_image_upload.py`

---

## 📋 What Each Script Does

### Script 1: `odoo_image_upload.py`

**Tasks:**
✅ Connects to Odoo
✅ Uploads all images from `images/` folder
✅ Creates product categories
✅ Attaches images to categories
✅ Enables website display

**Result in Odoo:**
- Images in: **Website > Media**
- Categories in: **eCommerce > Product Categories**
- All categories show 3 images each

---

### Script 2: `odoo_website_products.py`

**Tasks:**
✅ Connects to Odoo
✅ Creates 6 product records
✅ Assigns categories to products
✅ Sets pricing and descriptions
✅ Publishes to website

**Result in Odoo:**
- Products in: **eCommerce > Products**
- Visible on website: **Yes**
- Website Category: Automatically assigned

---

## ✅ Verify in Odoo

### Step 1: Check Images Uploaded

1. Login to Odoo: https://country-cove-inc.odoo.com
2. Go to: **Website > Media**
3. You should see all 15 images:
   - ✓ sports-cards-center.png
   - ✓ cards_left.png
   - ✓ cards_right.png
   - ✓ giftbasket_center.jpg
   - ✓ giftbasket_left.jpg
   - ✓ giftbasket_right.jpg
   - ✓ BalloonsCenter.png
   - ✓ balloon_left.jfif
   - ✓ balloon_right.jfif
   - ✓ printmail_center.jpeg
   - ✓ printmail_left.jpeg
   - ✓ printmail_right.jpeg
   - ✓ GreetingCardLeft.png
   - ✓ GreetingCardRight.png
   - ✓ Gemini_Generated_Image...png

### Step 2: Check Categories

1. Go to: **eCommerce > Categories**
2. You should see 6 categories:
   - ✓ Sports Cards (with 3 images)
   - ✓ Gift Baskets (with 3 images)
   - ✓ Balloons & Décor (with 3 images)
   - ✓ Print & Mail (with 3 images)
   - ✓ Game Cards (with 3 images)
   - ✓ Greeting Cards (with 3 images)

### Step 3: Check Products

1. Go to: **eCommerce > Products**
2. You should see 6 products:
   - ✓ Sports Cards
   - ✓ Gift Baskets
   - ✓ Balloons & Décor
   - ✓ Print & Mail Services
   - ✓ Game Cards
   - ✓ Greeting Cards

---

## 🔄 Run Scripts Again?

You can run the scripts multiple times safely:

✅ Images: Won't duplicate (Odoo checks for existing)
✅ Categories: Will update if they exist
✅ Products: Will update if they exist

**Safe to re-run anytime!**

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'xmlrpc.client'"

**Solution:**
```bash
pip install xmlrpc2
# Or just use built-in (should work)
python odoo_image_upload.py
```

### Error: "Connection failed"

**Check:**
1. Odoo URL is correct: `https://country-cove-inc.odoo.com`
2. Credentials are correct:
   - Email: `countrycoveinc@gmail.com`
   - Password: `M@nhattan1234`
3. Internet connection is working
4. Odoo instance is online

**Test connection:**
```bash
# Open PowerShell and test:
Invoke-WebRequest https://country-cove-inc.odoo.com
```

### Error: "Image file not found"

**Check:**
1. Images folder path is correct:
   ```
   c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\images
   ```
2. All image files exist in folder
3. File names match exactly (case-sensitive)

**List images:**
```bash
dir images/
```

### Error: "Permission denied"

**Solution:**
1. Run PowerShell as Administrator
2. Or check Odoo user permissions (countrycoveinc@gmail.com should be admin)

---

## 📊 What Gets Created

| Type | Count | Location |
|------|-------|----------|
| Images | 15 | Website > Media |
| Categories | 6 | eCommerce > Categories |
| Products | 6 | eCommerce > Products |

---

## 🔐 Security Notes

✅ **Credentials in script**: Safe for private/internal use
⚠️ **For production**: Use environment variables
```python
import os
ODOO_USER = os.getenv('ODOO_USER')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD')
```

---

## 📝 Customization

### Add More Images

1. Add images to `images/` folder
2. Update script:

```python
PRODUCT_CATEGORIES = {
    'Sports Cards': {
        'images': [
            'sports-cards-center.png',
            'cards_left.png',
            'cards_right.png',
            'NEW_IMAGE.png'  # ← Add here
        ]
    }
}
```

3. Run script again

### Update Product Prices

Edit `odoo_website_products.py`:

```python
PRODUCTS = [
    {
        'name': 'Sports Cards',
        'list_price': 39.99,  # ← Change here
        ...
    }
]
```

### Add New Product

Add to `PRODUCTS` array:

```python
{
    'name': 'New Product Name',
    'category': 'Category Name',
    'description': 'Product description here',
    'list_price': 49.99,
    'website_published': True,
}
```

---

## ✨ Complete Process

```
Step 1: Run odoo_image_upload.py
   ↓
   Uploads all images to Odoo Media
   Creates 6 product categories
   
Step 2: Run odoo_website_products.py
   ↓
   Creates 6 product records
   Assigns to categories
   Publishes to website
   
Step 3: Verify in Odoo
   ↓
   Check Website > Media
   Check eCommerce > Categories
   Check eCommerce > Products
   
✅ Done!
```

---

## 📞 Support

If scripts fail:
1. Check error message carefully
2. Verify Odoo credentials
3. Verify images folder path
4. Check internet connection
5. Contact: kahpk1933@gmail.com

---

## 🎯 Next Steps After Scripts

1. **Images are uploaded** ✓
2. **Products are created** ✓
3. **Categories are set up** ✓
4. **Now integrate with website pages** → Use iframe code from `ODOO_IFRAME_CODE.md`

---

**Ready to run?** Start with `odoo_image_upload.py` first! 🚀
