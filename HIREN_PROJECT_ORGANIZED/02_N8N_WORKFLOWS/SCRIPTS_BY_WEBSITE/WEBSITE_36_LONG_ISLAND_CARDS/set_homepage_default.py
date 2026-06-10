#!/usr/bin/env python3
"""
Set the Homepage page as the default homepage for Long Island Cards website
"""

import xmlrpc.client

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"
WEBSITE_ID = 36

print("=" * 80)
print("SET HOMEPAGE AS DEFAULT - Long Island Cards")
print("=" * 80)
print()

# Connect
print("[1/3] Connecting to Odoo...")
try:
    common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common")
    uid = common.authenticate(DB, EMAIL, PASSWORD, {})
    models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object")
    print("[OK] Connected\n")
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
    exit(1)

# Find Homepage page
print("[2/3] Finding Homepage page...")
try:
    page_ids = models.execute_kw(DB, uid, PASSWORD,
        'website.page', 'search',
        [[['name', '=', 'Homepage'], ['website_id', '=', WEBSITE_ID]]]
    )

    if not page_ids:
        print("[ERROR] Homepage page not found!")
        print()
        print("Make sure:")
        print("  1. Homepage page has been created")
        print("  2. It's for the correct website (Long Island Cards - ID 36)")
        exit(1)

    page_id = page_ids[0]
    print(f"[OK] Found Homepage page (ID: {page_id})\n")

except Exception as e:
    print(f"[ERROR] Error finding page: {e}")
    exit(1)

# Set as default homepage
print("[3/3] Setting as default homepage...")
try:
    # Update website to use this page as homepage
    models.execute_kw(DB, uid, PASSWORD, 'website', 'write',
        [WEBSITE_ID],
        {'homepage_url': f'/page/{page_id}/'}
    )

    print("[OK] Homepage set as default!")
    print()
    print("=" * 80)
    print("SUCCESS!")
    print("=" * 80)
    print()
    print("The Homepage page is now set as the default homepage!")
    print()
    print("NEXT STEPS:")
    print("  1. Clear browser cache completely (Ctrl+Shift+Delete)")
    print("  2. Close browser completely")
    print("  3. Reopen browser and go to https://longislandcards.com")
    print("  4. You should see the new professional homepage!")
    print()

except Exception as e:
    print(f"[ERROR] Error setting homepage: {str(e)[:100]}")
    print()
    print("ALTERNATIVE: Set manually in Odoo:")
    print("  1. Go to Odoo admin")
    print("  2. Go to Websites")
    print("  3. Select 'Long Island Cards'")
    print("  4. Set 'Homepage URL' to the Homepage page")
    print("  5. Save")
    print()
