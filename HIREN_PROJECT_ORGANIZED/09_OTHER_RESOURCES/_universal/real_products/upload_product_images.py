#!/usr/bin/env python3
"""
Generate and upload product images for Long Island Cards.
Uses PIL to create professional branded images for each product.
"""
import xmlrpc.client, sys, base64, io, math
from PIL import Image, ImageDraw, ImageFont

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

def connect():
    uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
    if not uid: sys.exit("Auth failed")
    m = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    return m, uid

def xc(m, uid, model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

# ── Color palettes per category ──────────────────────────────
THEMES = {
    'sports':    {'bg': (10, 15, 35),    'accent': (220, 40, 60),   'card': (20, 30, 60),   'icon': '⚾'},
    'basketball':{'bg': (25, 12, 5),     'accent': (255, 100, 20),  'card': (45, 22, 8),    'icon': '🏀'},
    'baseball':  {'bg': (5, 20, 50),     'accent': (30, 100, 210),  'card': (10, 35, 80),   'icon': '⚾'},
    'football':  {'bg': (10, 25, 10),    'accent': (50, 180, 50),   'card': (15, 40, 15),   'icon': '🏈'},
    'hockey':    {'bg': (5, 15, 35),     'accent': (60, 160, 255),  'card': (10, 25, 55),   'icon': '🏒'},
    'pokemon':   {'bg': (30, 5, 5),      'accent': (255, 215, 0),   'card': (55, 10, 10),   'icon': '⚡'},
    'mtg':       {'bg': (15, 5, 30),     'accent': (150, 80, 255),  'card': (28, 10, 55),   'icon': '✦'},
    'yugioh':    {'bg': (5, 10, 30),     'accent': (100, 180, 255), 'card': (8, 18, 55),    'icon': '⭐'},
    'onepiece':  {'bg': (25, 5, 5),      'accent': (255, 80, 30),   'card': (50, 10, 5),    'icon': '☠'},
    'graded':    {'bg': (8, 8, 8),       'accent': (212, 175, 55),  'card': (18, 18, 18),   'icon': '🏆'},
    'accessories':{'bg': (12, 12, 20),   'accent': (160, 160, 180), 'card': (22, 22, 35),   'icon': '📦'},
    'sealed':    {'bg': (5, 20, 5),      'accent': (80, 210, 80),   'card': (8, 35, 8),     'icon': '📦'},
    'default':   {'bg': (10, 10, 18),    'accent': (212, 175, 55),  'card': (20, 20, 35),   'icon': '🎴'},
}

def hex_lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i]-c1[i])*t) for i in range(3))

def draw_gradient(draw, w, h, c1, c2):
    for y in range(h):
        t = y / h
        r = int(c1[0]*(1-t) + c2[0]*t)
        g = int(c1[1]*(1-t) + c2[1]*t)
        b = int(c1[2]*(1-t) + c2[2]*t)
        draw.line([(0,y),(w,y)], fill=(r,g,b))

def draw_card_art(draw, W, H, theme):
    """Draw decorative card art in the upper portion"""
    A = theme['accent']
    C = theme['card']
    gold = (212, 175, 55)

    # Card background panel
    pad = 40
    draw.rounded_rectangle([pad, pad, W-pad, int(H*0.58)], radius=20,
        fill=C, outline=A, width=2)

    # Geometric pattern inside card
    cx, cy = W//2, int(H*0.29)
    r = min(W,H)//6

    # Outer glow ring
    for i in range(8, 0, -1):
        alpha = int(25 * i/8)
        ring_col = (A[0], A[1], A[2])
        draw.ellipse([cx-r-i*5, cy-r-i*5, cx+r+i*5, cy+r+i*5],
            outline=ring_col, width=1)

    # Center circle
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=A)

    # Inner pattern - 6 rays
    import math
    for i in range(6):
        angle = math.radians(i * 60)
        x1 = cx + int((r+10) * math.cos(angle))
        y1 = cy + int((r+10) * math.sin(angle))
        x2 = cx + int((r+55) * math.cos(angle))
        y2 = cy + int((r+55) * math.sin(angle))
        draw.line([x1,y1,x2,y2], fill=gold, width=3)

    # Stars in corners of card panel
    star_pos = [(pad+30, pad+30), (W-pad-30, pad+30), (pad+30, int(H*0.58)-30), (W-pad-30, int(H*0.58)-30)]
    for sx, sy in star_pos:
        draw.regular_polygon((sx, sy, 8), 4, rotation=45, fill=gold)

