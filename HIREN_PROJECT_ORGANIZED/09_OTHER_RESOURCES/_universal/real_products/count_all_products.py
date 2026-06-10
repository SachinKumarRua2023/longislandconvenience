import xmlrpc.client

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PASS, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# Count ALL products, no filter
total = models.execute_kw(DB, uid, PASS, 'product.template', 'search_count', [[]])
print(f"Total products (all): {total}")

all_p = models.execute_kw(DB, uid, PASS, 'product.template', 'search_read',
    [[]], {'fields': ['id', 'name', 'type', 'sale_ok', 'list_price'], 'limit': 10})
print("Sample:")
for p in all_p:
    print(f"  ID {p['id']:4} | {p['name'][:50]:50} | sale_ok={p['sale_ok']} | type={p['type']}")
