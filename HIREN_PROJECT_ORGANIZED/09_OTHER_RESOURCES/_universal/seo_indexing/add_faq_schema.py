import xmlrpc.client, json, re

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

DOMAIN = 'https://www.longislandconvenience.com'

# ── Per-category FAQ bank + business info ─────────────────────────────────
CATS = {
    'Sports & Trading Cards': {
        'biz_name': "Long Island Cards | Hiren's Card Shop",
        'biz_url':  'https://www.longislandcards.com',
        'biz_type': 'HobbyShop',
        'faqs': [
            ("Where can I buy Pokemon, MTG and Yu-Gi-Oh cards in Long Island?",
             "Hiren's Long Island Cards at 605 Old Country Road, Plainview NY 11803 carries Pokemon, MTG, Yu-Gi-Oh, One Piece TCG and sports cards. Open 7 days a week in Nassau County."),
            ("Does Long Island Cards buy old trading cards for cash?",
             "Yes. Hiren offers same-day cash and store credit for Pokemon, MTG, Yu-Gi-Oh, One Piece and sports cards. No appointment needed — walk in to Long Island Cards in Plainview NY."),
            ("Are there PSA graded cards available in Nassau County?",
             "Yes. Long Island Cards specializes in PSA-authenticated and BGS-graded cards. Browse the display case at 605 Old Country Road, Plainview NY 11803."),
            ("What card shops are near Hicksville, Syosset or Bethpage NY?",
             "Long Island Cards in Plainview NY is centrally located in Nassau County — minutes from Hicksville, Syosset, Bethpage, Westbury and Old Bethpage at 605 Old Country Road, Plainview NY 11803."),
        ]
    },
    'Print & Mail Services': {
        'biz_name': "Long Island Print & Mail | Hiren's Print Shop",
        'biz_url':  'https://www.longislandprintandmail.com',
        'biz_type': 'LocalBusiness',
        'faqs': [
            ("Where can I get same-day printing in Plainview NY?",
             "Long Island Print & Mail at 605 Old Country Road, Plainview NY offers same-day printing for business cards, flyers, banners and brochures. Most jobs ready within hours in Nassau County."),
            ("Does Hiren's Print Shop have a walk-in notary public?",
             "Yes. Long Island Print & Mail in Plainview NY has a licensed notary available walk-in with no appointment. Serving Nassau County for real estate docs, affidavits, power of attorney and more."),
            ("Can I ship UPS, FedEx and USPS from Plainview NY at one location?",
             "Yes. Long Island Print & Mail at 605 Old Country Road, Plainview NY accepts all carriers. Packing materials and label printing available on-site. One stop for all shipping in Nassau County."),
            ("How much does private mailbox rental cost in Nassau County?",
             "Long Island Print & Mail offers competitive monthly mailbox rental in Plainview NY — real street address, all-carrier package acceptance, 24/7 lobby access. Contact the shop for current pricing."),
        ]
    },
    'Balloons & Party Decor': {
        'biz_name': "Long Island Balloons & Decor | Hiren's Party Shop",
        'biz_url':  'https://www.longislandconvenience.com',
        'biz_type': 'PartySupplyStore',
        'faqs': [
            ("Where can I get custom balloon decorations on Long Island?",
             "Hiren's creates custom balloon arches, garlands and centerpieces in Plainview NY — serving all of Nassau County. Order at longislandconvenience.com or visit 605 Old Country Road, Plainview NY 11803."),
            ("Does Hiren's do same-day balloon pickup in Nassau County?",
             "Yes. Order by noon for same-day balloon pickup at Hiren's in Plainview NY 11803. Rush orders available by phone. Bouquets and simple arrangements ready within hours."),
            ("Can Hiren's deliver balloon setups to venues across Long Island?",
             "Yes. Hiren's delivers balloon setups to venues across Nassau County including Hicksville, Syosset, Westbury, Garden City, Bethpage and Farmingdale."),
            ("What balloon decorations does Hiren's specialize in?",
             "Hiren's specializes in organic balloon arches, garlands, confetti balloons, gender reveals, baby showers, wedding backdrops, graduation displays and corporate event balloon installations on Long Island."),
        ]
    },
    'Gift Baskets & Gifts': {
        'biz_name': "Long Island Gift Baskets | Hiren's Gift Shop",
        'biz_url':  'https://www.longislandconvenience.com',
        'biz_type': 'GiftShop',
        'faqs': [
            ("Where can I get custom gift baskets in Nassau County NY?",
             "Hiren's creates custom handcrafted gift baskets in Plainview NY — same-day pickup or Nassau County delivery. Personalized for birthdays, corporate gifting, holidays and more at 605 Old Country Road, Plainview NY 11803."),
            ("Does Hiren's offer same-day gift basket pickup in Plainview NY?",
             "Yes. Order by 11 AM for same-day gift basket pickup at Hiren's Long Island shop. Rush orders welcome — call to confirm. Located at 605 Old Country Road, Plainview NY 11803."),
            ("Can I order corporate gift baskets in bulk on Long Island?",
             "Yes. Hiren's handles bulk corporate gift basket orders with volume discounts. Branded ribbons and delivery across Nassau and Suffolk County available. Contact the shop for a corporate quote."),
            ("What occasions does Hiren's make gift baskets for?",
             "Hiren's creates gift baskets for birthdays, anniversaries, holidays (Christmas, Hanukkah, New Year), baby showers, sympathy, corporate appreciation, employee gifts and more — in Plainview Nassau County NY."),
        ]
    },
    'Long Island News': {
        'biz_name': "Long Island Convenience | Hiren's Local Store Hub",
        'biz_url':  'https://www.longislandconvenience.com',
        'biz_type': 'LocalBusiness',
        'faqs': [
            ("What stores does Hiren Chauhan own on Long Island?",
             "Hiren Chauhan owns 7 businesses in Plainview NY — Long Island Cards, Long Island Print & Mail, Long Island Convenience, Long Island Balloons & Decor, Long Island Gift Baskets, Cyber Consulting IT services, and more. All at or near 605 Old Country Road, Plainview NY 11803."),
            ("Where is Hiren's store on Long Island?",
             "Hiren's stores are at 605 Old Country Road, Plainview NY 11803 in Nassau County. Easy access from the LIE, Northern State Pkwy and Route 135."),
            ("Is Hiren Chauhan a local Long Island business owner?",
             "Yes. Hiren Chauhan has operated businesses in Plainview Nassau County NY since 1998 — a 25+ year local entrepreneur building community-focused stores on Long Island."),
            ("How do I contact Hiren's Long Island stores?",
             "Visit longislandconvenience.com or call 212-564-8585. Central address: 605 Old Country Road, Plainview NY 11803. Also: longislandcards.com and longislandprintandmail.com."),
        ]
    },
    'Convenience & Grocery': {
        'biz_name': "Long Island Convenience | Hiren's Local Store Hub",
        'biz_url':  'https://www.longislandconvenience.com',
        'biz_type': 'ConvenienceStore',
        'faqs': [
            ("What are the hours at Hiren's convenience store in Plainview NY?",
             "Long Island Convenience at 605 Old Country Road, Plainview NY 11803 is open 7 days a week with extended hours to serve Nassau County commuters and families."),
            ("Where is the nearest convenience store in Plainview NY?",
             "Long Island Convenience is at 605 Old Country Road, Plainview NY 11803 — centrally located near the LIE, Northern State Pkwy and Route 135. Easy parking."),
            ("Does Hiren's convenience store carry cold drinks and snacks?",
             "Yes. Long Island Convenience stocks cold beverages (soda, energy drinks, water, juice), hot coffee, snacks, candy, chips, hot grab-and-go food and household essentials."),
            ("Is there a local convenience store open late in Nassau County?",
             "Yes. Long Island Convenience in Plainview NY stays open late for Nassau County residents needing essentials after regular store hours — snacks, drinks, toiletries, medicine and more."),
        ]
    },
    'IT & Cyber Services': {
        'biz_name': "Cyber Consulting | Hiren's IT Services Plainview NY",
        'biz_url':  'https://www.longislandconvenience.com',
        'biz_type': 'LocalBusiness',
        'faqs': [
            ("Where can I get IT support for my small business in Nassau County?",
             "Hiren's Cyber Consulting at 605 Old Country Road, Plainview NY 11803 has provided IT support to Long Island businesses since 1998. On-site and remote IT, network setup, computer repair and cybersecurity."),
            ("How fast can I get computer repair in Plainview NY?",
             "Most repairs at Hiren's Cyber Consulting are completed same-day or next-day. No appointment needed for drop-off diagnostics at 605 Old Country Road, Plainview NY."),
            ("Does Hiren's offer cybersecurity services on Long Island?",
             "Yes. Cyber Consulting in Plainview NY offers security assessments, antivirus, email security, firewall setup and compliance guidance for Long Island small businesses. Founded 1998. Call 212-564-8585."),
            ("Can Hiren's repair my laptop or Mac in Nassau County?",
             "Yes. Hiren's fixes PCs, Macs and laptops — screen replacement, virus removal, hard drive swap, RAM upgrades and data recovery. Walk in to 605 Old Country Road, Plainview NY 11803."),
        ]
    },
}

