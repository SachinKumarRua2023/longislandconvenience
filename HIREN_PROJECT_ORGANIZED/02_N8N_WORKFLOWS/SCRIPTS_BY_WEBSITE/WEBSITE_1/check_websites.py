#!/usr/bin/env python3
"""
Check all websites in Odoo and find Long Island Cards website ID
"""

import xmlrpc.client

URL = "https://country-cove-inc.odoo.com"
DB = "country-cove-inc"
EMAIL = "countrycoveinc@gmail.com"
PASSWORD = "M@nhattan1234"

print("=" * 80)
print("ODOO WEBSITES - Check Configuration")
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

# Get all websites
print("[2/2] Fetching all websites...\n")

try:
    website_ids = models.execute_kw(DB, uid, PASSWORD,
        'website', 'search',
        [[]],
        {'order': 'id asc'}
    )

    if not website_ids:
        print("✗ No websites found in Odoo")
        exit(1)

    websites = models.execute_kw(DB, uid, PASSWORD,
        'website', 'read',
        [website_ids, ['id', 'name', 'domain']]
    )

    print("=" * 80)
    print("WEBSITES IN ODOO")
    print("=" * 80)
    print()

    for website in websites:
        website_id = website['id']
        name = website['name']
        domain = website['domain'] if website['domain'] else 'N/A'

        print(f"Website ID: {website_id}")
        print(f"  Name: {name}")
        print(f"  Domain: {domain}")
        print()

    print("=" * 80)
    print("INSTRUCTIONS")
    print("=" * 80)
    print()
    print("1. Find your website in the list above")
    print("2. Note the Website ID number")
    print("3. Update deploy_homepage_odoo.py with correct WEBSITE_ID")
    print()
    print("Example:")
    print("  If 'Long Island Cards' has ID 2, change:")
    print("  WEBSITE_ID = 1  →  WEBSITE_ID = 2")
    print()
    print("Then run:")
    print("  python deploy_homepage_odoo.py")
    print()

except Exception as e:
    print(f"✗ Error: {str(e)[:100]}")
    exit(1)
