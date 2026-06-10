#!/usr/bin/env python3
"""
Simple check of all 14 Odoo websites
"""

import xmlrpc.client

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

print("[CONNECTING] To Odoo...")
common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
print(f"[OK] Authenticated\n")

models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")

print("=" * 80)
print("CHECKING ALL 14 WEBSITES")
print("=" * 80)
print()

# Get all websites
try:
    websites = models.execute_kw(DB, uid, PASSWORD, 'website', 'search', [[]], {})
    print(f"Found {len(websites)} websites in database")
    print(f"Website IDs: {websites}")
    print()
except Exception as e:
    print(f"[ERROR] Could not search websites: {str(e)[:100]}")

# Check products
print("=" * 80)
print("CHECKING PRODUCTS")
print("=" * 80)
print()

try:
    # Total products
    all_products = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'search', [[]], {})
    print(f"Total Products in Database: {len(all_products)}")

    # Published products
    published = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'search',
        [['website_published', '=', True]], {})
    print(f"Published Products: {len(published)}")

    # Products with active status
    active = models.execute_kw(DB, uid, PASSWORD, 'product.product', 'search',
        [['active', '=', True]], {})
    print(f"Active Products: {len(active)}")

except Exception as e:
    print(f"[ERROR] {str(e)[:100]}")

print()

# Check categories
print("=" * 80)
print("CHECKING CATEGORIES")
print("=" * 80)
print()

try:
    categories = models.execute_kw(DB, uid, PASSWORD, 'product.category', 'search', [[]], {})
    print(f"Total Categories: {len(categories)}")
except Exception as e:
    print(f"[ERROR] {str(e)[:100]}")

print()

# Check images in product.image table
print("=" * 80)
print("CHECKING PRODUCT IMAGES")
print("=" * 80)
print()

try:
    images = models.execute_kw(DB, uid, PASSWORD, 'product.image', 'search', [[]], {})
    print(f"Total Product Images: {len(images)}")
except Exception as e:
    print(f"[ERROR] {str(e)[:100]}")

print()
print("=" * 80)
print("DATABASE STATUS SUMMARY")
print("=" * 80)
print()
print(f"  Websites:          {len(websites) if 'websites' in locals() else '?'}")
print(f"  Total Products:    {len(all_products) if 'all_products' in locals() else '?'}")
print(f"  Active Products:   {len(active) if 'active' in locals() else '?'}")
print(f"  Published Products: {len(published) if 'published' in locals() else '?'}")
print(f"  Categories:        {len(categories) if 'categories' in locals() else '?'}")
print(f"  Product Images:    {len(images) if 'images' in locals() else '?'}")
print()

print("=" * 80)
print()
print("NOTE: Database is very clean (most products deleted)")
print("You can now:")
print("  1. Upload new products with images")
print("  2. Use HOMEPAGE_IMAGE_FIX_GUIDE.md for image updates")
print("  3. Or use Python scripts in this folder")
print()
