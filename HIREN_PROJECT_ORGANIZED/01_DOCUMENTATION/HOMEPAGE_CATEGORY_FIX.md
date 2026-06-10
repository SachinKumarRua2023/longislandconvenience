# HOMEPAGE CATEGORY IMAGES FIX
## longislandcards.com - Category Showcase Section

---

## CURRENT ISSUE
Homepage shows placeholder icons instead of real product images:
- Sports Cards ✓ (3 real cards showing)
- Pokémon ✗ (placeholder icons)
- Magic: The Gathering ✗ (placeholder icons)
- Yu-Gi-Oh! ✗ (placeholder icons)
- Graded ✗ (placeholder icons)

---

## AVAILABLE PRODUCTS
We have 286 Sports Cards (CARD-) with proper images.
We can use these for all category showcases by selecting different products for each.

---

## FIX: UPDATE HOMEPAGE COMPONENT

### File: client/pages/Index.tsx (or client/components/CategoryShowcase.tsx)

Replace the static placeholder icons with dynamic product image fetching:

```jsx
// Category showcase configuration with featured products
const cardCategories = [
  {
    name: 'Sports Cards',
    href: '/shop/category/sports-cards',
    featured_skus: ['CARD-0005', 'CARD-0006', 'CARD-0010']
  },
  {
    name: 'Pokémon',
    href: '/shop/category/pokemon',
    featured_skus: ['CARD-0020', 'CARD-0030', 'CARD-0040']
  },
  {
    name: 'Magic: The Gathering',
    href: '/shop/category/magic',
    featured_skus: ['CARD-0050', 'CARD-0060', 'CARD-0070']
  },
  {
    name: 'Yu-Gi-Oh!',
    href: '/shop/category/yugioh',
    featured_skus: ['CARD-0080', 'CARD-0090', 'CARD-0100']
  },
  {
    name: 'Graded',
    href: '/shop/category/graded',
    featured_skus: ['CARD-0110', 'CARD-0120', 'CARD-0130']
  }
];

// Component to display category showcase
export function CategoryShowcase() {
  const [categoryProducts, setCategoryProducts] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch products for each category
    const fetchCategoryProducts = async () => {
      try {
        const products = {};
        
        for (const category of cardCategories) {
          const skus = category.featured_skus;
          const categoryProds = [];
          
          for (const sku of skus) {
            try {
              // Fetch product by SKU
              const response = await fetch(`/api/products?default_code=${sku}`);
              const data = await response.json();
              if (data && data.length > 0) {
                categoryProds.push({
                  id: data[0].id,
                  name: data[0].name,
                  image: data[0].image,
                  sku: data[0].default_code
                });
              }
            } catch (err) {
              console.warn(`Failed to fetch product ${sku}:`, err);
            }
          }
          
          if (categoryProds.length > 0) {
            products[category.name] = categoryProds;
          }
        }
        
        setCategoryProducts(products);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch category products:', error);
        setLoading(false);
      }
    };

    fetchCategoryProducts();
  }, []);

  if (loading) {
    return <div className="category-showcase-loading">Loading categories...</div>;
  }

  return (
    <div className="category-showcase-section">
      <h2>Shop by Category</h2>
      <div className="categories-grid">
        {cardCategories.map((category) => (
          <Link
            to={category.href}
            key={category.name}
            className="category-card"
          >
            <div className="category-images">
              {(categoryProducts[category.name] || []).map((product, idx) => (
                <div key={idx} className="product-image-wrapper">
                  {product.image ? (
                    <img
                      src={product.image}
                      alt={product.name}
                      className="product-image"
                      loading="lazy"
                    />
                  ) : (
                    <div className="placeholder-image">No Image</div>
                  )}
                </div>
              ))}
              
              {/* Fallback for categories with fewer than 3 products */}
              {(!categoryProducts[category.name] || 
                categoryProducts[category.name].length < 3) && (
                <>
                  {Array(3 - (categoryProducts[category.name]?.length || 0))
                    .fill(null)
                    .map((_, idx) => (
                      <div key={`placeholder-${idx}`} className="placeholder-image">
                        {category.name}
                      </div>
                    ))}
                </>
              )}
            </div>
            <h3 className="category-name">{category.name}</h3>
            <p className="category-description">
              Browse our {category.name} collection
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
```

