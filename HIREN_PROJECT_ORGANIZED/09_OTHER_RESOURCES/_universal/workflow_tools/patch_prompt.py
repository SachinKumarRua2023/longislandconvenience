#!/usr/bin/env python3
"""Patches the Code: Build Cards HTML Prompt node in ai-cloner-odoo.json with a professional prompt."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

NEW_JS = r"""
// ── Buffer decoder ──────────────────────────────────────────────────────────
function decodeBuffer(resp) {
  if (resp?.content || resp?.result !== undefined || resp?.data) return resp;
  if (!resp?._readableState) return resp;
  try {
    const chunks = Array.isArray(resp._readableState.buffer) ? resp._readableState.buffer : [];
    const allBytes = [];
    for (const chunk of chunks) {
      const d = chunk?.data;
      if (Array.isArray(d)) allBytes.push(...d);
      else if (d?.type === 'Buffer' && Array.isArray(d.data)) allBytes.push(...d.data);
    }
    if (allBytes.length > 0) return JSON.parse(Buffer.from(allBytes).toString('utf-8'));
  } catch(e) {}
  return resp;
}

const resp = decodeBuffer($input.item.json);
const prev = $('Code: Build Analysis Prompt').item.json;

// ── Parse Claude design analysis ─────────────────────────────────────────────
const raw = resp?.content?.[0]?.text || '';
let d = {};
try { const m = raw.match(/\{[\s\S]*\}/); if (m) d = JSON.parse(m[0]); } catch(e) {}

// ── Lock brand + fill all fallbacks ─────────────────────────────────────────
d.brandName    = 'Long Island Cards';
d.tagline      = d.tagline   || "Long Island's Premier Trading Card & Collectibles Store";
d.colorPalette = d.colorPalette || {
  primary:'#0f172a', secondary:'#1e293b', accent:'#f59e0b',
  background:'#0f172a', cardBg:'#1e293b', textPrimary:'#ffffff', textSecondary:'#94a3b8'
};
d.heroSection = d.heroSection || {
  headline:     "Long Island's #1 Trading Card Store",
  subheadline:  'Pokemon TCG · Magic: The Gathering · Yu-Gi-Oh! · Sports Cards · Graded Slabs — Shipped Same Day',
  primaryCTA:   'Shop All Cards',
  secondaryCTA: 'Sell Your Cards'
};
d.trustElements  = d.trustElements  || ['Free Shipping $75+','Same-Day Shipping Before 2pm','PSA/BGS Grading Service','100% Authentic Cards'];
d.featuredBrands = d.featuredBrands || ['Pokemon TCG','Magic: The Gathering','Yu-Gi-Oh!','Sports Cards','One Piece TCG','Dragon Ball Super','Digimon','Lorcana','Flesh & Blood'];
d.footerLinks    = d.footerLinks    || {
  shop:    ['All Singles','Sealed Products','Graded Cards','Sports Cards','Accessories','Pre-Orders'],
  support: ['FAQ','Condition Guide','Grading Info','Contact Us','Returns & Refunds','Track Order'],
  social:  ['Instagram','YouTube','TikTok','Twitter / X','Discord','Facebook']
};

const PRODUCTS = [
  { name:'Charizard ex SAR',            set:'Scarlet & Violet 151',   price:'$89.99',  orig:'$109.99', badge:'Hot',    badgeColor:'amber',  condition:'NM',     stock:'Only 3 left!', rating:4.9, reviews:312, imgSeed:11 },
  { name:'Black Lotus (VG)',             set:'Alpha Edition',          price:'$4,999',  orig:'$4,999',  badge:'Rare',   badgeColor:'purple', condition:'VG',     stock:'1 In Stock',   rating:5.0, reviews:18,  imgSeed:22 },
  { name:'Pokemon 151 Booster Box',      set:'Sealed Product',         price:'$129.99', orig:'$149.99', badge:'Sale',   badgeColor:'red',    condition:'Sealed', stock:'12 In Stock',  rating:4.8, reviews:541, imgSeed:33 },
  { name:'Shohei Ohtani RC PSA 10',      set:'2018 Bowman Chrome',     price:'$299.00', orig:'$349.00', badge:'PSA 10', badgeColor:'blue',   condition:'PSA 10', stock:'1 In Stock',   rating:5.0, reviews:74,  imgSeed:44 },
  { name:'Dark Magician LCKC',           set:'Legendary Collection',   price:'$24.99',  orig:'$24.99',  badge:'New',    badgeColor:'green',  condition:'NM',     stock:'8 In Stock',   rating:4.7, reviews:189, imgSeed:55 },
  { name:'MTG Fetch Land Lot x4',        set:'Khans of Tarkir',        price:'$79.99',  orig:'$99.99',  badge:'Sale',   badgeColor:'red',    condition:'LP',     stock:'5 In Stock',   rating:4.8, reviews:267, imgSeed:66 },
  { name:'One Piece OP-07 Booster Box',  set:'Sealed',                 price:'$109.99', orig:'$119.99', badge:'New',    badgeColor:'green',  condition:'Sealed', stock:'7 In Stock',   rating:4.9, reviews:93,  imgSeed:77 },
  { name:'Goku Ultra Instinct SSP',      set:'Dragon Ball Super S5',   price:'$34.99',  orig:'$44.99',  badge:'Sale',   badgeColor:'red',    condition:'NM',     stock:'4 left',       rating:4.7, reviews:156, imgSeed:88 }
];
const sp = (d.sampleProducts || []).slice(0,8);
while (sp.length < 8) sp.push(PRODUCTS[sp.length]);
d.sampleProducts = sp.map((p,i) => ({ ...PRODUCTS[i], ...p, imgSeed: PRODUCTS[i].imgSeed }));

