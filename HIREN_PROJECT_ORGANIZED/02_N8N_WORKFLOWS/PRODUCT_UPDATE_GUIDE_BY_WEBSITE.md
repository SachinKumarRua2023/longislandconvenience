# 📦 Product Update Guide - By Website
**Hiren Kumar's 14 Odoo Websites**

---

## 🌐 All Website IDs & Names

| Website ID | Website Name | Domain | Status |
|-----------|-----------|--------|--------|
| **1** | Long Island Convenience | longislandconvenience.com | 🟢 Live |
| **18** | Country Cove Balloons | longislandballoonsdecor.com | 🟢 Active |
| **27** | Country Cove Gift Baskets | ligiftbasket.com | 🟢 Active |
| **29** | Long Island Print & Copy | longislandprintandmail.org | 🟢 Active |
| **33** | Long Island Card Shop | longislandcard.com | 🟢 Active |
| **36** | E-Commerce Site #6 | TBD | 🟢 Active |
| **37** | E-Commerce Site #7 | TBD | 🟢 Active |
| **38** | E-Commerce Site #8 | TBD | 🟢 Active |
| **39** | E-Commerce Site #9 | TBD | 🟢 Active |
| **40** | E-Commerce Site #10 | TBD | 🟢 Active |
| **41** | E-Commerce Site #11 | TBD | 🟢 Active |
| **42** | E-Commerce Site #12 | TBD | 🟢 Active |
| **45** | E-Commerce Site #13 | TBD | 🟢 Active |
| **46** | E-Commerce Site #14 | TBD | 🟢 Active |

---

## 📍 Where This Is Documented

| Topic | File Location | Details |
|-------|--------------|---------|
| **Website IDs** | `01_DOCUMENTATION/ODOO_WEBSITE_IDS.md` | All 14 website IDs |
| **Product System** | `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md` | Complete architecture |
| **API Reference** | `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md` | XML-RPC methods |
| **Website Setup** | `01_DOCUMENTATION/ODOO_WEBSITE45_SETUP.md` | Website configuration |
| **Update Scripts** | `02_N8N_WORKFLOWS/` | Python/n8n examples |

---

## 🔄 How Product Update System Works

### Architecture Flow

```
Product Added/Updated
    ↓
[Odoo Database]
    ├─ Stores product data
    ├─ Stores website assignments
    └─ Stores product variants
    ↓
[Website 1, 18, 27, 29, 33, 36-46]
    ├─ Website 1: Shows assigned products
    ├─ Website 18: Shows assigned products
    ├─ Website 27: Shows assigned products
    └─ ... All 14 websites
    ↓
[Product Visibility]
    ├─ Published: Visible on website
    ├─ Unpublished: Hidden
    └─ Website-specific: Only on selected websites
```

---

## 📝 Method 1: Manual Update Via UI

### Step-by-Step: Add Product to Specific Website

#### Step 1: Login to Odoo
```
URL: https://country-cove-inc.odoo.com/
Email: countrycoveinc@gmail.com
Password: M@nhattan1234
```

#### Step 2: Navigate to Products
```
Menu: eCommerce → Products
Click: Create
```

#### Step 3: Enter Product Details
```
Name:           Product Name
Category:       Select category
Price:          Sale price
Cost:           Cost price
Description:    Product details
```

#### Step 4: Upload Images
```
Main Image:     Click "Add an image"
Gallery:        Click "Add images"
Drag/upload:    Your image files
```

#### Step 5: Assign to Website(s)
```
Scroll down to: "SALES"
Find:           "Website"
Select:         Check website(s) you want
    ☐ Website 1 (Long Island Convenience)
    ☐ Website 18 (Country Cove Balloons)
    ☐ Website 27 (Country Cove Gift Baskets)
    ☐ Website 29 (Long Island Print & Copy)
    ☐ Website 33 (Long Island Card Shop)
    ☐ Website 36-46 (Other sites)
    
Or:             "All Websites" checkbox
```

#### Step 6: Publish Product
```
Scroll down to: "WEBSITE"
Find:           "Published"
Check:          ☑ Published
```

#### Step 7: Save
```
Click: Save
Status: Product now visible on selected websites
```

---

## 🐍 Method 2: Update Via Python Script

### Script 1: Add Product to Specific Website

