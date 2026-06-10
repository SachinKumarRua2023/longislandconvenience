"""
Fix Odoo websites so all stores work on country-cove-inc.odoo.com
- Remove custom domains (so no redirect to unregistered domains)
- Keep only the 8 correct websites, delete duplicates/old ones
- Long Island Convenience keeps its domain (it's live)
"""
import xmlrpc.client

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PASS, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# The 8 correct websites — only Long Island Convenience keeps its domain
KEEP = {
    "Long Island Convenience":        "https://www.longislandconvenience.com",
    "Country Cove Sports and Cards":   False,
    "Country Cove Gift Baskets":       False,
    "Country Cove Gift Cards":         False,
    "Country Cove Game Cards":         False,
    "Country Cove Balloons":           False,
    "Country Cove Greeting Cards":     False,
    "Cyber Consulting":                False,
}

print("\n=== Current websites in Odoo ===")
all_sites = models.execute_kw(DB, uid, PASS, 'website', 'search_read', [[]], {'fields': ['id','name','domain']})
for s in all_sites:
    print(f"  ID {s['id']:2} | {s['name'][:40]:40} | {s['domain']}")

print("\n=== Removing duplicate/old websites ===")
keep_names = list(KEEP.keys())
for site in all_sites:
    if site['name'] not in keep_names:
        try:
            models.execute_kw(DB, uid, PASS, 'website', 'unlink', [[site['id']]])
            print(f"  DELETED: {site['name']} (ID {site['id']})")
        except Exception as e:
            print(f"  Could not delete {site['name']}: {e}")

print("\n=== Clearing domains so all sites load on Odoo subdomain ===")
all_sites = models.execute_kw(DB, uid, PASS, 'website', 'search_read', [[]], {'fields': ['id','name','domain']})
for site in all_sites:
    if site['name'] in KEEP:
        correct_domain = KEEP[site['name']]
        if site['domain'] != correct_domain:
            try:
                models.execute_kw(DB, uid, PASS, 'website', 'write',
                    [[site['id']], {'domain': correct_domain}])
                print(f"  Updated: {site['name']} -> '{correct_domain or '(no domain)'}'")
            except Exception as e:
                print(f"  SKIP {site['name']}: {e}")
        else:
            print(f"  OK: {site['name']} -> '{site['domain'] or '(no domain)'}'")

print("\n=== FINAL WEBSITE LIST ===")
all_sites = models.execute_kw(DB, uid, PASS, 'website', 'search_read', [[]], {'fields': ['id','name','domain']})
for s in all_sites:
    domain_display = s['domain'] if s['domain'] else "(accessible via Odoo backend)"
    print(f"  ID {s['id']:2} | {s['name'][:38]:38} | {domain_display}")
print(f"\nTOTAL: {len(all_sites)} websites")

print("\n=== HOW TO ACCESS EACH STORE (without custom domains) ===")
print("  Go to: https://country-cove-inc.odoo.com/web")
print("  Click 'Website' module -> use the site picker dropdown (top bar)")
print("  Each site ID for direct backend preview:")
for s in all_sites:
    print(f"  ID {s['id']:2} | {s['name']}")
