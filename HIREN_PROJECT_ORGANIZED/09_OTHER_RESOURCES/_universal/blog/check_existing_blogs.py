import xmlrpc.client

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

# All blog categories
cats = xc('blog.blog', 'search_read', [[]], {'fields': ['id','name','website_id']})
print('=== BLOG CATEGORIES ===')
for c in cats:
    print(f"  ID={c['id']} name={c['name']} website={c['website_id']}")

# All blog posts
posts = xc('blog.post', 'search_read', [[]], {
    'fields': ['id','name','blog_id','website_published','tag_ids','website_meta_title'],
    'order': 'blog_id asc, id asc'
})
print(f'\n=== BLOG POSTS ({len(posts)} total) ===')
for p in posts:
    print(f"  ID={p['id']} blog={p['blog_id'][1] if p['blog_id'] else '-'} pub={p['website_published']} title={p['name'][:60]}")