```python
import xmlrpc.client

# Odoo Connection
URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

# Connect
common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

# Create product
product_data = {
    'name': 'Premium Gift Basket',
    'type': 'product',
    'categ_id': 27,  # Category ID
    'list_price': 89.99,
    'standard_price': 45.00,
    'description': 'Luxury gift basket with premium items',
}

product_id = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'create', [product_data])
print(f"Product created with ID: {product_id}")

# Assign to Website 1 (Long Island Convenience)
models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
    [product_id],
    {
        'website_ids': [(4, 1)],  # Assign to Website ID 1
        'website_published': True,  # Publish
    }
)
print(f"Product assigned to Website 1")

# Assign to Website 27 (Gift Baskets)
models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
    [product_id],
    {
        'website_ids': [(4, 27)],  # Add Website ID 27
        'website_published': True,
    }
)
print(f"Product assigned to Website 27")
```

### Script 2: Add Product to Multiple Websites

```python
import xmlrpc.client

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

# Website IDs to assign
website_ids = [1, 18, 27]  # Assign to 3 websites

# Prepare website assignment data
website_data = [(4, website_id) for website_id in website_ids]

# Update product
product_id = 100  # Your product ID

models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
    [product_id],
    {
        'website_ids': website_data,
        'website_published': True,
    }
)

print(f"Product {product_id} assigned to websites: {website_ids}")
```

### Script 3: Update Product for All Websites

```python
import xmlrpc.client

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

# Get all websites
websites = models.execute_kw(DB, uid, PASSWORD, 'website', 'search', [[]])

# Prepare data for all websites
website_data = [(4, website_id) for website_id in websites]

product_id = 100  # Your product ID

# Assign to all websites
models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
    [product_id],
    {
        'website_ids': website_data,
        'website_published': True,
    }
)

print(f"Product {product_id} assigned to ALL {len(websites)} websites")
print(f"Websites: {websites}")
```

### Script 4: Bulk Update Multiple Products

```python
import xmlrpc.client

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

# Products to update with their website assignments
products_to_update = [
    {
        'product_id': 100,
        'websites': [1, 18, 27]  # Assign to 3 websites
    },
    {
        'product_id': 101,
        'websites': [29, 33]  # Assign to 2 websites
    },
    {
        'product_id': 102,
        'websites': [36, 37, 38, 39, 40, 41, 42, 45, 46]  # All other sites
    }
]

for product_data in products_to_update:
    product_id = product_data['product_id']
    website_ids = product_data['websites']
    
    website_data = [(4, wid) for wid in website_ids]
    
    models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
        [product_id],
        {
            'website_ids': website_data,
            'website_published': True,
        }
    )
    
    print(f"✓ Product {product_id} → Websites {website_ids}")

print("✓ All products updated!")
```

---

## 🤖 Method 3: Update Via n8n Workflow

### n8n Workflow for Product Website Assignment

```json
{
  "name": "Product Website Assignment",
  "nodes": [
    {
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 300]
    },
    {
      "name": "Product Input",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "return {\n  product_id: 100,\n  product_name: 'Gift Basket Premium',\n  websites: [1, 18, 27],\n  publish: true\n}"
      },
      "position": [500, 300]
    },
    {
      "name": "Connect Odoo",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://country-cove-inc.odoo.com/xmlrpc/2/object",
        "method": "POST",
        "body": "{\n  'method': 'write',\n  'params': {\n    'product_id': '={{$json.product_id}}',\n    'website_ids': '={{$json.websites}}',\n    'website_published': '={{$json.publish}}'\n  }\n}"
      },
      "position": [750, 300]
    },
    {
      "name": "Send Notification",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "text": "✓ Product {{$json.product_name}} assigned to {{$json.websites.length}} websites"
      },
      "position": [1000, 300]
    }
  ]
}
```

---

## 🔐 API Reference: Website Assignment Methods

### Method 1: Add Website (Keep Existing)

```python
'website_ids': [(4, website_id)]  # 4 = Add
```

**Result**: Adds website to existing list

### Method 2: Replace All Websites

```python
'website_ids': [(6, False, [1, 18, 27])]  # 6 = Replace
```

**Result**: Replaces all with new list

### Method 3: Remove Website

```python
'website_ids': [(3, website_id)]  # 3 = Remove
```

**Result**: Removes website from list

### Method 4: Clear All Websites

```python
'website_ids': [(5, False)]  # 5 = Clear
```

**Result**: Removes product from all websites

---

## 📊 Field Reference

### Product Fields for Website Control

```python
{
    # Basic Info
    'name': 'Product Name',
    'category_id': 27,  # Category ID
    
    # Pricing
    'list_price': 99.99,  # Sell price
    'standard_price': 50.00,  # Cost price
    
    # Website Assignment
    'website_ids': [(4, 1), (4, 18), (4, 27)],  # Websites
    
    # Visibility
    'website_published': True,  # Publish on website
    
    # Images
    'image_1920': base64_image,  # Main image
    
    # Description
    'description': 'Product details',
}
```

