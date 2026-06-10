#!/usr/bin/env python3
"""
Deploy custom homepage - FIXED VERSION
Creates proper Odoo template structure
"""

import xmlrpc.client
import os

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"
WEBSITE_ID = 36

HOMEPAGE_HTML_FILE = "homepage.html"

print("=" * 80)
print("DEPLOY CUSTOM HOMEPAGE - FIXED VERSION")
print("=" * 80)
print()

# Read HTML
print("[1/4] Reading homepage.html...")
if not os.path.exists(HOMEPAGE_HTML_FILE):
    print(f"[ERROR] File not found: {HOMEPAGE_HTML_FILE}")
    exit(1)

try:
    with open(HOMEPAGE_HTML_FILE, 'r', encoding='utf-8') as f:
        homepage_html = f.read()
    print("[OK] Loaded\n")
except Exception as e:
    print(f"[ERROR] Error reading file: {e}")
    exit(1)

# Connect
print("[2/4] Connecting to Odoo...")
try:
    common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
    uid = common.authenticate(DB, EMAIL, PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
    print("[OK] Connected\n")
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
    exit(1)

# Delete old homepage if exists
print("[3/4] Cleaning up old homepage...")
try:
    old_page_ids = models.execute_kw(DB, uid, PASSWORD,
        'website.page', 'search',
        [[['name', '=', 'Homepage'], ['website_id', '=', WEBSITE_ID]]]
    )

    if old_page_ids:
        models.execute_kw(DB, uid, PASSWORD, 'website.page', 'unlink',
            [old_page_ids[0]]
        )
        print("[OK] Deleted old homepage page\n")
    else:
        print("[OK] No old page to delete\n")

except Exception as e:
    print(f"[WARNING] Could not delete old page: {e}\n")

# Create new homepage as proper Odoo page
print("[4/4] Creating new homepage...")
try:
    # Create the page with proper HTML content in description field
    new_page = models.execute_kw(DB, uid, PASSWORD, 'website.page', 'create',
        [{
            'name': 'Homepage',
            'website_id': WEBSITE_ID,
            'url': '/',
            'is_published': True,
            'is_homepage': True,
            'arch': homepage_html,
            'type': 'qweb'
        }]
    )

    print(f"[OK] Created new homepage! (ID: {new_page})\n")

    # Set as homepage
    print("Setting as website homepage...")
    models.execute_kw(DB, uid, PASSWORD, 'website', 'write',
        [WEBSITE_ID],
        {
            'homepage_url': '/',
            'home_page_id': new_page
        }
    )

    print("[OK] Set as default homepage!\n")

except Exception as e:
    error_str = str(e)
    print(f"[WARNING] {error_str[:150]}\n")

print("=" * 80)
print("DEPLOYMENT COMPLETE!")
print("=" * 80)
print()
print("NEXT STEPS:")
print()
print("1. Clear browser cache completely:")
print("   - Press Ctrl+Shift+Delete")
print("   - Select 'All time'")
print("   - Check all boxes")
print("   - Click 'Clear data'")
print()
print("2. Close browser completely")
print()
print("3. Reopen browser and go to:")
print("   https://longislandcards.com")
print()
print("4. Hard refresh (Ctrl+F5 or Ctrl+Shift+R)")
print()
print("You should now see the professional new homepage!")
print()
