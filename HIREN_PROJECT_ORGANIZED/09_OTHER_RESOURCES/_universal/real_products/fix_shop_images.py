#!/usr/bin/env python3
"""
Assign correct PrintAndMailImages to shop products via image_1920 field.
"""
import sys, base64, os, xmlrpc.client, time
sys.stdout.reconfigure(encoding="utf-8")

ODOO = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

IMG  = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\PrintAndMailImages"

common = xmlrpc.client.ServerProxy(f'{ODOO}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{ODOO}/xmlrpc/2/object')
print(f"Connected UID: {uid}")

def xc(model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

def b64img(filename):
    path = os.path.join(IMG, filename)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

# Load all images once
print("Loading images from PrintAndMailImages...")
imgs = {
    "biz_card_1": b64img("4-Free-Stacked-Business-Cards-Mockup-PSD-Set-1.jpg"),
    "biz_card_2": b64img("Stacked-Business-Card-Mockup.jpg"),
    "biz_card_3": b64img("Business-Card-Stack-Mockup.jpg"),
    "printer":    b64img("6Feet-Large-Format-Eco-Solvent-Printer-600x600.webp"),
    "flyers":     b64img("Mailing-flyers-1.jpg"),
    "mimage":     b64img("mimage1.jpg"),
    "direct_mail":b64img("Direct-mail-services-1.jpg"),
    "mail_hdr":   b64img("1668462597_mailing-header2-webp.jpg"),
}
print(f"  Loaded {len(imgs)} images OK")

# product_id -> image key (use each image for the most relevant product)
PRODUCT_IMAGES = {
    # Business Cards
    138: "biz_card_1",   # 250 Pack
    139: "biz_card_2",   # 500 Pack
    # Flyers & Brochures
    140: "flyers",       # Flyers 100 Pack
    141: "flyers",       # Flyers 250 Pack
    142: "flyers",       # Tri-Fold Brochure
    # Banners & Signs
    143: "printer",      # Vinyl Banner 2x4
    144: "printer",      # Vinyl Banner 3x6
    145: "mimage",       # Yard Signs
    146: "mimage",       # Roll-Up Banner Stand
    # Copying & Scanning
    147: "printer",      # Copying B&W
    148: "printer",      # Copying Color
    # Notary
    149: "biz_card_3",   # Notary Service
    # Scan to PDF
    150: "printer",      # Scan to PDF
    # Shipping
    151: "direct_mail",  # Shipping Box Small
    152: "mail_hdr",     # Shipping Box Medium
}

print(f"\nUpdating {len(PRODUCT_IMAGES)} product images...")
ok = 0
fail = 0
for pid, img_key in PRODUCT_IMAGES.items():
    try:
        result = xc("product.template", "write", [[pid], {"image_1920": imgs[img_key]}])
        status = "OK" if result else "FAIL"
        print(f"  [{pid}] {img_key}: {status}")
        if result:
            ok += 1
        else:
            fail += 1
    except Exception as e:
        print(f"  [{pid}] ERROR: {e}")
        fail += 1
    time.sleep(0.3)

print(f"\n{ok} updated, {fail} failed")

# Verify a few via HTTP
import requests
sess = requests.Session()
print("\nVerifying product images via HTTP...")
for pid in [138, 139, 140, 151, 152]:
    url = f"https://www.longislandprintandmail.com/web/image/product.template/{pid}/image_512"
    r = sess.get(url, timeout=15)
    sz = len(r.content)
    ct = r.headers.get("Content-Type", "?")[:20]
    ok_str = "OK" if sz > 10000 else "BROKEN"
    print(f"  product {pid}: HTTP {r.status_code} | {sz:,} bytes | {ct} | {ok_str}")

print("\nDONE — hard-refresh /shop")
