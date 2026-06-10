import xmlrpc.client, urllib.request

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

FILENAME = 'google7eab7c6a696479f4.html'
TOKEN_LINE = 'google-site-verification: google7eab7c6a696479f4.html'

# Fix: update view to output ONLY the verification text (no HTML wrapper)
# When a QWeb template doesn't call any layout, it renders just its content
view_arch = '<t t-name="website.google_verification_page">' + TOKEN_LINE + '</t>'

existing = xc('ir.ui.view', 'search_read',
    [[['key', '=', 'website.google_verification_page']]],
    {'fields': ['id']})
if existing:
    view_id = existing[0]['id']
    xc('ir.ui.view', 'write', [[view_id], {'arch_db': view_arch}])
    print(f'Updated view {view_id} — now outputs only: {TOKEN_LINE}')
else:
    print('ERROR: view not found')

# Also ensure the page URL is set to /google7eab7c6a696479f4.html directly
# (redirect_type '0' = URL rewrite, not HTTP redirect)
pages = xc('website.page', 'search_read',
    [[['view_id.key', '=', 'website.google_verification_page']]],
    {'fields': ['id', 'url']})
print(f'Page: {pages}')

# Check if redirect is set up
redirects = xc('website.rewrite', 'search_read',
    [[['url_from', '=', f'/{FILENAME}']]],
    {'fields': ['id', 'url_from', 'url_to', 'redirect_type']})
print(f'Redirects: {redirects}')

import time
print('\nWaiting 5 seconds for cache clear...')
time.sleep(5)

# Test both www and non-www
test_urls = [
    f'https://www.longislandconvenience.com/{FILENAME}',
    f'https://www.longislandconvenience.com/google7eab7c6a696479f4',
    f'https://longislandconvenience.com/{FILENAME}',
]
for test_url in test_urls:
    print(f'\nFetching {test_url} ...')
    try:
        req = urllib.request.Request(test_url, headers={'User-Agent': 'Googlebot/2.1'})
        with urllib.request.urlopen(req, timeout=12) as resp:
            body = resp.read(300).decode('utf-8', errors='replace')
            print(f'  HTTP {resp.status}')
            print(f'  First 100 chars: {repr(body[:100])}')
            starts_correct = body.strip().startswith('google-site-verification')
            print(f'  Starts with verification string: {starts_correct}')
    except urllib.error.HTTPError as e:
        print(f'  HTTP {e.code}: {e.reason}')
    except Exception as e:
        print(f'  Error: {type(e).__name__}: {e}')
