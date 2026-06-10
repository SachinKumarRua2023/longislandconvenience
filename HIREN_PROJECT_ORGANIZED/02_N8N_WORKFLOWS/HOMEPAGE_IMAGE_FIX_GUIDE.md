# 🏠 Homepage Image Fix Guide
**All 14 Odoo Websites - Homepage Image Configuration & Fix**

---

## 🌐 Website Homepages Overview

### Access All Websites

| Website ID | Name | Homepage URL | Check Method |
|-----------|------|-------------|--------------|
| 1 | Long Island Convenience | https://longislandconvenience.com | Browser check |
| 18 | Country Cove Balloons | https://longislandballoonsdecor.com | Browser check |
| 27 | Gift Baskets | https://ligiftbasket.com | Browser check |
| 29 | Print & Copy | https://longislandprintandmail.org | Browser check |
| 33 | Card Shop | https://longislandcard.com | Browser check |
| 36-46 | Expansion Sites | https://[domain].com | Browser check |

---

## 🔍 STEP 1: Check If Images Exist on Homepage

### Method 1: Visual Browser Check

```
1. Open website URL in browser
2. Look at homepage
3. Check:
   ├─ Banner/Hero image at top
   ├─ Category images
   ├─ Featured products
   ├─ Footer images
   └─ Logo/branding
```

### Method 2: Check Odoo Backend - Images on Homepage

**In Odoo Admin Panel**:
```
1. Go to: Website → Homepage
2. Click: Website 1 (or any website)
3. Check: "Home Page" field
4. Look for: Content block images
5. Verify: Image URLs are working
```

### Method 3: Check via Database - Homepage Content

```python
import xmlrpc.client

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

# Check homepage for Website 1
website = models.execute_kw(DB, uid, PASSWORD, 'website', 'read',
    [1],  # Website ID 1
    ['id', 'name', 'homepage_url', 'logo'])

print(f"Website: {website[0]['name']}")
print(f"Homepage URL: {website[0].get('homepage_url', 'Not set')}")
print(f"Logo: {website[0].get('logo', 'Not set')}")
```

---

## 🖼️ STEP 2: Homepage Image Locations (Where Images Are Used)

### Common Homepage Image Areas

```
Homepage Layout:
┌─────────────────────────────────────────┐
│         LOGO / HEADER IMAGE             │
├─────────────────────────────────────────┤
│                                         │
│       BANNER / HERO IMAGE               │  ← Main banner
│       (Large image at top)              │
│                                         │
├─────────────────────────────────────────┤
│  CAT1    CAT2    CAT3    CAT4    CAT5  │  ← Category images
│ [img]   [img]   [img]   [img]   [img]  │
├─────────────────────────────────────────┤
│                                         │
│   FEATURED PRODUCTS / CAROUSEL          │  ← Product images
│   [img] [img] [img] [img]               │
│                                         │
├─────────────────────────────────────────┤
│  Featured Blog / News / Promotions      │  ← Promo images
│         [img] [img] [img]               │
├─────────────────────────────────────────┤
│         FOOTER WITH IMAGES              │  ← Footer images
│         (Social, badges, etc)           │
└─────────────────────────────────────────┘
```

### Odoo Homepage Building Blocks

Each homepage has these sections:

1. **Hero Banner** - Main large image
2. **Category Cards** - Category thumbnail images
3. **Product Carousel** - Product images
4. **Testimonials** - Avatar images
5. **CTA Blocks** - Call-to-action images
6. **Footer** - Footer images

---

## ✅ How to Check Image Status

### Check 1: Logo Is Present?

```python
# Check if website has logo
website_data = models.execute_kw(DB, uid, PASSWORD, 'website', 'read',
    [1],  # Website 1
    ['logo'])

if website_data[0]['logo']:
    print("✅ Logo exists")
else:
    print("❌ Logo missing - NEEDS FIX")
```

### Check 2: Homepage Has Content?

```python
# Check if homepage has HTML content
website_data = models.execute_kw(DB, uid, PASSWORD, 'website', 'read',
    [1],
    ['homepage_url'])

if website_data[0]['homepage_url']:
    print("✅ Homepage configured")
else:
    print("❌ Homepage not configured - NEEDS FIX")
```

### Check 3: Product Images Exist?

```python
# Get all products and check images
products = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'search',
    [['website_published', '=', True]])

for product_id in products[:5]:
    product = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'read',
        [product_id],
        ['name', 'image_1920'])
    
    if product[0]['image_1920']:
        print(f"✅ {product[0]['name']} - Has image")
    else:
        print(f"❌ {product[0]['name']} - NO IMAGE - NEEDS FIX")
```

### Check 4: Category Images Exist?

```python
# Check categories for images
categories = models.execute_kw(DB, uid, PASSWORD, 'product.category', 'search',
    [[]])

for cat_id in categories[:10]:
    cat = models.execute_kw(DB, uid, PASSWORD, 'product.category', 'read',
        [cat_id],
        ['name', 'image_128'])
    
    if cat[0]['image_128']:
        print(f"✅ {cat[0]['name']} - Has image")
    else:
        print(f"❌ {cat[0]['name']} - NO IMAGE - NEEDS FIX")
```

