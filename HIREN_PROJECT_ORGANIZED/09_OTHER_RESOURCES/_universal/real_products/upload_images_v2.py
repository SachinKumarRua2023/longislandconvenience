#!/usr/bin/env python3
"""
v2 — Product-type specific images:
  hobby_box  → realistic box shape with foil stripes
  graded     → PSA/BGS slab with card inside
  pack       → single booster pack
  deck       → fanned cards / deck box
  binder     → open binder pages
  sleeves    → sleeve pack
  toploaders → rigid loader stack
  bundle     → fanned cards stack
  playing    → classic card back
"""
import xmlrpc.client, sys, base64, io, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

def connect():
    uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
    m   = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
    print("Connected UID", uid)
    return m, uid

def xc(m, uid, model, method, args, kwargs={}):
    return m.execute_kw(DB, uid, PASS, model, method, args, kwargs)

def load_font(size):
    for path in ["C:/Windows/Fonts/arialbold.ttf","C:/Windows/Fonts/arial.ttf","arial.ttf"]:
        try: return ImageFont.truetype(path, size)
        except: pass
    return ImageFont.load_default()

def text_center(draw, text, font, y, W, color):
    bb = draw.textbbox((0,0), text, font=font)
    x = (W - (bb[2]-bb[0])) // 2
    draw.text((x, y), text, font=font, fill=color)
    return bb[3]-bb[1]

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, line = [], []
    for w in words:
        test = ' '.join(line+[w])
        bb = draw.textbbox((0,0), test, font=font)
        if bb[2]-bb[0] <= max_w: line.append(w)
        else:
            if line: lines.append(' '.join(line))
            line = [w]
    if line: lines.append(' '.join(line))
    return lines

GOLD = (212,175,55)
WHITE = (255,255,255)
BLACK = (8,8,8)

