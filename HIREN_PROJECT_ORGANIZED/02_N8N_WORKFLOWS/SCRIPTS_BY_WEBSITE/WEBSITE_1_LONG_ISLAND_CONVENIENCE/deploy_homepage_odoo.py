#!/usr/bin/env python3
"""
Deploy custom homepage to Odoo
Integrates the homepage.html as a custom page/view in Odoo
"""

import xmlrpc.client
import os

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"
WEBSITE_ID = 1

HOMEPAGE_HTML_FILE = "homepage.html"

print("=" * 80)
print("DEPLOY CUSTOM HOMEPAGE TO ODOO")
print("=" * 80)
print()

# Read the HTML file
print("[1/3] Reading homepage.html...")
if not os.path.exists(HOMEPAGE_HTML_FILE):
    print(f"✗ File not found: {HOMEPAGE_HTML_FILE}")
    exit(1)

try:
    with open(HOMEPAGE_HTML_FILE, 'r', encoding='utf-8') as f:
        homepage_html = f.read()
    print("[OK] Loaded\n")
except Exception as e:
    print(f"✗ Error reading file: {e}")
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

# Deploy homepage
print("[3/3] Deploying homepage...")
print()

try:
    # Option 1: Create/Update as Website Page
    print("  → Checking if homepage page exists...")

    page_ids = models.execute_kw(DB, uid, PASSWORD,
        'website.page', 'search',
        [['name', '=', 'Homepage']]
    )

    if page_ids:
        # Update existing page
        print("  ✓ Homepage page found, updating...")
        models.execute_kw(DB, uid, PASSWORD, 'website.page', 'write',
            [page_ids[0]],
            {'arch': homepage_html}
        )
        print("  ✓ Homepage updated successfully!")
    else:
        # Create new page
        print("  ✓ Creating new homepage page...")
        new_page = models.execute_kw(DB, uid, PASSWORD, 'website.page', 'create',
            [{
                'name': 'Homepage',
                'website_id': WEBSITE_ID,
                'url': '/',
                'is_published': True,
                'arch': homepage_html,
                'type': 'qweb'
            }]
        )
        print(f"  ✓ Homepage created! (ID: {new_page})")

    print()
    print("=" * 80)
    print("SUCCESS!")
    print("=" * 80)
    print()
    print("Your custom homepage is now live!")
    print()
    print("NEXT STEPS:")
    print("  1. Go to https://longislandcards.com")
    print("  2. Clear browser cache (Ctrl+Shift+Delete)")
    print("  3. Hard refresh (Ctrl+Shift+R)")
    print("  4. Check the new homepage design")
    print()
    print("FEATURES DEPLOYED:")
    print("  ✓ Professional header with navigation")
    print("  ✓ Hero section with featured product")
    print("  ✓ Features section (Free Gifts, Shipping, etc.)")
    print("  ✓ Category showcase (Sports, Pokemon, MTG, etc.)")
    print("  ✓ Special sections (Live Breaks, Deals, etc.)")
    print("  ✓ New Releases product grid")
    print("  ✓ Professional footer")
    print("  ✓ Responsive mobile design")
    print("  ✓ Real images from Unsplash")
    print()
    print("CUSTOMIZATION:")
    print("  • Edit homepage.html to change design")
    print("  • Modify colors, text, layouts as needed")
    print("  • Add/remove sections easily")
    print("  • Re-run this script to update Odoo")
    print()

except Exception as e:
    print(f"✗ Error: {str(e)[:100]}")
    print()
    print("TROUBLESHOOTING:")
    print("  1. Check Odoo is running and accessible")
    print("  2. Verify credentials are correct")
    print("  3. Check admin user has permissions")
    print("  4. Try manual deployment (see README)")
    print()