const CATEGORIES = [
  { name:'Pokemon TCG',           emoji:'⚡', desc:'Singles, Boxes & ETBs',              color:'#ef4444', href:'/shop/pokemon'     },
  { name:'Magic: The Gathering',  emoji:'🔮', desc:'Modern, Legacy & Sealed',            color:'#8b5cf6', href:'/shop/mtg'         },
  { name:'Yu-Gi-Oh!',             emoji:'🐉', desc:'Rare Singles, Decks & Accessories',  color:'#3b82f6', href:'/shop/yugioh'      },
  { name:'Sports Cards',          emoji:'🏆', desc:'MLB · NBA · NFL · NHL',              color:'#10b981', href:'/shop/sports'      },
  { name:'One Piece TCG',         emoji:'⚓', desc:'All Sets — Boxes & Singles',         color:'#f97316', href:'/shop/onepiece'    },
  { name:'Dragon Ball Super',     emoji:'💥', desc:'Sealed Sets & Rare Cards',           color:'#eab308', href:'/shop/dbs'         },
  { name:'Graded Slabs PSA/BGS',  emoji:'🏅', desc:'Certified Investment-Grade',         color:'#14b8a6', href:'/shop/graded'      },
  { name:'Sealed Booster Boxes',  emoji:'📦', desc:'Factory Sealed — All Games',         color:'#ec4899', href:'/shop/sealed'      },
  { name:'Singles — All Games',   emoji:'🃏', desc:'Buy by the Card, All Conditions',    color:'#6366f1', href:'/shop/singles'     },
  { name:'Accessories',           emoji:'🛡️', desc:'Sleeves, Toploaders, Binders',       color:'#64748b', href:'/shop/accessories' },
  { name:'Vintage & Rare',        emoji:'💎', desc:'1990s–2000s Collectibles',           color:'#a855f7', href:'/shop/vintage'     },
  { name:'Pre-Orders',            emoji:'🚀', desc:'Upcoming Sets — Lock In Your Copy',  color:'#0ea5e9', href:'/shop/preorder'    },
];

const RELEASES = [
  { name:'Pokemon Stellar Crown',       date:'September 13 2025', badge:'Pre-Order Open', price:'$139.99', seed:91 },
  { name:'MTG Final Fantasy',           date:'June 13 2025',      badge:'Pre-Order Open', price:'$199.99', seed:92 },
  { name:'One Piece OP-10 Booster Box', date:'August 2025',       badge:'Coming Soon',    price:'$109.99', seed:93 },
];

const REVIEWS = [
  { name:'Michael R.', loc:'Plainview NY', text:'Best card shop on Long Island. Found a PSA 10 Charizard I had been hunting for 2 years. Lightning-fast shipping, packed perfectly.', stars:5 },
  { name:'Sarah T.',   loc:'Syosset NY',   text:'Sent 15 cards for grading — came back PSA 9 and 10. The team actually knows their stuff and the prices are fair. My go-to store.', stars:5 },
  { name:'Danny K.',   loc:'Huntington NY',text:'Three booster boxes, all genuine, all arrived sealed and fast. Better prices than big-box stores. Will always order from Long Island Cards.', stars:5 },
];

const p   = d.colorPalette;
const acc = p.accent || '#f59e0b';
const bg  = p.primary || '#0f172a';
const bg2 = p.secondary || '#1e293b';
const style = prev.designStyle || 'Modern Dark';

const htmlPrompt =
'You are a senior frontend engineer. Build a complete, production-ready, single-file TailwindCSS HTML homepage for "Long Island Cards" that matches the quality and feature set of TCGPlayer, TrollAndToad, StarCityGames, ChannelFireball, and Dave & Adams combined.\n\n' +

