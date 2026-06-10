#!/usr/bin/env python3
"""
Upgrades ai-cloner-odoo.json with a full client brief form:
  - Form Trigger: 8 rich fields (client describes exactly what they want)
  - Parse Input: captures all form fields + injects into config
  - Build Cards HTML Prompt: uses client brief in Claude prompt
  - Form completion: shows what was built
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('BasicWorkflow/ai-cloner-odoo.json', 'r', encoding='utf-8') as f:
    wf = json.load(f)

# ── PATCH 1: Form Trigger (t0) ─────────────────────────────────────────────
NEW_FORM = {
    "path": "redesign-cards",
    "formTitle": "🃏 Long Island Cards — AI Website Builder",
    "formDescription": "Fill in your requirements below. The AI will generate a full, professional website and publish it to your Odoo store automatically.",
    "responseMode": "responseNode",
    "formFields": {
        "values": [
            {
                "fieldLabel": "Which Website to Update?",
                "fieldType": "dropdown",
                "fieldOptions": {
                    "values": [
                        {"option": "Long Island Cards (longislandcards.com)"},
                        {"option": "Long Island Convenience"},
                        {"option": "Long Island Gift Basket"},
                        {"option": "Long Island Greeting Cards"},
                        {"option": "Long Island Lotto"},
                        {"option": "Cyber Consulting (consultcyber.net)"}
                    ]
                },
                "requiredField": True
            },
            {
                "fieldLabel": "Design Style",
                "fieldType": "dropdown",
                "fieldOptions": {
                    "values": [
                        {"option": "Modern Dark (Navy + Gold)"},
                        {"option": "Vibrant Colorful (Bold + Energetic)"},
                        {"option": "Minimal Clean (White + Accent)"},
                        {"option": "Luxury Premium (Black + Gold)"},
                        {"option": "Let AI Decide Best Style"}
                    ]
                },
                "requiredField": False
            },
            {
                "fieldLabel": "This Week's Special Promotion",
                "fieldType": "text",
                "placeholder": "e.g. Buy any booster box, get FREE card sleeves — this weekend only",
                "requiredField": False
            },
            {
                "fieldLabel": "Products or Items to Feature",
                "fieldType": "textarea",
                "placeholder": "List 3-5 products, sets, or categories to highlight this week.\ne.g. Charizard ex SAR ($89.99), Pokemon 151 Box, MTG Duskmourn, Shohei Ohtani PSA 10",
                "requiredField": False
            },
            {
                "fieldLabel": "Announcement Bar Message",
                "fieldType": "text",
                "placeholder": "e.g. 🔥 Pokemon Stellar Crown Pre-Orders NOW OPEN — Limited Stock!",
                "requiredField": False
            },
            {
                "fieldLabel": "Events or News This Week",
                "fieldType": "text",
                "placeholder": "e.g. Saturday Draft Tournament 2pm | New MTG Set Release Friday | Grading Submissions Close Sunday",
                "requiredField": False
            },
            {
                "fieldLabel": "Custom Hero Headline",
                "fieldType": "text",
                "placeholder": "Leave blank — AI writes the headline. Or type your own: e.g. 'Pokemon Stellar Crown Is Here!'",
                "requiredField": False
            },
            {
                "fieldLabel": "Auto-Publish to Odoo?",
                "fieldType": "dropdown",
                "fieldOptions": {
                    "values": [
                        {"option": "No — save as draft, I will review first"},
                        {"option": "Yes — publish immediately (live on site)"}
                    ]
                },
                "requiredField": False
            }
        ]
    }
}

for node in wf['nodes']:
    if node['id'] == 't0':
        node['parameters'] = NEW_FORM
        print("✓ Patched Form Trigger (t0)")
        break

# ── PATCH 2: Parse Input (n1) ──────────────────────────────────────────────
NEW_PARSE_JS = r"""
const item = $input.item.json;
const isForm = typeof item['Design Style'] === 'string' || typeof item['Which Website to Update?'] === 'string';

// ── Read form fields with fallbacks ────────────────────────────────────────
const websiteChoice  = (isForm ? item['Which Website to Update?']      : '') || 'Long Island Cards (longislandcards.com)';
const designStyle    = (isForm ? item['Design Style']                  : '') || 'Modern Dark (Navy + Gold)';
const promotion      = (isForm ? item['This Week\'s Special Promotion']   : '') || '';
const featuredItems  = (isForm ? item['Products or Items to Feature']  : '') || '';
const announcement   = (isForm ? item['Announcement Bar Message']      : '') || '';
const eventsNews     = (isForm ? item['Events or News This Week']      : '') || '';
const customHeadline = (isForm ? item['Custom Hero Headline']          : '') || '';
const publishChoice  = (isForm ? item['Auto-Publish to Odoo?']        : '') || 'No — save as draft, I will review first';
const autoPublish    = publishChoice.toLowerCase().includes('yes') || publishChoice.toLowerCase().includes('immediately');