# ── Build HTML FAQ block ───────────────────────────────────────────────────
def faq_html(faqs):
    items = ''.join(
        f'<div class="faq-item" style="margin-bottom:20px;">'
        f'<h3 style="color:#1a1a2e;font-size:1.05rem;margin-bottom:6px;">Q: {q}</h3>'
        f'<p style="color:#444;line-height:1.7;margin:0;padding-left:16px;'
        f'border-left:3px solid #e63946;">{a}</p></div>'
        for q, a in faqs
    )
    return (
        '<div class="faq-section" style="background:#f8f9fa;border-radius:12px;'
        'padding:32px;margin-top:48px;">'
        '<h2 style="color:#1a1a2e;font-size:1.4rem;margin-bottom:24px;'
        'border-bottom:2px solid #e63946;padding-bottom:12px;">'
        'Frequently Asked Questions</h2>' + items + '</div>'
    )

# ── Build JSON-LD schema block ─────────────────────────────────────────────
def schema_ld(title, desc, post_url, faqs, biz):
    data = [
        {
            '@context': 'https://schema.org',
            '@type': 'BlogPosting',
            'headline': title,
            'description': desc,
            'url': post_url,
            'author': {
                '@type': 'Person',
                'name': 'Hiren Chauhan',
                'url': 'https://www.longislandconvenience.com/about-hiren',
            },
            'publisher': {
                '@type': 'Organization',
                'name': "Long Island Convenience | Hiren's Local Store Hub",
                'url': 'https://www.longislandconvenience.com',
            },
            'mainEntityOfPage': {'@type': 'WebPage', '@id': post_url},
        },
        {
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': [
                {'@type': 'Question', 'name': q,
                 'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                for q, a in faqs
            ],
        },
        {
            '@context': 'https://schema.org',
            '@type': biz['biz_type'],
            'name': biz['biz_name'],
            'url':  biz['biz_url'],
            'address': {
                '@type': 'PostalAddress',
                'streetAddress': '605 Old Country Road',
                'addressLocality': 'Plainview',
                'addressRegion': 'NY',
                'postalCode': '11803',
                'addressCountry': 'US',
            },
            'telephone': '+12125648585',
            'areaServed': [
                {'@type': 'City', 'name': 'Plainview'},
                {'@type': 'AdministrativeArea', 'name': 'Nassau County'},
                {'@type': 'State', 'name': 'New York'},
            ],
        },
    ]
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'

