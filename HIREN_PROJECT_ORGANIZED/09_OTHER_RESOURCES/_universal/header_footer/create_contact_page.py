#!/usr/bin/env python3
"""Create a /contact page for Long Island Cards (website 36)."""
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

CONTACT_ARCH = """<odoo>
<template id="lic_contact_page" name="Long Island Cards - Contact">
  <t t-call="website.layout">
    <t t-set="pageName" t-value="'contact'"/>
    <div id="wrap" class="oe_structure">

      <!-- Hero Banner -->
      <section style="background:linear-gradient(135deg,#0a0f23 0%,#1a2550 100%);padding:60px 20px 50px;text-align:center;">
        <div style="max-width:800px;margin:0 auto;">
          <div style="display:inline-block;background:#d4af37;color:#000;font-size:11px;font-weight:700;letter-spacing:3px;padding:5px 18px;border-radius:20px;margin-bottom:18px;">GET IN TOUCH</div>
          <h1 style="color:#fff;font-size:clamp(28px,5vw,48px);font-weight:800;margin:0 0 14px;">Contact Long Island Cards</h1>
          <p style="color:#aab8d4;font-size:17px;max-width:520px;margin:0 auto;">Questions about products, orders, or grading? We&#39;re here to help every day.</p>
        </div>
      </section>

      <!-- Main Content -->
      <section style="background:#f8f9fc;padding:60px 20px;">
        <div style="max-width:1100px;margin:0 auto;display:flex;flex-wrap:wrap;gap:40px;align-items:flex-start;">

          <!-- Left: Contact Form -->
          <div style="flex:1 1 380px;min-width:300px;background:#fff;border-radius:16px;padding:40px;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
            <h2 style="font-size:22px;font-weight:700;color:#0a0f23;margin:0 0 6px;">Send Us a Message</h2>
            <p style="color:#6b7280;font-size:14px;margin:0 0 28px;">We reply within 24 hours on business days.</p>

            <form action="/web/dataset/call_kw" method="post" style="display:flex;flex-direction:column;gap:18px;">
              <div>
                <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;">Full Name *</label>
                <input type="text" name="contact_name" required="required"
                  style="width:100%;padding:11px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;box-sizing:border-box;outline:none;transition:border-color .2s;"
                  onfocus="this.style.borderColor='#d4af37'" onblur="this.style.borderColor='#e5e7eb'"
                  placeholder="John Smith"/>
              </div>
              <div>
                <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;">Email Address *</label>
                <input type="email" name="contact_email" required="required"
                  style="width:100%;padding:11px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;box-sizing:border-box;outline:none;transition:border-color .2s;"
                  onfocus="this.style.borderColor='#d4af37'" onblur="this.style.borderColor='#e5e7eb'"
                  placeholder="john@email.com"/>
              </div>
              <div>
                <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;">Subject</label>
                <select name="contact_subject"
                  style="width:100%;padding:11px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;box-sizing:border-box;background:#fff;outline:none;">
                  <option value="order">Order / Shipping Question</option>
                  <option value="product">Product Inquiry</option>
                  <option value="graded">Graded Card Question</option>
                  <option value="sell">I Want to Sell Cards</option>
                  <option value="bulk">Bulk / Wholesale</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;">Message *</label>
                <textarea name="contact_message" required="required" rows="5"
                  style="width:100%;padding:11px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;box-sizing:border-box;resize:vertical;outline:none;transition:border-color .2s;font-family:inherit;"
                  onfocus="this.style.borderColor='#d4af37'" onblur="this.style.borderColor='#e5e7eb'"
                  placeholder="How can we help you?"></textarea>
              </div>
              <a href="mailto:info@longislandcards.com"
                style="display:block;text-align:center;background:#d4af37;color:#000;font-weight:700;font-size:15px;padding:14px 28px;border-radius:8px;text-decoration:none;letter-spacing:.5px;transition:opacity .2s;"
                onmouseover="this.style.opacity='.85'" onmouseout="this.style.opacity='1'">
                Send Message &#8594;
              </a>
              <p style="font-size:12px;color:#9ca3af;text-align:center;margin:0;">Or email us directly at <a href="mailto:info@longislandcards.com" style="color:#d4af37;">info@longislandcards.com</a></p>
            </form>
          </div>

          <!-- Right: Info Cards -->
          <div style="flex:1 1 300px;min-width:260px;display:flex;flex-direction:column;gap:20px;">

            <!-- Visit Us -->
            <div style="background:#fff;border-radius:14px;padding:28px;box-shadow:0 4px 18px rgba(0,0,0,0.07);border-left:4px solid #d4af37;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
                <div style="width:42px;height:42px;background:#fef9e7;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;">&#128205;</div>
                <h3 style="font-size:16px;font-weight:700;color:#0a0f23;margin:0;">Visit Our Store</h3>
              </div>
              <p style="color:#374151;font-size:14px;line-height:1.7;margin:0;">
                <strong>Long Island Cards</strong><br/>
                Plainview, New York 11803<br/>
                Long Island, NY
              </p>
            </div>

            <!-- Hours -->
            <div style="background:#fff;border-radius:14px;padding:28px;box-shadow:0 4px 18px rgba(0,0,0,0.07);border-left:4px solid #10b981;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
                <div style="width:42px;height:42px;background:#ecfdf5;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;">&#128337;</div>
                <h3 style="font-size:16px;font-weight:700;color:#0a0f23;margin:0;">Store Hours</h3>
              </div>
              <table style="width:100%;font-size:13px;border-collapse:collapse;">
                <tr><td style="color:#374151;padding:3px 0;">Monday – Friday</td><td style="color:#0a0f23;font-weight:600;text-align:right;">10 AM – 7 PM</td></tr>
                <tr><td style="color:#374151;padding:3px 0;">Saturday</td><td style="color:#0a0f23;font-weight:600;text-align:right;">10 AM – 6 PM</td></tr>
                <tr><td style="color:#374151;padding:3px 0;">Sunday</td><td style="color:#0a0f23;font-weight:600;text-align:right;">11 AM – 5 PM</td></tr>
              </table>
              <div style="margin-top:12px;background:#ecfdf5;border-radius:6px;padding:8px 12px;">
                <span style="color:#059669;font-size:12px;font-weight:600;">&#9679; Open Today — Same-day dispatch before 3 PM</span>
              </div>
            </div>

            <!-- Contact Info -->
            <div style="background:#fff;border-radius:14px;padding:28px;box-shadow:0 4px 18px rgba(0,0,0,0.07);border-left:4px solid #6366f1;">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
                <div style="width:42px;height:42px;background:#eef2ff;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px;">&#128222;</div>
                <h3 style="font-size:16px;font-weight:700;color:#0a0f23;margin:0;">Contact Info</h3>
              </div>
              <div style="display:flex;flex-direction:column;gap:10px;">
                <a href="mailto:info@longislandcards.com" style="display:flex;align-items:center;gap:10px;color:#374151;text-decoration:none;font-size:14px;">
                  <span style="color:#6366f1;font-size:16px;">&#9993;</span> info@longislandcards.com
                </a>
                <a href="tel:+15163001234" style="display:flex;align-items:center;gap:10px;color:#374151;text-decoration:none;font-size:14px;">
                  <span style="color:#6366f1;font-size:16px;">&#128222;</span> (516) 300-1234
                </a>
              </div>
            </div>

            <!-- Shipping Note -->
            <div style="background:linear-gradient(135deg,#0a0f23,#1a2550);border-radius:14px;padding:28px;">
              <h3 style="color:#d4af37;font-size:15px;font-weight:700;margin:0 0 10px;">&#128666; Shipping Info</h3>
              <ul style="color:#aab8d4;font-size:13px;line-height:1.8;margin:0;padding-left:16px;">
                <li>Free shipping on orders over <strong style="color:#fff;">$75</strong></li>
                <li>Same-day dispatch before <strong style="color:#fff;">3 PM</strong></li>
                <li>Tracked &amp; insured shipping</li>
                <li>Ships across the <strong style="color:#fff;">USA</strong></li>
              </ul>
            </div>

          </div>
        </div>
      </section>

      <!-- FAQ Strip -->
      <section style="background:#0a0f23;padding:50px 20px;">
        <div style="max-width:900px;margin:0 auto;text-align:center;">
          <h2 style="color:#fff;font-size:24px;font-weight:700;margin:0 0 8px;">Frequently Asked Questions</h2>
          <p style="color:#aab8d4;font-size:14px;margin:0 0 36px;">Quick answers to common questions</p>
          <div style="display:flex;flex-wrap:wrap;gap:20px;justify-content:center;text-align:left;">
            <div style="flex:1 1 250px;min-width:220px;background:#111827;border-radius:12px;padding:22px;">
              <h4 style="color:#d4af37;font-size:14px;font-weight:700;margin:0 0 8px;">Do you buy cards?</h4>
              <p style="color:#9ca3af;font-size:13px;line-height:1.6;margin:0;">Yes! We buy singles, collections, and graded cards. Contact us with photos for a quote.</p>
            </div>
            <div style="flex:1 1 250px;min-width:220px;background:#111827;border-radius:12px;padding:22px;">
              <h4 style="color:#d4af37;font-size:14px;font-weight:700;margin:0 0 8px;">Do you do card grading?</h4>
              <p style="color:#9ca3af;font-size:13px;line-height:1.6;margin:0;">We help submit cards to PSA and BGS. Ask us about our group submission service.</p>
            </div>
            <div style="flex:1 1 250px;min-width:220px;background:#111827;border-radius:12px;padding:22px;">
              <h4 style="color:#d4af37;font-size:14px;font-weight:700;margin:0 0 8px;">Can I pick up in store?</h4>
              <p style="color:#9ca3af;font-size:13px;line-height:1.6;margin:0;">Yes, local pickup is available in Plainview, NY. Select "Local Pickup" at checkout.</p>
            </div>
            <div style="flex:1 1 250px;min-width:220px;background:#111827;border-radius:12px;padding:22px;">
              <h4 style="color:#d4af37;font-size:14px;font-weight:700;margin:0 0 8px;">What&#39;s your return policy?</h4>
              <p style="color:#9ca3af;font-size:13px;line-height:1.6;margin:0;">Sealed products: 30-day unopened returns. Singles and graded: 7-day return on misrepresented items.</p>
            </div>
          </div>
        </div>
      </section>

    </div>
  </t>
</template>
</odoo>"""

