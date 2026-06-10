"""
CLEAN SETUP — Country Cove Inc / Long Island Convenience
Delete all duplicate/messy websites, recreate exactly the right set.
One website per domain. No duplicates. Clean names.
"""
import xmlrpc.client

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PASS, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# ── THE ONE TRUE WEBSITE LIST ────────────────────────────────
# name, domain, registrar_email, registrar
FINAL = [
    ("Long Island Convenience",    "https://www.longislandconvenience.com",    "GoDaddy (old account)"),
    ("Long Island Cards",          "https://www.longislandcards.com",           "kahpk1933@gmail.com / IONOS"),
    ("LI Gift Basket",             "https://www.ligiftbasket.com",              "parulhc@gmail.com / IONOS"),
    ("Long Island Balloons",       "https://www.longislandballoonsdecor.com",   "countrycoveinc@gmail.com / Hostinger"),
    ("Long Island Print & Mail",   "https://www.longislandprintandmail.com",    "kahpk1933@gmail.com / IONOS"),
    ("Cyber Consulting",           "https://www.consultcyber.net",              "GoDaddy (consultcyber10@gmail.com)"),
    ("Country Cove Greeting Cards","",                                           "No domain yet"),
    ("Country Cove Gift Cards",    "",                                           "No domain yet"),
    ("Country Cove Cigars",        "",                                           "No domain yet"),
    ("Country Cove Lotto",         "",                                           "No domain yet"),
]

final_names = [f[0] for f in FINAL]

print("=" * 60)
print("  STEP 1: Current websites in Odoo")
print("=" * 60)
all_sites = models.execute_kw(DB, uid, PASS, 'website', 'search_read', [[]], {'fields': ['id','name','domain']})
for s in all_sites:
    marker = "KEEP" if s['name'] in final_names else "DELETE"
    print(f"  [{marker}] ID {s['id']:2} | {s['name'][:40]:40} | {s['domain'] or ''}")

print("\n" + "=" * 60)
print("  STEP 2: Deleting duplicate / wrong-named websites")
print("=" * 60)
for s in all_sites:
    if s['name'] not in final_names:
        try:
            models.execute_kw(DB, uid, PASS, 'website', 'unlink', [[s['id']]])
            print(f"  DELETED: {s['name']} (ID {s['id']})")
        except Exception as e:
            print(f"  SKIP (in use): {s['name']} (ID {s['id']}) — {str(e)[:80]}")

print("\n" + "=" * 60)
print("  STEP 3: Ensuring all final websites exist with correct names/domains")
print("=" * 60)
for name, domain, registrar in FINAL:
    existing = models.execute_kw(DB, uid, PASS, 'website', 'search_read',
        [[['name', '=', name]]], {'fields': ['id', 'domain']})

    domain_val = domain if domain else False

    if existing:
        wid = existing[0]['id']
        if existing[0]['domain'] != domain_val:
            models.execute_kw(DB, uid, PASS, 'website', 'write',
                [[wid], {'domain': domain_val}])
            print(f"  UPDATED: {name} (ID {wid}) -> {domain or 'no domain'}")
        else:
            print(f"  OK:      {name} (ID {wid}) -> {domain or 'no domain'}")
    else:
        vals = {'name': name}
        if domain_val:
            vals['domain'] = domain_val
        wid = models.execute_kw(DB, uid, PASS, 'website', 'create', [vals])
        print(f"  CREATED: {name} (ID {wid}) -> {domain or 'no domain'}")

print("\n" + "=" * 60)
print("  FINAL CLEAN WEBSITE LIST")
print("=" * 60)
all_sites = models.execute_kw(DB, uid, PASS, 'website', 'search_read', [[]], {'fields': ['id','name','domain']})
for s in all_sites:
    domain_display = s['domain'] if s['domain'] else '(no domain yet)'
    print(f"  ID {s['id']:2} | {s['name']:35} | {domain_display}")
print(f"\n  TOTAL: {len(all_sites)} websites")

print("\n" + "=" * 60)
print("  EMAIL -> DOMAIN MAPPING (for DNS setup)")
print("=" * 60)
print("  GoDaddy (old acct)              | longislandconvenience.com  LIVE")
print("  kahpk1933@gmail.com  / IONOS    | longislandcards.com        DNS: pending")
print("  kahpk1933@gmail.com  / IONOS    | longislandprintandmail.com DNS: pending")
print("  parulhc@gmail.com    / IONOS    | ligiftbasket.com           DNS: pending")
print("  countrycoveinc@gmail / Hostinger| longislandballoonsdecor.com DNS: pending")
print("  consultcyber10@gmail / GoDaddy  | consultcyber.net           EXPIRES Jun 6!")