---

## 🔧 STEP 3: Fix Homepage Images

### Fix Type 1: Add/Update Website Logo

**Via Odoo UI**:
```
1. Go to: Settings → Website → Branding
2. Find: "Logo"
3. Click: "Upload an image"
4. Select: Your logo image
5. Save
```

**Via Python Script**:
```python
import base64

# Read image file
with open('path/to/logo.png', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

# Update website logo
models.execute_kw(DB, uid, PASSWORD, 'website', 'write',
    [1],  # Website 1
    {
        'logo': image_data,
    }
)

print("✅ Logo updated")
```

### Fix Type 2: Add/Update Hero Banner Image

**Via Odoo UI**:
```
1. Go to: Website → Edit Website
2. Click: Edit Homepage
3. Find: Hero section / Banner block
4. Click: Image field
5. Upload: Banner image
6. Save
```

**Via Python Script**:
```python
# Get the homepage (usually a web.page record)
homepage = models.execute_kw(DB, uid, PASSWORD, 'website.page', 'search',
    [['website_id', '=', 1], ['is_homepage', '=', True]])

if homepage:
    # Update the page with new image in content
    models.execute_kw(DB, uid, PASSWORD, 'website.page', 'write',
        [homepage[0]],
        {
            # Content would be updated via HTML/XML
        }
    )
```

### Fix Type 3: Add Product Images

**Via Odoo UI**:
```
1. Go to: eCommerce → Products
2. Open: Product
3. Scroll: To Images section
4. Click: "Add an image"
5. Upload: Product image
6. Save
```

**Via Python Script**:
```python
import base64

# Read image
with open('path/to/product.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

# Update product
models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
    [product_id],
    {
        'image_1920': image_data,  # Main image
    }
)

# Add additional images
models.execute_kw(DB, uid, PASSWORD, 'product.image', 'create',
    [{
        'product_id': product_id,
        'image_1920': image_data,
        'name': 'Product image 2',
        'sequence': 1,
    }]
)

print("✅ Product images updated")
```

### Fix Type 4: Add Category Images

**Via Odoo UI**:
```
1. Go to: eCommerce → Categories
2. Open: Category
3. Find: Icon/Image field
4. Upload: Category image
5. Save
```

**Via Python Script**:
```python
import base64

# Read image
with open('path/to/category.png', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

# Update category
models.execute_kw(DB, uid, PASSWORD, 'product.category', 'write',
    [category_id],
    {
        'image_128': image_data,  # Icon image
    }
)

print("✅ Category image updated")
```

---

## 🌐 Fix Images for All 14 Websites

### Script: Check All Websites

```python
import xmlrpc.client

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

# All website IDs
websites = [1, 18, 27, 29, 33, 36, 37, 38, 39, 40, 41, 42, 45, 46]

print("CHECKING ALL WEBSITES FOR IMAGES:")
print("=" * 60)

for website_id in websites:
    try:
        website = models.execute_kw(DB, uid, PASSWORD, 'website', 'read',
            [website_id],
            ['id', 'name', 'logo'])
        
        name = website[0]['name']
        has_logo = bool(website[0].get('logo'))
        
        status = "✅ HAS LOGO" if has_logo else "❌ NO LOGO"
        print(f"Website {website_id:2d}: {name:30s} | {status}")
    except:
        print(f"Website {website_id:2d}: ERROR")

print("=" * 60)
```

### Script: Bulk Add Images to All Websites

```python
import xmlrpc.client
import base64
import os

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

# Get image path
logo_path = "C:\\path\\to\\logo.png"

# Read and encode image
with open(logo_path, 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

# All websites
websites = [1, 18, 27, 29, 33, 36, 37, 38, 39, 40, 41, 42, 45, 46]

print("UPDATING LOGOS FOR ALL WEBSITES:")

for website_id in websites:
    try:
        models.execute_kw(DB, uid, PASSWORD, 'website', 'write',
            [website_id],
            {'logo': image_data}
        )
        print(f"✅ Website {website_id}: Logo updated")
    except Exception as e:
        print(f"❌ Website {website_id}: Error - {str(e)[:50]}")

print("\nDone!")
```

---

## 📋 Homepage Image Fix Checklist

### For Each Website, Check & Fix:

```
Website ID: _____

☐ LOGO
  Status: Missing / Present
  Fix: Upload logo

☐ HERO BANNER
  Status: Missing / Present
  Fix: Upload banner image

☐ CATEGORY IMAGES
  Count: _____ categories
  Missing: _____ categories
  Fix: Bulk upload category images

☐ PRODUCT IMAGES
  Count: _____ products
  Missing images: _____ products
  Fix: Bulk upload product images

☐ FOOTER IMAGES
  Status: Missing / Present
  Fix: Add footer images

☐ TESTIMONIAL IMAGES
  Count: _____ testimonials
  Missing: _____ testimonials
  Fix: Add testimonial avatars
```

