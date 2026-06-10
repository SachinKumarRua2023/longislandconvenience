#!/usr/bin/env python3
"""
Fix product-image-scraper.json:
  1. Set continueOnFail=true on all 4 HTTP API nodes (n3, n4, n5, n6)
     so a 504 on pokemontcg.io doesn't kill the whole workflow
  2. Update n7: add fallback CDN images for each API when it returns an error
     so products are always created even if one API is down
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

WORKFLOW = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\BasicWorkflow\product-image-scraper.json"

with open(WORKFLOW, 'r', encoding='utf-8') as f:
    wf = json.load(f)

nodes_list = wf['nodes']
nodes = {n['id']: n for n in nodes_list}

# ── FIX 1: continueOnFail=true on all 4 HTTP API nodes ───────────────────────
for nid in ['n3', 'n4', 'n5', 'n6']:
    nodes[nid]['continueOnFail'] = True
    print(f"{nid} ({nodes[nid]['name']}): continueOnFail set to True")

# ── FIX 2: update n7 — add fallback cards for each API ───────────────────────
OLD_POKE = """// Decode all 4 API responses
const pokeRaw   = decodeBuffer($('HTTP: Pokemon TCG API').item.json);
const mtgRaw    = decodeBuffer($('HTTP: Scryfall MTG Cards').item.json);
const ygoRaw    = decodeBuffer($('HTTP: YGO Cards').item.json);
const sportsRaw = decodeBuffer($('HTTP: Firecrawl Sports + Custom URL').item.json);

// --- Pokemon cards ---
const pokeCards = Array.isArray(pokeRaw?.data) ? pokeRaw.data : [];
const pokeProducts = pokeCards.slice(0, cfg.cardsPerCat || 5).map(c => ({
  name: c.name || 'Pokemon Card',
  category: 'Pokemon TCG',
  imageUrl: c.images?.large || c.images?.small || null,
  set: c.set?.name || 'Scarlet & Violet',
  rarity: c.rarity || 'Rare',
  price: c.tcgplayer?.prices?.holoRare?.market || c.tcgplayer?.prices?.normal?.market || 9.99,
  source: 'pokemontcg.io'
}));
console.log('[Pokemon] found ' + pokeProducts.length + ' cards');"""

NEW_POKE = """// Decode all 4 API responses — safe even if a node failed (continueOnFail=true)
const pokeRaw   = decodeBuffer($('HTTP: Pokemon TCG API').item.json);
const mtgRaw    = decodeBuffer($('HTTP: Scryfall MTG Cards').item.json);
const ygoRaw    = decodeBuffer($('HTTP: YGO Cards').item.json);
const sportsRaw = decodeBuffer($('HTTP: Firecrawl Sports + Custom URL').item.json);

// Pokemon fallback CDN images (used when pokemontcg.io returns 504 or any error)
const POKEMON_FALLBACK = [
  { name: 'Charizard ex (Obsidian Flames)',  set: 'Scarlet & Violet — Obsidian Flames', rarity: 'Double Rare', price: 49.99, imageUrl: 'https://images.pokemontcg.io/sv3/125_hires.png' },
  { name: 'Gardevoir ex (Scarlet & Violet)', set: 'Scarlet & Violet Base',              rarity: 'Double Rare', price: 24.99, imageUrl: 'https://images.pokemontcg.io/sv1/86_hires.png' },
  { name: 'Pikachu ex (Paldean Fates)',      set: 'Scarlet & Violet — Paldean Fates',   rarity: 'Double Rare', price: 19.99, imageUrl: 'https://images.pokemontcg.io/sv4pt5/30_hires.png' },
  { name: 'Miraidon ex (Scarlet & Violet)',  set: 'Scarlet & Violet Base',              rarity: 'Ultra Rare',  price: 29.99, imageUrl: 'https://images.pokemontcg.io/sv1/81_hires.png' },
  { name: 'Koraidon ex (Scarlet & Violet)',  set: 'Scarlet & Violet Base',              rarity: 'Ultra Rare',  price: 27.99, imageUrl: 'https://images.pokemontcg.io/sv1/254_hires.png' },
  { name: 'Iono (Paldea Evolved)',           set: 'Scarlet & Violet — Paldea Evolved',  rarity: 'Ultra Rare',  price: 14.99, imageUrl: 'https://images.pokemontcg.io/sv2/185_hires.png' },
];

// MTG fallback images (used when Scryfall is down)
const MTG_FALLBACK = [
  { name: 'Ragavan, Nimble Pilferer', set: 'Modern Horizons 2',      price: 45.99, imageUrl: 'https://cards.scryfall.io/normal/front/a/9/a9a4e9c3-23ab-4b0c-bac9-c59e44e60e4a.jpg' },
  { name: 'Murktide Regent',          set: 'Modern Horizons 2',      price: 28.99, imageUrl: 'https://cards.scryfall.io/normal/front/1/d/1d5d9dcd-7b76-4585-9c24-87f13a9e1b83.jpg' },
  { name: 'Wrenn and Six',            set: 'Modern Horizons',        price: 34.99, imageUrl: 'https://cards.scryfall.io/normal/front/5/b/5bd498cc-a609-4457-9325-6888d9ce1d8d.jpg' },
  { name: 'Orcish Bowmasters',        set: 'Lord of the Rings',      price: 19.99, imageUrl: 'https://cards.scryfall.io/normal/front/0/9/09fd2d9c-1793-4bef-8f57-5e85a9a0e9e5.jpg' },
  { name: 'Solitude',                 set: 'Modern Horizons 2',      price: 22.99, imageUrl: 'https://cards.scryfall.io/normal/front/4/7/473b1f17-4e5e-4e60-8f45-37a4bd86c7bf.jpg' },
];