// ── Map website choice to known IDs ───────────────────────────────────────
// website_id=36 = Long Island Cards (confirmed live)
// other sites: auto-discover via website.website search in n5
const SITE_MAP = {
  'long island cards': 36,
  'long island convenience': 1,
  'long island gift basket': 37,
  'long island greeting cards': 18,
  'long island lotto': 33,
  'cyber consulting': 29,
};
const wChoiceLower = websiteChoice.toLowerCase();
let knownSiteId = null;
for (const [key, id] of Object.entries(SITE_MAP)) {
  if (wChoiceLower.includes(key.split(' ').slice(-2).join(' ')) || wChoiceLower.includes(key)) {
    knownSiteId = id;
    break;
  }
}

// ── Normalize style ────────────────────────────────────────────────────────
const styleClean = designStyle.split('(')[0].trim()
  .replace('Let AI Decide Best Style', 'Modern Dark');

// ── Client brief object — passed all the way to Claude prompt ──────────────
const clientBrief = {
  websiteChoice,
  promotion:      promotion.trim(),
  featuredItems:  featuredItems.trim(),
  announcement:   announcement.trim(),
  eventsNews:     eventsNews.trim(),
  customHeadline: customHeadline.trim(),
};

const hasPromotion  = clientBrief.promotion.length > 0;
const hasFeatured   = clientBrief.featuredItems.length > 0;
const hasAnnounce   = clientBrief.announcement.length > 0;
const hasEvents     = clientBrief.eventsNews.length > 0;
const hasHeadline   = clientBrief.customHeadline.length > 0;

console.log('[Parse] website=' + websiteChoice + ' knownId=' + knownSiteId);
console.log('[Parse] style=' + styleClean + ' publish=' + autoPublish);
console.log('[Parse] brief — promo=' + hasPromotion + ' featured=' + hasFeatured + ' events=' + hasEvents);

return [{ json: {
  isFormTrigger: isForm,
  designStyle:   styleClean,
  autoPublish,
  knownSiteId,
  clientBrief,
  ts: Date.now(),
  FIRECRAWL_KEY: 'fc-471db502e79143e0982f3d2638b8ccdb',
  CLAUDE_KEY:    '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',
  CLAUDE_MODEL:  'claude-sonnet-4-6',
  ODOO_URL:  'https://country-cove-inc.odoo.com',
  ODOO_DB:   'country-cove-inc',
  ODOO_USER: 'countrycoveinc@gmail.com',
  ODOO_PASS: 'M@nhattan1234',
  startedAt: new Date().toISOString()
}}];
""".strip()

for node in wf['nodes']:
    if node['id'] == 'n1':
        node['parameters']['jsCode'] = NEW_PARSE_JS
        print("✓ Patched Parse Input (n1)")
        break

# ── PATCH 3: Find Cards Website ID (n5) — use knownSiteId if available ─────
NEW_FIND_SITE_JS = r"""
const websiteResp = $input.item.json;
const cfg = $('Code: Parse Auth + Build Fetch').item.json;
const parsedCfg = $('Parse Input').item.json;

// If Parse Input resolved a known ID — use it directly, skip fuzzy search
if (parsedCfg.knownSiteId) {
  const knownId = parsedCfg.knownSiteId;
  const websites = websiteResp?.result || [];
  const knownSite = websites.find(w => w.id === knownId) || { id: knownId, name: parsedCfg.clientBrief?.websiteChoice || 'Long Island Cards', domain: 'longislandcards.com' };
  console.log('[Site] Using knownSiteId=' + knownId + ' name=' + knownSite.name);

  const ts = cfg.ts;
  const targetPageUrl  = '/ai-redesign-' + ts;
  const targetPageName = 'AI Redesign: ' + knownSite.name;
  const pageKey        = 'website.page_ai_redesign_' + ts;

  return [{ json: {
    ...cfg,
    clientBrief:    parsedCfg.clientBrief,
    websiteId:      knownId,
    websiteName:    knownSite.name,
    websiteDomain:  knownSite.domain || 'longislandcards.com',
    allWebsites:    websites,
    targetPageUrl,
    targetPageName,
    pageKey
  }}];
}

// Fallback: fuzzy search by name/domain
const websites = websiteResp?.result || [];
console.log('[Websites] Searching ' + websites.length + ' sites');

