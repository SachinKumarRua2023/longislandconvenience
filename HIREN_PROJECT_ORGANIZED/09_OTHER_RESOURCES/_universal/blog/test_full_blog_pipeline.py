import urllib.request, json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

CLAUDE_KEY = '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'
ODOO_URL   = 'https://country-cove-inc.odoo.com'

def post_json(url, payload, headers={}):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json', **headers}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        hdr = r.headers.get('Set-Cookie', '')
        body = json.loads(r.read())
    return body, hdr

# ══════════════════════════════════════════════════════════════
# STEP 1: Real Claude API call
# ══════════════════════════════════════════════════════════════
print('Step 1: Calling Claude API (claude-opus-4-7)...')

SYSTEM = (
    'You are an expert local SEO content writer for Long Island, New York. '
    'You write blog posts for LongIslandConvenience.com at 605 Old Country Road, '
    'Plainview NY 11803 (Nassau County). They sell: gift baskets, balloons & decor, '
    'greeting cards, sports trading cards, and printing services. '
    'Write geo-targeted blog posts. HTML uses h2/h3/p/ul/li/strong/em only — no CSS.'
)

PROMPT = """Write a 750-900 word SEO blog post for LongIslandConvenience.com.

TODAY: Wednesday, May 28, 2026
SEASON: Father's Day + Graduation season peak, early summer Long Island
BLOG FOCUS: Graduation Gift Baskets Long Island NY
CATEGORY: gift_baskets

PRIMARY KEYWORDS (use each naturally 2-4 times):
graduation gift basket Long Island
graduation gifts Nassau County
gift basket for graduate Plainview NY
class of 2026 gift Long Island

ANGLE: Curated graduation gift basket ideas available for same-day pickup in Plainview NY

SEO RULES:
- Title: 50-60 chars, includes primary keyword + Long Island OR Nassau County
- Meta description: exactly 150-160 chars, end with a CTA (Visit us / Shop now / Call today)
- Subtitle: 1 sentence, 80-100 chars, includes geo keyword
- First paragraph: hook the reader, include primary keyword naturally
- Use 3-4 H2 headings, each targeting a keyword variation
- Mention "605 Old Country Road, Plainview NY" once naturally
- Mention "Nassau County" at least 3 times
- Mention "Long Island" at least 4 times
- Closing CTA paragraph inviting to visit or call +1 (917) 338-7086
- Include 1 bulleted or numbered list
- Tone: warm, local, helpful — NOT corporate or salesy
- Use ONLY: h2, h3, p, ul, li, ol, strong, em — no inline CSS

Return ONLY valid JSON (no markdown wrapper, no explanation):
{
  "title": "Blog title (50-60 chars)",
  "subtitle": "One sentence subtitle 80-100 chars with geo keyword",
  "meta_title": "50-60 chars",
  "meta_description": "155-char meta description ending with CTA",
  "meta_keywords": "kw1, kw2, kw3, kw4, kw5",
  "tags": ["Long Island", "Plainview NY", "Nassau County", "Graduation 2026"],
  "html_body": "<h2>...</h2><p>...</p>"
}"""

claude_resp, _ = post_json(
    'https://api.anthropic.com/v1/messages',
    {
        'model': 'claude-opus-4-7',
        'max_tokens': 3000,
        'system': SYSTEM,
        'messages': [{'role': 'user', 'content': PROMPT}]
    },
    {
        'x-api-key': CLAUDE_KEY,
        'anthropic-version': '2023-06-01'
    }
)

raw_text = claude_resp['content'][0]['text']
print(f'  Claude returned {len(raw_text)} chars')

