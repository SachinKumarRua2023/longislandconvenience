"""
fix_blog_images_author.py
─────────────────────────
1. Generates attractive category-themed cover images for all 36 LIC blog posts
2. Uploads each as ir.attachment and links via cover_properties
3. Changes author from "Sachin Kumar" to "James Mitchell"
"""
import xmlrpc.client, base64, json, os, sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

URL  = 'https://country-cove-inc.odoo.com'
DB   = 'country-cove-inc'
USER = 'countrycoveinc@gmail.com'
PASS = 'M@nhattan1234'

common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid    = common.authenticate(DB, USER, PASS, {})
m      = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
xc     = lambda mo, me, a, k={}: m.execute_kw(DB, uid, PASS, mo, me, a, k)

FONT_BOLD  = 'C:/Windows/Fonts/segoeuib.ttf'
FONT_LIGHT = 'C:/Windows/Fonts/segoeuil.ttf'
FONT_REG   = 'C:/Windows/Fonts/segoeui.ttf'

# ── Category themes ────────────────────────────────────────────────────────────
BLOG_THEMES = {
    'Sports & Trading Cards': {
        'bg1': (10, 10, 20), 'bg2': (25, 20, 5),
        'accent1': (212, 175, 55), 'accent2': (180, 140, 30),
        'label': 'SPORTS & TRADING CARDS', 'icon': 'CARDS',
    },
    'Gift Baskets & Gifts': {
        'bg1': (5, 15, 10), 'bg2': (10, 25, 15),
        'accent1': (45, 180, 100), 'accent2': (30, 130, 70),
        'label': 'GIFT BASKETS & GIFTS', 'icon': 'GIFTS',
    },
    'Balloons & Party Decor': {
        'bg1': (12, 5, 22), 'bg2': (20, 10, 35),
        'accent1': (199, 125, 255), 'accent2': (150, 80, 220),
        'label': 'BALLOONS & PARTY DECOR', 'icon': 'EVENTS',
    },
    'Print & Mail Services': {
        'bg1': (5, 10, 28), 'bg2': (10, 20, 45),
        'accent1': (67, 120, 255), 'accent2': (40, 80, 200),
        'label': 'PRINT & MAIL SERVICES', 'icon': 'PRINT',
    },
    'Convenience & Grocery': {
        'bg1': (22, 5, 8), 'bg2': (35, 10, 12),
        'accent1': (230, 80, 80), 'accent2': (190, 50, 50),
        'label': 'CONVENIENCE & GROCERY', 'icon': 'SHOP',
    },
    'IT & Cyber Services': {
        'bg1': (5, 12, 22), 'bg2': (8, 20, 35),
        'accent1': (0, 200, 255), 'accent2': (0, 140, 200),
        'label': 'IT & CYBER SERVICES', 'icon': 'TECH',
    },
    'Long Island News': {
        'bg1': (10, 10, 18), 'bg2': (18, 18, 28),
        'accent1': (255, 200, 60), 'accent2': (200, 150, 30),
        'label': 'LONG ISLAND NEWS', 'icon': 'NEWS',
    },
    'Our blog': {
        'bg1': (10, 15, 10), 'bg2': (18, 25, 18),
        'accent1': (80, 200, 120), 'accent2': (50, 160, 90),
        'label': 'LONG ISLAND BLOG', 'icon': 'BLOG',
    },
}

def horiz_grad(img, xy, c1, c2):
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = xy
    for x in range(x0, x1):
        t = (x - x0) / max(1, x1 - x0)
        r = int(c1[0] + (c2[0]-c1[0])*t)
        g = int(c1[1] + (c2[1]-c1[1])*t)
        b = int(c1[2] + (c2[2]-c1[2])*t)
        draw.line([(x,y0),(x,y1)], fill=(r,g,b))

def vert_grad(img, c_top, c_bot):
    draw = ImageDraw.Draw(img)
    W, H = img.size
    for y in range(H):
        t = y / H
        r = int(c_top[0] + (c_bot[0]-c_top[0])*t)
        g = int(c_top[1] + (c_bot[1]-c_top[1])*t)
        b = int(c_top[2] + (c_bot[2]-c_top[2])*t)
        draw.line([(0,y),(W,y)], fill=(r,g,b))

