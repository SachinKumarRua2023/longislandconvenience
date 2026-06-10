# CATEGORY SHOWCASE IMAGE UPDATE
## longislandcards.com | Homepage Category Section

---

## CURRENT DESIGN
The homepage displays category cards with images:
- **Sports Cards** ✅ - Shows 3 actual trading card images (working)
- **Pokémon** ❌ - Shows placeholder icon
- **Magic: The Gathering** ❌ - Shows placeholder icon  
- **Yu-Gi-Oh!** ❌ - Shows placeholder icon
- **Graded Cards** ❌ - Shows placeholder icon

---

## SOLUTION: UPDATE CATEGORY CARDS WITH 3 PRODUCT IMAGES

### Design Requirements
Each category card should display:
- **3 featured product images** arranged horizontally
- **Category name** below the images
- **Same styling** as current Sports Cards showcase
- **Responsive layout** (mobile-friendly)
- **Click to browse category** functionality

### Current Sports Cards Design (Reference)
```
[Card 1 Image] [Card 2 Image] [Card 3 Image]
        Sports Cards
```

---

## IMPLEMENTATION APPROACH

### Option 1: Code-Based (RECOMMENDED - Dynamic)
Update the website React/Vue component to:
1. Fetch featured products from each category via API
2. Display 3 product images per category
3. Auto-update when new products are added

**File to Update:** `client/pages/Index.tsx` or category component
**Method:** Use product API to fetch featured items

```javascript
// Pseudo-code for category showcase
const categories = [
  { name: 'Sports Cards', products: fetchProducts('CARD-0005, CARD-0006, CARD-0007') },
  { name: 'Pokémon', products: fetchProducts('pokemon_category') },
  { name: 'Magic: The Gathering', products: fetchProducts('magic_category') },
  { name: 'Yu-Gi-Oh!', products: fetchProducts('yugioh_category') },
  { name: 'Graded Cards', products: fetchProducts('graded_category') }
];

categories.map(cat => (
  <CategoryCard
    name={cat.name}
    images={cat.products.map(p => p.image_1920)}
  />
))
```

### Option 2: Manual Images (Quick Fix)
1. Create composite images (3 products side-by-side)
2. Upload to `/public/assets/images/categories/`
3. Update HTML image sources

**Files:**
- `/public/assets/images/categories/pokemon-showcase.jpg`
- `/public/assets/images/categories/magic-showcase.jpg`
- `/public/assets/images/categories/yugioh-showcase.jpg`
- `/public/assets/images/categories/graded-showcase.jpg`

---

## FEATURED PRODUCTS PER CATEGORY

### Sports Cards (Already set up)
Featured Products:
- CARD-0005 - Sports Trading Card Set 5 ($49.99)
- CARD-0006 - Sports Trading Card Set 6 ($49.99)
- CARD-0010 - Sports Trading Card Set 10 ($49.99)

### Pokémon Cards (TO BE IDENTIFIED)
Suggested Featured Products:
- Pokémon Surging Sparks Booster Box
- Pokemon Elite Trainer Box
- Pokemon Destined Rivals Booster Box

### Magic: The Gathering (TO BE IDENTIFIED)
Suggested Featured Products:
- Magic 2025 Booster Pack
- Magic Mystery Booster
- Magic Elite Collection

### Yu-Gi-Oh! (TO BE IDENTIFIED)
Suggested Featured Products:
- Yu-Gi-Oh! Burst Protocol Booster Box
- Yu-Gi-Oh! Burst Protocol Starter
- Yu-Gi-Oh! Starter Deck

### Graded Cards (TO BE IDENTIFIED)
Suggested Featured Products:
- Luka Doncic 2018 PSA 10
- Patrick Mahomes 2017 PSA 9
- LeBron James 2003 PSA 8

---

## STEP-BY-STEP UPDATE INSTRUCTIONS

### Step 1: Identify Category Products in Odoo
```
Go to: Odoo > eCommerce > Products
Filter by:
- Pokemon (name contains "pokemon")
- Magic (name contains "magic")
- Yu-Gi-Oh (name contains "yu-gi-oh")
- Graded (name contains "graded" or "PSA")
```

### Step 2: Select Top 3 Products Per Category
For each category, choose:
- 1 highest priced product
- 1 mid-range product
- 1 most popular product

### Step 3: Get Product Image URLs
Each product's image is available in Odoo as `image_1920`
Download or reference via Odoo REST API endpoint:
```
/api/products/{product_id}/image
```

### Step 4: Update Website Component
**If using React/Vue:**
```javascript
// Add to HomePage or Category Section Component
const categoryShowcases = [
  {
    name: 'Sports Cards',
    products: [card5Id, card6Id, card10Id]
  },
  {
    name: 'Pokémon',
    products: [pokemonProduct1, pokemonProduct2, pokemonProduct3]
  },
  // ... etc
];

{categoryShowcases.map(cat => (
  <div className="category-card">
    <div className="product-images">
      {cat.products.map(productId => (
        <img src={`/api/products/${productId}/image`} />
      ))}
    </div>
    <h3>{cat.name}</h3>
  </div>
))}
```

### Step 5: Update CSS Styling
```css
.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.product-images {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.product-images img {
  width: 150px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.category-card h3 {
  font-size: 20px;
  font-weight: bold;
  color: white;
  text-align: center;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .product-images img {
    width: 100px;
    height: 140px;
  }
}
```

---

## CURRENT STATUS
- ✅ Sports Cards showcase working
- ⏳ Pokémon category - needs product image mapping
- ⏳ Magic: The Gathering - needs product image mapping
- ⏳ Yu-Gi-Oh! - needs product image mapping
- ⏳ Graded Cards - needs product image mapping

---

## QUICK WIN: Update Sports Cards Component First
Before updating other categories, ensure the Sports Cards showcase is properly styled:
1. Verify 3 product images are showing
2. Check image quality and sizing
3. Test on mobile devices
4. Use as template for other categories

---

## ESTIMATED EFFORT
- **Code-based approach:** 2-3 hours (development + testing)
- **Manual image approach:** 1-2 hours (image creation + upload)

## RECOMMENDATION
**Use Code-Based Approach** for:
- Automatic product updates
- Consistent styling
- Scalability for future products
- A/B testing different product combinations

---

## FILES TO UPDATE
1. `/client/pages/Index.tsx` - Add category showcase section
2. `/client/styles/categories.css` - Add styling
3. `/server/products-api.ts` - Add featured products endpoint (optional)

## NEXT STEPS
1. Identify 3 featured products per category
2. Implement dynamic category card component
3. Test on both desktop and mobile
4. Deploy to staging environment
5. Get user feedback before production launch