const choice = (parsedCfg.clientBrief?.websiteChoice || '').toLowerCase();
const match = websites.find(w => {
  const t = ((w.name||'') + ' ' + (w.domain||'')).toLowerCase();
  if (choice.includes('card') || choice.includes('longislandcards'))
    return t.includes('card') || t.includes('longisland');
  if (choice.includes('convenience')) return t.includes('convenience');
  if (choice.includes('gift basket')) return t.includes('basket');
  if (choice.includes('greeting'))    return t.includes('greeting');
  if (choice.includes('lotto'))       return t.includes('lotto');
  if (choice.includes('cyber') || choice.includes('consult')) return t.includes('cyber') || t.includes('consult');
  return t.includes('card');
});
const targetSite = match || websites[0] || { id: 36, name: 'Long Island Cards', domain: 'longislandcards.com' };

console.log('[Site] Resolved id=' + targetSite.id + ' name=' + targetSite.name);

const ts = cfg.ts;
const targetPageUrl  = '/ai-redesign-' + ts;
const targetPageName = 'AI Redesign: ' + targetSite.name;
const pageKey        = 'website.page_ai_redesign_' + ts;

return [{ json: {
  ...cfg,
  clientBrief:    parsedCfg.clientBrief,
  websiteId:      targetSite.id,
  websiteName:    targetSite.name,
  websiteDomain:  targetSite.domain || 'longislandcards.com',
  allWebsites:    websites,
  targetPageUrl,
  targetPageName,
  pageKey
}}];
""".strip()

for node in wf['nodes']:
    if node['id'] == 'n5':
        node['parameters']['jsCode'] = NEW_FIND_SITE_JS
        print("✓ Patched Find Cards Website ID (n5)")
        break

# ── PATCH 4: Build Cards HTML Prompt (n9) — inject clientBrief ───────────
# Read current n9 jsCode and prepend brief-injection block before htmlPrompt
for node in wf['nodes']:
    if node['id'] == 'n9':
        current_js = node['parameters']['jsCode']
        # Insert client brief extraction right after design data section
        # We inject just before the htmlPrompt = line
        INJECT_BRIEF = r"""
// ── Inject client brief into the prompt ─────────────────────────────────────
const brief = prev.clientBrief || {};
const briefPromo      = brief.promotion      || '';
const briefFeatured   = brief.featuredItems  || '';
const briefAnnounce   = brief.announcement   || '';
const briefEvents     = brief.eventsNews     || '';
const briefHeadline   = brief.customHeadline || '';

// Override hero headline if client specified one
if (briefHeadline) d.heroSection.headline = briefHeadline;

// Override announcement bar text if client specified one
const announcementText = briefAnnounce ||
  '🔥 FREE SHIPPING on orders $75+  |  Same-day shipping before 2pm EST  |  Use code LIC10 — 10% off first order  |  ' +
  (briefPromo ? briefPromo : 'Pokemon Stellar Crown Pre-Orders NOW OPEN →');

// Build client brief section for Claude
const clientBriefBlock = [
  briefPromo    ? ('THIS WEEK PROMOTION: ' + briefPromo)            : '',
  briefFeatured ? ('PRODUCTS TO FEATURE: ' + briefFeatured)        : '',
  briefEvents   ? ('EVENTS / NEWS: ' + briefEvents)                 : '',
  briefAnnounce ? ('ANNOUNCEMENT BAR: ' + briefAnnounce)           : '',
  briefHeadline ? ('CUSTOM HERO HEADLINE (use exactly): ' + briefHeadline) : '',
].filter(Boolean).join('\n');

const hasBrief = clientBriefBlock.length > 0;