// YGO fallback images (used when YGOPRODECK is down)
const YGO_FALLBACK = [
  { name: 'Blue-Eyes White Dragon',     set: 'Legend of Blue Eyes',   price: 15.99, imageUrl: 'https://images.ygoprodeck.com/images/cards/89631139.jpg' },
  { name: 'Dark Magician',              set: 'Legend of Blue Eyes',   price: 8.99,  imageUrl: 'https://images.ygoprodeck.com/images/cards/46986414.jpg' },
  { name: 'Red-Eyes Black Dragon',      set: 'Legend of Blue Eyes',   price: 6.99,  imageUrl: 'https://images.ygoprodeck.com/images/cards/74677422.jpg' },
  { name: 'Exodia the Forbidden One',   set: 'Legend of Blue Eyes',   price: 12.99, imageUrl: 'https://images.ygoprodeck.com/images/cards/33396948.jpg' },
  { name: 'Seto Kaiba',                 set: 'Duelist League',        price: 4.99,  imageUrl: 'https://images.ygoprodeck.com/images/cards/88979991.jpg' },
];

// --- Pokemon cards — live API with fallback ---
const apiPokeOk = Array.isArray(pokeRaw?.data) && pokeRaw.data.length > 0;
const pokeSource = apiPokeOk ? pokeRaw.data.slice(0, cfg.cardsPerCat || 5) : [];
const pokeProducts = apiPokeOk
  ? pokeSource.map(c => ({
      name: c.name || 'Pokemon Card',
      category: 'Pokemon TCG',
      imageUrl: c.images?.large || c.images?.small || null,
      set: c.set?.name || 'Scarlet & Violet',
      rarity: c.rarity || 'Rare',
      price: c.tcgplayer?.prices?.holoRare?.market || c.tcgplayer?.prices?.normal?.market || 9.99,
      source: 'pokemontcg.io'
    }))
  : POKEMON_FALLBACK.slice(0, cfg.cardsPerCat || 5).map(c => ({ ...c, category: 'Pokemon TCG', rarity: c.rarity || 'Rare', source: 'CDN fallback' }));