def main():
    m, uid = connect()

    # Check if contact page already exists for website 36
    existing_pages = xc(m, uid, 'website.page', 'search_read',
        [[('url','=','/contact'), ('website_id','=',SITE_ID)]],
        {'fields':['id','name','view_id']})

    if existing_pages:
        print(f"Contact page already exists for site 36: {existing_pages}")
        # Update the view
        view_id = existing_pages[0]['view_id'][0]
        xc(m, uid, 'ir.ui.view', 'write', [[view_id], {'arch_db': CONTACT_ARCH}])
        xc(m, uid, 'website.page', 'write', [[existing_pages[0]['id']], {
            'is_published': True,
            'website_id': SITE_ID,
        }])
        print(f"Updated existing contact page view {view_id}")
        return

    # Create new ir.ui.view
    view_id = xc(m, uid, 'ir.ui.view', 'create', [{
        'name': 'Long Island Cards - Contact',
        'type': 'qweb',
        'key': 'website.lic_contact_page',
        'arch_db': CONTACT_ARCH,
        'website_id': SITE_ID,
    }])
    print(f"Created view ID {view_id}")

    # Create website.page pointing to that view
    page_id = xc(m, uid, 'website.page', 'create', [{
        'name': 'Contact Us',
        'url': '/contact',
        'view_id': view_id,
        'website_id': SITE_ID,
        'is_published': True,
        'website_indexed': True,
    }])
    print(f"Created page ID {page_id}")
    print("Contact page live at: https://www.longislandcards.com/contact")

if __name__ == '__main__':
    main()