def make_blog_image(title, blog_name):
    W, H = 1200, 628   # standard OG image size
    theme = BLOG_THEMES.get(blog_name, BLOG_THEMES['Our blog'])
    img = Image.new('RGB', (W, H))

    # Background gradient
    vert_grad(img, theme['bg1'], theme['bg2'])
    draw = ImageDraw.Draw(img)

    # Diagonal light sweep (decorative)
    for i in range(0, 8):
        x = W//2 + i * 80 - 200
        pts = [(x, 0), (x+300, 0), (x+W, H), (x+W-300, H)]
        overlay = Image.new('RGBA', (W, H), (0,0,0,0))
        od = ImageDraw.Draw(overlay)
        od.polygon(pts, fill=(255,255,255,6))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)

    # Left accent bar
    horiz_grad(img, (0, 0, 8, H), theme['accent1'], theme['accent2'])

    # Top label strip
    horiz_grad(img, (0, 0, W, 52), theme['accent2'], theme['bg1'])
    try:
        label_font = ImageFont.truetype(FONT_BOLD, 13)
    except:
        label_font = ImageFont.load_default()
    draw.text((28, 18), theme['label'], font=label_font,
              fill=(255,255,255,180))
    draw.text((W-200, 18), 'LONG ISLAND NY', font=label_font,
              fill=theme['accent1'] + (200,) if len(theme['accent1'])==3 else theme['accent1'])

    # Large decorative icon text (background)
    try:
        big_font = ImageFont.truetype(FONT_BOLD, 180)
    except:
        big_font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), theme['icon'], font=big_font)
    iw = bbox[2]-bbox[0]
    r, g, b = theme['accent1']
    draw.text((W - iw - 40, H//2 - 100), theme['icon'],
              font=big_font, fill=(r, g, b, 18))

    # Main title
    try:
        title_font = ImageFont.truetype(FONT_BOLD, 52)
        sub_font   = ImageFont.truetype(FONT_REG, 22)
    except:
        title_font = sub_font = ImageFont.load_default()

    # Word-wrap title
    words = title.split()
    lines = []
    current = ''
    for word in words:
        test = (current + ' ' + word).strip()
        bbox = draw.textbbox((0,0), test, font=title_font)
        if bbox[2]-bbox[0] > W - 120:
            if current:
                lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)

    total_h = len(lines) * 65
    y_start = H//2 - total_h//2 - 20
    for line in lines:
        draw.text((60, y_start), line, font=title_font,
                  fill=(255,255,255,240))
        y_start += 65

    # Bottom bar
    draw.rectangle([0, H-56, W, H], fill=theme['bg2'])
    horiz_grad(img, (0, H-3, W, H), theme['accent1'], theme['accent2'])
    draw.text((60, H-42), 'LongIslandConvenience.com  •  605 Old Country Rd, Plainview NY',
              font=sub_font, fill=(180,180,180,200))

    # Save to bytes
    import io
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=88)
    return buf.getvalue()


# ── Step 1: Change author ─────────────────────────────────────────────────────
print('=== Step 1: Updating Author ===')

# Create or find "James Mitchell" partner
existing = xc('res.partner', 'search_read',
    [[['name','=','James Mitchell']]],
    {'fields':['id','name']})
if existing:
    author_id = existing[0]['id']
    print(f'  Found existing partner: James Mitchell (ID={author_id})')
else:
    author_id = xc('res.partner', 'create', [{
        'name': 'James Mitchell',
        'type': 'contact',
        'comment': 'Blog author — Long Island Convenience',
    }])
    print(f'  Created new partner: James Mitchell (ID={author_id})')

# Get all LIC blog post IDs
all_posts = xc('blog.post', 'search_read',
    [[['website_id','=',1]]],
    {'fields':['id','name','blog_id','cover_properties'],'order':'id asc'})
post_ids = [p['id'] for p in all_posts]

# Reassign author on all posts
xc('blog.post', 'write', [post_ids, {'author_id': author_id}])
print(f'  Updated author to James Mitchell on {len(post_ids)} posts')

# ── Step 2: Generate & upload cover images ────────────────────────────────────
print('\n=== Step 2: Generating & Uploading Cover Images ===')
for p in all_posts:
    blog_name = p['blog_id'][1] if p['blog_id'] else 'Our blog'
    title = p['name']

    # Generate image
    img_bytes = make_blog_image(title, blog_name)
    b64 = base64.b64encode(img_bytes).decode()

    # Upload as public attachment linked to this blog post
    att_id = xc('ir.attachment', 'create', [{
        'name': f'cover_{p["id"]}.jpg',
        'type': 'binary',
        'datas': b64,
        'res_model': 'blog.post',
        'res_id': p['id'],
        'mimetype': 'image/jpeg',
        'public': True,
    }])

    # Update cover_properties to use this image
    cover = json.dumps({
        "background_color_class": "o_cc3",
        "background-image": f"url('/web/image/ir.attachment/{att_id}/datas')",
        "opacity": "0.4",
        "resize_class": "o_half_screen_height"
    })
    xc('blog.post', 'write', [[p['id']], {'cover_properties': cover}])
    print(f'  [{p["id"]}] {title[:55]}...' if len(title)>55 else f'  [{p["id"]}] {title}')

print(f'\n=== ALL DONE ===')
print(f'Author: Sachin Kumar -> James Mitchell on all {len(post_ids)} posts')
print(f'Cover images: generated and uploaded for all {len(post_ids)} posts')
print('Hard refresh (Ctrl+Shift+R) to see changes.')
