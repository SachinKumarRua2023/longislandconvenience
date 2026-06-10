import xmlrpc.client

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

# Set domains in Odoo for both websites
configs = [
    (37, 'https://www.ligiftbasket.com',           'Long Island Gift Basket'),
    (38, 'https://www.longislandballoonsdecor.com', 'Long Island Balloons'),
]

for wid, domain, name in configs:
    xc('website', 'write', [[wid], {'domain': domain}])
    site = xc('website', 'search_read', [[['id','=',wid]]], {'fields':['id','name','domain']})[0]
    print(f"Set: {name} (ID {wid}) -> {site['domain']}")

print('\nOdoo domain config done. Now do the DNS steps below.')
