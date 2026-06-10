#!/usr/bin/env python3
"""
Fix two issues:
1. n11: extract body content + head styles only (not full HTML with DOCTYPE)
2. n15: fix liveUrl to use websiteDomain not ODOO_URL
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

# ── FIX 1: n11 — extract body content + preserve head styles ─────────────────
nodes['n11']['parameters']['jsCode'] = DECODE_BUFFER + r"""
const resp = decodeBuffer($input.item.json);
const prev = $('Code: Build Cards HTML Prompt').item.json;

const raw = resp?.content?.[0]?.text || '';
let fullHtml = raw.trim();

// Extract from fenced code block or doctype
const fenced    = raw.match(/```html?\s*([\s\S]*?)```/i);
const doctypeIdx = raw.toLowerCase().indexOf('<!doctype');
if (fenced)        fullHtml = fenced[1].trim();
else if (doctypeIdx >= 0) fullHtml = raw.substring(doctypeIdx).trim();

// ── Extract <style> and <link rel="stylesheet"> from <head> ──────────────────
const headMatch  = fullHtml.match(/<head[^>]*>([\s\S]*?)<\/head>/i);
const headContent = headMatch ? headMatch[1] : '';

// Keep: <style>, <link rel="stylesheet">, <script src="...tailwind...">
const styleTags = [];
const styleRegex = /<style[\s\S]*?<\/style>/gi;
let sm;
while ((sm = styleRegex.exec(headContent)) !== null) styleTags.push(sm[0]);

const linkRegex = /<link[^>]+(?:stylesheet|font)[^>]*\/?>/gi;
let lm;
while ((lm = linkRegex.exec(headContent)) !== null) styleTags.push(lm[0]);

const scriptRegex = /<script[^>]+src=['"][^'"]*(?:tailwind|cdn\.tailwindcss)[^'"]*['"][^>]*><\/script>/gi;
let scm;
while ((scm = scriptRegex.exec(headContent)) !== null) styleTags.push(scm[0]);

const headAssets = styleTags.join('\n');

// ── Extract <body> content ────────────────────────────────────────────────────
const bodyMatch   = fullHtml.match(/<body[^>]*>([\s\S]*)<\/body>/i);
let bodyContent   = bodyMatch ? bodyMatch[1].trim() : fullHtml;

// Remove any remaining <html>, <head>, </html>, <!DOCTYPE lines if they slipped through
bodyContent = bodyContent
  .replace(/<!DOCTYPE[^>]*>/gi, '')
  .replace(/<\/?html[^>]*>/gi, '')
  .replace(/<head[\s\S]*?<\/head>/gi, '')
  .replace(/<\/?body[^>]*>/gi, '')
  .trim();

// Fallback: if we got nothing useful
if (bodyContent.length < 200) {
  bodyContent = '<div class="min-h-screen bg-slate-900 text-white flex items-center justify-center">'
    + '<div class="text-center"><h1 class="text-4xl font-bold text-amber-400 mb-4">Long Island Cards</h1>'
    + '<p class="text-gray-400">Nassau County\'s Trading Card Shop</p>'
    + '<p class="text-red-400 mt-4 text-sm">Generation returned ' + raw.length + ' chars — retry to regenerate.</p>'
    + '</div></div>';
}

// ── Build Odoo QWeb arch_db ───────────────────────────────────────────────────
// website.layout provides the full HTML wrapper; we inject assets + body content
const odooArch = '<t t-name="' + prev.pageKey + '">'
  + '<t t-call="website.layout">'
  + '<div id="wrap" class="oe_structure">'
  + (headAssets ? '\n' + headAssets + '\n' : '')
  + bodyContent
  + '\n</div>'
  + '</t>'
  + '</t>';

console.log('[HTML] fullHtml=' + fullHtml.length + ' bodyContent=' + bodyContent.length + ' assets=' + headAssets.length);

const createViewReq = JSON.stringify({
  jsonrpc: '2.0', method: 'call', id: 3,
  params: {
    service: 'object', method: 'execute_kw',
    args: [
      prev.ODOO_DB, prev.uid, prev.ODOO_PASS,
      'ir.ui.view', 'create',
      [{
        name:    'AI Cards Store: ' + prev.targetPageName,
        type:    'qweb',
        arch_db: odooArch,
        key:     prev.pageKey,
        mode:    'primary'
      }]
    ]
  }
});

return [{ json: {
  ...prev,
  html: bodyContent,
  htmlLength: bodyContent.length,
  fullHtmlLength: fullHtml.length,
  odooArch,
  createViewReq
}}];
"""
print(f"n11: body-only extraction written. Length: {len(nodes['n11']['parameters']['jsCode'])}")

# ── FIX 2: n15 — fix liveUrl to use websiteDomain ────────────────────────────
n15 = nodes['n15']
js15 = n15['parameters']['jsCode']

OLD15 = "const liveUrl   = odooOk ? (prev.ODOO_URL + prev.targetPageUrl) : null;"
NEW15 = ("const siteDomain = prev.websiteDomain || 'longislandcards.com';\n"
         "const siteBase   = siteDomain.startsWith('http') ? siteDomain : 'https://' + siteDomain;\n"
         "const liveUrl    = odooOk ? (siteBase + prev.targetPageUrl) : null;\n"
         "const adminUrl   = prev.ODOO_URL + prev.targetPageUrl;")

count = js15.count(OLD15)
print(f"n15 liveUrl fix — OLD found: {count}")
if count == 1:
    js15_new = js15.replace(OLD15, NEW15, 1)
    # Also add adminUrl to the return statement
    OLD_RETURN = "  liveUrl,"
    NEW_RETURN = "  liveUrl,\n  adminUrl,"
    js15_new = js15_new.replace(OLD_RETURN, NEW_RETURN, 1)
    n15['parameters']['jsCode'] = js15_new
    print(f"n15: liveUrl fixed to use websiteDomain. Length: {len(js15_new)}")
else:
    print("WARNING: replacement not found, printing current liveUrl line:")
    for line in js15.split('\n'):
        if 'liveUrl' in line: print(f"  {line}")

# ── Save ──────────────────────────────────────────────────────────────────────
for i, n in enumerate(wf['nodes']):
    if n['id'] in nodes:
        wf['nodes'][i] = nodes[n['id']]

with open(WORKFLOW, 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)

with open(WORKFLOW, 'r', encoding='utf-8') as f:
    wf2 = json.load(f)
print(f"\n✓ JSON valid — {len(wf2['nodes'])} nodes")

# Verify
nodes2 = {n['id']: n for n in wf2['nodes']}
n11js = nodes2['n11']['parameters']['jsCode']
n15js = nodes2['n15']['parameters']['jsCode']
print(f"\nn11 checks:")
print(f"  bodyMatch extraction: {'bodyMatch' in n11js}")
print(f"  styleTags extraction: {'styleTags' in n11js}")
print(f"  DOCTYPE stripped: {'removeDoctype' in n11js or 'DOCTYPE' in n11js}")
print(f"  body-only in arch_db: {'bodyContent' in n11js}")
print(f"\nn15 checks:")
print(f"  websiteDomain used: {'websiteDomain' in n15js}")
print(f"  adminUrl added: {'adminUrl' in n15js}")
print(f"  liveUrl uses siteBase: {'siteBase' in n15js}")