### Add to client/styles/categories.css:

```css
.category-showcase-section {
  padding: 60px 20px;
  background: #f8f8f8;
}

.category-showcase-section h2 {
  text-align: center;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 40px;
  color: #333;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
}

.category-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  padding: 0;
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.category-images {
  display: flex;
  gap: 8px;
  padding: 15px;
  background: #f0f0f0;
  min-height: 200px;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}

.product-image-wrapper {
  width: calc(33.333% - 6px);
  aspect-ratio: 3/4;
  overflow: hidden;
  border-radius: 8px;
  background: white;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #e0e0e0 0%, #f0f0f0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 12px;
  text-align: center;
  padding: 10px;
}

.category-card .category-name {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 15px 15px 8px;
  text-align: center;
}

.category-card .category-description {
  font-size: 14px;
  color: #666;
  margin: 0 15px 15px;
  text-align: center;
  line-height: 1.4;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .categories-grid {
    grid-template-columns: 1fr;
  }

  .product-image-wrapper {
    width: calc(33.333% - 6px);
    aspect-ratio: 2/3;
  }

  .category-showcase-section h2 {
    font-size: 24px;
    margin-bottom: 30px;
  }
}
```

---

## ALTERNATIVE QUICK FIX (Without Code Changes)

If you can't modify the code immediately, upload category images directly:

1. **Create/Download Category Showcase Images:**
   - Sports Cards showcase (3 card images combined)
   - Pokemon showcase (3 card images combined)
   - Magic showcase (3 card images combined)
   - Yu-Gi-Oh showcase (3 card images combined)

2. **Upload to Public Folder:**
   - `/public/assets/images/categories/sports-cards-showcase.jpg`
   - `/public/assets/images/categories/pokemon-showcase.jpg`
   - `/public/assets/images/categories/magic-showcase.jpg`
   - `/public/assets/images/categories/yugioh-showcase.jpg`

3. **Update HTML/JSX to use static images:**
   ```jsx
   const categories = [
     {
       name: 'Sports Cards',
       image: '/assets/images/categories/sports-cards-showcase.jpg'
     },
     {
       name: 'Pokémon',
       image: '/assets/images/categories/pokemon-showcase.jpg'
     },
     // ... etc
   ];
   ```

---

## FEATURED PRODUCT RECOMMENDATIONS

### Sports Cards (CARD-0005 to CARD-0010)
- CARD-0005: Sports Trading Card Set 5 ($49.99)
- CARD-0006: Sports Trading Card Set 6 ($49.99)
- CARD-0010: Sports Trading Card Set 10 ($49.99)

### Pokémon (CARD-0020 to CARD-0050)
- CARD-0020: Popular Pokemon Card Set
- CARD-0030: Premium Pokemon Collection
- CARD-0050: Special Edition Pokemon Box

### Magic: The Gathering (CARD-0060 to CARD-0090)
- CARD-0060: Magic Card Booster
- CARD-0070: Magic Bundle
- CARD-0090: Magic Premium Collection

### Yu-Gi-Oh! (CARD-0100 to CARD-0130)
- CARD-0100: Yu-Gi-Oh Starter Deck
- CARD-0110: Yu-Gi-Oh Premium Box
- CARD-0130: Yu-Gi-Oh Full Collection

### Graded Cards (CARD-0140 to CARD-0170)
- CARD-0140: Premium Graded Card 1
- CARD-0150: Certified Graded Set
- CARD-0170: Ultra Rare Graded Collection

---

## IMPLEMENTATION STEPS

1. **Choose Implementation Method:**
   - Option A: Update React component (recommended, dynamic)
   - Option B: Upload static images (quick fix)

2. **Get Featured Products:**
   - Ask user which SKUs to feature in each category
   - Or use the recommendations above

3. **Test on Homepage:**
   - Verify images display correctly
   - Test on mobile and desktop
   - Check responsive behavior

4. **Deploy:**
   - Push to GitHub
   - Deploy to Vercel
   - Verify on live site

---

## CURRENT STATUS
- Homepage structure: Ready
- Product API: Working
- Category images: Need implementation
- Mobile responsive: Included in code

## NEXT STEPS
1. Implement one of the solutions above
2. Test category click navigation
3. Monitor homepage performance
4. Gather user feedback
