import xmlrpc.client, urllib.request, base64, os

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

FILENAME = 'google7eab7c6a696479f4.html'
FILE_CONTENT = b'google-site-verification: google7eab7c6a696479f4.html\n'
ATT_ID = 1839

# Check redirects that exist
redirects = xc('website.rewrite', 'search_read',
    [[['url_from', '=', f'/{FILENAME}']]],
    {'fields': ['id', 'url_from', 'url_to', 'redirect_type', 'website_id']})
print('Existing redirects:', redirects)

# Delete existing redirects
if redirects:
    xc('website.rewrite', 'unlink', [[r['id'] for r in redirects]])
    print('Deleted old redirects')

# Delete the broken attachment
xc('ir.attachment', 'unlink', [[ATT_ID]])
print(f'Deleted attachment {ATT_ID}')

# Approach: Create a website.page with the verification content embedded
# The page URL will be /google7eab7c6a696479f4 (no .html)
# Then create a 301 redirect from .html -> no-extension URL
# Google follows redirects for HTML file verification

# Step 1: Create QWeb view with JUST the verification text (minimal html, no website layout)
view_arch = '''<t t-name="website.google_verification_page">
<html>
<head><title>Google Verification</title></head>
<body>google-site-verification: google7eab7c6a696479f4.html</body>
</html>
</t>'''

# Check if view already exists
existing_views = xc('ir.ui.view', 'search_read',
    [[['key', '=', 'website.google_verification_page']]],
    {'fields': ['id']})
if existing_views:
    view_id = existing_views[0]['id']
    xc('ir.ui.view', 'write', [[view_id], {
        'arch_db': view_arch,
        'active': True,
    }])
    print(f'Updated view {view_id}')
else:
    view_id = xc('ir.ui.view', 'create', [{
        'name': 'Google Verification Page',
        'key': 'website.google_verification_page',
        'type': 'qweb',
        'arch_db': view_arch,
    }])
    print(f'Created view {view_id}')

# Step 2: Create website.page pointing to this view
existing_pages = xc('website.page', 'search_read',
    [[['url', 'in', ['/google7eab7c6a696479f4', '/google7eab7c6a696479f4.html']]]],
    {'fields': ['id', 'url']})
if existing_pages:
    page_id = existing_pages[0]['id']
    xc('website.page', 'write', [[page_id], {
        'url': '/google7eab7c6a696479f4',
        'website_published': True,
        'is_published': True,
        'website_id': 1,
        'view_id': view_id,
    }])
    print(f'Updated page {page_id}')
else:
    page_id = xc('website.page', 'create', [{
        'url': '/google7eab7c6a696479f4',
        'website_published': True,
        'is_published': True,
        'website_id': 1,
        'view_id': view_id,
    }])
    print(f'Created page {page_id}')

# Step 3: Create redirect /google7eab7c6a696479f4.html -> /google7eab7c6a696479f4
redirect_id = xc('website.rewrite', 'create', [{
    'name': 'Google Verification Redirect',
    'url_from': f'/{FILENAME}',
    'url_to': '/google7eab7c6a696479f4',
    'redirect_type': '301',
    'website_id': 1,
    'active': True,
}])
print(f'Created redirect ID {redirect_id}')

# Step 4: Test the page URL
import time
print('\nWaiting 5 seconds...')
time.sleep(5)

for test_url in [
    'https://www.longislandconvenience.com/google7eab7c6a696479f4',
    'https://www.longislandconvenience.com/google7eab7c6a696479f4.html',
]:
    print(f'\nFetching {test_url} ...')
    try:
        req = urllib.request.Request(test_url, headers={'User-Agent': 'Googlebot/2.1'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read(500).decode('utf-8', errors='replace')
            print(f'HTTP {resp.status}')
            if 'google-site-verification' in body:
                print('  FOUND: google-site-verification in response')
                print(f'  Content snippet: {repr(body[:200])}')
            else:
                print(f'  NOT FOUND. Content: {repr(body[:200])}')
    except urllib.error.HTTPError as e:
        print(f'HTTP {e.code}: {e.reason}')
    except Exception as e:
        print(f'Error: {type(e).__name__}: {e}')
