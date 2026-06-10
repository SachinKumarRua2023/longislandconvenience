import xmlrpc.client, base64, requests

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PASS, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# Test category creation
print("Test: create category...")
try:
    cid = models.execute_kw(DB, uid, PASS, 'product.category', 'create', [{'name': 'Test Root Cat'}])
    print(f"  Root cat OK: ID {cid}")
    cid2 = models.execute_kw(DB, uid, PASS, 'product.category', 'create',
        [{'name': 'Test Child Cat', 'parent_id': cid}])
    print(f"  Child cat OK: ID {cid2}")
except Exception as e:
    print(f"  FAILED: {str(e)[:300]}")
    cid2 = None

# Test product with categ_id
if cid2:
    print("\nTest: product with categ_id...")
    try:
        pid = models.execute_kw(DB, uid, PASS, 'product.template', 'create',
            [{'name': 'Test With Categ', 'list_price': 9.99, 'categ_id': cid2,
              'type': 'service', 'sale_ok': True}])
        print(f"  OK: ID {pid}")
        models.execute_kw(DB, uid, PASS, 'product.template', 'unlink', [[pid]])
    except Exception as e:
        print(f"  FAILED: {str(e)[:400]}")

# Test product with small image
print("\nTest: product with image...")
try:
    r = requests.get("https://loremflickr.com/400/400/baseball,card", timeout=15, allow_redirects=True)
    img_b64 = base64.b64encode(r.content).decode('utf-8')
    print(f"  Image size: {len(img_b64)} chars")
    pid = models.execute_kw(DB, uid, PASS, 'product.template', 'create',
        [{'name': 'Test With Image', 'list_price': 9.99, 'type': 'service',
          'sale_ok': True, 'image_1920': img_b64}])
    print(f"  OK: ID {pid}")
    models.execute_kw(DB, uid, PASS, 'product.template', 'unlink', [[pid]])
except Exception as e:
    print(f"  FAILED: {str(e)[:400]}")

# Cleanup test categories
try:
    models.execute_kw(DB, uid, PASS, 'product.category', 'unlink', [[cid, cid2]])
    print("\nTest categories cleaned up.")
except:
    pass
