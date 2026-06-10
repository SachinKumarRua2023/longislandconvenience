#!/usr/bin/env python3
"""
WEBSITE 1 - Long Island Cards: Add category images from Unsplash (free stock photos)
Dynamically fetches copyright-free images for each card category
"""

import xmlrpc.client
import requests
import base64

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"
WEBSITE_ID = 1

# Unsplash API (no key required for basic usage)
UNSPLASH_API = "https://api.unsplash.com"
UNSPLASH_SEARCH = f"{UNSPLASH_API}/search/photos"

print("=" * 80)
print("WEBSITE 1 - Long Island Cards: Add Category Images")
print("=" * 80)
print()

# Connect
print("[1/2] Connecting to Odoo...")
common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
uid = common.authenticate(DB, EMAIL, PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
print("[OK] Connected\n")

# ============================================================================
# HELPER: Fetch image from Unsplash and convert to base64
# ============================================================================

def get_unsplash_image(query, page=1):
    """Fetch a free image from Unsplash by search query"""
    try:
        params = {
            'query': query,
            'page': page,
            'per_page': 1,
            'order_by': 'relevant'
        }
        response = requests.get(UNSPLASH_SEARCH, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data['results']:
            image_url = data['results'][0]['urls']['regular']
            return image_url
        return None
    except Exception as e:
        print(f"    ⚠ Could not fetch from Unsplash: {str(e)[:60]}")
        return None

def image_url_to_base64(image_url):
    """Download image from URL and convert to base64"""
    try:
        response = requests.get(image_url, timeout=15)
        response.raise_for_status()
        image_base64 = base64.b64encode(response.content).decode()
        return image_base64
    except Exception as e:
        print(f"    ⚠ Could not download image: {str(e)[:60]}")
        return None


# ============================================================================
# STEP 2: Add Category Images (from Unsplash)
# ============================================================================

print("[2/2] Adding Category Images from Unsplash...")

# Long Island Cards categories with Unsplash search keywords
category_images = [
    {'category_name': 'Baseball', 'search_keyword': 'baseball card collection'},
    {'category_name': 'Basketball', 'search_keyword': 'basketball card'},
    {'category_name': 'Football', 'search_keyword': 'football sports card'},
    {'category_name': 'Hockey', 'search_keyword': 'hockey trading card'},
    {'category_name': 'Soccer', 'search_keyword': 'soccer card sport'},
    {'category_name': 'Gaming', 'search_keyword': 'gaming card collection'},
    {'category_name': 'Racing', 'search_keyword': 'racing card motorsport'},
    {'category_name': 'Entertainment', 'search_keyword': 'entertainment trading cards'},
    {'category_name': 'Vintage', 'search_keyword': 'vintage collectible cards'},
    {'category_name': 'Singles', 'search_keyword': 'individual cards collection'},
    {'category_name': 'Live Box Breaks', 'search_keyword': 'box break opening cards'},
    {'category_name': 'Reed Buys', 'search_keyword': 'buying cards high value'},
    {'category_name': 'Daily Deals', 'search_keyword': 'special deals discount'},
    {'category_name': 'Best Deals List', 'search_keyword': 'best price offers'},
    {'category_name': 'Hit Parade', 'search_keyword': 'graded card collection rare'}
]

categories_updated = 0

for item in category_images:
    category_name = item['category_name']
    search_keyword = item['search_keyword']

    print(f"  → {category_name}...", end=" ", flush=True)

    # Fetch image from Unsplash
    image_url = get_unsplash_image(search_keyword)

    if image_url:
        # Download and convert to base64
        image_data = image_url_to_base64(image_url)

        if image_data:
            try:
                # Find category by name and update
                category_ids = models.execute_kw(DB, uid, PASSWORD,
                    'product.category', 'search',
                    [['name', '=', category_name]]
                )

                if category_ids:
                    # SECURITY: Only write image data to image_128 field - no code execution
                    models.execute_kw(DB, uid, PASSWORD, 'product.category', 'write',
                        [category_ids[0]],
                        {'image_128': image_data}  # Binary image data only
                    )
                    print(f"✓ ({image_url.split('/')[-1][:20]}...)")
                    categories_updated += 1
                else:
                    print(f"⚠ Category not found in Odoo")

            except Exception as e:
                print(f"✗ Error updating Odoo: {str(e)[:50]}")
        else:
            print(f"✗ Could not download image")
    else:
        print(f"✗ No image found on Unsplash")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Category Images:   {categories_updated}/{len(category_images)} added")
print()
print("NEXT STEPS:")
print("  1. Check website: https://longislandcards.com")
print("  2. Verify images appear on category pages")
print("  3. Test on mobile view")
print()
print("IMAGE SOURCES:")
print("  • All images from Unsplash (free stock photos)")
print("  • No copyright restrictions")
print("  • Auto-refreshes when script runs again")
print()
