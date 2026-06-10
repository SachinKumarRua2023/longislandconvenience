#!/usr/bin/env python3
"""
WEBSITE 1 - LONG ISLAND CONVENIENCE
Add products with images to Website 1 only
"""

import xmlrpc.client
import base64

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"
WEBSITE_ID = 1  # ← Website 1 only

print("=" * 80)
print("WEBSITE 1 - LONG ISLAND CONVENIENCE")
print("Add Products Script")
print("=" * 80)
print()

# Connect
print("[1/5] Connecting to Odoo...")
common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
print("[OK] Connected\n")

# Products to add
products = [
    {
        'name': 'Premium Gift Basket Deluxe',
        'category_id': 74,  # Gift Baskets
        'price': 89.99,
        'cost': 45.00,
        'description': 'Luxury gift basket with premium items',
        'image_path': 'C:\\path\\to\\product1.jpg'
    },
    {
        'name': 'Celebration Balloon Bundle',
        'category_id': 51,  # Balloons
        'price': 34.99,
        'cost': 15.00,
        'description': 'Colorful balloons for celebrations',
        'image_path': 'C:\\path\\to\\product2.jpg'
    },
    {
        'name': 'Greeting Card Set',
        'category_id': 144,  # Cards
        'price': 12.99,
        'cost': 5.00,
        'description': 'Assorted greeting cards',
        'image_path': 'C:\\path\\to\\product3.jpg'
    }
]

print(f"[2/5] Adding {len(products)} products to Website {WEBSITE_ID}...\n")

# Add products
added = 0
for product in products:
    try:
        # Read image if provided
        image_data = None
        if product.get('image_path'):
            try:
                with open(product['image_path'], 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode()
            except FileNotFoundError:
                print(f"  [WARN] Image not found: {product['image_path']}")

        # Create product
        product_data = {
            'name': product['name'],
            'type': 'product',
            'categ_id': product['category_id'],
            'list_price': product['price'],
            'standard_price': product['cost'],
            'description': product['description'],
        }

        if image_data:
            product_data['image_1920'] = image_data

        product_id = models.execute_kw(DB, uid, PASSWORD, 'product.product',
            'create', [product_data])

        # Assign to Website 1
        models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
            [product_id],
            {
                'website_ids': [(4, WEBSITE_ID)],
                'website_published': True
            }
        )

        print(f"  ✓ {product['name']}")
        print(f"    → Product ID: {product_id}")
        print(f"    → Website: {WEBSITE_ID} (Long Island Convenience)")
        print(f"    → Price: ${product['price']}")
        print()

        added += 1

    except Exception as e:
        print(f"  ✗ {product['name']}: Error - {str(e)[:80]}")
        print()

print("=" * 80)
print(f"RESULTS: {added}/{len(products)} products added")
print("=" * 80)
print()

# Get product count
print("[3/5] Getting product count...")
products_on_site = models.execute_kw(DB, uid, PASSWORD, 'product.product',
    'search', [['website_published', '=', True]], {})
print(f"Total published products on Website {WEBSITE_ID}: {len(products_on_site)}")
print()

# Get website info
print("[4/5] Website info:")
try:
    website = models.execute_kw(DB, uid, PASSWORD, 'website', 'read',
        [WEBSITE_ID], ['id', 'name'])
    print(f"  Website ID: {website[0]['id']}")
    print(f"  Name: {website[0]['name']}")
except:
    pass

print()

print("[5/5] Done!")
print()
print("NEXT STEPS:")
print("  1. Check products on website: https://longislandconvenience.com")
print("  2. If images missing, run: add_images_website_1.py")
print("  3. If need to update homepage, run: update_homepage_website_1.py")
print()