'══ MANDATORY COLOR RULES — NEVER VIOLATE ══\n' +
'1. <body class="bg-[' + bg + '] text-white" style="background:' + bg + ';color:#ffffff;font-family:Inter,sans-serif">\n' +
'2. EVERY text on dark bg MUST have class="text-white" or class="text-slate-300" — never rely on default inherit\n' +
'3. ALL headings: class="text-white font-black" (add font-family: Rajdhani via style tag)\n' +
'4. ALL body copy on dark panels: class="text-slate-300"\n' +
'5. ALL cards/panels: class="bg-slate-800 text-white" — never class="bg-slate-800" alone\n' +
'6. Accent color ' + acc + ' for CTAs, highlights, hover borders, active states\n' +
'7. In <script>tailwind.config add colors:{ brand:"' + bg + '", accent:"' + acc + '" }\n\n' +

'══ BRAND ══\n' +
'Name: Long Island Cards | Address: 605 Old Country Road Plainview NY 11803 | Phone: (212) 564-8585\n' +
'Tagline: ' + d.tagline + '\n' +
'Hero H1: ' + d.heroSection.headline + '\n' +
'Hero sub: ' + d.heroSection.subheadline + '\n' +
'CTA1: "' + d.heroSection.primaryCTA + '" (bg accent, text black) | CTA2: "' + d.heroSection.secondaryCTA + '" (border white)\n' +
'Trust badges: ' + d.trustElements.join(' | ') + '\n\n' +

'══ DATA ══\n' +
'PRODUCTS: ' + JSON.stringify(d.sampleProducts) + '\n' +
'CATEGORIES: ' + JSON.stringify(CATEGORIES) + '\n' +
'UPCOMING_RELEASES: ' + JSON.stringify(RELEASES) + '\n' +
'REVIEWS: ' + JSON.stringify(REVIEWS) + '\n' +
'BRANDS: ' + d.featuredBrands.join(', ') + '\n\n' +

'══ BUILD ALL 17 SECTIONS IN EXACT ORDER ══\n\n' +

'[S1] ANNOUNCEMENT BAR (z-60, bg-[' + acc + '] text-black text-sm font-medium, py-2)\n' +
'  Left: scrolling marquee text: "🔥 FREE SHIPPING on orders $75+ &nbsp;|&nbsp; Same-day shipping before 2pm EST &nbsp;|&nbsp; Use code LIC10 — 10% off first order &nbsp;|&nbsp; Pokemon Stellar Crown Pre-Orders now OPEN →"\n' +
'  Right: × dismiss button (removes bar on click)\n' +
'  CSS: @keyframes marquee { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }\n\n' +

'[S2] STICKY HEADER (z-50 fixed top w-full bg-[' + bg + ']/95 backdrop-blur-xl border-b border-white/10)\n' +
'  Desktop layout: 3 zones\n' +
'    LEFT: ♠ logo icon (text-[' + acc + '] text-2xl) + "Long Island Cards" (font-bold text-white text-xl Rajdhani) + "Plainview, NY" (text-xs text-slate-400)\n' +
'    CENTER: nav links (text-sm font-medium text-slate-300 hover:text-white transition): Home · Shop · Singles · Sealed · Graded · Sports · Pre-Orders · Sell Cards · About\n' +
'    RIGHT: 🔍 search icon (onclick expands search bar) + ♡ wishlist (badge pill, amber) + 🛒 cart (badge pill, shows count) \n' +
'  SEARCH BAR: hidden div below nav, full-width, expands/collapses on search icon click — placeholder "Search 50,000+ cards, sets, players..."\n' +
'  Mobile (<lg): only logo left + hamburger right (3-line icon). Hamburger toggles full-width dropdown menu with all nav links stacked.\n\n' +

'[S3] HERO (min-h-screen flex items-center, bg-gradient-to-br from-[' + bg + '] via-[' + bg2 + '] to-[' + bg + '], pt-24)\n' +
'  Left 55% (text content):\n' +
'    Small badge pill (bg-[' + acc + ']/20 text-[' + acc + '] border border-[' + acc + ']/30 rounded-full px-4 py-1 text-sm): "🃏 New Arrivals This Week"\n' +
'    H1 (text-6xl md:text-7xl font-black text-white leading-tight, font-family Rajdhani): "' + d.heroSection.headline + '"\n' +
'    P (text-xl text-slate-300 mt-4 max-w-xl): "' + d.heroSection.subheadline + '"\n' +
'    Button row (mt-8 flex gap-4 flex-wrap):\n' +
'      Primary: class="bg-[' + acc + '] text-black font-bold px-8 py-4 rounded-xl hover:scale-105 transition-transform text-lg" — "' + d.heroSection.primaryCTA + '"\n' +
'      Secondary: class="border-2 border-white/30 text-white font-bold px-8 py-4 rounded-xl hover:bg-white/10 transition text-lg" — "' + d.heroSection.secondaryCTA + '"\n' +
'    Trust row (mt-8 flex flex-wrap gap-4): each trust item = checkmark ✓ + text, class="flex items-center gap-2 text-slate-300 text-sm"\n' +
'  Right 45% (visual):\n' +
'    3 rotated overlapping card images (picsum.photos/200/280?random=1,2,3), each in a div with rotate-[-8deg], rotate-[0deg], rotate-[8deg], shadow-2xl rounded-xl\n' +
'    Floating price badge on top card: "PSA 10 — $299" (bg-[' + acc + '] text-black font-bold px-3 py-1 rounded-lg absolute)\n' +
'    Background glow: absolute div w-96 h-96 bg-[' + acc + ']/10 blur-3xl rounded-full\n\n' +

