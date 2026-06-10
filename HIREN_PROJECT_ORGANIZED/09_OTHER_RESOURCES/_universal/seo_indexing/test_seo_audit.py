import urllib.request, json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

CLAUDE_KEY = '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'
ODOO_URL   = 'https://country-cove-inc.odoo.com'

def post_json(url, payload, headers={}):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={'Content-Type':'application/json', **headers})
    with urllib.request.urlopen(req, timeout=90) as r:
        hdr = r.headers.get('Set-Cookie','')
        body = json.loads(r.read())
    return body, hdr

# ── 1. Claude call with tightened prompt ─────────────────────────────
print('Calling Claude API...')
SYSTEM = (
    'You are an expert local SEO content writer for LongIslandConvenience.com at 605 Old Country Road, '
    'Plainview NY 11803 (Nassau County). One-stop shop: balloons, gift baskets, greeting cards, sports/trading cards, '
    'printing, shipping. Write geo-targeted blog posts. HTML: h2/h3/p/ul/li/strong/em only. No CSS.'
)
PROMPT = """Write a 900-1000 word SEO blog post for LongIslandConvenience.com.

TODAY: Wednesday, May 28, 2026
SEASON: Father's Day + Graduation season peak, early summer
BLOG SECTION: Balloons & Party Decor (blog_id: 3)
BLOG FOCUS: Graduation Balloon Arch Long Island NY 2026
SPECIAL DAY: Graduation

PRIMARY KEYWORDS — use FIRST minimum 3x, others minimum 2x each:
graduation balloon arch Long Island
class of 2026 balloons Nassau County
balloon arch graduation Plainview NY

ANGLE: Stunning graduation balloon arches and setups for Nassau County Class of 2026 parties

STRICT SEO REQUIREMENTS:
- Title: exactly 50-60 chars, includes primary keyword + 'Long Island' or 'Nassau County'
- Subtitle: 1 sentence, 80-100 chars, geo-targeted
- Meta description: MUST be 155-160 chars exactly, includes primary keyword, ends with CTA
- Meta keywords: 6-8 geo-targeted comma-separated keywords
- Tags: 4-5 including geographic
- First paragraph: hook with primary keyword in first 2 sentences
- 3-4 H2 headings targeting different keyword variations
- Mention "605 Old Country Road, Plainview NY" once
- "Nassau County" MINIMUM 4 times
- "Long Island" MINIMUM 5 times
- "Plainview" MINIMUM 3 times
- Closing H2 with CTA and +1 (917) 338-7086
- 1 bulleted list (5-7 items)
- Reference 3+ nearby towns: Hicksville, Syosset, Bethpage, Farmingdale, Westbury, Old Bethpage, Jericho
- HTML: h2 h3 p ul li ol strong em only — no CSS

Return ONLY valid JSON (no markdown):
{"title":"","subtitle":"","meta_title":"","meta_description":"","meta_keywords":"","tags":[],"html_body":""}"""

resp, _ = post_json('https://api.anthropic.com/v1/messages', {
    'model':'claude-opus-4-7','max_tokens':3500,'system':SYSTEM,
    'messages':[{'role':'user','content':PROMPT}]
}, {'x-api-key':CLAUDE_KEY,'anthropic-version':'2023-06-01'})

raw = resp['content'][0]['text'].strip()
if raw.startswith('```'):
    raw = re.sub(r'^```[a-z]*\s*','',raw); raw = re.sub(r'\s*```$','',raw).strip()
blog = json.loads(raw)
print(f'Claude returned: title={len(blog["title"])} chars, body={len(blog["html_body"])} chars')

# Add image
blog['html_body'] = '<p><img src="https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=900&h=500&fit=crop&auto=format&q=80" alt="Graduation balloon arch Long Island NY Nassau County"/></p>' + blog['html_body']

# ── 2. SEO Audit ─────────────────────────────────────────────────────
plain = re.sub(r'<[^>]+>',' ',blog['html_body'])
plain = re.sub(r'\s+',' ',plain).strip()
words = plain.split()
h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', blog['html_body'], re.IGNORECASE)

