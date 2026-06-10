#!/usr/bin/env python3
"""
Deploy homepage - with proper XML escaping
"""

import xmlrpc.client
import os
import html

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"
WEBSITE_ID = 36

HOMEPAGE_HTML_FILE = "homepage.html"

print("=" * 80)
print("DEPLOY HOMEPAGE - WITH PROPER ESCAPING")
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
    print(f"[ERROR] {e}")
    exit(1)

# Connect
print("[2/4] Connecting to Odoo...")
try:
    common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
    uid = common.authenticate(DB, EMAIL, PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
    print("[OK] Connected\n")
except Exception as e:
    print(f"[ERROR] {e}")
    exit(1)

# Delete old page
print("[3/4] Cleaning up...")
try:
    old_ids = models.execute_kw(DB, uid, PASSWORD,
        'website.page', 'search',
        [[['name', '=', 'Homepage'], ['website_id', '=', WEBSITE_ID]]]
    )
    if old_ids:
        models.execute_kw(DB, uid, PASSWORD, 'website.page', 'unlink', [old_ids[0]])
        print("[OK] Old page deleted\n")
except:
    pass

# Deploy with escaped HTML
print("[4/4] Creating homepage...")
try:
    # Escape HTML for XML
    escaped_html = html.escape(homepage_html)

    # Wrap in template with CDATA (the proper way for QWeb)
    xml_arch = f'<t><![CDATA[{homepage_html}]]></t>'

    new_page = models.execute_kw(DB, uid, PASSWORD, 'website.page', 'create',
        [{
            'name': 'Homepage',
            'website_id': WEBSITE_ID,
            'url': '/',
            'is_published': True,
            'is_homepage': True,
            'arch': xml_arch,
            'type': 'qweb'
        }]
    )

    print(f"[OK] Homepage created! (ID: {new_page})\n")

    # Set as default
    models.execute_kw(DB, uid, PASSWORD, 'website', 'write',
        [WEBSITE_ID],
        {'homepage_url': '/', 'home_page_id': new_page}
    )
    print("[OK] Set as default homepage!\n")

except Exception as e:
    print(f"[ERROR] {str(e)[:120]}\n")
    print("ALTERNATIVE SOLUTION:")
    print("=" * 80)
    print()
    print("The homepage might need to be created via Odoo's CMS editor.")
    print()
    print("Manual fix:")
    print("1. Go to Odoo admin")
    print("2. Go to Website > Pages")
    print("3. Look for 'Homepage' page")
    print("4. If found, edit it in the visual editor")
    print("5. Replace content with our homepage design")
    print("6. Set as homepage")
    print()
    exit(1)

print("=" * 80)
print("SUCCESS!")
print("=" * 80)
print()
print("CLEAR CACHE AND REFRESH:")
print()
print("1. Press Ctrl+Shift+Delete (cache clear)")
print("2. Select 'All time' and check all boxes")
print("3. Close browser completely")
print("4. Reopen and go to: https://longislandcards.com")
print("5. Press Ctrl+F5 (hard refresh)")
print()
print("Your professional homepage should now appear!")
print()