# ── Hobby Box ─────────────────────────────────────────────────
def draw_hobby_box(W, H, accent, bg, brand_line, sub_line):
    img = Image.new('RGB',(W,H), bg)
    d   = ImageDraw.Draw(img)
    # bg gradient
    for y in range(H):
        t = y/H
        r = int(bg[0]*(1-t) + min(bg[0]+30,255)*t)
        g = int(bg[1]*(1-t) + min(bg[1]+20,255)*t)
        b = int(bg[2]*(1-t) + min(bg[2]+20,255)*t)
        d.line([(0,y),(W,y)], fill=(r,g,b))

    # box shadow
    bx1,by1,bx2,by2 = 80, 55, W-80, int(H*0.60)
    d.rounded_rectangle([bx1+6,by1+8,bx2+6,by2+8], radius=14, fill=(0,0,0,180))

    # box body
    d.rounded_rectangle([bx1,by1,bx2,by2], radius=14, fill=(15,15,25))

    # box top band (foil stripe)
    band_h = 38
    d.rounded_rectangle([bx1,by1,bx2,by1+band_h], radius=14, fill=accent)
    d.rectangle([bx1,by1+14,bx2,by1+band_h], fill=accent)

    # diagonal shimmer lines on box
    for i in range(-4,20,3):
        x = bx1 + i*22
        d.line([(x,by1),(x+90,by2)], fill=(255,255,255,25), width=1)

    # foil strip bottom
    strip_h = 10
    d.rectangle([bx1,by2-strip_h,bx2,by2], fill=GOLD)
    d.rectangle([bx1,by2-strip_h-4,bx2,by2-strip_h], fill=(180,140,30))

    # brand text on box
    f24 = load_font(24); f16 = load_font(16); f13 = load_font(13)
    by_top = by1+6
    text_center(d, brand_line, f24, by_top, W, WHITE)
    # sub line centered in box body
    mid_y = (by1+band_h + by2-strip_h)//2 - 20
    lines = wrap(d, sub_line, f16, bx2-bx1-30)
    for ln in lines[:3]:
        bb = d.textbbox((0,0),ln,font=f16)
        tw = bb[2]-bb[0]
        d.text((bx1+(bx2-bx1-tw)//2, mid_y), ln, font=f16, fill=(220,220,220))
        mid_y += (bb[3]-bb[1])+5

    # small "HOBBY BOX" badge
    badge_text = "HOBBY BOX"
    bb = d.textbbox((0,0),badge_text,font=f13)
    bw,bh = bb[2]-bb[0], bb[3]-bb[1]
    bpx = bx1+(bx2-bx1-bw)//2 - 10
    d.rounded_rectangle([bpx-2, by2-strip_h-28, bpx+bw+12, by2-strip_h-8], radius=6, fill=(40,40,60))
    d.text((bpx+4, by2-strip_h-26), badge_text, font=f13, fill=GOLD)

    return img, d

# ── PSA/BGS Graded Slab ───────────────────────────────────────
def draw_graded_slab(W, H, grade_num, grade_label, card_color, player_name, year):
    img = Image.new('RGB',(W,H),(8,8,12))
    d   = ImageDraw.Draw(img)
    # Subtle grid bg
    for y in range(0,H,20):
        d.line([(0,y),(W,y)], fill=(18,18,28))
    for x in range(0,W,20):
        d.line([(x,0),(x,H)], fill=(18,18,28))

    # Slab outer
    sx1,sy1,sx2,sy2 = 90, 40, W-90, int(H*0.64)
    # Shadow
    d.rounded_rectangle([sx1+4,sy1+6,sx2+4,sy2+6], radius=12, fill=(0,0,0))
    # Slab body (translucent plastic look)
    d.rounded_rectangle([sx1,sy1,sx2,sy2], radius=12, fill=(225,235,245))
    # Slab inner border
    d.rounded_rectangle([sx1+4,sy1+4,sx2-4,sy2-4], radius=9, outline=(180,195,210), width=2)

    # Grade label band (top of slab)
    band_col = (180,30,30) if grade_label=='PSA' else (0,60,140) if grade_label=='BGS' else (20,20,60)
    d.rectangle([sx1,sy1,sx2,sy1+44], fill=band_col)
    d.rectangle([sx1,sy1,sx2,sy1+4], fill=band_col)
    f22 = load_font(22); f18=load_font(18); f14=load_font(14); f12=load_font(12)
    # Grade company name
    bb = d.textbbox((0,0),grade_label,font=f22)
    d.text((sx1+(sx2-sx1-(bb[2]-bb[0]))//2, sy1+8), grade_label, font=f22, fill=WHITE)

    # Card inside slab
    cx1,cy1,cx2,cy2 = sx1+22, sy1+56, sx2-22, sy2-22
    # Card art bg
    d.rounded_rectangle([cx1,cy1,cx2,cy2], radius=8, fill=card_color)
    # Card top banner
    d.rectangle([cx1,cy1,cx2,cy1+30], fill=(0,0,0,180))
    # Simple card art - geometric
    ccx,ccy = (cx1+cx2)//2, cy1+30+(cy2-cy1-30)//2
    cr = min(cx2-cx1,cy2-cy1-30)//3
    d.ellipse([ccx-cr,ccy-cr,ccx+cr,ccy+cr], outline=GOLD, width=2)
    d.ellipse([ccx-cr//2,ccy-cr//2,ccx+cr//2,ccy+cr//2], fill=GOLD)
    # Player / card name on card
    plines = wrap(d, player_name, f12, cx2-cx1-16)
    py = cy1+4
    for ln in plines[:1]:
        bb2 = d.textbbox((0,0),ln,font=f12)
        d.text((cx1+8,py), ln, font=f12, fill=WHITE)
    d.text((cx1+8, cy2-20), year, font=f12, fill=(220,220,180))

    # Grade score (large)
    grade_text = str(grade_num)
    gf = load_font(56)
    bb = d.textbbox((0,0), grade_text, font=gf)
    gx = sx2+12
    gy = (sy1+sy2)//2 - (bb[3]-bb[1])//2
    d.text((gx, gy), grade_text, font=gf, fill=GOLD)
    d.text((gx+2, gy+bb[3]-bb[1]-4), "GEM MT", font=f12, fill=(180,180,180))

    return img, d

# ── Booster Pack ─────────────────────────────────────────────
def draw_booster_pack(W, H, accent, bg, brand, set_name):
    img = Image.new('RGB',(W,H),bg)
    d   = ImageDraw.Draw(img)
    for y in range(H):
        t=y/H
        c = tuple(int(bg[i]*(1-t)+min(bg[i]+40,255)*t) for i in range(3))
        d.line([(0,y),(W,y)],fill=c)

    # Pack shape
    px1,py1,px2,py2 = 130, 40, W-130, int(H*0.62)
    # shadow
    d.rounded_rectangle([px1+5,py1+7,px2+5,py2+7], radius=18, fill=(0,0,0))
    d.rounded_rectangle([px1,py1,px2,py2], radius=18, fill=(20,20,30))

    # Holographic foil effect (diagonal gradient bands)
    for i,col in enumerate([(accent),(GOLD),(WHITE),(accent)]):
        for j in range(3):
            x = px1 + i*50 + j*4 - 20
            d.line([(x,py1),(x+(py2-py1)*0.4,py2)], fill=col, width=2+j)

    # Top tear notch
    d.rectangle([px1+30, py1, px2-30, py1+8], fill=(40,40,50))

    # Brand
    f20=load_font(20); f15=load_font(15); f12=load_font(12)
    pcx = (px1+px2)//2
    text_center(d, brand, f20, py1+18, W, WHITE)
    text_center(d, set_name, f15, py1+46, W, GOLD)
    text_center(d, "BOOSTER PACK", f12, py2-28, W, (200,200,200))

    # Rarity dots
    for i,col in enumerate([(160,160,160),(80,180,80),(80,80,220),(180,30,180)]):
        d.ellipse([pcx-60+i*30-6,py2-14,pcx-60+i*30+6,py2-2], fill=col)

    return img, d

# ── Card Binder ───────────────────────────────────────────────
def draw_binder(W, H, accent):
    img = Image.new('RGB',(W,H),(15,20,30))
    d   = ImageDraw.Draw(img)
    # Page pages (behind)
    for offset in [20,12,4]:
        d.rounded_rectangle([65+offset, 50+offset, W-65+offset, int(H*0.60)+offset],
            radius=6, fill=(230,228,220))
    # Binder cover
    bx1,by1,bx2,by2 = 65, 50, W-65, int(H*0.60)
    d.rounded_rectangle([bx1,by1,bx2,by2], radius=10, fill=accent)
    # Spine
    d.rectangle([bx1,by1,bx1+28,by2], fill=tuple(int(c*0.6) for c in accent))
    # Rings
    for ry in [by1+(by2-by1)//4, (by1+by2)//2, by1+3*(by2-by1)//4]:
        d.ellipse([bx1+8,ry-10,bx1+22,ry+10], fill=(180,180,180))
        d.ellipse([bx1+10,ry-8,bx1+20,ry+8], fill=(100,100,100))
    # Card grid on cover
    cpad = 14
    card_w = (bx2-bx1-28-cpad*4)//3
    card_h = int(card_w*1.38)
    for col in range(3):
        for row in range(2):
            cx = bx1+28+cpad+(card_w+cpad)*col
            cy = by1+cpad+(card_h+cpad)*row
            if cx+card_w < bx2-8:
                d.rounded_rectangle([cx,cy,cx+card_w,cy+card_h], radius=3,
                    fill=(255,255,255,80), outline=(255,255,255,40))
    return img, d

# ── Sleeve / Top Loader pack ──────────────────────────────────
def draw_sleeve_pack(W, H, accent, label):
    img = Image.new('RGB',(W,H),(12,12,20))
    d   = ImageDraw.Draw(img)
    # Bag shape
    bx1,by1,bx2,by2 = 100, 45, W-100, int(H*0.60)
    d.rounded_rectangle([bx1,by1,bx2,by2], radius=16, fill=(240,240,245))
    # Header seal
    d.rounded_rectangle([bx1,by1,bx2,by1+44], radius=16, fill=accent)
    d.rectangle([bx1,by1+22,bx2,by1+44], fill=accent)
    # Hang hole
    hcx = (bx1+bx2)//2
    d.ellipse([hcx-12,by1-2,hcx+12,by1+22], fill=(210,210,210))
    d.ellipse([hcx-7,by1+3,hcx+7,by1+17], fill=accent)
    # Sleeves inside bag (stacked)
    sl_w = int((bx2-bx1)*0.7)
    sl_h = int(sl_w*1.35)
    slx = bx1+(bx2-bx1-sl_w)//2
    sly = by1+50
    for off in range(5,0,-1):
        d.rounded_rectangle([slx+off*2, sly+off*3, slx+sl_w+off*2, sly+sl_h+off*3],
            radius=3, fill=(200+off*8, 205+off*8, 215+off*8), outline=(180,180,190))
    f14=load_font(14)
    text_center(d, label, f14, by2-30, W, (60,60,80))
    return img, d

# ── Fanned Cards Bundle ───────────────────────────────────────
def draw_bundle(W, H, accent, category):
    img = Image.new('RGB',(W,H),(10,12,20))
    d   = ImageDraw.Draw(img)
    cw,ch = 160, 224
    cx,cy = W//2, int(H*0.30)
    angles = [-25,-13,-4,6,18]
    colors = [(30,60,100),(50,20,80),(80,30,20),(20,70,20),(60,50,10)]
    for i,ang in enumerate(angles):
        card_img = Image.new('RGBA',(cw,ch),(0,0,0,0))
        cd = ImageDraw.Draw(card_img)
        cd.rounded_rectangle([0,0,cw,ch], radius=10, fill=colors[i%len(colors)])
        cd.rounded_rectangle([6,6,cw-6,ch-6], radius=7, outline=GOLD, width=1)
        # mini art
        cd.ellipse([cw//2-28,ch//2-40,cw//2+28,ch//2+20], fill=accent)
        f10 = load_font(10)
        cd.text((8,8), category[:8], font=f10, fill=(200,200,200))
        rot = card_img.rotate(ang, expand=True, resample=Image.BICUBIC)
        paste_x = cx - rot.width//2 + i*12 - 24
        paste_y = cy - rot.height//2
        img.paste(rot, (paste_x, paste_y), rot)
    return img, d

# ── Playing Cards ─────────────────────────────────────────────
def draw_playing_cards(W, H):
    img = Image.new('RGB',(W,H),(18,5,5))
    d   = ImageDraw.Draw(img)
    # Two cards fanned
    for offset, bg_col in [(-18,(220,30,30)), (18,(255,255,255))]:
        cw,ch = 200,285
        cx,cy = W//2+offset, int(H*0.29)
        c1 = cx-cw//2; c2 = cx+cw//2; cr = cy-ch//2; cb = cy+ch//2
        shadow_d = 6
        d.rounded_rectangle([c1+shadow_d,cr+shadow_d,c2+shadow_d,cb+shadow_d], radius=14, fill=(0,0,0))
        d.rounded_rectangle([c1,cr,c2,cb], radius=14, fill=bg_col)
        # Bicycle back pattern for red card
        if bg_col[0]==220:
            d.rounded_rectangle([c1+10,cr+10,c2-10,cb-10], radius=8, outline=WHITE, width=1)
            for iy in range(cr+16,cb-10,12):
                d.line([(c1+12,iy),(c2-12,iy)], fill=(200,10,10), width=1)
            d.ellipse([cx-22,cy-22,cx+22,cy+22], fill=(200,20,20))
            d.ellipse([cx-12,cy-12,cx+12,cy+12], fill=WHITE)
            d.text((c1+6,cr+4),"A", font=load_font(22), fill=WHITE)
            d.text((c2-26,cr+4),"♥", font=load_font(18), fill=WHITE)
        else:
            # Back of blue card
            d.rounded_rectangle([c1+8,cr+8,c2-8,cb-8], radius=10, fill=(20,80,200))
            d.rounded_rectangle([c1+14,cr+14,c2-14,cb-14], radius=6, outline=(100,160,255), width=2)
            for iy in range(cr+20,cb-16,10):
                d.line([(c1+16,iy),(c2-16,iy)], fill=(40,100,220), width=1)
            # diamond center
            d.regular_polygon(((cx,cy),18), 4, rotation=0, fill=(100,160,255))
    return img, d

# ──────────────────────────────────────────────────────────────
def make_image(pid, name, price, cat, **kwargs):
    """Route to correct drawing function based on product type"""
    W,H = 800,1000
    f28=load_font(28); f22=load_font(22); f16=load_font(16); f13=load_font(13); f11=load_font(11)
    GOLD=(212,175,55); WHITE=(255,255,255)

    ptype = kwargs.get('ptype','hobby_box')
    accent = kwargs.get('accent',(212,175,55))
    bg = kwargs.get('bg',(10,10,20))

    if ptype == 'hobby_box':
        brand_line = kwargs.get('brand','PANINI')
        sub_line   = name
        img, d = draw_hobby_box(W,H,accent,bg,brand_line,sub_line)

    elif ptype == 'graded':
        grade_num   = kwargs.get('grade_num',10)
        grade_label = kwargs.get('grade_label','PSA')
        card_col    = kwargs.get('card_color',(30,30,80))
        player      = kwargs.get('player','Card')
        year        = kwargs.get('year','2024')
        img, d = draw_graded_slab(W,H,grade_num,grade_label,card_col,player,year)

    elif ptype == 'pack':
        img, d = draw_booster_pack(W,H,accent,bg,kwargs.get('brand',''),name)

    elif ptype == 'binder':
        img, d = draw_binder(W,H,accent)

    elif ptype == 'sleeves':
        img, d = draw_sleeve_pack(W,H,accent,cat)

    elif ptype == 'bundle':
        img, d = draw_bundle(W,H,accent,cat)

    elif ptype == 'playing':
        img, d = draw_playing_cards(W,H)

    else:
        img, d = draw_hobby_box(W,H,accent,bg,kwargs.get('brand',''),name)

    # ── Bottom info panel (same for all) ─────────────────────
    panel_y = int(H*0.64)
    d.rectangle([0,panel_y,W,H], fill=(6,6,8))
    d.rectangle([0,panel_y,W,panel_y+3], fill=GOLD)

    # Product name
    lines = wrap(d, name, f22, W-60)
    if len(lines) > 2: lines = wrap(d, name, f16, W-60)
    ty = panel_y + 22
    nf = f22 if len(wrap(d,name,f22,W-60))<=2 else f16
    for ln in lines[:3]:
        bb = d.textbbox((0,0),ln,font=nf)
        d.text(((W-(bb[2]-bb[0]))//2, ty), ln, font=nf, fill=WHITE)
        ty += (bb[3]-bb[1])+5

    # Price
    pr_text = f"${price:.2f}"
    bb = d.textbbox((0,0),pr_text,font=f28)
    d.text(((W-(bb[2]-bb[0]))//2, ty+6), pr_text, font=f28, fill=GOLD)

    # Category tag
    tag_y = H-42
    bb = d.textbbox((0,0),cat,font=f11)
    tw = bb[2]-bb[0]
    d.rounded_rectangle([(W-tw)//2-14, tag_y-6, (W+tw)//2+14, tag_y+18],
        radius=8, fill=accent)
    d.text(((W-tw)//2, tag_y), cat, font=f11, fill=(0,0,0))

    # Brand watermark
    bw = "LONG ISLAND CARDS"
    bb = d.textbbox((0,0),bw,font=f11)
    d.text((W-(bb[2]-bb[0])-14, 12), bw, font=f11,
           fill=(int(GOLD[0]*0.4), int(GOLD[1]*0.4), int(GOLD[2]*0.4)))

    return img

def to_b64(img):
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=92)
    return base64.b64encode(buf.getvalue()).decode()

# ── Product definitions ───────────────────────────────────────
PRODUCTS = [
  # id,  name,                                              price,   cat,              ptype,         kwargs
  (117, "2024-25 Panini Prizm Basketball Hobby Box",        189.99, "Basketball",     "hobby_box",   {'brand':'PANINI','accent':(255,90,20),'bg':(22,8,2)}),
  (118, "2024 Topps Baseball Series 1 Hobby Box",           99.99, "Baseball",        "hobby_box",   {'brand':'TOPPS','accent':(30,100,210),'bg':(5,15,40)}),
  (119, "2024-25 Panini Donruss Football Hobby Box",       119.99, "Football",        "hobby_box",   {'brand':'PANINI','accent':(50,180,50),'bg':(8,22,8)}),
  (120, "2024-25 Upper Deck Hockey Series 1 Hobby Box",     89.99, "Hockey",          "hobby_box",   {'brand':'UPPER DECK','accent':(60,160,255),'bg':(5,12,35)}),
  (121, "Pokemon Prismatic Evolutions Booster Box",        169.99, "Pokemon",         "hobby_box",   {'brand':'POKEMON','accent':(255,215,0),'bg':(30,5,5)}),
  (122, "Pokemon Elite Trainer Box - Scarlet & Violet",     59.99, "Pokemon ETB",     "hobby_box",   {'brand':'POKEMON','accent':(220,40,80),'bg':(28,4,10)}),
  (123, "Pokemon Single Booster Pack",                       5.99, "Pokemon Pack",    "pack",        {'brand':'POKEMON','accent':(255,215,0),'bg':(25,5,5)}),
  (124, "Pokemon Charizard ex PSA 10 — Obsidian Flames",  349.99, "PSA 10",          "graded",      {'grade_num':10,'grade_label':'PSA','card_color':(80,20,10),'player':'Charizard ex','year':'2023'}),
  (125, "MTG Duskmourn Draft Booster Box",                 124.99, "MTG",             "hobby_box",   {'brand':'MAGIC','accent':(140,70,240),'bg':(14,5,28)}),
  (126, "MTG Commander Precon Deck",                        44.99, "MTG Commander",   "pack",        {'brand':'MAGIC','accent':(140,70,240),'bg':(12,4,24)}),
  (127, "Yu-Gi-Oh! Burst Protocol Booster Box",             89.99, "Yu-Gi-Oh!",       "hobby_box",   {'brand':'YU-GI-OH!','accent':(80,180,255),'bg':(4,8,28)}),
  (128, "Yu-Gi-Oh! Blue-Eyes White Dragon PSA 9",          199.99, "PSA 9",           "graded",      {'grade_num':9,'grade_label':'PSA','card_color':(10,40,100),'player':'Blue-Eyes White Dragon','year':'2002'}),
  (129, "One Piece Two Legends Booster Box",                99.99, "One Piece",       "hobby_box",   {'brand':'ONE PIECE','accent':(255,70,30),'bg':(22,5,2)}),
  (130, "Mike Trout 2011 Topps Rookie PSA 10",             499.99, "PSA 10",          "graded",      {'grade_num':10,'grade_label':'PSA','card_color':(10,35,80),'player':'Mike Trout','year':'2011'}),
  (131, "Luka Doncic Panini Prizm Rookie BGS 9.5",         379.99, "BGS 9.5",         "graded",      {'grade_num':'9.5','grade_label':'BGS','card_color':(60,10,10),'player':'Luka Doncic','year':'2018'}),
  (132, "Ultra Pro 9-Pocket Card Binder",                   19.99, "Binder",          "binder",      {'accent':(30,80,200),'bg':(10,15,30)}),
  (133, "Top Loaders 3x4 inch — 25 Pack",                    7.99, "Top Loaders",     "sleeves",     {'accent':(180,180,200)}),
  (134, "Perfect Fit Inner Sleeves — 100 Pack",              4.99, "Card Sleeves",    "sleeves",     {'accent':(80,200,80)}),
  (135, "Bicycle Playing Cards — 2 Deck Set",                9.99, "Playing Cards",   "playing",     {}),
  (136, "Long Island Cards Sports Starter Pack",            49.99, "Sports Bundle",   "bundle",      {'accent':(220,40,60),'bg':(10,15,30)}),
  (137, "Long Island Cards TCG Starter Bundle",             39.99, "TCG Bundle",      "bundle",      {'accent':(255,215,0),'bg':(10,10,20)}),
]

def main():
    m, uid = connect()
    print(f"Uploading {len(PRODUCTS)} product images...\n")
    ok = 0
    for row in PRODUCTS:
        pid, name, price, cat, ptype, kw = row
        try:
            img = make_image(pid, name, price, cat, ptype=ptype, **kw)
            b64 = to_b64(img)
            xc(m, uid, 'product.template','write',[[pid],{'image_1920':b64}])
            print(f"  OK [{pid}] {name[:50]}")
            ok += 1
        except Exception as e:
            print(f"  FAIL [{pid}]: {e}")
    print(f"\n{ok}/{len(PRODUCTS)} uploaded.")

if __name__=='__main__':
    main()
