# Odoo Product Import Guide - Long Island Cards

## CSV File Created: LONG_ISLAND_CARDS_PRODUCTS.csv

**16 Products** organized by **6 categories**:

| Category | Products | SKU Range |
|----------|----------|-----------|
| Sports Cards | 3 | SPORTS-001 to SPORTS-003 |
| Pokemon Cards | 3 | POKEMON-001 to POKEMON-003 |
| Magic: The Gathering | 3 | MTG-001 to MTG-003 |
| Yu-Gi-Oh! | 3 | YUGIOH-001 to YUGIOH-003 |
| Graded Cards | 3 | GRADED-001 to GRADED-003 |
| Premium Collections | 1 | BUNDLE-001 |

---

## Step 1: Create Product Categories in Odoo

Before importing products, create these categories:

1. Go to **eCommerce → Categories**
2. Click **Create**
3. Add each category:
   - **Sports Cards**
   - **Pokemon Cards**
   - **Magic: The Gathering**
   - **Yu-Gi-Oh!**
   - **Graded Cards**
   - **Premium Collections**

---

## Step 2: Import CSV into Odoo

### Method A: Direct Import (Recommended)

1. Go to **Inventory → Products** (or eCommerce Products)
2. Click **Import**
3. Select **LONG_ISLAND_CARDS_PRODUCTS.csv**
4. Map columns:
   - Category → Category
   - Product Name → Name
   - SKU → Internal Reference
   - Price → List Price
   - Description → Description
5. Click **Import**

### Method B: Manual Import

If automatic import fails:

1. Go to **Inventory → Products**
2. Click **Create** for each product
3. Fill in:
   - **Name**: Product Name from CSV
   - **Internal Reference**: SKU
   - **Category**: Match from dropdown
   - **Price**: List Price
   - **Description**: From CSV

---

## Step 3: Link Homepage Categories to Odoo Products

Update the homepage iframe code to link to Odoo products:

**Current links (in homepage):**
```html
<a href="/shop/sports-cards">Sports Cards</a>
<a href="/shop/pokemon-cards">Pokemon Cards</a>
```

**Update to point to Odoo shop pages:**
```html
<a href="/shop/category/sports-cards-1">Sports Cards</a>
<a href="/shop/category/pokemon-cards-1">Pokemon Cards</a>
<a href="/shop/category/magic-the-gathering-1">Magic: The Gathering</a>
<a href="/shop/category/yugioh-1">Yu-Gi-Oh!</a>
<a href="/shop/category/graded-cards-1">Graded Cards</a>
<a href="/shop/category/premium-collections-1">Premium Collections</a>
```

---

## Step 4: Add Product Images

For each product, you can add the card image:

1. Go to **Inventory → Products**
2. Open each product
3. Scroll to **Images** section
4. Upload the image from:
   ```
   C:\Users\Sachin Kumar\OneDrive\Desktop\HirenTask\longislandcards\images\
   ```
   
**Image mapping:**
- SPORTS-001 → sports-cards-left.png
- SPORTS-002 → sports-cards-center.png
- SPORTS-003 → sports-cards-right.png
- POKEMON-001 → pokemon-cards-left.png
- (etc...)

---

## Step 5: Verify Products

1. Go to your shop page: `lonislandcards.com/shop`
2. Check each category displays products
3. Click on product → should show details, price, image
4. Test "Add to Cart" functionality

---

## CSV Column Reference

```
Category       → Odoo Product Category (must exist first)
Product Name   → Product display name
SKU            → Internal Reference (unique ID)
Price          → List Price (retail price)
Description    → Product description
Image Name     → Image filename (for reference)
```

---

## If Import Fails

**Error: "Category doesn't exist"**
- Solution: Create categories first (Step 1)

**Error: "Product already exists"**
- Solution: SKUs must be unique, check for duplicates

**Error: "Price format invalid"**
- Solution: Use decimal format: 49.99 (not $49.99)

---

## Quick Checklist

- [ ] Create 6 product categories
- [ ] Import CSV file into Odoo
- [ ] Verify all 16 products created
- [ ] Add images to products
- [ ] Update homepage links to Odoo shop
- [ ] Test category pages work
- [ ] Test product pages display correctly
- [ ] Verify "Add to Cart" works

---

## Product List Summary

### Sports Cards (3 products)
- SPORTS-001: Sports Card Pack - Legacy Series ($49.99)
- SPORTS-002: Sports Card - Hall of Famers ($39.99)
- SPORTS-003: Sports Card - Signed Edition ($59.99)

### Pokemon Cards (3 products)
- POKEMON-001: Pokemon Card - Ancient Sol Ring ($34.99)
- POKEMON-002: Pokemon Card - Center Showcase ($44.99)
- POKEMON-003: Pokemon Card - Dragon Collection ($54.99)

### Magic: The Gathering (3 products)
- MTG-001: MTG Card - Left Collection ($39.99)
- MTG-002: MTG Card - Center Pack ($49.99)
- MTG-003: MTG Card - Right Bundle ($59.99)

### Yu-Gi-Oh! (3 products)
- YUGIOH-001: Yu-Gi-Oh Card Pack ($29.99)
- YUGIOH-002: Yu-Gi-Oh Starter Deck ($39.99)
- YUGIOH-003: Yu-Gi-Oh Premium Bundle ($49.99)

### Graded Cards (3 products)
- GRADED-001: Graded Cards - PSA Left ($79.99)
- GRADED-002: Graded Cards - PSA Center ($89.99)
- GRADED-003: Graded Cards - PSA Right ($99.99)

### Premium Collections (1 product)
- BUNDLE-001: Premium Bundle - Dragon Collection ($149.99)

---

**Total: 16 products, 6 categories, organized by card type**

Once products are in Odoo, your homepage will:
1. ✅ Display category cards
2. ✅ Link to actual product pages
3. ✅ Show inventory & prices
4. ✅ Allow customers to purchase
5. ✅ Auto-sync with GitHub images