---

## 🔗 External Image Resources

### Where to Get Images

| Source | Type | For What |
|--------|------|----------|
| Unsplash | Free stock | Banners, backgrounds |
| Pexels | Free stock | Product backdrops |
| Pixabay | Free stock | Category images |
| Your files | Custom | Logos, specific products |
| Canva | Design tool | Custom banners |
| Adobe Stock | Premium | Professional images |

### Using External URLs (If Hosting Elsewhere)

```python
# Instead of base64, use URL reference
models.execute_kw(DB, uid, PASSWORD, 'website', 'write',
    [website_id],
    {
        'social_media_image': 'https://example.com/image.jpg'
    }
)
```

---

## 🎨 Image Specifications

### Recommended Image Sizes

| Element | Width | Height | Format | Size |
|---------|-------|--------|--------|------|
| Logo | 200px | 80px | PNG/SVG | <100KB |
| Hero Banner | 1920px | 600px | JPG | <500KB |
| Category Icon | 256px | 256px | PNG | <100KB |
| Product Image | 1920px | 1920px | JPG | <300KB |
| Footer Logo | 150px | 50px | PNG | <50KB |
| Social Share | 1200px | 630px | JPG | <200KB |

---

## 🚀 N8N Automation: Auto-Fix Missing Images

```json
{
  "name": "Homepage Image Checker & Fixer",
  "nodes": [
    {
      "name": "Schedule Daily",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "interval": ["days"],
        "triggerAtHour": 8
      }
    },
    {
      "name": "Get All Websites",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://country-cove-inc.odoo.com/xmlrpc/2/object"
      }
    },
    {
      "name": "Check Images",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "// Check each website for missing images"
      }
    },
    {
      "name": "Report Missing",
      "type": "n8n-nodes-base.emailSend",
      "parameters": {
        "subject": "Homepage Images Status Report"
      }
    }
  ]
}
```

---

## 🔍 Troubleshooting: Image Not Showing

### Issue 1: Image Uploaded But Not Showing

```
Solution:
1. Check image format (JPG/PNG/GIF)
2. Verify file size < 5MB
3. Clear browser cache (Ctrl+Shift+Delete)
4. Check image dimensions meet specs
5. Reload page (F5)
```

### Issue 2: Broken Image Link (404)

```
Solution:
1. Verify URL is correct
2. Check image still exists on server
3. Re-upload the image
4. Use CDN if available
5. Check file permissions
```

### Issue 3: Image Appears But Looks Distorted

```
Solution:
1. Check image resolution (use recommended size)
2. Verify aspect ratio matches placeholder
3. Compress image if too large
4. Use proper format (PNG for transparency, JPG for photos)
```

### Issue 4: Image Not Updating After Upload

```
Solution:
1. Clear Odoo cache: Settings → Tools → Clear Cache
2. Hard refresh: Ctrl+Shift+R (not just F5)
3. Incognito/Private mode to test
4. Wait 5 minutes for CDN to update
5. Logout and login again
```

---

## 📊 Status Check Script Template

```python
# Run this to get full status of all websites

import xmlrpc.client

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

websites = [1, 18, 27, 29, 33, 36, 37, 38, 39, 40, 41, 42, 45, 46]

report = []

for wid in websites:
    website = models.execute_kw(DB, uid, PASSWORD, 'website', 'read', [wid], ['id', 'name', 'logo'])
    
    has_logo = bool(website[0].get('logo'))
    name = website[0]['name']
    
    report.append({
        'id': wid,
        'name': name,
        'logo': 'OK' if has_logo else 'MISSING'
    })

# Print report
print("\nHOMEPAGE IMAGE STATUS REPORT")
print("=" * 70)
for item in report:
    print(f"Website {item['id']:2d}: {item['name']:30s} | Logo: {item['logo']}")
print("=" * 70)
```

---

## 🎯 Next Steps

1. **Run Status Check** - See which websites have missing images
2. **Collect Images** - Gather logos, banners, product images
3. **Choose Method** - Manual UI or Python script
4. **Apply Fix** - Update all websites systematically
5. **Verify** - Check each website visually in browser
6. **Monitor** - Set up n8n automation to check daily

---

## 📞 Quick Commands

### Check Website 1 Logo
```python
models.execute_kw(DB, uid, PASSWORD, 'website', 'read', [1], ['logo'])
```

### Update Website 1 Logo
```python
models.execute_kw(DB, uid, PASSWORD, 'website', 'write', [1], {'logo': image_data})
```

### Get All Website IDs
```python
models.execute_kw(DB, uid, PASSWORD, 'website', 'search', [[]])
```

---

**Last Updated**: June 7, 2026
**Status**: Complete Homepage Image Fix Guide Ready
**Next Step**: Check your websites and apply fixes!
