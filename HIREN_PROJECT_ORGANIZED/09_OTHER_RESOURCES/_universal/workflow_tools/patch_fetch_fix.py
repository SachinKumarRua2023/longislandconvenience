#!/usr/bin/env python3
"""
Fix n9: replace fetch() with $helpers.httpRequest()
n8n Code nodes do NOT have fetch — must use $helpers.httpRequest
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

WORKFLOW = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\BasicWorkflow\product-image-scraper.json"

with open(WORKFLOW, 'r', encoding='utf-8') as f:
    wf = json.load(f)
nodes = {n['id']: n for n in wf['nodes']}

NEW_N9 = """// Decode Buffer helper
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

const prev = $('Code: Aggregate Products + Build Claude Prompt').item.json;
const cfg  = prev.cfg;
const uid  = prev.uid;
const allProducts = prev.allProducts || [];

// Decode and parse Claude JSON descriptions
const claudeRaw = decodeBuffer($input.item.json);
const rawText = claudeRaw?.content?.[0]?.text || '';
let descriptions = [];
try {
  const m = rawText.match(/\\[\\s\\S]*\\]/);
  if (m) descriptions = JSON.parse(m[0]);
} catch(e) {
  console.log('[Descriptions] parse error: ' + e.message);
}
console.log('[Descriptions] parsed ' + descriptions.length + ' from Claude');

const descMap = {};
for (const d of descriptions) {
  if (d.name) descMap[d.name.toLowerCase().trim()] = d;
}

// ── $helpers.httpRequest replaces fetch() — fetch is NOT in n8n Code nodes ──

async function getImageB64(url) {
  if (!url) return null;
  try {
    const buf = await $helpers.httpRequest({
      method: 'GET',
      url: url,
      encoding: 'arraybuffer',
      returnFullResponse: false,
      timeout: 10000,
    });
    return Buffer.from(buf).toString('base64');
  } catch(e) {
    console.log('[Image] failed ' + url.substring(0, 60) + ' — ' + e.message);
    return null;
  }
}

const odooCall = async (method, model, args, kwargs={}) => {
  const req = {
    jsonrpc: '2.0', method: 'call', id: Date.now(),
    params: {
      service: 'object', method: 'execute_kw',
      args: [cfg.ODOO_DB, uid, cfg.ODOO_PASS, model, method, args, kwargs]
    }
  };
  const r = await $helpers.httpRequest({
    method: 'POST',
    url: cfg.ODOO_URL + '/jsonrpc',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(req),
  });
  const parsed = (typeof r === 'string') ? JSON.parse(r) : r;
  return parsed?.result;
};

// Download all images in parallel
const imageUrls = allProducts.map(p => p.imageUrl || null);
console.log('[Images] downloading ' + imageUrls.filter(Boolean).length + ' images...');
const imageB64s = await Promise.all(imageUrls.map(url => getImageB64(url)));
console.log('[Images] downloaded ' + imageB64s.filter(Boolean).length + ' successfully');

// Find Long Island Cards website
let targetWebsiteId = null;
if (uid) {
  try {
    const websites = await odooCall('search_read', 'website.website', [[[]]], { fields: ['id', 'name', 'domain'], limit: 20 });
    console.log('[Websites] found ' + (websites?.length || 0));
    const cardsSite = (websites || []).find(w => {
      const t = ((w.name||'') + ' ' + (w.domain||'')).toLowerCase();
      return t.includes('card') || t.includes('longisland');
    });
    if (cardsSite) {
      targetWebsiteId = cardsSite.id;
      console.log('[Websites] Long Island Cards: id=' + cardsSite.id + ' name=' + cardsSite.name);
    }
  } catch(e) {
    console.log('[Websites] lookup error: ' + e.message);
  }
}

// Get or create Odoo product categories
const categoryNames = ['Pokemon TCG', 'Magic: The Gathering', 'Yu-Gi-Oh!', 'Sports Cards', 'Sealed Products'];
const categoryIds = {};

