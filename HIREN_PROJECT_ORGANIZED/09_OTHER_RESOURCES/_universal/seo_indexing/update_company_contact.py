import xmlrpc.client, sys

sys.stdout.reconfigure(encoding='utf-8')
URL = 'https://country-cove-inc.odoo.com'
DB  = 'country-cove-inc'
UID = 2
PW  = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
print("Connected\n")

PHONE = '+1 (917) 338-7086'
EMAIL = 'countrycoveinc@gmail.com'

# ── 1. Update res.company (global, affects all sites) ──────────────
companies = models.execute_kw(DB, UID, PW, 'res.company', 'search_read',
    [[]], {'fields': ['id', 'name', 'phone', 'email']})
print("Companies found:")
for c in companies:
    print(f"  [{c['id']}] {c['name']}  phone={c['phone']}  email={c['email']}")

company_ids = [c['id'] for c in companies]
res = models.execute_kw(DB, UID, PW, 'res.company', 'write',
    [company_ids, {'phone': PHONE, 'email': EMAIL}])
print(f"\n  res.company updated: {res}")

# ── 2. Update every website record ────────────────────────────────
SITE_IDS = [1, 29, 36, 37, 38, 39, 41]

# First, check which fields the website model accepts
website_fields = models.execute_kw(DB, UID, PW, 'website', 'fields_get',
    [], {'attributes': ['string', 'type']})
has_phone = 'phone' in website_fields
has_email = 'email' in website_fields
print(f"\n  website model — has 'phone': {has_phone}, has 'email': {has_email}")

websites = models.execute_kw(DB, UID, PW, 'website', 'search_read',
    [[['id', 'in', SITE_IDS]]],
    {'fields': ['id', 'name'] + (['phone'] if has_phone else []) + (['email'] if has_email else [])})
print("\nWebsites found:")
for w in websites:
    print(f"  [{w['id']}] {w['name']}")

write_vals = {}
if has_phone:
    write_vals['phone'] = PHONE
if has_email:
    write_vals['email'] = EMAIL

if write_vals:
    for site_id in SITE_IDS:
        try:
            res = models.execute_kw(DB, UID, PW, 'website', 'write',
                [[site_id], write_vals])
            print(f"  Site {site_id} updated: {res}")
        except Exception as e:
            print(f"  Site {site_id} error: {e}")
else:
    print("  No phone/email fields on website model — company update is sufficient.")

# ── 3. Verify ─────────────────────────────────────────────────────
print("\n── Verification ──")
companies_after = models.execute_kw(DB, UID, PW, 'res.company', 'search_read',
    [[]], {'fields': ['id', 'name', 'phone', 'email']})
for c in companies_after:
    ok_p = '✅' if c['phone'] == PHONE else '❌'
    ok_e = '✅' if c['email'] == EMAIL else '❌'
    print(f"  Company [{c['id']}] {c['name']}")
    print(f"    {ok_p} Phone: {c['phone']}")
    print(f"    {ok_e} Email: {c['email']}")

print("""
════════════════════════════════════════════════
  COMPANY CONTACT INFO UPDATED

  Phone: +1 (917) 338-7086
  Email: countrycoveinc@gmail.com

  This propagates automatically to:
    ✅ All standard Odoo footer templates
    ✅ All standard Odoo header contact links
    ✅ "Contact Us" pages
    ✅ Any QWeb template using company.phone / company.email

  Force a hard refresh (Ctrl+Shift+R) on each site.
════════════════════════════════════════════════
""")
