import xmlrpc.client

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PASS, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# Count all products
all_prods = models.execute_kw(DB, uid, PASS, 'product.template', 'search_read',
    [[['sale_ok', '=', True]]], {'fields': ['id', 'name', 'categ_id', 'list_price'], 'limit': 500})

print(f"Total sale products in Odoo: {len(all_prods)}")
print("\nFirst 10 products:")
for p in all_prods[:10]:
    print(f"  ID {p['id']:4} | {p['name'][:55]:55} | ${p['list_price']}")

# Group by category
from collections import Counter
categs = Counter(p['categ_id'][1] if p['categ_id'] else 'None' for p in all_prods)
print(f"\nProducts by category (top 20):")
for cat, count in categs.most_common(20):
    print(f"  {count:3}x  {cat}")

# Check website menu pages
print("\nWebsite pages (IR menu / website.page):")
try:
    pages = models.execute_kw(DB, uid, PASS, 'website.page', 'search_read',
        [[]], {'fields': ['id', 'name', 'url', 'website_id', 'is_published'], 'limit': 20})
    for pg in pages:
        print(f"  {pg['url']:40} | published={pg['is_published']} | site={pg.get('website_id')}")
except Exception as e:
    print(f"  Could not fetch pages: {e}")
