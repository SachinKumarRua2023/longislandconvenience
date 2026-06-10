import xmlrpc.client

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PASS, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

SITES = [
    ("Long Island Convenience",        "https://www.longislandconvenience.com"),
    ("Country Cove Sports and Cards",   "https://countrycovesportscards.com"),
    ("Country Cove Gift Baskets",       "https://countrycovegiftbaskets.com"),
    ("Country Cove Gift Cards",         "https://countrycovegiftcards.com"),
    ("Country Cove Game Cards",         "https://countrycovegamecards.com"),
    ("Country Cove Balloons",           "https://countrycoveballoons.com"),
    ("Country Cove Greeting Cards",     "https://countrycovecards.com"),
    ("Cyber Consulting",                "https://www.consultcyber.net"),
]

# First clean up any old/wrong names
all_sites = models.execute_kw(DB, uid, PASS, 'website', 'search_read', [[]], {'fields': ['id','name']})
keep_names = [s[0] for s in SITES]
for site in all_sites:
    if site['name'] not in keep_names:
        try:
            models.execute_kw(DB, uid, PASS, 'website', 'unlink', [[site['id']]])
            print(f"Removed: {site['name']} (ID {site['id']})")
        except Exception as e:
            print(f"Could not remove {site['name']}: {e}")

# Create missing websites
for name, domain in SITES:
    existing = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
        [[['name', '=', name]]], {'fields': ['id']})
    if existing:
        wid = existing[0]['id']
        models.execute_kw(DB, uid, PASS, 'website', 'write', [[wid], {'domain': domain}])
        print(f"EXISTS  : {name} (ID {wid})")
    else:
        wid = models.execute_kw(DB, uid, PASS, 'website', 'create',
            [{'name': name, 'domain': domain}])
        print(f"CREATED : {name} (ID {wid})")

# Final list
print("\n--- FINAL WEBSITE LIST ---")
all_sites = models.execute_kw(DB, uid, PASS, 'website', 'search_read', [[]], {'fields': ['id','name','domain']})
for s in all_sites:
    print(f"  ID {s['id']:2} | {s['name']:40} | {s['domain']}")
print(f"\nTOTAL: {len(all_sites)} websites")
