#!/usr/bin/env python3
"""
WEBSITE 1 - Long Island Cards: Update Homepage Category Images (Config-based)
Reads from homepage_config.json for easy customization
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

CONFIG_FILE = "homepage_config.json"
UNSPLASH_API = "https://api.unsplash.com"
UNSPLASH_SEARCH = f"{UNSPLASH_API}/search/photos"

print("=" * 80)
print("LONG ISLAND CARDS - Update Homepage Categories (Config-based)")
print("=" * 80)
print()

# Load config
print("[1/3] Loading configuration...")
if not os.path.exists(CONFIG_FILE):
    print(f"✗ Config file not found: {CONFIG_FILE}")
    exit(1)

try:
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    categories = config.get('homepage_categories', [])
    settings = config.get('settings', {})
    print(f"✓ Loaded {len(categories)} categories\n")
except Exception as e:
    print(f"✗ Error loading config: {e}")
    exit(1)

# Connect to Odoo
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
# HELPER: Fetch and convert images
# ============================================================================

def get_unsplash_image(query):
    """Fetch a free image from Unsplash by search query"""
    try:
        timeout = settings.get('api_fetch_timeout', 10)
        params = {
            'query': query,
            'page': 1,
            'per_page': 1,
            'order_by': 'relevant'
        }
        response = requests.get(UNSPLASH_SEARCH, params=params, timeout=timeout)
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
        timeout = settings.get('image_download_timeout', 15)
        response = requests.get(image_url, timeout=timeout)
        response.raise_for_status()
        return base64.b64encode(response.content).decode()
    except Exception as e:
        return None

# ============================================================================
# Update Homepage Categories
# ============================================================================

print("[3/3] Updating Homepage Categories...\n")

updated = 0
skipped = 0

for cat in categories:
    cat_name = cat.get('name')
    keyword = cat.get('keyword')
    enabled = cat.get('enabled', True)

    if not enabled:
        print(f"  ⊘ {cat_name} (disabled)")
        skipped += 1
        continue

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
print(f"Categories Updated: {updated}/{len(categories)}")
if skipped > 0:
    print(f"Categories Skipped: {skipped} (disabled in config)")
print()

if updated == len(categories):
    print("✓ All homepage categories updated successfully!")
elif updated > 0:
    print(f"⚠ {updated}/{len(categories)} updated. Check category names in Odoo.")
else:
    print("✗ No categories updated. Check Odoo connection.")

print()
print("NEXT STEPS:")
print("  1. Go to https://longislandcards.com")
print("  2. Clear browser cache (Ctrl+Shift+Delete)")
print("  3. Hard refresh (Ctrl+Shift+R)")
print("  4. Verify homepage category images appear")
print()
print("TO CUSTOMIZE:")
print("  • Edit homepage_config.json to change search keywords")
print("  • Set 'enabled': false to skip a category")
print("  • No Python editing needed!")
print()