'[S4] TRENDING TICKER (overflow-hidden bg-[' + acc + '] text-black py-3 border-y-2 border-black/10)\n' +
'  Two divs side by side (flex whitespace-nowrap) — each contains the full ticker text — creating seamless loop via animation\n' +
'  Text: "🔥 Charizard ex SAR — $89.99 &nbsp;&nbsp;·&nbsp;&nbsp; 📈 Black Lotus — $4,999 &nbsp;&nbsp;·&nbsp;&nbsp; ⬆ Shohei Ohtani RC PSA 10 — $299 &nbsp;&nbsp;·&nbsp;&nbsp; 🆕 Pokemon 151 Box — $129.99 &nbsp;&nbsp;·&nbsp;&nbsp; 💎 1986 Fleer Jordan Sticker — $599 &nbsp;&nbsp;·&nbsp;&nbsp; 🔥 MTG Force of Will — $74.99 &nbsp;&nbsp;·&nbsp;&nbsp; ⬆ Blue-Eyes LOB — $149 &nbsp;&nbsp;·&nbsp;&nbsp; 🆕 OP-07 Booster Box — $109.99"\n' +
'  CSS: animation: marquee 25s linear infinite\n\n' +

'[S5] FEATURED BRANDS BAR (py-6 bg-slate-900 border-y border-white/10)\n' +
'  Left: "Shop by Brand" (text-sm text-slate-400 font-semibold uppercase tracking-wider)\n' +
'  Right: overflow-x-auto flex gap-3. Each brand pill: class="shrink-0 flex items-center gap-2 bg-slate-800 hover:bg-slate-700 hover:border-[' + acc + '] border border-transparent text-white text-sm font-medium px-4 py-2 rounded-full cursor-pointer transition-all whitespace-nowrap"\n' +
'  Brands: ' + d.featuredBrands.join(', ') + '\n\n' +

'[S6] TRUST BAR (py-8 bg-[' + acc + '] text-black)\n' +
'  4-column grid (grid-cols-2 md:grid-cols-4)\n' +
'  Each item (flex flex-col items-center text-center):\n' +
'    Icon (text-3xl mb-2): 🚚 / ⚡ / 🔒 / 🏆\n' +
'    Title (font-black text-lg): "Free Shipping" / "Same-Day Shipping" / "100% Authentic" / "PSA/BGS Grading"\n' +
'    Sub (text-sm font-medium opacity-80): "On orders over $75" / "Order before 2pm EST" / "Every card verified" / "Submit directly through us"\n\n' +

'[S7] HOT RIGHT NOW (py-16 px-4 max-w-7xl mx-auto)\n' +
'  Header row: "🔥 Hot Right Now" (text-3xl font-black text-white Rajdhani) + "View All Cards →" link (text-[' + acc + '] hover:underline)\n' +
'  Grid (mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6)\n\n' +
'  EACH PRODUCT CARD (class="bg-slate-800 rounded-2xl overflow-hidden group hover:scale-[1.02] transition-all duration-300 shadow-lg border border-white/5 hover:border-[' + acc + ']/30"):\n' +
'    IMAGE ZONE (relative aspect-[3/4] bg-slate-700 overflow-hidden):\n' +
'      img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"\n' +
'      src="https://picsum.photos/300/400?random={imgSeed}" alt="{name}"\n' +
'      BADGE top-left: rounded-full px-3 py-1 text-xs font-bold — colors: amber=bg-amber-500, red=bg-red-500, green=bg-green-500, purple=bg-purple-500, blue=bg-blue-500\n' +
'      WISHLIST top-right: heart button ♡/♥ (toggle class, JS), class="absolute top-3 right-3 w-8 h-8 bg-black/50 rounded-full flex items-center justify-center text-white hover:text-red-400 transition cursor-pointer wishlist-btn"\n' +
'      QUICK VIEW center overlay (opacity-0 group-hover:opacity-100 transition-opacity absolute inset-0 bg-black/50 flex items-center justify-center):\n' +
'        button class="bg-white text-black font-bold px-4 py-2 rounded-xl text-sm hover:bg-[' + acc + '] transition-colors" — "Quick View"\n' +
'    CONTENT ZONE (p-4):\n' +
'      Condition row: colored dot + condition text ("NM","LP","VG","Sealed","PSA 10") class="flex items-center gap-1 text-xs font-semibold mb-2"\n' +
'        Dot colors: NM=green, LP=yellow, VG=orange, Sealed=blue, PSA10=purple\n' +
'      Name: class="font-bold text-white text-sm leading-tight" — {name}\n' +
'      Set: class="text-xs text-slate-400 mt-1 mb-2" — {set}\n' +
'      Stars row: class="flex items-center gap-1 text-amber-400 text-xs" — filled ★ × floor(rating) + {reviews} reviews text\n' +
'      Stock: class="text-xs mt-1" — "Only X left!" in text-red-400 if stock contains "left", else text-green-400\n' +
'      Price row: class="flex items-end gap-2 mt-2" — price (text-xl font-black text-white) + originalPrice (text-sm line-through text-slate-500, only if differs)\n' +
'      Add to Cart btn: class="mt-3 w-full bg-[' + acc + '] text-black font-bold py-2.5 rounded-xl hover:bg-opacity-90 transition-colors text-sm add-to-cart"\n\n' +

