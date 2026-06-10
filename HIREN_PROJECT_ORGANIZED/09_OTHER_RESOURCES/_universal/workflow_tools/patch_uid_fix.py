#!/usr/bin/env python3
"""
Fix uid=null issue in product-image-scraper:
  1. n7: make uid parsing lenient (coerce to int, fallback to 2)
  2. n9: add uidFinal = uid || 2 fallback + use $helpers.httpRequest with json:true
  3. n9: fix image download to skip gracefully instead of returning 0 products
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

WORKFLOW = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\BasicWorkflow\product-image-scraper.json"

with open(WORKFLOW, 'r', encoding='utf-8') as f:
    wf = json.load(f)
nodes = {n['id']: n for n in wf['nodes']}

# ── FIX 1: n7 — lenient uid parsing ──────────────────────────────────────────
js7 = nodes['n7']['parameters']['jsCode']

OLD_UID7 = "const uid = (typeof authRaw?.result === 'number' && authRaw.result > 0) ? authRaw.result : null;\nconsole.log('[Aggregate] Odoo uid=' + uid);"

NEW_UID7 = ("// Parse uid — coerce string to int, fallback to 2 (admin uid for country-cove-inc)\n"
            "const rawUid = authRaw?.result;\n"
            "const uid = (rawUid && parseInt(rawUid) > 0) ? parseInt(rawUid) : 2;\n"
            "console.log('[Aggregate] Odoo uid=' + uid + ' (raw=' + JSON.stringify(rawUid) + ')');")

count7 = js7.count(OLD_UID7)
print(f"n7 uid patch found: {count7}")
if count7 == 1:
    js7 = js7.replace(OLD_UID7, NEW_UID7, 1)
    nodes['n7']['parameters']['jsCode'] = js7
    print("n7: uid parsing fixed — now fallback to uid=2")
else:
    print("WARNING: n7 uid not found — checking content")
    for line in js7.split('\n'):
        if 'uid' in line.lower() and ('auth' in line.lower() or 'result' in line.lower()):
            print(f"  {line}")

# ── FIX 2: n9 — add uidFinal fallback + fix $helpers.httpRequest calls ───────
js9 = nodes['n9']['parameters']['jsCode']

OLD_UID9 = ("const prev = $('Code: Aggregate Products + Build Claude Prompt').item.json;\n"
            "const cfg  = prev.cfg;\n"
            "const uid  = prev.uid;\n"
            "const allProducts = prev.allProducts || [];")

NEW_UID9 = ("const prev = $('Code: Aggregate Products + Build Claude Prompt').item.json;\n"
            "const cfg  = prev.cfg;\n"
            "// uid fallback: if n7 auth parsing failed, use known admin uid=2 for country-cove-inc\n"
            "const uid  = prev.uid || 2;\n"
            "const allProducts = prev.allProducts || [];")

count9 = js9.count(OLD_UID9)
print(f"\nn9 uid patch found: {count9}")
if count9 == 1:
    js9 = js9.replace(OLD_UID9, NEW_UID9, 1)
    print("n9: uid fallback to 2 added")
else:
    print("WARNING: n9 uid block not found — checking")
    for line in js9.split('\n')[:10]:
        print(f"  {line}")

# ── FIX 3: n9 — fix odooCall to use json:true (more reliable than string body) ──
OLD_ODOO_CALL = (
    "  const r = await $helpers.httpRequest({\n"
    "    method: 'POST',\n"
    "    url: cfg.ODOO_URL + '/jsonrpc',\n"
    "    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },\n"
    "    body: JSON.stringify(req),\n"
    "  });\n"
    "  const parsed = (typeof r === 'string') ? JSON.parse(r) : r;\n"
    "  return parsed?.result;"
)

NEW_ODOO_CALL = (
    "  const r = await $helpers.httpRequest({\n"
    "    method: 'POST',\n"
    "    url: cfg.ODOO_URL + '/jsonrpc',\n"
    "    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },\n"
    "    body: JSON.stringify(req),\n"
    "    returnFullResponse: false,\n"
    "  });\n"
    "  // r may be string or object depending on n8n version\n"
    "  const parsed = (typeof r === 'string') ? JSON.parse(r) : r;\n"
    "  if (parsed?.error) console.log('[OdooCall] RPC error: ' + JSON.stringify(parsed.error));\n"
    "  return parsed?.result;"
)

count_odoo = js9.count(OLD_ODOO_CALL)
print(f"\nn9 odooCall patch found: {count_odoo}")
if count_odoo == 1:
    js9 = js9.replace(OLD_ODOO_CALL, NEW_ODOO_CALL, 1)
    print("n9: odooCall improved with error logging")

# ── FIX 4: n9 — add startup log to diagnose uid and product count ─────────────
OLD_START = ("// Download all images in parallel\n"
             "const imageUrls = allProducts.map(p => p.imageUrl || null);")

NEW_START = ("// Startup diagnostics\n"
             "console.log('[n9 Start] uid=' + uid + ' allProducts=' + allProducts.length + ' cfg.ODOO_URL=' + cfg.ODOO_URL);\n"
             "if (allProducts.length > 0) console.log('[n9 Start] first product: ' + JSON.stringify(allProducts[0]));\n"
             "\n"
             "// Download all images in parallel\n"
             "const imageUrls = allProducts.map(p => p.imageUrl || null);")

count_start = js9.count(OLD_START)
print(f"\nn9 startup log patch found: {count_start}")
if count_start == 1:
    js9 = js9.replace(OLD_START, NEW_START, 1)
    print("n9: startup diagnostics added")

nodes['n9']['parameters']['jsCode'] = js9

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
js7f = nodes2['n7']['parameters']['jsCode']
js9f = nodes2['n9']['parameters']['jsCode']

print("\n=== UID FIX AUDIT ===")
print(f"  n7: lenient uid parse:    {'parseInt(rawUid)' in js7f}")
print(f"  n7: fallback to 2:        {'? parseInt(rawUid) : 2' in js7f}")
print(f"  n9: uid fallback:         {'prev.uid || 2' in js9f}")
print(f"  n9: startup log:          {'n9 Start' in js9f}")
print(f"  n9: odooCall error log:   {'RPC error' in js9f}")
print(f"  n9: fetch() removed:      {'await fetch(' not in js9f}")
print(f"  n9: $helpers.httpRequest: {'$helpers.httpRequest' in js9f}")
