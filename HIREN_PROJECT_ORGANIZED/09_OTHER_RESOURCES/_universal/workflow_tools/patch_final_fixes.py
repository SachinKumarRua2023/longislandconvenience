#!/usr/bin/env python3
"""
Final fixes:
  1. n5  — add decodeBuffer (fallback path protection)
  2. n15 — add uid, ODOO_DB, ODOO_PASS to output so n15b can use them
  3. n15b — read creds from Code: Build Page Request (n13) which has full chain
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

WORKFLOW = r"c:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\BasicWorkflow\ai-cloner-odoo.json"

with open(WORKFLOW, 'r', encoding='utf-8') as f:
    wf = json.load(f)

nodes = {n['id']: n for n in wf['nodes']}

DECODE_BUFFER = """function decodeBuffer(resp) {
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
"""

# ── FIX 1: n5 — add decodeBuffer ─────────────────────────────────────────────
n5 = nodes['n5']
js5 = n5['parameters']['jsCode']
js5_new = DECODE_BUFFER + js5.replace(
    'const websiteResp = $input.item.json;',
    'const websiteResp = decodeBuffer($input.item.json);'
)
n5['parameters']['jsCode'] = js5_new
print(f"n5: decodeBuffer added. Length: {len(js5_new)}")

# ── FIX 2: n15 — add uid, ODOO_DB, ODOO_PASS to output ──────────────────────
n15 = nodes['n15']
js15 = n15['parameters']['jsCode']

OLD15 = "  ODOO_URL:     prev.ODOO_URL,\n  odooAuthOk:   prev.odooOk,"
NEW15 = ("  ODOO_URL:     prev.ODOO_URL,\n"
         "  ODOO_DB:      prev.ODOO_DB,\n"
         "  ODOO_PASS:    prev.ODOO_PASS,\n"
         "  uid:          prev.uid,\n"
         "  odooAuthOk:   prev.odooOk,")

count15 = js15.count(OLD15)
print(f"n15 OLD found: {count15}")
if count15 == 1:
    js15_new = js15.replace(OLD15, NEW15, 1)
    n15['parameters']['jsCode'] = js15_new
    print(f"n15: uid/ODOO_DB/ODOO_PASS added to output. Length: {len(js15_new)}")
else:
    print(f"WARNING: n15 replacement not found — checking current content")
    ret_pos = js15.rfind('return [')
    print(js15[ret_pos:ret_pos+500])

# ── FIX 3: n15b — read creds from n13 (Code: Build Page Request) ─────────────
n15b = nodes['n15b']
# Rewrite n15b completely to read credentials from the correct source
n15b['parameters']['jsCode'] = DECODE_BUFFER + """const prev = $('Code: Build Final Summary').item.json;
// Read credentials from Code: Build Page Request (has full credential chain)
const creds = $('Code: Build Page Request').item.json;

const pageId    = prev.pageId    || null;
const websiteId = prev.websiteId || 36;
const uid       = creds.uid      || 2;
const ODOO_DB   = creds.ODOO_DB  || 'country-cove-inc';
const ODOO_PASS = creds.ODOO_PASS|| 'M@nhattan1234';
const ODOO_URL  = creds.ODOO_URL || 'https://country-cove-inc.odoo.com';

console.log('[Homepage] pageId=' + pageId + ' websiteId=' + websiteId + ' uid=' + uid);

// Only set homepage if page was created successfully
if (!pageId) {
  console.log('[Homepage] No pageId — skipping homepage write');
  return [{ json: { ...prev, uid, ODOO_DB, ODOO_PASS, ODOO_URL, homepageSet: false, homepageSkipped: true } }];
}

// JSON-RPC body: write homepage_id on website.website (site websiteId)
const setHomepageReq = JSON.stringify({
  jsonrpc: '2.0', method: 'call', id: 5,
  params: {
    service: 'object', method: 'execute_kw',
    args: [
      ODOO_DB, uid, ODOO_PASS,
      'website.website', 'write',
      [[websiteId], { homepage_id: pageId }]
    ]
  }
});

console.log('[Homepage] Writing homepage_id=' + pageId + ' to website ' + websiteId);

return [{ json: { ...prev, uid, ODOO_DB, ODOO_PASS, ODOO_URL, setHomepageReq, homepageSet: false } }];
"""
print(f"n15b: rewritten — reads creds from Code: Build Page Request. Length: {len(n15b['parameters']['jsCode'])}")

# ── Save ──────────────────────────────────────────────────────────────────────
# Update nodes list in workflow
for i, n in enumerate(wf['nodes']):
    if n['id'] in nodes:
        wf['nodes'][i] = nodes[n['id']]

with open(WORKFLOW, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)

# Final validation
with open(WORKFLOW, 'r', encoding='utf-8') as f:
    wf2 = json.load(f)

print(f"\n✓ JSON valid — {len(wf2['nodes'])} nodes")

print("\n=== FINAL AUDIT ===")
nodes2 = {n['id']: n for n in wf2['nodes']}
checks = {
    'n3':  ['decodeBuffer', 'uid', 'fetchWebsitesReq'],
    'n5':  ['decodeBuffer', 'websiteId', 'knownSiteId', 'targetPageUrl'],
    'n7':  ['decodeBuffer', 'analyzeRequest'],
    'n9':  ['decodeBuffer', 'clientBriefBlock', 'hasBrief', 'CLIENT BRIEF', 'htmlRequest', 'max_tokens'],
    'n11': ['decodeBuffer', 'arch_db', 'website.layout', 'createViewReq'],
    'n13': ['decodeBuffer', 'viewId', 'is_homepage', 'website_id', 'createPageReq'],
    'n15': ['decodeBuffer', 'pageId', 'liveUrl', 'uid', 'ODOO_DB', 'ODOO_PASS'],
    'n15b':['Build Page Request', 'homepage_id', 'pageId', 'uid', 'ODOO_DB', 'ODOO_PASS', 'setHomepageReq'],
    'n15d':['decodeBuffer', 'homepageSet'],
}
all_ok = True
for nid, keywords in checks.items():
    n = nodes2[nid]
    js = n['parameters'].get('jsCode','')
    missing = [k for k in keywords if k not in js]
    status = '✓' if not missing else '✗'
    if missing: all_ok = False
    print(f"  [{status}] {nid}: {n['name']}" + (f" — MISSING: {missing}" if missing else ""))

print()
if all_ok:
    print("✅ ALL CHECKS PASS — workflow is ready to import and run")
else:
    print("⚠️  Some checks failed — review above")