def make_product_image(name, price, category, theme_key, size=(800,800)):
    W, H = size
    theme = THEMES.get(theme_key, THEMES['default'])
    gold = (212, 175, 55)
    white = (255, 255, 255)
    dark = (0, 0, 0)

    img = Image.new('RGB', (W, H), theme['bg'])
    draw = ImageDraw.Draw(img)

    # Background gradient
    bg2 = tuple(min(255, c+20) for c in theme['bg'])
    draw_gradient(draw, W, H, theme['bg'], bg2)

    # Card art
    draw_card_art(draw, W, H, theme)

    # Gold accent line
    draw.rectangle([0, int(H*0.62), W, int(H*0.62)+3], fill=gold)

    # Bottom info panel
    panel_y = int(H*0.62)+3
    draw.rectangle([0, panel_y, W, H], fill=(8, 8, 8))

    # Product name - word wrap
    try:
        font_lg = ImageFont.truetype("arial.ttf", 34)
        font_md = ImageFont.truetype("arial.ttf", 22)
        font_sm = ImageFont.truetype("arial.ttf", 17)
        font_xs = ImageFont.truetype("arial.ttf", 14)
    except:
        try:
            font_lg = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 34)
            font_md = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
            font_sm = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 17)
            font_xs = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
        except:
            font_lg = ImageFont.load_default()
            font_md = font_lg
            font_sm = font_lg
            font_xs = font_lg

    # Wrap text to fit width
    def wrap_text(text, font, max_w):
        words = text.split()
        lines = []
        line = []
        for word in words:
            test = ' '.join(line + [word])
            bb = draw.textbbox((0,0), test, font=font)
            if bb[2] - bb[0] <= max_w:
                line.append(word)
            else:
                if line:
                    lines.append(' '.join(line))
                line = [word]
        if line:
            lines.append(' '.join(line))
        return lines

    max_w = W - 60
    lines = wrap_text(name, font_lg, max_w)
    if len(lines) > 2:
        lines = wrap_text(name, font_md, max_w)
        name_font = font_md
    else:
        name_font = font_lg

    # Draw name lines
    text_y = panel_y + 22
    for line in lines[:3]:
        bb = draw.textbbox((0,0), line, font=name_font)
        tw = bb[2] - bb[0]
        draw.text(((W-tw)//2, text_y), line, font=name_font, fill=white)
        text_y += (bb[3]-bb[1]) + 6

    # Price
    price_text = f"${price:.2f}"
    bb = draw.textbbox((0,0), price_text, font=font_lg)
    tw = bb[2]-bb[0]
    draw.text(((W-tw)//2, text_y+8), price_text, font=font_lg, fill=gold)

    # Category tag
    cat_y = H - 40
    cat_text = category.upper()
    bb = draw.textbbox((0,0), cat_text, font=font_xs)
    tw = bb[2]-bb[0]
    # tag bg
    draw.rounded_rectangle([(W-tw)//2 - 12, cat_y-6, (W+tw)//2+12, cat_y+20],
        radius=8, fill=theme['accent'])
    draw.text(((W-tw)//2, cat_y), cat_text, font=font_xs, fill=dark)

    # Brand watermark top-right corner
    brand = "LONG ISLAND CARDS"
    bb = draw.textbbox((0,0), brand, font=font_xs)
    draw.text((W - (bb[2]-bb[0]) - 16, 16), brand, font=font_xs,
              fill=tuple(int(c*0.4) for c in gold))

    return img

def img_to_b64(img):
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=90)
    return base64.b64encode(buf.getvalue()).decode()

# ── Product list: (id, name, price, theme_key, category_label)
PRODUCTS = [
    (117, "2024-25 Panini Prizm Basketball Hobby Box",       189.99, 'basketball', 'Basketball'),
    (118, "2024 Topps Baseball Series 1 Hobby Box",          99.99,  'baseball',   'Baseball'),
    (119, "2024-25 Panini Donruss Football Hobby Box",       119.99, 'football',   'Football'),
    (120, "2024-25 Upper Deck Hockey Series 1 Hobby Box",    89.99,  'hockey',     'Hockey'),
    (121, "Pokemon Prismatic Evolutions Booster Box",        169.99, 'pokemon',    'Pokemon'),
    (122, "Pokemon Elite Trainer Box — Scarlet & Violet",    59.99,  'pokemon',    'Pokemon ETB'),
    (123, "Pokemon Single Booster Pack",                     5.99,   'pokemon',    'Pokemon'),
    (124, "Pokemon Charizard ex PSA 10 — Obsidian Flames",   349.99, 'graded',     'PSA 10 Graded'),
    (125, "MTG Duskmourn Draft Booster Box",                 124.99, 'mtg',        'Magic: The Gathering'),
    (126, "MTG Commander Precon Deck",                       44.99,  'mtg',        'MTG Commander'),
    (127, "Yu-Gi-Oh! Burst Protocol Booster Box",            89.99,  'yugioh',     'Yu-Gi-Oh!'),
    (128, "Yu-Gi-Oh! Blue-Eyes White Dragon PSA 9",          199.99, 'graded',     'PSA 9 Graded'),
    (129, "One Piece Two Legends Booster Box",               99.99,  'onepiece',   'One Piece'),
    (130, "Mike Trout 2011 Topps Update Rookie PSA 10",      499.99, 'graded',     'PSA 10 Graded'),
    (131, "Luka Doncic 2018-19 Panini Prizm Rookie BGS 9.5", 379.99, 'graded',     'BGS 9.5 Graded'),
    (132, "Ultra Pro 9-Pocket Binder (360 cards)",           19.99,  'accessories','Card Accessories'),
    (133, "Top Loaders 3x4 inch — 25 Pack",                  7.99,   'accessories','Accessories'),
    (134, "Perfect Fit Inner Sleeves — 100 Pack",            4.99,   'accessories','Accessories'),
    (135, "Bicycle Playing Cards — 2 Deck Set",              9.99,   'accessories','Playing Cards'),
    (136, "Long Island Cards Sports Starter Pack",           49.99,  'sports',     'Sports Bundle'),
    (137, "Long Island Cards TCG Starter Bundle",            39.99,  'pokemon',    'TCG Bundle'),
]

def main():
    m, uid = connect()
    print(f"Connected. Generating + uploading {len(PRODUCTS)} product images...\n")

    done = 0
    for pid, name, price, theme, cat_label in PRODUCTS:
        try:
            img = make_product_image(name, price, cat_label, theme)
            b64 = img_to_b64(img)
            xc(m, uid, 'product.template', 'write', [[pid], {
                'image_1920': b64,
            }])
            print(f"  [{pid}] {name[:48]}")
            done += 1
        except Exception as e:
            print(f"  FAIL [{pid}]: {str(e)[:80]}")

    print(f"\nDone: {done}/{len(PRODUCTS)} images uploaded.")
    print("Hard refresh the shop page to see product images.")

if __name__ == '__main__':
    main()