if (uid) {
  for (const catName of categoryNames) {
    try {
      const existing = await odooCall('search_read', 'product.category',
        [[['name', '=', catName]]], { fields: ['id', 'name'], limit: 1 });
      if (existing && existing.length > 0) {
        categoryIds[catName] = existing[0].id;
        console.log('[Category] found "' + catName + '" id=' + existing[0].id);
      } else {
        const newId = await odooCall('create', 'product.category', [{ name: catName }]);
        categoryIds[catName] = newId;
        console.log('[Category] created "' + catName + '" id=' + newId);
      }
    } catch(e) {
      console.log('[Category] error for ' + catName + ': ' + e.message);
    }
  }
}

// Create products in Odoo
const createdProducts = [];

if (uid) {
  for (let i = 0; i < allProducts.length; i++) {
    const p = allProducts[i];
    const desc = descMap[p.name.toLowerCase().trim()] || {};
    const listPrice = desc.price || p.price || 9.99;
    const catId = categoryIds[p.category] || false;
    const imgB64 = imageB64s[i] || null;

    const productVals = {
      name: p.name,
      type: 'consu',
      sale_ok: true,
      list_price: listPrice,
      standard_price: Math.round(listPrice * 0.5 * 100) / 100,
      description_sale: desc.fullDescription || desc.shortDescription || ('Premium ' + p.category + ' — ' + (p.set || '')),
      is_published: cfg.autoPublish === true
    };
    if (catId) productVals.categ_id = catId;
    if (imgB64) productVals.image_1920 = imgB64;
    if (targetWebsiteId) productVals.website_id = targetWebsiteId;

    try {
      const newId = await odooCall('create', 'product.template', [productVals]);
      createdProducts.push({ name: p.name, category: p.category, odooId: newId, price: listPrice, badge: desc.badge || 'New', hasImage: !!(imgB64) });
      console.log('[Odoo] created "' + p.name + '" id=' + newId);
    } catch(e) {
      console.log('[Odoo] error "' + p.name + '": ' + e.message);
      createdProducts.push({ name: p.name, category: p.category, odooId: null, error: e.message });
    }
  }
} else {
  console.log('[Odoo] skipping — no uid');
  for (const p of allProducts) createdProducts.push({ name: p.name, category: p.category, odooId: null, skipped: true });
}

const totalCreated = createdProducts.filter(p => p.odooId).length;
console.log('[Done] Created ' + totalCreated + ' / ' + allProducts.length + ' products in Odoo');

return [{ json: {
  cfg, uid,
  websiteId: targetWebsiteId,
  createdProducts,
  totalAttempted: allProducts.length,
  totalCreated,
  totalImages: imageB64s.filter(Boolean).length,
  categories: Object.keys(categoryIds)
}}];"""

nodes['n9']['parameters']['jsCode'] = NEW_N9.strip()

for i, n in enumerate(wf['nodes']):
    if n['id'] in nodes:
        wf['nodes'][i] = nodes[n['id']]

with open(WORKFLOW, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)

with open(WORKFLOW, 'r', encoding='utf-8') as f:
    wf2 = json.load(f)

nodes2 = {n['id']: n for n in wf2['nodes']}
js9f = nodes2['n9']['parameters']['jsCode']
print(f"JSON valid: {len(wf2['nodes'])} nodes")
print()
print('=== n9 AUDIT ===')
print(f"  fetch() removed:          {'await fetch(' not in js9f}")
print(f"  httpRequest image:        {'encoding' in js9f and 'arraybuffer' in js9f}")
print(f"  httpRequest odoo:         {'$helpers.httpRequest' in js9f}")
print(f"  decodeBuffer kept:        {'decodeBuffer' in js9f}")
print(f"  odooCall defined:         {'odooCall' in js9f}")
print(f"  product.template create:  {'product.template' in js9f}")
print(f"  image_1920 set:           {'image_1920' in js9f}")
print(f"  is_published set:         {'is_published' in js9f}")
print(f"  website_id set:           {'website_id' in js9f}")