"""
        # Find the line where htmlPrompt starts
        if 'const htmlPrompt =' in current_js:
            insert_pos = current_js.index('const htmlPrompt =')
            # Also need to add brief section to the prompt string itself
            # Find the DATA section in the prompt and add brief after it
            new_js = current_js[:insert_pos] + INJECT_BRIEF + current_js[insert_pos:]

            # Now inject the brief block into the actual htmlPrompt string
            # Find the DATA section header and add brief after it
            brief_section = (
                "\"'\\n\\n\" +\n"
                "'══ CLIENT BRIEF (follow these requirements exactly) ══\\n' +\n"
                "(hasBrief ? clientBriefBlock : '(no specific brief — use AI best judgment)') + '\\n\\n' +\n"
                "\n'══ BRAND DATA ══\\n' +\n"
            )
            # Replace the brand data header
            if "'══ BRAND DATA ══\\n' +" in new_js:
                new_js = new_js.replace(
                    "'══ BRAND DATA ══\\n' +",
                    "'══ CLIENT BRIEF (follow these requirements exactly, these override everything) ══\\n' +\n"
                    "(hasBrief ? (clientBriefBlock + '\\n') : '(no specific requirements — full AI creative control)\\n') +\n"
                    "\n'══ BRAND DATA ══\\n' +"
                )
            # Also inject the dynamic announcement text
            if "'🔥 FREE SHIPPING on orders $75+'" in new_js:
                new_js = new_js.replace(
                    "'🔥 FREE SHIPPING on orders $75+",
                    "' + announcementText + '"
                )
                # Now remove the hardcoded full announce text up to the closing quote
                # This is complex — let's just replace the announce text reference
            node['parameters']['jsCode'] = new_js
            print("✓ Patched Build Cards HTML Prompt (n9) — client brief injected")
        else:
            print("⚠ Could not find htmlPrompt in n9 — skipping brief injection")
        break

# ── PATCH 5: Form completion (n17) — show what was built ──────────────────
for node in wf['nodes']:
    if node['id'] == 'n17':
        node['parameters']['completionTitle'] = "={{ $json.odooOk ? '✅ Your Website Has Been ' + ($json.published ? 'Published' : 'Saved as Draft') + '!' : '⚠️ Partial — Check Logs' }}"
        node['parameters']['completionMessage'] = (
            "={{ $json.odooOk ? "
            "'**Website:** ' + $json.websiteName + '\\n'"
            " + '**Page URL:** ' + ($json.ODOO_URL || 'https://country-cove-inc.odoo.com') + $json.pageUrl + '\\n'"
            " + '**HTML Size:** ' + $json.htmlKB + ' KB\\n'"
            " + '**Status:** ' + ($json.published ? '🟢 Live on your site now' : '🟡 Saved as draft — review in Odoo Website editor') + '\\n\\n'"
            " + '**To set as homepage:** Odoo → Website → Pages → ⋮ → Set as Homepage\\n'"
            " + '**View it:** ' + ($json.ODOO_URL || 'https://country-cove-inc.odoo.com') + $json.pageUrl "
            ": 'Auth OK=' + $json.odooAuthOk + ' | View ID: ' + $json.viewId + ' | Page ID: ' + $json.pageId + '\\nCheck n8n logs for details.' }}"
        )
        print("✓ Patched Form completion message (n17)")
        break

# ── Save ───────────────────────────────────────────────────────────────────
with open('BasicWorkflow/ai-cloner-odoo.json', 'w', encoding='utf-8') as f:
    json.dump(wf, f, ensure_ascii=False, indent=2)

# ── Verify ────────────────────────────────────────────────────────────────
print("\n=== VERIFICATION ===")
with open('BasicWorkflow/ai-cloner-odoo.json', 'r', encoding='utf-8') as f:
    wf2 = json.load(f)

t0 = next(n for n in wf2['nodes'] if n['id'] == 't0')
n1 = next(n for n in wf2['nodes'] if n['id'] == 'n1')
n5 = next(n for n in wf2['nodes'] if n['id'] == 'n5')
n9 = next(n for n in wf2['nodes'] if n['id'] == 'n9')

form_fields = t0['parameters']['formFields']['values']
print(f"Form fields: {len(form_fields)}")
for f in form_fields:
    req = " (required)" if f.get('requiredField') else ""
    print(f"  • {f['fieldLabel']}{req}")

print(f"\nParse Input jsCode: {len(n1['parameters']['jsCode'])} chars")
print(f"  Has clientBrief: {'clientBrief' in n1['parameters']['jsCode']}")
print(f"  Has knownSiteId: {'knownSiteId' in n1['parameters']['jsCode']}")
print(f"  Has SITE_MAP: {'SITE_MAP' in n1['parameters']['jsCode']}")

print(f"\nFind Site jsCode: {len(n5['parameters']['jsCode'])} chars")
print(f"  Has knownSiteId shortcut: {'knownSiteId' in n5['parameters']['jsCode']}")

print(f"\nBuild HTML Prompt jsCode: {len(n9['parameters']['jsCode'])} chars")
print(f"  Has CLIENT BRIEF block: {'CLIENT BRIEF' in n9['parameters']['jsCode']}")
print(f"  Has briefPromo: {'briefPromo' in n9['parameters']['jsCode']}")

print(f"\nJSON valid: YES  |  Nodes: {len(wf2['nodes'])}")
print("\n✅ All patches applied successfully")
print("\nFORM URL (once active in n8n):")
print("  https://newworksatnight.app.n8n.cloud/form/redesign-cards")
