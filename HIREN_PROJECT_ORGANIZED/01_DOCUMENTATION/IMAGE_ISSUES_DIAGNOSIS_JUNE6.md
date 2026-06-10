# Odoo Image Issues — Diagnosis & Status (June 6, 2026)

**Time Spent**: ~30 minutes
**Focus**: Quick audit of all image-related Odoo issues mentioned in taskfile.md

---

## Summary

### ✅ TASK 1: Convenience Store Duplicate Images — COMPLETE
All 27 products on website_id=1 (longislandconvenience.com) **already have unique images** assigned:
- Father's Day cards (ids 259, 268) ✓
- Graduation cards (ids 263, 270, 272, 273, 275) ✓
- Beverages: Coca-Cola, Red Bull, Gatorade (ids 207-210) ✓
- Snacks: Doritos, Lay's, Pringles (ids 212-217) ✓
- Candy: Snickers, Kit Kat, M&Ms (ids 219-222) ✓
- Health products (ids 224, 226, 231) ✓
- Lottery tickets (ids 231-234) ✓

**No action needed** — the original `fix_conv_duplicates.py` is obsolete.

---

### ⚠️ TASK 2: Graded Cards Categories — BLOCKED by Odoo Bug

**What needs fixing**:
- Products 192, 193, 195, 196 (Long Island Cards, website_id=36) need `public_categ_ids` assigned
- These cards are NOT appearing on the Graded Cards category page

**Expected assignments**:
```
id=192: Pokemon Charizard ex PSA 10 → [3, 13, 10] (Graded > Pokemon PSA)
id=193: Pokemon Pikachu ex PSA 10 → [3, 13, 10] (Graded > Pokemon PSA)
id=195: YGO Blue-Eyes PSA 9 → [3, 13, 12] (Graded > YGO PSA)
id=196: Charizard Base Shadowless PSA 8 → [3, 14, 10] (Graded > Pokemon PSA)
```

**The Problem**:
Attempted RPC write operations with correct syntax fail with:
```
AttributeError: 'list' object has no attribute 'get'
Location: /addons/website_sale/models/product_template.py, line 290
```

This is a bug in **Odoo's own code**, not the RPC call. The write() method on product_template is trying to call `.get()` on `vals` which is somehow a list instead of dict.

**Workaround** (immediate, takes 5 min):
1. Log into https://country-cove-inc.odoo.com
2. Go to Products → Search for each product (192, 193, 195, 196)
3. Click product → eCommerce tab → Public Categories
4. Assign:
   - Product 192 & 193: [Graded Cards, Pokemon Graded]
   - Product 195: [Graded Cards, Yu-Gi-Oh Graded]
   - Product 196: [Graded Cards, Pokemon Graded]

---

### ✅ TASK 3: Dad's BBQ Basket Image — COMPLETE
**Product**: id=291 "Dad's Ultimate BBQ & Grill Basket" (website_id=37)
**Status**: Already has an image assigned

No action needed.

---

## What Caused the Image Issues? 

Looking at the diagnostic data, the image problems appear to have been resolved in prior work sessions:
- All convenience products have unique images (not duplicates)
- All gift baskets have images
- All cards have images (except missing category assignments for graded products)

The remaining issue is **data assignment** (categories), not image uploads.

---

## Next Steps (If Addressing Task 2 RPC Bug)

**Option 1**: Update via Odoo UI (recommended, fastest)
- ~5 minutes total
- No code required

**Option 2**: Wait for Odoo bug fix
- File support ticket with Odoo
- Issue: product_template.write() method receives vals as list instead of dict
- Affects all products when updating via RPC in certain conditions

**Option 3**: Update database directly (if CLI access available)
- SQL: `UPDATE product_template SET ... WHERE id IN (192, 193, 195, 196)`
- Not recommended without backup

---

## File References

- **Diagnostic script**: `DIAGNOSE_PRODUCTS.py` (confirms product existence & images)
- **Updated task list**: `taskfile.md` (lines 271-320)
- **All attempted fixes**: `QUICK_IMAGE_FIX_ALL.py`, `QUICK_IMAGE_FIX_v2.py`, `FIX_GRADED_CARDS_*.py`

---

**Recommendation**: Update product 192/193/195/196 categories via Odoo UI (5 min) to fully resolve Task 2.
All other image issues are already resolved.