---

## 🎯 Common Use Cases

### Use Case 1: New Product for One Website Only

```python
# Add product for Website 1 (Long Island Convenience)
models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
    [product_id],
    {
        'website_ids': [(4, 1)],
        'website_published': True,
    }
)
```

### Use Case 2: Balloon Products to Website 18 Only

```python
# All balloon products to Website 18
balloon_products = [101, 102, 103, 104, 105]

for prod_id in balloon_products:
    models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
        [prod_id],
        {
            'website_ids': [(4, 18)],
            'website_published': True,
        }
    )
```

### Use Case 3: Gift Baskets to Websites 1, 27, 29

```python
# All gift basket products
gift_products = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'search',
    [['categ_id', '=', 27]])  # Category 27 = Gift Baskets

for prod_id in gift_products:
    models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
        [prod_id],
        {
            'website_ids': [(4, 1), (4, 27), (4, 29)],
            'website_published': True,
        }
    )
```

### Use Case 4: Sync Product to All 14 Websites

```python
# Get all website IDs
all_websites = models.execute_kw(DB, uid, PASSWORD, 'website', 'search', [[]])

# Prepare data
website_data = [(4, wid) for wid in all_websites]

# Update product
models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
    [product_id],
    {
        'website_ids': website_data,
        'website_published': True,
    }
)
```

---

## 📋 Website Product Assignment Strategy

### Recommended Setup

| Website | Products | Strategy |
|---------|----------|----------|
| **1** Long Island Convenience | All items | Master store - most products |
| **18** Balloons | Balloons only | Niche shop |
| **27** Gift Baskets | Baskets only | Niche shop |
| **29** Print & Mail | Print items | Niche shop |
| **33** Card Shop | Cards only | Niche shop |
| **36-42** Expansion | All items | Future growth |
| **45-46** International | Selected | Expansion markets |

### Update Workflow

```
Product Created
    ↓
[Assign to Category] (e.g., Balloons = Cat 51)
    ↓
[Assign to Website(s)]
    ├─ Website 1 (Master)
    ├─ Website 18 (Balloons) ← if category 51
    ├─ Website 27 (Baskets) ← if category 74
    └─ etc.
    ↓
[Set Images & Prices]
    ├─ Main image
    ├─ Gallery images
    ├─ Set prices per website (if needed)
    └─ Configure variants
    ↓
[Publish]
    ├─ website_published = True
    └─ Ready for customers
```

---

## 🔍 Query: Check Product Website Assignment

```python
# Get websites for a product
product = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'read',
    [product_id],
    ['name', 'website_ids', 'website_published'])

print(f"Product: {product[0]['name']}")
print(f"Websites: {product[0]['website_ids']}")
print(f"Published: {product[0]['website_published']}")
```

---

## 🚨 Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Product not showing on website | Not published | Set `website_published = True` |
| Product on wrong website | Wrong assignment | Use `(6, False, [list])` to replace |
| Image not displaying | Missing image | Add `image_1920` field |
| Price not showing | Missing price | Set `list_price` and `standard_price` |
| Category missing | Category ID wrong | Check category ID first |

---

## 📞 Quick Reference

### Odoo Credentials
```
URL: https://country-cove-inc.odoo.com/
Email: countrycoveinc@gmail.com
Password: M@nhattan1234
Database: country-cove-inc
```

### All Website IDs
```
[1, 18, 27, 29, 33, 36, 37, 38, 39, 40, 41, 42, 45, 46]
```

### Key Category IDs (Examples)
```
Balloons: 51
Gift Baskets: 74
Cards: 144
Printing: 126
```

---

## 📚 Related Documentation

- **Full Architecture**: `01_DOCUMENTATION/ODOO_WEBSITES_AND_SCRIPTS_DOCUMENTATION.md`
- **Website Setup**: `01_DOCUMENTATION/ODOO_WEBSITE45_SETUP.md`
- **Website IDs**: `01_DOCUMENTATION/ODOO_WEBSITE_IDS.md`
- **Python Scripts**: `02_N8N_WORKFLOWS/` (various JSON examples)
- **N8N Guide**: `02_N8N_WORKFLOWS/README_N8N_WORKFLOWS.md`

---

**Last Updated**: June 7, 2026  
**Status**: Complete Guide Ready  
**Next Step**: Choose your update method and start adding products!