# Parse JSON from Claude
cleaned = raw_text.strip()
if cleaned.startswith('```'):
    cleaned = re.sub(r'^```[a-z]*\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned).strip()

blog = json.loads(cleaned)

print(f'  title ({len(blog["title"])} chars): {blog["title"]}')
print(f'  meta_desc ({len(blog["meta_description"])} chars): {blog["meta_description"]}')
print(f'  html_body: {len(blog["html_body"])} chars')
print(f'  tags: {blog["tags"]}')

# Prepend Unsplash header image (gift basket)
img_url = 'https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=900&h=500&fit=crop&auto=format&q=80'
img_alt = 'Graduation gift baskets Long Island NY Nassau County Plainview'
blog['html_body'] = (
    f'<p><img src="{img_url}" alt="{img_alt}" '
    f'style="max-width:100%;border-radius:8px;margin:16px 0;" /></p>'
    + blog['html_body']
)

# ══════════════════════════════════════════════════════════════
# STEP 2: Odoo JSON-RPC Auth
# ══════════════════════════════════════════════════════════════
print('\nStep 2: Odoo auth...')
auth_resp, cookie_hdr = post_json(
    f'{ODOO_URL}/web/session/authenticate',
    {
        'jsonrpc': '2.0', 'method': 'call', 'id': 1,
        'params': {
            'db': 'country-cove-inc',
            'login': 'countrycoveinc@gmail.com',
            'password': 'M@nhattan1234'
        }
    }
)
uid = auth_resp['result']['uid']
session_id = ''
for part in cookie_hdr.split(';'):
    p = part.strip()
    if p.startswith('session_id='):
        session_id = p.split('=', 1)[1]
        break
print(f'  uid={uid}  session={session_id[:16]}...')

# ══════════════════════════════════════════════════════════════
# STEP 3: Create Blog Post
# ══════════════════════════════════════════════════════════════
print('\nStep 3: Creating blog post on Odoo...')
create_resp, _ = post_json(
    f'{ODOO_URL}/web/dataset/call_kw',
    {
        'jsonrpc': '2.0', 'method': 'call', 'id': 2,
        'params': {
            'model': 'blog.post',
            'method': 'create',
            'args': [{
                'name':                     blog['title'][:255],
                'subtitle':                 blog.get('subtitle', '')[:255],
                'content':                  blog['html_body'],
                'blog_id':                  5,   # Gift Baskets & Gifts
                'website_id':               1,   # longislandconvenience.com
                'website_published':        True,
                'is_published':             True,
                'website_meta_title':       blog.get('meta_title', blog['title'])[:255],
                'website_meta_description': blog.get('meta_description', '')[:400],
                'website_meta_keywords':    blog.get('meta_keywords', '')[:255],
            }],
            'kwargs': {}
        }
    },
    {'Cookie': f'session_id={session_id}'}
)
post_id = create_resp.get('result')
err = create_resp.get('error')
print(f'  post_id={post_id}  error={err}')

if not post_id or not isinstance(post_id, int):
    print('ERROR: Post creation failed')
    print(json.dumps(create_resp, indent=2)[:500])
    sys.exit(1)

# ══════════════════════════════════════════════════════════════
# STEP 4: Read Live URL from Odoo
# ══════════════════════════════════════════════════════════════
print('\nStep 4: Reading live URL from Odoo...')
read_resp, _ = post_json(
    f'{ODOO_URL}/web/dataset/call_kw',
    {
        'jsonrpc': '2.0', 'method': 'call', 'id': 3,
        'params': {
            'model': 'blog.post',
            'method': 'read',
            'args': [[post_id], ['id', 'name', 'website_absolute_url', 'is_published']],
            'kwargs': {}
        }
    },
    {'Cookie': f'session_id={session_id}'}
)
post_data = read_resp['result'][0]
live_url = post_data['website_absolute_url']

gsc_url = (
    'https://search.google.com/search-console/inspect'
    '?resource_id=https%3A%2F%2Fwww.longislandconvenience.com%2F'
    f'&id={urllib.request.quote(live_url)}'
)

# ══════════════════════════════════════════════════════════════
# RESULT
# ══════════════════════════════════════════════════════════════
print()
print('=' * 65)
print('  REAL END-TO-END PIPELINE COMPLETE')
print('=' * 65)
print(f'  Post ID    : {post_id}')
print(f'  Title      : {post_data["name"]}')
print(f'  Published  : {post_data["is_published"]}')
print(f'  Live URL   : {live_url}')
print()
print('  Google Search Console — Request Indexing:')
print(f'  {gsc_url}')
print()
print('  Blog section (Gift Baskets):')
print('  https://www.longislandconvenience.com/blog/gift-baskets-gifts-5')
print()
print('  Full Blog:')
print('  https://www.longislandconvenience.com/blog')
print()
print('  Claude-generated HTML body (first 800 chars):')
print(blog['html_body'][200:1000])