'[S8] BROWSE BY CATEGORY (py-16 px-4 max-w-7xl mx-auto bg-slate-900/50 rounded-3xl my-4)\n' +
'  Header: "Browse by Category" (text-3xl font-black text-white Rajdhani) + subtitle "Everything a collector needs — all in one place" (text-slate-400)\n' +
'  Grid (mt-8 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4)\n' +
'  EACH CATEGORY CARD (class="relative bg-slate-800 rounded-2xl p-5 text-center hover:border-[' + acc + '] border border-transparent transition-all cursor-pointer group hover:scale-[1.02]"):\n' +
'    Color circle (w-14 h-14 mx-auto rounded-2xl flex items-center justify-center text-2xl, bg uses {color} at 20% opacity via style="background:{color}33")\n' +
'    Name: class="font-bold text-white mt-3 text-sm" — {name}\n' +
'    Desc: class="text-xs text-slate-400 mt-1" — {desc}\n' +
'    Arrow: class="text-[' + acc + '] text-sm mt-2 opacity-0 group-hover:opacity-100 transition-opacity" — "Shop Now →"\n\n' +

'[S9] UPCOMING RELEASES & PRE-ORDERS (py-16 px-4 max-w-7xl mx-auto)\n' +
'  Header: "🚀 Upcoming Releases" + badge "Pre-order — Limited Allocation"\n' +
'  Grid (grid grid-cols-1 md:grid-cols-3 gap-6 mt-8)\n' +
'  EACH RELEASE CARD (bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl overflow-hidden border border-white/10):\n' +
'    Image: picsum.photos/400/220?random={seed} — h-44 w-full object-cover\n' +
'    Content p-5:\n' +
'      Badge pill: {badge} in amber or blue\n' +
'      Name: text-lg font-bold text-white\n' +
'      Release date: text-sm text-slate-400 "Releases: {date}"\n' +
'      COUNTDOWN: <div class="flex gap-3 my-3" id="cd-{index}"> — 4 spans each with number (text-2xl font-black text-[' + acc + ']) + label (text-xs text-slate-400): DAYS HOURS MINS SECS\n' +
'      Price + Pre-Order button: justify-between flex items-center\n' +
'        Price: text-xl font-black text-white — {price}\n' +
'        Button: bg-[' + acc + '] text-black font-bold px-4 py-2 rounded-xl text-sm — "Pre-Order Now"\n\n' +

'[S10] JUST LANDED — NEW ARRIVALS (py-16 px-4 max-w-7xl mx-auto)\n' +
'  Header: "📦 Just Landed" + "View all new arrivals →"\n' +
'  Horizontal scroll row (flex overflow-x-auto gap-4 pb-4 scrollbar-hide snap-x snap-mandatory)\n' +
'  6 product mini-cards (min-w-[180px] snap-start bg-slate-800 rounded-xl overflow-hidden hover:scale-[1.03] transition cursor-pointer):\n' +
'    Image: picsum.photos/180/240?random={N} — aspect-[3/4] object-cover\n' +
'    Content p-3: "New" green badge + name (font-bold text-white text-xs leading-tight) + price (text-sm text-[' + acc + '] font-bold)\n\n' +