console.log('[Pokemon] ' + pokeProducts.length + ' cards (' + (apiPokeOk ? 'live API' : 'FALLBACK — API was down') + ')');"""

js7 = nodes['n7']['parameters']['jsCode']
count = js7.count(OLD_POKE)
print(f"\nn7 OLD_POKE found: {count}")

if count == 1:
    js7 = js7.replace(OLD_POKE, NEW_POKE, 1)
    print("n7: Pokemon section replaced with fallback logic")
else:
    print("WARNING: exact match not found — searching for partial match")
    idx = js7.find("// --- Pokemon cards ---")
    if idx >= 0:
        print(f"Found '// --- Pokemon cards ---' at pos {idx}")
        print(repr(js7[idx:idx+300]))

# Also add fallback for MTG if API fails
OLD_MTG = """// --- MTG Scryfall cards ---
const mtgCards = Array.isArray(mtgRaw?.data) ? mtgRaw.data : [];
const mtgProducts = mtgCards.slice(0, cfg.cardsPerCat || 5).map(c => ({
  name: c.name || 'MTG Card',
  category: 'Magic: The Gathering',
  imageUrl: c.image_uris?"""

NEW_MTG = """// --- MTG Scryfall cards — live API with fallback ---
const apiMtgOk = Array.isArray(mtgRaw?.data) && mtgRaw.data.length > 0;
const mtgCards = apiMtgOk ? mtgRaw.data : [];
const mtgProducts = apiMtgOk
  ? mtgCards.slice(0, cfg.cardsPerCat || 5).map(c => ({
      name: c.name || 'MTG Card',
      category: 'Magic: The Gathering',
      imageUrl: c.image_uris?"""

count_mtg = js7.count(OLD_MTG)
print(f"n7 OLD_MTG found: {count_mtg}")
if count_mtg == 1:
    # Find the end of the mtg map block to close it properly
    idx_mtg = js7.find(OLD_MTG)
    # Find the closing of the .map block for mtg
    # Look for 'console.log' after mtg section
    after_mtg = js7[idx_mtg:]
    console_idx = after_mtg.find("console.log('[MTG]")
    if console_idx >= 0:
        mtg_block = after_mtg[:console_idx]
        # Replace the opening
        new_mtg_block = mtg_block.replace(
            "// --- MTG Scryfall cards ---\nconst mtgCards = Array.isArray(mtgRaw?.data) ? mtgRaw.data : [];\nconst mtgProducts = mtgCards.slice(0, cfg.cardsPerCat || 5).map(c => ({",
            "// --- MTG Scryfall cards — live API with fallback ---\nconst apiMtgOk = Array.isArray(mtgRaw?.data) && mtgRaw.data.length > 0;\nconst mtgProductsLive = (apiMtgOk ? mtgRaw.data : []).slice(0, cfg.cardsPerCat || 5).map(c => ({"
        )
        # Close and add fallback
        closing = "  source: 'scryfall'\n}));"
        if closing in new_mtg_block:
            new_mtg_block = new_mtg_block.replace(
                closing,
                "  source: 'scryfall'\n}));\nconst mtgProducts = apiMtgOk ? mtgProductsLive : MTG_FALLBACK.slice(0, cfg.cardsPerCat || 5).map(c => ({ ...c, category: 'Magic: The Gathering', rarity: 'Rare', source: 'CDN fallback' }));"
            )
            js7 = js7[:idx_mtg] + new_mtg_block + js7[idx_mtg + console_idx:]
            print("n7: MTG section updated with fallback")
        else:
            print(f"  MTG closing not found. Block tail: {repr(mtg_block[-200:])}")
    else:
        print("  MTG console.log not found")

# Update YGO fallback similarly — simpler approach
OLD_YGO_LOG = "console.log('[MTG] found ' + mtgProducts.length + ' cards');"
# Find YGO section
idx_ygo_section = js7.find("// --- YGO cards ---")
if idx_ygo_section >= 0:
    # Replace YGO simple map with fallback version
    OLD_YGO_BLOCK = """// --- YGO cards ---
const ygoCards = Array.isArray(ygoRaw?.data) ? ygoRaw.data : [];
const ygoProducts = ygoCards.slice(0, cfg.cardsPerCat || 5).map(c => ({"""
    NEW_YGO_BLOCK = """// --- YGO cards — live API with fallback ---
const apiYgoOk = Array.isArray(ygoRaw?.data) && ygoRaw.data.length > 0;
const ygoProductsLive = (apiYgoOk ? ygoRaw.data : []).slice(0, cfg.cardsPerCat || 5).map(c => ({"""
    if OLD_YGO_BLOCK in js7:
        js7 = js7.replace(OLD_YGO_BLOCK, NEW_YGO_BLOCK, 1)
        # Now find and replace the closing to add fallback
        OLD_YGO_CLOSE = "  source: 'ygoprodeck'\n}));\nconsole.log('[YGO] found ' + ygoProducts.length + ' cards');"
        NEW_YGO_CLOSE = "  source: 'ygoprodeck'\n}));\nconst ygoProducts = apiYgoOk ? ygoProductsLive : YGO_FALLBACK.slice(0, cfg.cardsPerCat || 5).map(c => ({ ...c, category: 'Yu-Gi-Oh! TCG', rarity: 'Rare', source: 'CDN fallback' }));\nconsole.log('[YGO] ' + ygoProducts.length + ' cards (' + (apiYgoOk ? 'live API' : 'FALLBACK') + ')');"
        if OLD_YGO_CLOSE in js7:
            js7 = js7.replace(OLD_YGO_CLOSE, NEW_YGO_CLOSE, 1)
            print("n7: YGO section updated with fallback")
        else:
            print("WARNING: YGO close block not found exactly — skipping YGO close patch")
            for line in js7.split('\n'):
                if 'YGO' in line and ('source' in line or 'found' in line):
                    print(f"  {line}")
    else:
        print("WARNING: YGO block not found — skipping")
else:
    print("WARNING: YGO section comment not found")

nodes['n7']['parameters']['jsCode'] = js7
print(f"\nn7 updated. jsCode length: {len(js7)}")

# ── Save ──────────────────────────────────────────────────────────────────────
for i, n in enumerate(wf['nodes']):
    if n['id'] in nodes:
        wf['nodes'][i] = nodes[n['id']]

with open(WORKFLOW, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)

with open(WORKFLOW, 'r', encoding='utf-8') as f:
    wf2 = json.load(f)

print(f"\n✓ JSON valid — {len(wf2['nodes'])} nodes")

nodes2 = {n['id']: n for n in wf2['nodes']}
print("\n=== SCRAPER FIX AUDIT ===")
for nid in ['n3','n4','n5','n6']:
    cof = nodes2[nid].get('continueOnFail', False)
    print(f"  {nid} ({nodes2[nid]['name']}): continueOnFail={cof}")

js7f = nodes2['n7']['parameters']['jsCode']
print(f"\n  POKEMON_FALLBACK defined: {'POKEMON_FALLBACK' in js7f}")
print(f"  MTG_FALLBACK defined: {'MTG_FALLBACK' in js7f}")
print(f"  YGO_FALLBACK defined: {'YGO_FALLBACK' in js7f}")
print(f"  apiPokeOk check: {'apiPokeOk' in js7f}")
print(f"  apiMtgOk check: {'apiMtgOk' in js7f}")
print(f"  apiYgoOk check: {'apiYgoOk' in js7f}")
print(f"  CDN fallback message: {'CDN fallback' in js7f}")
