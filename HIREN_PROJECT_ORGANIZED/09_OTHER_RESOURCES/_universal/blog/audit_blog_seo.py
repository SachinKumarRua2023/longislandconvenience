import xmlrpc.client, re

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

def to_slug(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s)
    return s.strip('-')

posts = xc('blog.post', 'search_read', [[]], {
    'fields': ['id','name','blog_id',
               'website_meta_title','website_meta_description',
               'website_meta_keywords','website_published'],
    'order': 'blog_id asc, id asc'
})

DOMAIN = 'https://www.longislandconvenience.com'
print(f'Total blog posts: {len(posts)}\n')
print(f'{"ID":<4} {"PUB"} {"TITLE":<5} {"DESC":<5}  FULL URL')
print('='*110)

missing = []
for p in posts:
    blog_name = p['blog_id'][1] if p['blog_id'] else 'blog'
    blog_slug = to_slug(blog_name)
    post_slug = to_slug(p['name'])
    full_url  = f'{DOMAIN}/blog/{blog_slug}/{post_slug}'
    has_t = bool(p.get('website_meta_title'))
    has_d = bool(p.get('website_meta_description'))
    pub   = 'Y' if p['website_published'] else 'N'
    mt    = 'OK ' if has_t else 'NO '
    md    = 'OK ' if has_d else 'NO '
    print(f"{p['id']:<4} {pub}   {mt}  {md}  {full_url[:95]}")
    if not has_t or not has_d:
        missing.append(p['id'])

print(f'\nPosts missing meta: {missing if missing else "NONE — all good"}')
print(f'\nBlog hub: {DOMAIN}/blog')

# Also check the old 11 posts — do they have meta title/desc?
print('\n--- Posts needing SEO fix ---')
for p in posts:
    if not p.get('website_meta_title') or not p.get('website_meta_description'):
        print(f"  ID={p['id']} title={p['name'][:60]}")
        print(f"    meta_title: {p.get('website_meta_title') or 'MISSING'}")
        print(f"    meta_desc:  {p.get('website_meta_description') or 'MISSING'}")
