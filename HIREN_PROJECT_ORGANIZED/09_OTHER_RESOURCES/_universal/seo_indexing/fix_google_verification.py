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
FILE_CONTENT = 'google-site-verification: google7eab7c6a696479f4.html'

# -- 1. Check the attachment we created --
atts = xc('ir.attachment', 'search_read',
    [[['url', '=', f'/{FILENAME}']]],
    {'fields': ['id', 'name', 'url', 'type', 'public', 'mimetype', 'website_id']})
print('Existing attachments:', atts)

if atts:
    att_id = atts[0]['id']
else:
    att_id = 1839

# -- 2. Test if /web/content/<id> serves it --
content_url = f'https://www.longislandconvenience.com/web/content/{att_id}'
print(f'\nTesting {content_url} ...')
try:
    req = urllib.request.Request(content_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read(200).decode('utf-8', errors='replace')
        print(f'HTTP {resp.status}: {repr(body)}')
except Exception as e:
    print(f'Error: {e}')

# -- 3. Delete any existing redirects for this file --
existing_redirects = xc('website.rewrite', 'search_read',
    [[['url_from', '=', f'/{FILENAME}']]],
    {'fields': ['id', 'url_from', 'url_to']})
if existing_redirects:
    print(f'\nDeleting old redirect: {existing_redirects}')
    xc('website.rewrite', 'unlink', [[r['id'] for r in existing_redirects]])

# -- 4. Create a redirect from /google...html -> /web/content/<id> --
# Google follows 301 redirects for HTML file verification
redirect_id = xc('website.rewrite', 'create', [{
    'name': 'Google Search Console Verification',
    'url_from': f'/{FILENAME}',
    'url_to': f'/web/content/{att_id}',
    'redirect_type': '301',
    'website_id': 1,
    'active': True,
}])
print(f'\nCreated redirect ID {redirect_id}: /{FILENAME} → /web/content/{att_id}')

# -- 5. Verify the final URL works --
verify_url = f'https://www.longislandconvenience.com/{FILENAME}'
print(f'\nFetching {verify_url} ...')
try:
    req = urllib.request.Request(verify_url, headers={'User-Agent': 'Googlebot/2.1'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read(300).decode('utf-8', errors='replace')
        print(f'HTTP {resp.status}')
        print(f'Content: {repr(body[:200])}')
        if 'google-site-verification' in body:
            print('\nSUCCESS — Go to Google Search Console and click VERIFY now.')
        else:
            print('\nContent does not contain verification string yet.')
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.reason}')
    print('Try waiting 60 seconds for Odoo cache to clear, then re-check the URL manually.')
except Exception as e:
    print(f'Error: {e}')