'[S11] SPORTS CARDS SPOTLIGHT (py-16 px-4 max-w-7xl mx-auto)\n' +
'  Header: "🏆 Sports Cards" + subtitle "MLB · NBA · NFL · NHL — Singles, Rookies, PSA Graded"\n' +
'  Two columns (grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8):\n' +
'    LEFT: Large banner image (picsum.photos/600/380?random=90) rounded-2xl object-cover with overlay gradient + text "Baseball, Basketball, Football & Hockey" + "Shop Sports →" CTA\n' +
'    RIGHT: 2x2 grid of sport sub-categories:\n' +
'      Each: bg-slate-800 rounded-xl p-5 flex items-center gap-4 hover:border-[' + acc + '] border border-transparent cursor-pointer transition\n' +
'      Icon (text-3xl) + Name (font-bold text-white) + count ("450+ Cards") text-slate-400 text-sm + "→" arrow\n' +
'      Sports: ⚾ Baseball | 🏀 Basketball | 🏈 Football | 🏒 Hockey\n\n' +

'[S12] GRADING SERVICE (py-16 px-4 max-w-7xl mx-auto)\n' +
'  Full bg-gradient-to-r from-slate-800 to-slate-900 rounded-3xl overflow-hidden p-8 lg:p-12\n' +
'  Two columns:\n' +
'    LEFT:\n' +
'      Small badge: "PSA · BGS · CGC Certified"\n' +
'      H2 (text-4xl font-black text-white Rajdhani): "Get Your Cards Professionally Graded"\n' +
'      P (text-slate-300): "Submit directly through Long Island Cards. We handle everything — submission, tracking, and return. Protect and increase the value of your collection."\n' +
'      3-step pills row (mt-6 flex gap-4 flex-wrap):\n' +
'        Each: bg-[' + acc + ']/10 border border-[' + acc + ']/30 rounded-xl p-3 text-center min-w-[100px]\n' +
'          Step number (text-[' + acc + '] font-black text-xl) + label (text-white text-sm font-medium)\n' +
'          Steps: "1 Submit" → "2 Grade" → "3 Return"\n' +
'      CTA btn (mt-6): bg-[' + acc + '] text-black font-bold px-6 py-3 rounded-xl — "Start Grading Submission →"\n' +
'      Sub text: "Estimated turnaround: 45–90 days | All grades accepted"\n' +
'    RIGHT: picsum.photos/400/350?random=95 rounded-2xl shadow-2xl with floating badge "PSA 10" (bg-blue-600 text-white font-black px-4 py-2 rounded-lg absolute -top-3 -right-3)\n\n' +

'[S13] SELL YOUR CARDS — WE BUY (py-16 px-4 max-w-7xl mx-auto)\n' +
'  bg-gradient-to-r from-[' + acc + ']/10 to-transparent border border-[' + acc + ']/20 rounded-3xl p-8 lg:p-12\n' +
'  Two columns:\n' +
'    LEFT:\n' +
'      H2 (text-4xl font-black text-white Rajdhani): "💰 Sell Your Cards to Us"\n' +
'      P: "Get instant cash or trade credit. We buy singles, collections, and entire binders. Fair market prices, same-day offers."\n' +
'      4 bullet points (mt-4 space-y-2): each "✓ text" class="flex items-center gap-2 text-slate-300"\n' +
'        ✓ Instant Online Quotes  ✓ Top-Dollar Payouts  ✓ Ship to Us or Walk In  ✓ Full Collections Welcome\n' +
'      Button row (mt-6):\n' +
'        Primary: bg-[' + acc + '] text-black font-bold px-6 py-3 rounded-xl — "Get a Free Quote"\n' +
'        Secondary: border border-white/30 text-white px-6 py-3 rounded-xl — "Learn More"\n' +
'    RIGHT: 3 stat cards (grid grid-cols-1 gap-4):\n' +
'      Each: bg-slate-800 rounded-xl p-5 text-center — big number (text-3xl font-black text-[' + acc + ']) + label (text-slate-300 text-sm)\n' +
'      Stats: "5,000+" "Cards Bought This Month" | "$2M+" "Paid to Collectors" | "24hr" "Average Payout Time"\n\n' +

'[S14] CUSTOMER REVIEWS (py-16 px-4 max-w-7xl mx-auto)\n' +
'  Header: "⭐ What Collectors Say" + overall (text-slate-400): "4.9/5 from 1,200+ verified reviews"\n' +
'  Grid (grid grid-cols-1 md:grid-cols-3 gap-6 mt-8)\n' +
'  EACH REVIEW CARD (bg-slate-800 rounded-2xl p-6 border border-white/5):\n' +
'    Stars: 5× "★" class="text-amber-400 text-lg"\n' +
'    Quote: class="text-slate-300 text-sm mt-3 leading-relaxed italic" — "{text}"\n' +
'    Footer row (mt-4 flex items-center justify-between):\n' +
'      Name (font-bold text-white text-sm) + Location (text-slate-400 text-xs)\n' +
'      "Verified Buyer" badge (bg-green-500/20 text-green-400 border border-green-500/30 text-xs px-2 py-1 rounded-full)\n\n' +

