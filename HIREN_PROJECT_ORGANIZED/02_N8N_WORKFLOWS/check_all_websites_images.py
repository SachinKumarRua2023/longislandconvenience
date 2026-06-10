#!/usr/bin/env python3
"""
Check all 14 Odoo websites for homepage images
Shows which websites have images and which are missing
"""

import xmlrpc.client
import sys

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

# Connect to Odoo
print("[CONNECTING] Authenticating to Odoo...")
common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})

if not uid:
    print("[ERROR] Authentication failed!")
    sys.exit(1)

models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
print(f"[OK] Authenticated as user {uid}\n")

# All website IDs
websites = [1, 18, 27, 29, 33, 36, 37, 38, 39, 40, 41, 42, 45, 46]

print("=" * 80)
print("CHECKING ALL 14 WEBSITES FOR HOMEPAGE IMAGES")
print("=" * 80)
print()

# Status tracking
results = []
has_images = 0
missing_images = 0

# Check each website
for website_id in websites:
    try:
        # Get website data
        website = models.execute_kw(DB, uid, PASSWORD, 'website', 'read',
            [website_id],
            ['id', 'name', 'logo', 'social_media_image'])

        if not website:
            print(f"[WARN] Website {website_id}: Not found")
            continue

        name = website[0]['name']
        has_logo = bool(website[0].get('logo'))
        has_social_image = bool(website[0].get('social_media_image'))

        # Determine status
        if has_logo or has_social_image:
            status = "OK"
            has_images += 1
        else:
            status = "MISSING"
            missing_images += 1

        # Store result
        results.append({
            'id': website_id,
            'name': name,
            'has_logo': has_logo,
            'has_social_image': has_social_image,
            'status': status
        })

        # Print status
        logo_symbol = "[OK]" if has_logo else "[NO]"
        social_symbol = "[OK]" if has_social_image else "[NO]"

        print(f"Website {website_id:2d}: {name:30s} | Logo: {logo_symbol} | Social: {social_symbol}")

    except Exception as e:
        print(f"[ERROR] Website {website_id}: {str(e)[:60]}")
        missing_images += 1

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total Websites: {len(results)}")
print(f"With Images: {has_images}")
print(f"Missing Images: {missing_images}")
print(f"Coverage: {(has_images * 100) // len(results)}%")
print()

# Details of missing images
missing = [r for r in results if r['status'] == 'MISSING']
if missing:
    print("WEBSITES NEEDING IMAGE FIX:")
    print("-" * 80)
    for item in missing:
        print(f"  • Website {item['id']:2d}: {item['name']}")
    print()

# Check products with images
print("=" * 80)
print("CHECKING PRODUCT IMAGES")
print("=" * 80)
print()

try:
    products_total = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'search',
        [['website_published', '=', True]], {})

    products_with_images = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'search',
        [['website_published', '=', True], ['image_1920', '!=', False]], {})

    print(f"Total Published Products: {len(products_total)}")
    print(f"Products With Images: {len(products_with_images)}")
    print(f"Products Missing Images: {len(products_total) - len(products_with_images)}")
    print(f"Product Image Coverage: {(len(products_with_images) * 100) // len(products_total)}%" if len(products_total) > 0 else "N/A")

except Exception as e:
    print(f"[ERROR] Could not check products: {str(e)[:80]}")

print()

# Check categories with images
print("=" * 80)
print("CHECKING CATEGORY IMAGES")
print("=" * 80)
print()

try:
    categories_total = models.execute_kw(DB, uid, PASSWORD, 'product.category', 'search',
        [[]], {})

    categories_with_images = models.execute_kw(DB, uid, PASSWORD, 'product.category', 'search',
        [['image_128', '!=', False]], {})

    print(f"Total Categories: {len(categories_total)}")
    print(f"Categories With Images: {len(categories_with_images)}")
    print(f"Categories Missing Images: {len(categories_total) - len(categories_with_images)}")
    print(f"Category Image Coverage: {(len(categories_with_images) * 100) // len(categories_total)}%" if len(categories_total) > 0 else "N/A")

except Exception as e:
    print(f"[ERROR] Could not check categories: {str(e)[:80]}")

print()
print("=" * 80)
print("DETAILED RESULTS")
print("=" * 80)
print()

for item in results:
    print(f"Website {item['id']:2d}: {item['name']}")
    print(f"  Logo: {'YES' if item['has_logo'] else 'NO'}")
    print(f"  Social Image: {'YES' if item['has_social_image'] else 'NO'}")
    print(f"  Status: {item['status']}")
    print()

print("=" * 80)
print("NEXT STEPS:")
print("=" * 80)
print()
print("1. For websites MISSING images:")
print("   → Upload logo image via Odoo UI (Settings → Branding)")
print("   → Or use Python script to bulk update")
print()
print("2. For products missing images:")
print("   → Go to eCommerce → Products")
print("   → Add images to products")
print()
print("3. For categories missing images:")
print("   → Go to eCommerce → Categories")
print("   → Add category icons/images")
print()
print("See: HOMEPAGE_IMAGE_FIX_GUIDE.md for complete fix instructions")
print()
print("=" * 80)
