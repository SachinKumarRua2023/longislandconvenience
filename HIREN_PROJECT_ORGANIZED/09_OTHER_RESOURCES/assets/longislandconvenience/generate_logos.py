"""
generate_logos.py
─────────────────
Generates modern branded logos + .ico favicons for all 6 Long Island websites.
Output: PNG logos (600x200) + ICO favicons (64x64) in this folder.
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = os.path.dirname(os.path.abspath(__file__))

# ── Font paths ────────────────────────────────────────────────────────────────
FONT_BOLD   = 'C:/Windows/Fonts/segoeuib.ttf'
FONT_REG    = 'C:/Windows/Fonts/segoeui.ttf'
FONT_LIGHT  = 'C:/Windows/Fonts/segoeuil.ttf'

# ── Brand configs ─────────────────────────────────────────────────────────────
BRANDS = [
    {
        'file':    'lic',
        'name':    'Long Island',
        'sub':     'Convenience',
        'tagline': 'Your One-Stop Local Shop · Plainview, NY',
        'icon':    '🏪',
        'color1':  (230, 57,  70),   # #E63946 red
        'color2':  (180, 30,  40),   # darker red
        'bg':      (15,  15,  25),   # near black
        'text':    (255, 255, 255),
        'accent':  (230, 57,  70),
    },
    {
        'file':    'lic_cards',
        'name':    'Long Island',
        'sub':     'Cards',
        'tagline': 'Sports Cards & Collectibles · Plainview, NY',
        'icon':    '♦',
        'color1':  (212, 175, 55),   # #D4AF37 gold
        'color2':  (160, 120, 20),   # darker gold
        'bg':      (10,  10,  18),
        'text':    (255, 255, 255),
        'accent':  (212, 175, 55),
    },
    {
        'file':    'lic_giftbasket',
        'name':    'Long Island',
        'sub':     'Gift Basket',
        'tagline': 'Custom Gift Baskets · Plainview, NY',
        'icon':    '🎁',
        'color1':  (45,  106, 79),   # #2D6A4F forest green
        'color2':  (27,  67,  50),   # darker green
        'bg':      (8,   18,  8),
        'text':    (255, 255, 255),
        'accent':  (45,  106, 79),
    },
    {
        'file':    'lic_balloons',
        'name':    'Long Island',
        'sub':     'Balloons & Decor',
        'tagline': 'Events · Weddings · Celebrations · Plainview, NY',
        'icon':    '●',
        'color1':  (199, 125, 255),  # #C77DFF lavender
        'color2':  (140, 70,  200),  # deeper purple
        'bg':      (10,  8,   20),
        'text':    (255, 255, 255),
        'accent':  (199, 125, 255),
    },
    {
        'file':    'lic_printmail',
        'name':    'Long Island',
        'sub':     'Print & Mail',
        'tagline': 'Same-Day Printing · Shipping · Plainview, NY',
        'icon':    '▲',
        'color1':  (67,  97,  238),  # #4361EE blue
        'color2':  (30,  60,  180),  # darker blue
        'bg':      (8,   10,  20),
        'text':    (255, 255, 255),
        'accent':  (67,  97,  238),
    },
    {
        'file':    'jhd_advisor',
        'name':    'JHD',
        'sub':     'Advisor',
        'tagline': 'AI-First Digital Agency · Long Island, NY',
        'icon':    '◆',
        'color1':  (138, 43,  226),  # #8A2BE2 purple
        'color2':  (67,  97,  238),  # #4361EE blue
        'bg':      (5,   5,   5),
        'text':    (255, 255, 255),
        'accent':  (138, 43,  226),
    },
]

# ── Helper: draw rounded rectangle ───────────────────────────────────────────
def rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0+radius, y0, x1-radius, y1], fill=fill)
    draw.rectangle([x0, y0+radius, x1, y1-radius], fill=fill)
    draw.ellipse([x0, y0, x0+2*radius, y0+2*radius], fill=fill)
    draw.ellipse([x1-2*radius, y0, x1, y0+2*radius], fill=fill)
    draw.ellipse([x0, y1-2*radius, x0+2*radius, y1], fill=fill)
    draw.ellipse([x1-2*radius, y1-2*radius, x1, y1], fill=fill)

# ── Helper: vertical gradient background ─────────────────────────────────────
def gradient_bg(img, color_top, color_bottom):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        t = y / h
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * t)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * t)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

# ── Helper: horizontal gradient for accent bar ───────────────────────────────
def horiz_gradient_rect(img, xy, color_left, color_right):
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = xy
    for x in range(x0, x1):
        t = (x - x0) / max(1, x1 - x0)
        r = int(color_left[0] + (color_right[0] - color_left[0]) * t)
        g = int(color_left[1] + (color_right[1] - color_left[1]) * t)
        b = int(color_left[2] + (color_right[2] - color_left[2]) * t)
        draw.line([(x, y0), (x, y1)], fill=(r, g, b))

# ── Generate PNG logo (600x200) ───────────────────────────────────────────────
def make_logo(brand):
    W, H = 600, 200
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))

    # Background gradient
    bg_top    = tuple(min(255, c + 15) for c in brand['bg'])
    bg_bottom = brand['bg']
    gradient_bg(img, bg_top, bg_bottom)

    draw = ImageDraw.Draw(img)

    # Left accent bar (vertical gradient strip)
    horiz_gradient_rect(img, (0, 0, 6, H), brand['color1'], brand['color2'])

    # Glowing circle icon area on left
    cx, cy, cr = 80, H // 2, 42
    # outer glow rings
    for i in range(4, 0, -1):
        alpha = int(40 * i / 4)
        glow_color = brand['color1'] + (alpha,)
        glow_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow_img)
        gd.ellipse([cx-cr-i*6, cy-cr-i*6, cx+cr+i*6, cy+cr+i*6], fill=glow_color)
        img = Image.alpha_composite(img, glow_img)
        draw = ImageDraw.Draw(img)

    # Solid circle background
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=brand['color1'])
    # Inner lighter circle
    draw.ellipse([cx-cr+4, cy-cr+4, cx+cr-4, cy+cr-4], fill=brand['color2'])

    # Icon letter in circle (use first letter of sub as bold icon)
    try:
        icon_font = ImageFont.truetype(FONT_BOLD, 38)
    except:
        icon_font = ImageFont.load_default()
    icon_char = brand['sub'][0].upper()
    bbox = draw.textbbox((0,0), icon_char, font=icon_font)
    iw = bbox[2] - bbox[0]
    ih = bbox[3] - bbox[1]
    draw.text((cx - iw//2, cy - ih//2 - 2), icon_char,
              font=icon_font, fill=(255, 255, 255, 230))

    # Brand name (top part — "Long Island" or "JHD")
    try:
        name_font = ImageFont.truetype(FONT_LIGHT, 22)
        sub_font  = ImageFont.truetype(FONT_BOLD, 38)
        tag_font  = ImageFont.truetype(FONT_REG, 13)
    except:
        name_font = sub_font = tag_font = ImageFont.load_default()

    text_x = 145

    # Top label (e.g. "Long Island")
    draw.text((text_x, 38), brand['name'],
              font=name_font, fill=(200, 200, 200, 220))

    # Main brand name (e.g. "Convenience") in accent color
    draw.text((text_x, 62), brand['sub'],
              font=sub_font, fill=brand['color1'])

    # Thin separator line
    sep_y = 118
    horiz_gradient_rect(img, (text_x, sep_y, text_x + 280, sep_y + 2),
                        brand['color1'], brand['bg'])

    # Tagline
    draw.text((text_x, 128), brand['tagline'],
              font=tag_font, fill=(140, 140, 150, 200))

    # Decorative dots (bottom right)
    dot_colors = [brand['color1'], brand['color2']]
    for i, (dx, dy) in enumerate([(520,160),(540,148),(560,160),(550,175),(530,178)]):
        dc = dot_colors[i % 2] + (80,)
        dot_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(dot_img)
        r2 = 5 - (i % 2)
        dd.ellipse([dx-r2, dy-r2, dx+r2, dy+r2], fill=dc)
        img = Image.alpha_composite(img, dot_img)
        draw = ImageDraw.Draw(img)

    # Corner accent square (bottom right)
    for i in range(3):
        sq = 8 - i*2
        sx, sy = W - 30 + i*6, H - 30 + i*6
        draw.rectangle([sx, sy, sx+sq, sy+sq], fill=brand['color1'] + (100 - i*25,))

    return img


# ── Generate ICO favicon (64x64 multi-size) ───────────────────────────────────
def make_favicon(brand):
    sizes = [16, 32, 48, 64]
    images = []
    for sz in sizes:
        img = Image.new('RGBA', (sz, sz), (0,0,0,0))
        # Background circle
        gradient_bg(img, tuple(min(255,c+20) for c in brand['bg']), brand['bg'])
        draw = ImageDraw.Draw(img)
        # Colored circle
        pad = max(1, sz//10)
        draw.ellipse([pad, pad, sz-pad, sz-pad], fill=brand['color1'])
        draw.ellipse([pad+sz//8, pad+sz//8, sz-pad-sz//8, sz-pad-sz//8],
                     fill=brand['color2'])
        # Letter
        try:
            fsize = max(8, int(sz * 0.45))
            fnt = ImageFont.truetype(FONT_BOLD, fsize)
        except:
            fnt = ImageFont.load_default()
        ch = brand['sub'][0].upper()
        bbox = draw.textbbox((0,0), ch, font=fnt)
        tw = bbox[2]-bbox[0]; th = bbox[3]-bbox[1]
        draw.text(((sz-tw)//2, (sz-th)//2 - sz//16), ch,
                  font=fnt, fill=(255,255,255,240))
        images.append(img.convert('RGBA'))
    return images


# ── Main ──────────────────────────────────────────────────────────────────────
print('Generating logos and favicons...\n')
for brand in BRANDS:
    # PNG logo
    logo = make_logo(brand)
    png_path = os.path.join(OUT, f'{brand["file"]}_logo.png')
    logo.save(png_path, 'PNG')
    print(f'  Logo saved:   {brand["file"]}_logo.png')

    # ICO favicon
    favicon_imgs = make_favicon(brand)
    ico_path = os.path.join(OUT, f'{brand["file"]}_favicon.ico')
    favicon_imgs[0].save(
        ico_path, format='ICO',
        sizes=[(16,16),(32,32),(48,48),(64,64)],
        append_images=favicon_imgs[1:]
    )
    print(f'  Favicon saved: {brand["file"]}_favicon.ico')
    print()

print('All done! Files saved to:')
print(f'  {OUT}')
