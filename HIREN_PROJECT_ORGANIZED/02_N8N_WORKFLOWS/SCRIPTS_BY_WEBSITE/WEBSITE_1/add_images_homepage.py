#!/usr/bin/env python3
"""
WEBSITE 1 - Long Island Cards: Update Homepage Category Images
Fetches free card images from Unsplash for homepage categories:
Sports, Pokemon, MTG, Yu-Gi-Oh!, Graded
"""

import xmlrpc.client
import requests
import base64

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

UNSPLASH_API = "https://api.unsplash.com"
UNSPLASH_SEARCH = f"{UNSPLASH_API}/search/photos"

print("=" * 80)
print("LONG ISLAND CARDS - Update Homepage Categories")
print("=" * 80)
print()

# Connect to Odoo
print("[1/2] Connecting to Odoo...")
try:
    common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
    uid = common.authenticate(DB, EMAIL, PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
    print("[OK] Connected\n")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# ============================================================================
# HELPER: Fetch and convert images
# ============================================================================

def get_unsplash_image(query):
    """Fetch a free image from Unsplash by search query"""
    try:
        params = {
            'query': query,
            'page': 1,
            'per_page': 1,
            'order_by': 'relevant'
        }
        response = requests.get(UNSPLASH_SEARCH, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data['results']:
            return data['results'][0]['urls']['regular']
        return None
    except Exception as e:
        return None

def image_url_to_base64(image_url):
    """Download image from URL and convert to base64"""
    try:
        response = requests.get(image_url, timeout=15)
        response.raise_for_status()
        return base64.b64encode(response.content).decode()
    except Exception as e:
        return None

# ============================================================================
# Update Homepage Categories
# ============================================================================

print("[2/2] Updating Homepage Categories...\n")

homepage_categories = [
    {'name': 'Sports', 'keyword': 'baseball basketball football hockey cards'},
    {'name': 'Pokemon', 'keyword': 'pokemon trading cards collection'},
    {'name': 'MTG', 'keyword': 'magic the gathering cards'},
    {'name': 'Yu-Gi-Oh!', 'keyword': 'yugioh trading cards'},
    {'name': 'Graded', 'keyword': 'graded trading cards PSA BGS'}
]

updated = 0

for cat in homepage_categories:
    cat_name = cat['name']
    keyword = cat['keyword']

    print(f"  → {cat_name}...", end=" ", flush=True)

    # Get image from Unsplash
    image_url = get_unsplash_image(keyword)

    if not image_url:
        print("✗ No image found")
        continue

    # Download and convert
    image_data = image_url_to_base64(image_url)

    if not image_data:
        print("✗ Download failed")
        continue

    try:
        # Find category by exact name
        cat_ids = models.execute_kw(DB, uid, PASSWORD,
            'product.category', 'search',
            [['name', '=', cat_name]]
        )

        if not cat_ids:
            print(f"⚠ Not found in Odoo")
            continue

        # SECURITY: Only write image data to image_128 field - no code execution
        models.execute_kw(DB, uid, PASSWORD, 'product.category', 'write',
            [cat_ids[0]],
            {'image_128': image_data}  # Binary image data only
        )

        photo_id = image_url.split('/')[-1][:15]
        print(f"✓ ({photo_id}...)")
        updated += 1

    except Exception as e:
        print(f"✗ Odoo error: {str(e)[:40]}")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Homepage Categories Updated: {updated}/5")
print()

if updated == 5:
    print("✓ All homepage categories updated successfully!")
elif updated > 0:
    print(f"⚠ {updated}/5 categories updated. Check category names in Odoo.")
else:
    print("✗ No categories updated. Check Odoo connection and category names.")

print()
print("NEXT STEPS:")
print("  1. Go to https://longislandcards.com")
print("  2. Clear browser cache (Ctrl+Shift+Delete)")
print("  3. Hard refresh (Ctrl+Shift+R)")
print("  4. Check if homepage category images appear")
print()
