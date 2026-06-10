#!/usr/bin/env python3
"""Fix homepage layout - inline flexbox, proper margins, designer quality"""
import xmlrpc.client, sys

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"
SITE_ID = 36

def connect():
    uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
    if not uid: sys.exit("Auth failed")
    m = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    print("Connected UID", uid)
    return m, uid

def xc(m, uid, model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)


HOMEPAGE = '''<data>
    <xpath expr="//div[@id='wrap']" position="replace">
        <div id="wrap" class="oe_structure">

<!-- ═══════════════════════════════════════════════════
     HERO
═══════════════════════════════════════════════════ -->
<section style="background:linear-gradient(160deg,#0d0000 0%,#1c0800 45%,#0a0000 100%);min-height:88vh;display:flex;align-items:center;text-align:center;padding:80px 24px;">
    <div style="max-width:780px;margin:0 auto;width:100%;">

        <div style="display:inline-block;background:rgba(212,175,55,0.1);border:1px solid rgba(212,175,55,0.35);border-radius:100px;padding:7px 20px;margin-bottom:30px;">
            <span style="color:#D4AF37;font-size:11px;font-weight:700;letter-spacing:3.5px;text-transform:uppercase;">605 Old Country Rd &#8226; Plainview, NY</span>
        </div>

        <h1 style="font-size:clamp(40px,7vw,80px);font-weight:900;color:#ffffff;line-height:1.0;margin:0 0 22px;letter-spacing:-2.5px;">
            Long Island's<br/><span style="color:#D4AF37;">Premier</span> Card Shop
        </h1>

        <p style="font-size:clamp(15px,2vw,18px);color:rgba(255,255,255,0.5);max-width:540px;margin:0 auto 38px;line-height:1.7;">
            Sports cards, Pokemon, MTG, Yu-Gi-Oh!, graded cards &amp; accessories.
            Serving Nassau &amp; Suffolk County since 2010.
        </p>

        <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-bottom:52px;">
            <a href="/shop" style="background:#D4AF37;color:#000000;font-weight:800;font-size:15px;padding:15px 40px;border-radius:8px;text-decoration:none;letter-spacing:0.3px;display:inline-block;">Shop Now</a>
            <a href="/contact" style="background:transparent;color:#D4AF37;font-weight:700;font-size:15px;padding:15px 40px;border-radius:8px;text-decoration:none;border:2px solid rgba(212,175,55,0.4);display:inline-block;">Visit Store</a>
        </div>

        <!-- Trust row -->
        <div style="display:flex;gap:0;justify-content:center;flex-wrap:wrap;padding-top:28px;border-top:1px solid rgba(255,255,255,0.07);">
            <div style="padding:0 28px;text-align:center;border-right:1px solid rgba(255,255,255,0.08);">
                <div style="color:#D4AF37;font-size:20px;font-weight:900;line-height:1;">21+</div>
                <div style="color:rgba(255,255,255,0.28);font-size:10px;text-transform:uppercase;letter-spacing:1.8px;margin-top:4px;">Brands</div>
            </div>
            <div style="padding:0 28px;text-align:center;border-right:1px solid rgba(255,255,255,0.08);">
                <div style="color:#D4AF37;font-size:20px;font-weight:900;line-height:1;">500+</div>
                <div style="color:rgba(255,255,255,0.28);font-size:10px;text-transform:uppercase;letter-spacing:1.8px;margin-top:4px;">Products</div>
            </div>
            <div style="padding:0 28px;text-align:center;border-right:1px solid rgba(255,255,255,0.08);">
                <div style="color:#D4AF37;font-size:20px;font-weight:900;line-height:1;">PSA&#183;BGS</div>
                <div style="color:rgba(255,255,255,0.28);font-size:10px;text-transform:uppercase;letter-spacing:1.8px;margin-top:4px;">Graded</div>
            </div>
            <div style="padding:0 28px;text-align:center;">
                <div style="color:#D4AF37;font-size:20px;font-weight:900;line-height:1;">Same Day</div>
                <div style="color:rgba(255,255,255,0.28);font-size:10px;text-transform:uppercase;letter-spacing:1.8px;margin-top:4px;">Shipping</div>
            </div>
        </div>

    </div>
</section>

<!-- ═══════════════════════════════════════════════════
     CATEGORY GRID
═══════════════════════════════════════════════════ -->
<section style="background:#111111;padding:80px 0;">
    <div style="max-width:1200px;margin:0 auto;padding:0 32px;">

        <div style="text-align:center;margin-bottom:48px;">
            <h2 style="font-size:clamp(26px,4vw,36px);font-weight:900;color:#ffffff;margin:0 0 10px;">Shop by Category</h2>
            <p style="color:rgba(255,255,255,0.35);font-size:15px;margin:0;">From rookies to graded gems &#8212; we carry it all</p>
        </div>

        <!-- 6-col flex grid -->
        <div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;">

            <a href="/shop?category=sports-cards" style="flex:1 1 140px;min-width:130px;max-width:190px;background:#1a1a1a;border:1px solid rgba(212,175,55,0.12);border-radius:14px;padding:28px 16px 24px;text-align:center;text-decoration:none;display:block;">
                <div style="font-size:34px;margin-bottom:12px;line-height:1;">&#9918;&#65039;</div>
                <div style="color:#ffffff;font-weight:700;font-size:13px;margin-bottom:4px;">Sports Cards</div>
                <div style="color:rgba(255,255,255,0.28);font-size:11px;">MLB&#183;NBA&#183;NFL&#183;NHL</div>
            </a>

            <a href="/shop?category=pokemon" style="flex:1 1 140px;min-width:130px;max-width:190px;background:#1a1a1a;border:1px solid rgba(212,175,55,0.12);border-radius:14px;padding:28px 16px 24px;text-align:center;text-decoration:none;display:block;">
                <div style="font-size:34px;margin-bottom:12px;line-height:1;">&#128293;</div>
                <div style="color:#ffffff;font-weight:700;font-size:13px;margin-bottom:4px;">Pokemon</div>
                <div style="color:rgba(255,255,255,0.28);font-size:11px;">Packs&#183;Boxes&#183;Singles</div>
            </a>

            <a href="/shop?category=magic-the-gathering" style="flex:1 1 140px;min-width:130px;max-width:190px;background:#1a1a1a;border:1px solid rgba(212,175,55,0.12);border-radius:14px;padding:28px 16px 24px;text-align:center;text-decoration:none;display:block;">
                <div style="font-size:34px;margin-bottom:12px;line-height:1;">&#9986;&#65039;</div>
                <div style="color:#ffffff;font-weight:700;font-size:13px;margin-bottom:4px;">MTG</div>
                <div style="color:rgba(255,255,255,0.28);font-size:11px;">Magic: The Gathering</div>
            </a>

            <a href="/shop?category=yu-gi-oh" style="flex:1 1 140px;min-width:130px;max-width:190px;background:#1a1a1a;border:1px solid rgba(212,175,55,0.12);border-radius:14px;padding:28px 16px 24px;text-align:center;text-decoration:none;display:block;">
                <div style="font-size:34px;margin-bottom:12px;line-height:1;">&#9876;&#65039;</div>
                <div style="color:#ffffff;font-weight:700;font-size:13px;margin-bottom:4px;">Yu-Gi-Oh!</div>
                <div style="color:rgba(255,255,255,0.28);font-size:11px;">Booster&#183;Singles</div>
            </a>

            <a href="/shop?category=graded-cards" style="flex:1 1 140px;min-width:130px;max-width:190px;background:#1a1a1a;border:1px solid rgba(212,175,55,0.12);border-radius:14px;padding:28px 16px 24px;text-align:center;text-decoration:none;display:block;">
                <div style="font-size:34px;margin-bottom:12px;line-height:1;">&#127942;&#65039;</div>
                <div style="color:#ffffff;font-weight:700;font-size:13px;margin-bottom:4px;">Graded Cards</div>
                <div style="color:rgba(255,255,255,0.28);font-size:11px;">PSA&#183;BGS&#183;CGC</div>
            </a>

            <a href="/shop?category=card-accessories" style="flex:1 1 140px;min-width:130px;max-width:190px;background:#1a1a1a;border:1px solid rgba(212,175,55,0.12);border-radius:14px;padding:28px 16px 24px;text-align:center;text-decoration:none;display:block;">
                <div style="font-size:34px;margin-bottom:12px;line-height:1;">&#128218;</div>
                <div style="color:#ffffff;font-weight:700;font-size:13px;margin-bottom:4px;">Accessories</div>
                <div style="color:rgba(255,255,255,0.28);font-size:11px;">Sleeves&#183;Binders&#183;Cases</div>
            </a>

        </div><!-- /flex -->

        <div style="text-align:center;margin-top:40px;">
            <a href="/shop" style="display:inline-block;color:#D4AF37;font-weight:700;font-size:14px;padding:12px 30px;border-radius:8px;text-decoration:none;border:1.5px solid rgba(212,175,55,0.35);">View All Products &#8594;</a>
        </div>

    </div>
</section>

<!-- ═══════════════════════════════════════════════════
     WHY SHOP WITH US  (4 columns flex)
═══════════════════════════════════════════════════ -->
<section style="background:#0a0a0a;padding:80px 0;">
    <div style="max-width:1200px;margin:0 auto;padding:0 32px;">

        <div style="text-align:center;margin-bottom:52px;">
            <h2 style="font-size:clamp(24px,3.5vw,32px);font-weight:900;color:#ffffff;margin:0 0 10px;">Why Shop at Long Island Cards?</h2>
        </div>

        <div style="display:flex;flex-wrap:wrap;gap:32px;justify-content:center;">

            <div style="flex:1 1 200px;min-width:180px;max-width:260px;text-align:center;">
                <div style="width:64px;height:64px;background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:16px;display:flex;align-items:center;justify-content:center;margin:0 auto 18px;font-size:28px;">&#127970;</div>
                <h4 style="color:#D4AF37;font-size:15px;font-weight:700;margin:0 0 8px;">Local Store</h4>
                <p style="color:rgba(255,255,255,0.4);font-size:13px;line-height:1.65;margin:0;">605 Old Country Rd, Plainview. Open 7 days a week.</p>
            </div>

            <div style="flex:1 1 200px;min-width:180px;max-width:260px;text-align:center;">
                <div style="width:64px;height:64px;background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:16px;display:flex;align-items:center;justify-content:center;margin:0 auto 18px;font-size:28px;">&#128230;</div>
                <h4 style="color:#D4AF37;font-size:15px;font-weight:700;margin:0 0 8px;">Fast Shipping</h4>
                <p style="color:rgba(255,255,255,0.4);font-size:13px;line-height:1.65;margin:0;">Same-day on orders before 3pm. Ships nationwide.</p>
            </div>

            <div style="flex:1 1 200px;min-width:180px;max-width:260px;text-align:center;">
                <div style="width:64px;height:64px;background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:16px;display:flex;align-items:center;justify-content:center;margin:0 auto 18px;font-size:28px;">&#9989;</div>
                <h4 style="color:#D4AF37;font-size:15px;font-weight:700;margin:0 0 8px;">100% Authentic</h4>
                <p style="color:rgba(255,255,255,0.4);font-size:13px;line-height:1.65;margin:0;">Sourced from authorized distributors. PSA/BGS verified.</p>
            </div>

            <div style="flex:1 1 200px;min-width:180px;max-width:260px;text-align:center;">
                <div style="width:64px;height:64px;background:rgba(212,175,55,0.08);border:1px solid rgba(212,175,55,0.2);border-radius:16px;display:flex;align-items:center;justify-content:center;margin:0 auto 18px;font-size:28px;">&#128176;</div>
                <h4 style="color:#D4AF37;font-size:15px;font-weight:700;margin:0 0 8px;">Best Prices</h4>
                <p style="color:rgba(255,255,255,0.4);font-size:13px;line-height:1.65;margin:0;">Competitive LI market pricing. In-store price match available.</p>
            </div>

        </div>

    </div>
</section>

<!-- ═══════════════════════════════════════════════════
     CTA BANNER
═══════════════════════════════════════════════════ -->
<section style="background:#D4AF37;padding:56px 24px;text-align:center;">
    <div style="max-width:600px;margin:0 auto;">
        <h2 style="font-size:clamp(22px,3.5vw,30px);font-weight:900;color:#000000;margin:0 0 12px;">Ready to Start Your Collection?</h2>
        <p style="color:rgba(0,0,0,0.5);font-size:15px;margin:0 0 28px;line-height:1.6;">Browse 500+ products. New inventory added weekly.</p>
        <a href="/shop" style="background:#000000;color:#D4AF37;font-weight:800;font-size:15px;padding:15px 48px;border-radius:8px;text-decoration:none;display:inline-block;letter-spacing:0.3px;">Shop the Full Collection</a>
    </div>
</section>

        </div>
    </xpath>
</data>'''


def main():
    m, uid = connect()

    print("\nUpdating homepage view 2955 with fixed layout...")
    xc(m, uid, 'ir.ui.view', 'write', [[2955], {
        'arch_db': HOMEPAGE,
        'active': True,
    }])
    print("Done. Hard refresh longislandcards.com (Ctrl+Shift+R)")

if __name__ == '__main__':
    main()
