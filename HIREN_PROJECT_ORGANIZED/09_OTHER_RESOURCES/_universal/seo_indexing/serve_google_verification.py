import xmlrpc.client, base64, urllib.request, os

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

# Google HTML verification file content (53 bytes including newline)
FILENAME = 'google7eab7c6a696479f4.html'
FILE_CONTENT = b'google-site-verification: google7eab7c6a696479f4.html\n'

print(f'File content ({len(FILE_CONTENT)} bytes): {FILE_CONTENT}')

# Check if attachment already exists
existing = xc('ir.attachment', 'search_read',
    [[['url', '=', f'/{FILENAME}']]],
    {'fields': ['id', 'name', 'url', 'website_id']})

if existing:
    print(f'Attachment already exists: {existing}')
    att_id = existing[0]['id']
    # Update it
    xc('ir.attachment', 'write', [[att_id], {
        'datas': base64.b64encode(FILE_CONTENT).decode(),
        'mimetype': 'text/html',
        'public': True,
    }])
    print(f'Updated existing attachment ID {att_id}')
else:
    att_id = xc('ir.attachment', 'create', [{
        'name': FILENAME,
        'url': f'/{FILENAME}',
        'type': 'binary',
        'datas': base64.b64encode(FILE_CONTENT).decode(),
        'mimetype': 'text/html',
        'public': True,
        'website_id': 1,
    }])
    print(f'Created attachment ID {att_id}')

# Verify it's accessible
verify_url = f'https://www.longislandconvenience.com/{FILENAME}'
print(f'\nVerifying {verify_url} ...')
try:
    req = urllib.request.Request(verify_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode('utf-8', errors='replace')
        print(f'HTTP {resp.status}')
        print(f'Content: {repr(body)}')
        if 'google-site-verification' in body:
            print('\nSUCCESS — File is live. Go to Google Search Console and click VERIFY.')
        else:
            print('\nWARNING — Unexpected content returned.')
except Exception as e:
    print(f'Fetch error: {e}')
    print('The attachment was created — wait 30 seconds then try manually:')
    print(f'  {verify_url}')
