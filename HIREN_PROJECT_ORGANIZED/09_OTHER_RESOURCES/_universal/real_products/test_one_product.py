import xmlrpc.client

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PASS, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
print(f"Connected as UID {uid}")

# Test 1: minimal product — just name
print("\nTest 1: name only...")
try:
    pid = models.execute_kw(DB, uid, PASS, 'product.template', 'create', [{'name': 'Test Product A'}])
    print(f"  OK — ID {pid}")
    models.execute_kw(DB, uid, PASS, 'product.template', 'unlink', [[pid]])
except Exception as e:
    print(f"  FAILED: {str(e)[:300]}")

# Test 2: name + price
print("\nTest 2: name + price...")
try:
    pid = models.execute_kw(DB, uid, PASS, 'product.template', 'create',
        [{'name': 'Test Product B', 'list_price': 9.99}])
    print(f"  OK — ID {pid}")
    models.execute_kw(DB, uid, PASS, 'product.template', 'unlink', [[pid]])
except Exception as e:
    print(f"  FAILED: {str(e)[:300]}")

# Test 3: with type=service
print("\nTest 3: type=service...")
try:
    pid = models.execute_kw(DB, uid, PASS, 'product.template', 'create',
        [{'name': 'Test Product C', 'list_price': 9.99, 'type': 'service', 'sale_ok': True}])
    print(f"  OK — ID {pid}")
    models.execute_kw(DB, uid, PASS, 'product.template', 'unlink', [[pid]])
except Exception as e:
    print(f"  FAILED: {str(e)[:300]}")

# Test 4: check what fields are available
print("\nTest 4: check product fields...")
try:
    fields = models.execute_kw(DB, uid, PASS, 'product.template', 'fields_get',
        [], {'attributes': ['string', 'type', 'required']})
    important = ['name', 'type', 'list_price', 'sale_ok', 'categ_id', 'description']
    for f in important:
        if f in fields:
            print(f"  {f}: type={fields[f]['type']} required={fields[f].get('required', False)}")
    # Check valid type values
    if 'type' in fields:
        print(f"  type selection values:", fields['type'].get('selection', 'N/A'))
except Exception as e:
    print(f"  FAILED: {str(e)[:200]}")