'[S15] THIS WEEK ONLY — PROMO COUNTDOWN (py-12 px-4 text-center bg-[' + acc + '] text-black)\n' +
'  "⚡ This Week Only" (text-xs font-bold uppercase tracking-widest opacity-70)\n' +
'  H2 (text-3xl font-black): "Buy Any Booster Box → Get FREE Card Sleeves (100-pack)"\n' +
'  P: "Limited offer. While supplies last."\n' +
'  COUNTDOWN DISPLAY (mt-4 flex justify-center gap-6):\n' +
'    4 blocks — each: bg-black/20 rounded-xl px-6 py-3\n' +
'      Number span (id="ct-d/h/m/s" text-4xl font-black font-mono): 00\n' +
'      Label (text-xs uppercase tracking-wider opacity-70): DAYS / HRS / MINS / SECS\n' +
'  CTA (mt-6): bg-black text-[' + acc + '] font-bold px-8 py-3 rounded-xl text-lg hover:bg-gray-900 — "Claim This Offer →"\n\n' +

'[S16] NEWSLETTER (py-16 px-4 text-center max-w-2xl mx-auto)\n' +
'  Icon: "📬" text-5xl\n' +
'  H2 (text-3xl font-black text-white Rajdhani): "Join 8,000+ Long Island Card Collectors"\n' +
'  P (text-slate-400 mt-3): "Weekly pulls · New set releases · Local event news · Exclusive deals — straight to your inbox."\n' +
'  Form (mt-6 flex gap-3 max-w-md mx-auto):\n' +
'    Input: class="flex-1 bg-slate-800 text-white border border-white/20 rounded-xl px-4 py-3 placeholder-slate-500 focus:outline-none focus:border-[' + acc + ']" placeholder="Your email address"\n' +
'    Button: class="bg-[' + acc + '] text-black font-bold px-6 py-3 rounded-xl whitespace-nowrap hover:bg-opacity-90" — "Subscribe"\n' +
'  Subtext (mt-3 text-slate-500 text-xs): "No spam. Unsubscribe anytime."\n' +
'  Social row (mt-6 flex justify-center gap-4):\n' +
'    Each platform: class="w-10 h-10 bg-slate-800 hover:bg-[' + acc + '] hover:text-black text-slate-400 rounded-full flex items-center justify-center transition-colors text-sm font-bold cursor-pointer"\n' +
'    Platforms: IG · YT · TT · X · DC · FB\n\n' +

'[S17] FOOTER (bg-[' + bg + '] border-t border-white/10 pt-12 pb-6)\n' +
'  4-column grid (grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 px-4 max-w-7xl mx-auto)\n' +
'    COL 1 — Brand:\n' +
'      Logo line: ♠ "Long Island Cards" (font-black text-white text-xl)\n' +
'      Tagline (text-slate-400 text-sm mt-2 leading-relaxed): ' + d.tagline + '\n' +
'      Social icons row (mt-4 flex gap-3): each w-9 h-9 bg-slate-800 hover:bg-[' + acc + '] rounded-full text-slate-400 hover:text-black\n' +
'    COL 2 — Shop links: heading "SHOP" (text-xs font-bold text-slate-500 uppercase tracking-widest) + ul (space-y-2 mt-3 text-slate-400 text-sm hover:text-white each li)\n' +
'      Links: ' + (d.footerLinks.shop||[]).join(', ') + '\n' +
'    COL 3 — Support: same pattern\n' +
'      Links: ' + (d.footerLinks.support||[]).join(', ') + '\n' +
'    COL 4 — Store Info:\n' +
'      Heading "VISIT US"\n' +
'      📍 605 Old Country Road, Plainview NY 11803\n' +
'      📞 (212) 564-8585\n' +
'      🕐 Mon–Sat 10am–7pm · Sun 11am–5pm\n' +
'      ✉️ info@longislandcards.com\n' +
'  BOTTOM BAR (mt-10 pt-6 border-t border-white/10 px-4 max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4):\n' +
'    Copyright: "© 2025 Long Island Cards. All rights reserved." text-slate-500 text-sm\n' +
'    Payment badges row: each badge bg-slate-800 text-slate-300 text-xs px-3 py-1 rounded font-medium\n' +
'      Badges: VISA · MC · AMEX · PAYPAL · DISCOVER · APPLE PAY\n\n' +

