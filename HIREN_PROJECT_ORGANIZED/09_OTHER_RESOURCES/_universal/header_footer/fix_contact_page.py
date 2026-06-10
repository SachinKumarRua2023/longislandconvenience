#!/usr/bin/env python3
import xmlrpc.client, sys
sys.stdout.reconfigure(encoding='utf-8')

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
m   = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
def xc(model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

ARCH = (
    '<t name="Contact Us" t-name="website.lic_contact_page">'
    '<t t-call="website.layout">'
    '<div id="wrap" class="oe_structure">'

    # Hero
    '<section style="background:linear-gradient(135deg,#0a0f23 0%,#1a2550 100%);padding:60px 20px 50px;text-align:center;">'
    '<div style="max-width:800px;margin:0 auto;">'
    '<p style="font-size:11px;font-weight:700;letter-spacing:3px;color:#d4af37;text-transform:uppercase;margin:0 0 14px;">GET IN TOUCH</p>'
    '<h1 style="color:#fff;font-size:clamp(28px,5vw,48px);font-weight:800;margin:0 0 14px;">Contact Long Island Cards</h1>'
    '<p style="color:#aab8d4;font-size:17px;max-width:520px;margin:0 auto;">Questions about products, orders, or grading? We are here to help every day.</p>'
    '</div>'
    '</section>'

    # Main content
    '<section style="background:#f8f9fc;padding:60px 20px;">'
    '<div style="max-width:1100px;margin:0 auto;display:flex;flex-wrap:wrap;gap:40px;align-items:flex-start;">'

    # Left - form
    '<div style="flex:1 1 380px;min-width:300px;background:#fff;border-radius:16px;padding:40px;box-shadow:0 4px 24px rgba(0,0,0,0.08);">'
    '<h2 style="font-size:22px;font-weight:700;color:#0a0f23;margin:0 0 6px;">Send Us a Message</h2>'
    '<p style="color:#6b7280;font-size:14px;margin:0 0 28px;">We reply within 24 hours. You can also email us directly.</p>'
    '<div style="display:flex;flex-direction:column;gap:18px;">'
    '<div>'
    '<label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;">Full Name</label>'
    '<input type="text" style="width:100%;padding:11px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;box-sizing:border-box;" placeholder="John Smith"/>'
    '</div>'
    '<div>'
    '<label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;">Email Address</label>'
    '<input type="email" style="width:100%;padding:11px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;box-sizing:border-box;" placeholder="john@email.com"/>'
    '</div>'
    '<div>'
    '<label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;">Subject</label>'
    '<select style="width:100%;padding:11px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;background:#fff;box-sizing:border-box;">'
    '<option>Order / Shipping Question</option>'
    '<option>Product Inquiry</option>'
    '<option>Graded Card Question</option>'
    '<option>I Want to Sell Cards</option>'
    '<option>Bulk / Wholesale</option>'
    '<option>Other</option>'
    '</select>'
    '</div>'
    '<div>'
    '<label style="display:block;font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;">Message</label>'
    '<textarea rows="5" style="width:100%;padding:11px 14px;border:1.5px solid #e5e7eb;border-radius:8px;font-size:14px;box-sizing:border-box;resize:vertical;font-family:inherit;" placeholder="How can we help you?"></textarea>'
    '</div>'
    '<a href="mailto:info@longislandcards.com" style="display:block;text-align:center;background:#d4af37;color:#000;font-weight:700;font-size:15px;padding:14px 28px;border-radius:8px;text-decoration:none;">Send Message</a>'
    '<p style="font-size:12px;color:#9ca3af;text-align:center;margin:0;">Or email: <a href="mailto:info@longislandcards.com" style="color:#d4af37;">info@longislandcards.com</a></p>'
    '</div>'
    '</div>'

    # Right - info cards
    '<div style="flex:1 1 300px;min-width:260px;display:flex;flex-direction:column;gap:20px;">'

    '<div style="background:#fff;border-radius:14px;padding:28px;box-shadow:0 4px 18px rgba(0,0,0,0.07);border-left:4px solid #d4af37;">'
    '<h3 style="font-size:16px;font-weight:700;color:#0a0f23;margin:0 0 12px;">Visit Our Store</h3>'
    '<p style="color:#374151;font-size:14px;line-height:1.7;margin:0;"><strong>Long Island Cards</strong><br/>Plainview, New York 11803<br/>Long Island, NY</p>'
    '</div>'

    '<div style="background:#fff;border-radius:14px;padding:28px;box-shadow:0 4px 18px rgba(0,0,0,0.07);border-left:4px solid #10b981;">'
    '<h3 style="font-size:16px;font-weight:700;color:#0a0f23;margin:0 0 12px;">Store Hours</h3>'
    '<table style="width:100%;font-size:13px;border-collapse:collapse;">'
    '<tr><td style="color:#374151;padding:3px 0;">Monday - Friday</td><td style="color:#0a0f23;font-weight:600;text-align:right;">10 AM - 7 PM</td></tr>'
    '<tr><td style="color:#374151;padding:3px 0;">Saturday</td><td style="color:#0a0f23;font-weight:600;text-align:right;">10 AM - 6 PM</td></tr>'
    '<tr><td style="color:#374151;padding:3px 0;">Sunday</td><td style="color:#0a0f23;font-weight:600;text-align:right;">11 AM - 5 PM</td></tr>'
    '</table>'
    '<div style="margin-top:12px;background:#ecfdf5;border-radius:6px;padding:8px 12px;">'
    '<span style="color:#059669;font-size:12px;font-weight:600;">Open Today - Same-day dispatch before 3 PM</span>'
    '</div>'
    '</div>'

    '<div style="background:#fff;border-radius:14px;padding:28px;box-shadow:0 4px 18px rgba(0,0,0,0.07);border-left:4px solid #6366f1;">'
    '<h3 style="font-size:16px;font-weight:700;color:#0a0f23;margin:0 0 12px;">Contact Info</h3>'
    '<div style="display:flex;flex-direction:column;gap:10px;">'
    '<a href="mailto:info@longislandcards.com" style="color:#374151;text-decoration:none;font-size:14px;">Email: info@longislandcards.com</a>'
    '<a href="tel:+15163001234" style="color:#374151;text-decoration:none;font-size:14px;">Phone: (516) 300-1234</a>'
    '</div>'
    '</div>'

    '<div style="background:linear-gradient(135deg,#0a0f23,#1a2550);border-radius:14px;padding:28px;">'
    '<h3 style="color:#d4af37;font-size:15px;font-weight:700;margin:0 0 10px;">Shipping Info</h3>'
    '<ul style="color:#aab8d4;font-size:13px;line-height:1.8;margin:0;padding-left:16px;">'
    '<li>Free shipping on orders over <strong style="color:#fff;">$75</strong></li>'
    '<li>Same-day dispatch before <strong style="color:#fff;">3 PM</strong></li>'
    '<li>Tracked and insured shipping</li>'
    '<li>Ships across the <strong style="color:#fff;">USA</strong></li>'
    '</ul>'
    '</div>'

    '</div>'  # end right column
    '</div>'  # end flex container
    '</section>'

    # FAQ
    '<section style="background:#0a0f23;padding:50px 20px;">'
    '<div style="max-width:900px;margin:0 auto;text-align:center;">'
    '<h2 style="color:#fff;font-size:24px;font-weight:700;margin:0 0 8px;">Frequently Asked Questions</h2>'
    '<p style="color:#aab8d4;font-size:14px;margin:0 0 36px;">Quick answers to common questions</p>'
    '<div style="display:flex;flex-wrap:wrap;gap:20px;justify-content:center;text-align:left;">'
    '<div style="flex:1 1 250px;min-width:220px;background:#111827;border-radius:12px;padding:22px;">'
    '<h4 style="color:#d4af37;font-size:14px;font-weight:700;margin:0 0 8px;">Do you buy cards?</h4>'
    '<p style="color:#9ca3af;font-size:13px;line-height:1.6;margin:0;">Yes! We buy singles, collections, and graded cards. Contact us with photos for a quote.</p>'
    '</div>'
    '<div style="flex:1 1 250px;min-width:220px;background:#111827;border-radius:12px;padding:22px;">'
    '<h4 style="color:#d4af37;font-size:14px;font-weight:700;margin:0 0 8px;">Do you do card grading?</h4>'
    '<p style="color:#9ca3af;font-size:13px;line-height:1.6;margin:0;">We help submit cards to PSA and BGS. Ask us about our group submission service.</p>'
    '</div>'
    '<div style="flex:1 1 250px;min-width:220px;background:#111827;border-radius:12px;padding:22px;">'
    '<h4 style="color:#d4af37;font-size:14px;font-weight:700;margin:0 0 8px;">Can I pick up in store?</h4>'
    '<p style="color:#9ca3af;font-size:13px;line-height:1.6;margin:0;">Yes, local pickup is available in Plainview, NY. Select Local Pickup at checkout.</p>'
    '</div>'
    '<div style="flex:1 1 250px;min-width:220px;background:#111827;border-radius:12px;padding:22px;">'
    '<h4 style="color:#d4af37;font-size:14px;font-weight:700;margin:0 0 8px;">What is your return policy?</h4>'
    '<p style="color:#9ca3af;font-size:13px;line-height:1.6;margin:0;">Sealed products: 30-day unopened returns. Singles and graded: 7-day return on misrepresented items.</p>'
    '</div>'
    '</div>'
    '</div>'
    '</section>'

    '</div></t></t>'
)

result = xc('ir.ui.view', 'write', [[3510], {'arch_db': ARCH}])
print('View 3510 updated:', result)
print('Visit: https://www.longislandcards.com/contact')