geo_checks = [
    ('Long Island',          plain.count('Long Island'),          5),
    ('Nassau County',        plain.count('Nassau County'),         4),
    ('Plainview',            plain.count('Plainview'),             3),
    ('605 Old Country Road', plain.count('605 Old Country Road'),  1),
    ('+1 (917)',             plain.count('+1 (917)'),              1),
]
kw_checks = [
    ('graduation balloon arch Long Island',  plain.lower().count('graduation balloon arch long island'), 3),
    ('class of 2026 balloons Nassau County', plain.lower().count('class of 2026'),                      2),
    ('balloon arch graduation Plainview',    plain.lower().count('balloon arch graduation') + plain.lower().count('graduation balloon arch'), 2),
]
nearby = ['Hicksville','Syosset','Bethpage','Farmingdale','Westbury','Old Bethpage','Jericho','Levittown','Massapequa']
found_areas = [a for a in nearby if a in plain]
meta_len = len(blog['meta_description'])

print()
print('='*65)
print('SEO / GEO AUDIT — NEW BLOG POST (Balloon Arch Graduation)')
print('='*65)
print()
print('META FIELDS:')
print(f'  Title      ({len(blog["title"])} chars): {blog["title"]}')
meta_title = blog.get('meta_title', blog.get('title', ''))
print(f'  Meta Title ({len(meta_title)} chars): {meta_title}')
meta_ok = '✅' if 155 <= meta_len <= 165 else '⚠️ '
print(f'  Meta Desc  {meta_ok}({meta_len} chars): {blog["meta_description"]}')
print(f'  Meta KW    : {blog["meta_keywords"]}')
print(f'  Tags       : {blog["tags"]}')
print()
print(f'CONTENT STATS:')
print(f'  Word count : {len(words)} words  {"✅" if len(words)>=900 else "⚠️ "}(need 900+)')
print(f'  H2 count   : {len(h2s)}  {"✅" if len(h2s)>=3 else "⚠️ "}(need 3+)')
for h in h2s: print(f'    - {h}')
print()
print('GEO KEYWORD COUNTS:')
for label, count, required in geo_checks:
    ok = '✅' if count >= required else '❌'
    print(f'  {ok} "{label}": {count}x  (need {required}+)')
print()
print('PRIMARY KEYWORDS:')
for label, count, required in kw_checks:
    ok = '✅' if count >= required else ('⚠️ ' if count > 0 else '❌')
    print(f'  {ok} "{label}": {count}x  (need {required}+)')
print()
print(f'NEARBY TOWNS ({len(found_areas)}/3+ required): {found_areas}')
print()

all_pass = (
    all(c >= r for _,c,r in geo_checks) and
    all(c >= r for _,c,r in kw_checks) and
    len(words) >= 900 and len(h2s) >= 3 and
    155 <= meta_len <= 165 and len(found_areas) >= 3
)
print('OVERALL:', '✅ ALL SEO/GEO REQUIREMENTS PASS' if all_pass else '⚠️  SOME REQUIREMENTS NOT MET')

# ── 3. Post to Odoo ────────────────────────────────────────────────────
print()
print('Posting to Odoo...')
body2, ch = post_json(f'{ODOO_URL}/web/session/authenticate', {
    'jsonrpc':'2.0','method':'call','id':1,
    'params':{'db':'country-cove-inc','login':'countrycoveinc@gmail.com','password':'M@nhattan1234'}
})
session_id = next((p.split('=',1)[1] for p in ch.split(';') if p.strip().startswith('session_id=')), '')

body3, _ = post_json(f'{ODOO_URL}/web/dataset/call_kw', {
    'jsonrpc':'2.0','method':'call','id':2,
    'params':{'model':'blog.post','method':'create','args':[{
        'name':                     blog['title'][:255],
        'subtitle':                 blog['subtitle'][:255],
        'content':                  blog['html_body'],
        'blog_id':                  3,
        'website_id':               1,
        'website_published':        True,
        'is_published':             True,
        'website_meta_title':       blog.get('meta_title', blog['title'])[:255],
        'website_meta_description': blog['meta_description'][:400],
        'website_meta_keywords':    blog['meta_keywords'][:255],
    }],'kwargs':{}}
}, {'Cookie': f'session_id={session_id}'})

post_id = body3['result']
body4, _ = post_json(f'{ODOO_URL}/web/dataset/call_kw', {
    'jsonrpc':'2.0','method':'call','id':3,
    'params':{'model':'blog.post','method':'read','args':[[post_id],['website_absolute_url']],'kwargs':{}}
}, {'Cookie': f'session_id={session_id}'})
live_url = body4['result'][0]['website_absolute_url']

print(f'  Post ID  : {post_id}')
print(f'  Live URL : {live_url}')
print()
print('GSC Indexing:')
print(f'https://search.google.com/search-console/inspect?resource_id=https%3A%2F%2Fwww.longislandconvenience.com%2F&id={urllib.request.quote(live_url)}')