'══ JAVASCRIPT (place all before </body>) ══\n' +
'1. Announcement bar: document.querySelector(".dismiss-announce")?.addEventListener("click", e => e.target.closest("#announce-bar").remove())\n' +
'2. Hamburger: toggle hidden on mobile nav menu\n' +
'3. Search expand: toggle hidden on search bar div below header\n' +
'4. Wishlist hearts: document.querySelectorAll(".wishlist-btn").forEach(b => b.addEventListener("click", () => b.classList.toggle("text-red-500")))\n' +
'5. Cart counter: let cart=0; document.querySelectorAll(".add-to-cart").forEach(b => b.addEventListener("click", () => { cart++; document.querySelectorAll(".cart-count").forEach(el => el.textContent=cart) }))\n' +
'6. Pre-order countdowns: for each release, calculate days/hrs remaining to release date\n' +
'7. 48h promo countdown:\n' +
'   const end = Date.now() + 48*3600*1000;\n' +
'   setInterval(() => { const rem = Math.max(0, end - Date.now()); const d=Math.floor(rem/86400000), h=Math.floor(rem%86400000/3600000), m=Math.floor(rem%3600000/60000), s=Math.floor(rem%60000/1000); ["ct-d","ct-h","ct-m","ct-s"].forEach((id,i)=>{const el=document.getElementById(id); if(el) el.textContent=String([d,h,m,s][i]).padStart(2,"0")}) }, 1000)\n' +
'8. Sticky header: window.addEventListener("scroll", () => document.getElementById("main-header")?.classList.toggle("py-2", window.scrollY > 60))\n\n' +

'══ TECHNICAL ══\n' +
'- TailwindCSS: <script src="https://cdn.tailwindcss.com"></script>\n' +
'- tailwind.config: { theme: { extend: { colors: { brand: "' + bg + '", accent: "' + acc + '" }, fontFamily: { heading: ["Rajdhani","sans-serif"] } } } }\n' +
'- Fonts: <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">\n' +
'- <style>: @keyframes marquee { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} } .animate-marquee{animation:marquee 28s linear infinite} html{scroll-behavior:smooth} .scrollbar-hide::-webkit-scrollbar{display:none}\n' +
'- All images use picsum.photos with unique random seeds — never reuse same seed in same page\n' +
'- Each section has id attribute: announce, header, hero, ticker, brands, trust, products, categories, releases, arrivals, sports, grading, buylist, reviews, promo, newsletter, footer\n' +
'- PThere must be NO dark text on dark background anywhere in the page. Every text element must be explicitly visible.\n\n' +

'OUTPUT: Return ONLY the complete HTML starting with <!DOCTYPE html> and ending with </html>. NO markdown fences. NO explanations. JUST the HTML file.';

const htmlRequest = JSON.stringify({
  model:      prev.CLAUDE_MODEL,
  max_tokens: 10000,
  messages: [{ role: 'user', content: htmlPrompt }]
});

return [{ json: { ...prev, design: d, htmlRequest } }];
""".strip()

# Load workflow
with open('BasicWorkflow/ai-cloner-odoo.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

# Find and patch n9
patched = False
for node in wf['nodes']:
    if node['id'] == 'n9':
        node['parameters']['jsCode'] = NEW_JS
        patched = True
        break

if not patched:
    print("ERROR: node n9 not found!")
    sys.exit(1)

# Write back
with open('BasicWorkflow/ai-cloner-odoo.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)

print(f"Patched! New jsCode length: {len(NEW_JS)}")

# Verify
with open('BasicWorkflow/ai-cloner-odoo.json', 'r', encoding='utf-8') as f:
    wf2 = json.load(f)
n9 = next(n for n in wf2['nodes'] if n['id'] == 'n9')
js = n9['parameters']['jsCode']
checks = {
    'max_tokens 10000': '10000' in js,
    'Announcement bar S1': 'ANNOUNCEMENT BAR' in js,
    'Trending ticker S4': 'TRENDING TICKER' in js,
    'Pre-orders S9': 'UPCOMING RELEASES' in js,
    'Quick View': 'Quick View' in js,
    'Condition NM/LP': 'condition' in js.lower() and 'NM' in js,
    'Stock counter': 'Only 3 left' in js,
    'Testimonials S14': 'CUSTOMER REVIEWS' in js,
    'Sell cards S13': 'SELL YOUR CARDS' in js or 'buylist' in js.lower(),
    'Countdown timer': 'countdown' in js.lower() or 'ct-d' in js,
    'Wishlist hearts': 'wishlist' in js.lower(),
    'Cart counter': 'cart' in js.lower(),
    '17 sections': js.count('[S') >= 15,
    'Rajdhani font': 'Rajdhani' in js,
    'Color rules': 'MANDATORY COLOR RULES' in js,
    'No dark on dark': 'dark on dark' in js.lower() or 'NEVER VIOLATE' in js,
}
print("\nFeature checklist:")
all_ok = True
for feat, ok in checks.items():
    status = "✓" if ok else "✗"
    if not ok: all_ok = False
    print(f"  {status} {feat}")
print(f"\n{'ALL CHECKS PASSED' if all_ok else 'SOME CHECKS FAILED'}")
print(f"jsCode length: {len(js)} chars")
