#!/usr/bin/env python3
"""
WEBSITE 1 - Long Island Cards: Add category images from Unsplash (free stock photos)
Dynamically fetches copyright-free images for each card category
Uses JSON config file for easy customization
"""

import xmlrpc.client
import requests
import base64
import json
import os

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"
WEBSITE_ID = 1

# Load configuration from JSON file
CONFIG_FILE = "category_config.json"
UNSPLASH_API = "https://api.unsplash.com"
UNSPLASH_SEARCH = f"{UNSPLASH_API}/search/photos"

print("=" * 80)
print("WEBSITE 1 - Long Island Cards: Add Category Images")
print("=" * 80)
print()

# Load config
print("[1/3] Loading configuration...")
if not os.path.exists(CONFIG_FILE):
    print(f"✗ Configuration file not found: {CONFIG_FILE}")
    print("   Please ensure category_config.json exists in the same directory")
    exit(1)

try:
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    categories = config.get('categories', [])
    settings = config.get('settings', {})
    print(f"✓ Loaded {len(categories)} categories\n")
except Exception as e:
    print(f"✗ Error loading config: {e}")
    exit(1)

# Connect
print("[2/3] Connecting to Odoo...")
try:
    common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
    uid = common.authenticate(DB, EMAIL, PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
    print("[OK] Connected\n")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit(1)

# ============================================================================
# HELPER: Fetch image from Unsplash and convert to base64
# ============================================================================

def get_unsplash_image(query, page=1):
    """Fetch a free image from Unsplash by search query"""
    try:
        timeout = settings.get('api_fetch_timeout', 10)
        params = {
            'query': query,
            'page': page,
            'per_page': 1,
            'order_by': 'relevant'
        }
        response = requests.get(UNSPLASH_SEARCH, params=params, timeout=timeout)
        response.raise_for_status()

        data = response.json()
        if data['results']:
            image_url = data['results'][0]['urls']['regular']
            return image_url
        return None
    except Exception as e:
        return None

def image_url_to_base64(image_url):
    """Download image from URL and convert to base64"""
    try:
        timeout = settings.get('image_download_timeout', 15)
        response = requests.get(image_url, timeout=timeout)
        response.raise_for_status()
        image_base64 = base64.b64encode(response.content).decode()
        return image_base64
    except Exception as e:
        return None

# ============================================================================
# STEP 3: Add Category Images (from Unsplash)
# ============================================================================

print("[3/3] Adding Category Images from Unsplash...")

categories_updated = 0
categories_skipped = 0

for item in categories:
    category_name = item.get('name')
    search_keyword = item.get('search_keyword')
    enabled = item.get('enabled', True)

    if not enabled:
        print(f"  ⊘ {category_name} (disabled)")
        categories_skipped += 1
        continue

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
                    # Field name is hardcoded (not configurable) to prevent injection attacks
                    models.execute_kw(DB, uid, PASSWORD, 'product.category', 'write',
                        [category_ids[0]],
                        {'image_128': image_data}  # Binary image data only
                    )
                    photo_id = image_url.split('/')[-1][:20]
                    print(f"✓ ({photo_id}...)")
                    categories_updated += 1
                else:
                    print(f"⚠ Not found in Odoo")

            except Exception as e:
                print(f"✗ Odoo error: {str(e)[:40]}")
        else:
            print(f"✗ Download failed")
    else:
        print(f"✗ Not found on Unsplash")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Category Images:   {categories_updated}/{len(categories)} added")
if categories_skipped > 0:
    print(f"Categories Skipped: {categories_skipped} (disabled in config)")
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
print("TO CUSTOMIZE:")
print("  • Edit category_config.json to change search keywords")
print("  • Set 'enabled': false to skip categories")
print("  • No Python editing needed!")
print()
