#!/usr/bin/env python3
"""
BULK OPERATIONS - Run operations on ALL 14 websites at once
"""

import xmlrpc.client
import sys
import base64

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

print("=" * 80)
print("BULK OPERATIONS - ALL 14 WEBSITES")
print("=" * 80)
print()

# Connect
print("[1/4] Connecting to Odoo...")
common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
print("[OK] Connected\n")

# All websites
websites = [1, 18, 27, 29, 33, 36, 37, 38, 39, 40, 41, 42, 45, 46]

print(f"[2/4] Found {len(websites)} websites")
print(f"IDs: {websites}\n")

# ============================================================================
# OPERATION 1: Add Same Logo to All 14 Websites
# ============================================================================

print("=" * 80)
print("OPERATION 1: UPDATE LOGO ON ALL WEBSITES")
print("=" * 80)
print()

logo_path = "C:\\path\\to\\your\\logo.png"  # ← CHANGE THIS PATH

print(f"Logo file: {logo_path}")
print()

try:
    # Read logo
    with open(logo_path, 'rb') as f:
        logo_data = base64.b64encode(f.read()).decode()

    # Update all websites
    updated = 0
    for website_id in websites:
        try:
            models.execute_kw(DB, uid, PASSWORD, 'website', 'write',
                [website_id],
                {'logo': logo_data}
            )
            print(f"  ✓ Website {website_id:2d}: Logo updated")
            updated += 1
        except Exception as e:
            print(f"  ✗ Website {website_id:2d}: Error - {str(e)[:50]}")

    print(f"\n✓ Total updated: {updated}/{len(websites)}")

except FileNotFoundError:
    print(f"[ERROR] Logo file not found at: {logo_path}")
    print("Please update the path and try again")

print()

# ============================================================================
# OPERATION 2: Update Product Price Across All Websites
# ============================================================================

print("=" * 80)
print("OPERATION 2: UPDATE PRODUCT PRICE")
print("=" * 80)
print()

product_id = 100  # ← CHANGE THIS PRODUCT ID
new_price = 79.99  # ← CHANGE THIS PRICE

print(f"Product ID: {product_id}")
print(f"New Price: ${new_price}")
print()

try:
    # Update product (same for all websites since products are shared)
    models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
        [product_id],
        {
            'list_price': new_price,
            'website_published': True
        }
    )
    print(f"✓ Product {product_id}: Price updated to ${new_price}")
    print("✓ Updated on ALL 14 websites (shared database)")

except Exception as e:
    print(f"[ERROR] {str(e)[:100]}")

print()

# ============================================================================
# OPERATION 3: Get Status of All Websites
# ============================================================================

print("=" * 80)
print("OPERATION 3: GET STATUS OF ALL WEBSITES")
print("=" * 80)
print()

try:
    for website_id in websites:
        try:
            # Get website basic info by ID
            website = models.execute_kw(DB, uid, PASSWORD, 'website', 'search',
                [[('id', '=', website_id)]], {})

            if website:
                print(f"✓ Website {website_id:2d}: Active")
            else:
                print(f"✗ Website {website_id:2d}: Not found")
        except:
            print(f"✗ Website {website_id:2d}: Error accessing")

except Exception as e:
    print(f"[ERROR] {str(e)[:100]}")

print()

# ============================================================================
# OPERATION 4: Get Product Count for All Websites
# ============================================================================

print("=" * 80)
print("OPERATION 4: PRODUCT & IMAGE COUNT")
print("=" * 80)
print()

try:
    products = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'search', [[]], {})
    images = models.execute_kw(DB, uid, PASSWORD, 'product.image', 'search', [[]], {})
    categories = models.execute_kw(DB, uid, PASSWORD, 'product.category', 'search', [[]], {})

    print(f"✓ Total Products (Shared): {len(products)}")
    print(f"✓ Total Images: {len(images)}")
    print(f"✓ Total Categories: {len(categories)}")
    print()
    print("NOTE: All websites share the same product database")
    print("So products appear on websites they are assigned to")

except Exception as e:
    print(f"[ERROR] {str(e)[:100]}")

print()

# ============================================================================
# OPERATION 5: Bulk Assign Products to Websites
# ============================================================================

print("=" * 80)
print("OPERATION 5: ASSIGN PRODUCT TO MULTIPLE WEBSITES")
print("=" * 80)
print()

product_id = 100  # ← CHANGE THIS
assign_to = [1, 18, 27]  # ← CHANGE THIS (website IDs)

print(f"Product: {product_id}")
print(f"Assign to websites: {assign_to}")
print()

try:
    # Prepare website data
    website_data = [(4, wid) for wid in assign_to]

    models.execute_kw(DB, uid, PASSWORD, 'product.product', 'write',
        [product_id],
        {
            'website_ids': website_data,
            'website_published': True
        }
    )

    print(f"✓ Product {product_id} assigned to {len(assign_to)} websites")
    print(f"✓ Websites: {assign_to}")

except Exception as e:
    print(f"[ERROR] {str(e)[:100]}")

print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("BULK OPERATIONS SUMMARY")
print("=" * 80)
print()
print("Available operations in this script:")
print("  1. Update logo on all 14 websites")
print("  2. Update product price (affects all websites)")
print("  3. Check status of all websites")
print("  4. Get product/image/category counts")
print("  5. Assign product to multiple websites")
print()
print("INSTRUCTIONS:")
print("  1. Edit this file with your values (paths, IDs, prices)")
print("  2. Run: python bulk_operations.py")
print("  3. Check results in console output")
print()
print("For website-specific operations, use:")
print("  → WEBSITE_1/add_products.py")
print("  → WEBSITE_18/add_images.py")
print("  → etc.")
print()