# ── Fetch all posts ────────────────────────────────────────────────────────
posts = xc('blog.post', 'search_read', [[]], {
    'fields': ['id', 'name', 'blog_id', 'content',
               'website_meta_title', 'website_meta_description',
               'website_published'],
    'order': 'blog_id asc, id asc',
})
print(f'Fetched {len(posts)} posts')

updated = 0
skipped = 0

for p in posts:
    blog_name = p['blog_id'][1] if p['blog_id'] else ''
    biz = CATS.get(blog_name)
    if not biz:
        print(f"  SKIP (no category map): {blog_name} — {p['name'][:40]}")
        skipped += 1
        continue

    content = p.get('content') or ''

    # Don't double-add
    if 'faq-section' in content:
        print(f"  SKIP (already has FAQ): {p['name'][:55]}")
        skipped += 1
        continue

    blog_slug = to_slug(blog_name)
    post_slug = to_slug(p['name'])
    post_url  = f'{DOMAIN}/blog/{blog_slug}/{post_slug}'
    title     = p.get('website_meta_title') or p['name']
    desc      = p.get('website_meta_description') or ''
    faqs      = biz['faqs']

    new_content = (
        schema_ld(title, desc, post_url, faqs, biz) +
        content +
        faq_html(faqs)
    )

    xc('blog.post', 'write', [[p['id']], {'content': new_content}])
    print(f"  Updated ID={p['id']}: {p['name'][:60]}")
    updated += 1

print(f'\nDone. Updated: {updated}  Skipped: {skipped}')
