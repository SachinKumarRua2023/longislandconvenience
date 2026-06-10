#!/usr/bin/env python3
import xmlrpc.client, sys
sys.stdout.reconfigure(encoding="utf-8")

ODOO = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"
SITE = 39

common = xmlrpc.client.ServerProxy(f'{ODOO}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{ODOO}/xmlrpc/2/object')
def xc(model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

# Get ALL published products for website 39
products = xc("product.template", "search_read",
    [[["website_published", "=", True], ["website_id", "=", SITE]]],
    {"fields": ["id", "name", "list_price", "website_published"], "limit": 100})

print(f"Published products on website {SITE}: {len(products)}")
for p in products:
    print(f"  ID={p['id']} | ${p['list_price']:.2f} | {p['name']}")

# Also check without website filter - maybe website_id is null
print("\n--- Products with no website_id (global) ---")
products2 = xc("product.template", "search_read",
    [[["website_published", "=", True], ["website_id", "=", False]]],
    {"fields": ["id", "name", "list_price"], "limit": 100})
for p in products2:
    print(f"  ID={p['id']} | ${p['list_price']:.2f} | {p['name']}")

# Also get ALL products available to site 39 (published, any website_id)
print("\n--- ALL published products visible on site (website_id=39 OR null) ---")
products3 = xc("product.template", "search_read",
    [[["website_published", "=", True], "|", ["website_id", "=", SITE], ["website_id", "=", False]]],
    {"fields": ["id", "name", "list_price", "website_id"], "limit": 100})
for p in products3:
    wid = p["website_id"][0] if p["website_id"] else "global"
    print(f"  ID={p['id']} | site={wid} | ${p['list_price']:.2f} | {p['name']}")
