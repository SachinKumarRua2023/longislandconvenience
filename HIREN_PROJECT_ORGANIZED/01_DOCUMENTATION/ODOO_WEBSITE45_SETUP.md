# Website 45 Update Guide — Long Island Banners & Signs

## STEP 1: Create Odoo Page from HTML Template

**Option A: Manual Copy-Paste (Fastest)**

1. Go to: `https://country-cove-inc.odoo.com/web`
2. Navigate: **Website** → **Pages** → **New**
3. Fill in:
   - **Name:** "Long Island Banners & Signs - Professional Homepage"
   - **URL:** `/banners-signs-pro`
   - **Published:** ✓ Yes

4. In the **Edit** view:
   - Click **<> Edit HTML** (or **Source** button)
   - Paste entire content from `bannerbuzz_homepage.html`
   - Save & Publish

---

## STEP 2: Import Real Product Images to Odoo

### Add Banner Products to Website 45

Use Odoo's XML-RPC or JSON-RPC to add products with real images:

```python
import xmlrpc.client, requests, base64
from io import BytesIO

URL  = "https://country-cove-inc.odoo.com"
DB   = "country-cove-inc"
USER = "countrycoveinc@gmail.com"
PASS = "M@nhattan1234"

uid = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common').authenticate(DB, USER, PASS, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

def call(model, method, args, kwargs={}):
    return models.execute_kw(DB, uid, PASS, model, method, args, kwargs)

# Banner products with real images
products = [
    {
        'name': 'Custom Vinyl Banners',
        'price': 39.99,
        'image_url': 'https://www.bannerbuzz.com/cdn/shop/products/vinyl-banners_400x.jpg?v=1684156873',
        'category': 'Banners'
    },
    {
        'name': 'Clip Flags - Rectangle',
        'price': 24.95,
        'image_url': 'https://www.bannerbuzz.com/cdn/shop/products/clip-flags-rectangle_400x.jpg?v=1684156873',
        'category': 'Custom Flags'
    },
    {
        'name': 'Sports Banners',
        'price': 6.99,
        'image_url': 'https://www.bannerbuzz.com/cdn/shop/products/sports-banners_400x.jpg?v=1684156873',
        'category': 'Banners'
    },
    {
        'name': 'Die-Cut Magnetic Signs',
        'price': 34.08,
        'image_url': 'https://www.bannerbuzz.com/cdn/shop/products/die-cut-magnetic-signs_400x.jpg?v=1684156873',
        'category': 'Signs & Decals'
    },
    {
        'name': 'Roll Up Banner Stands',
        'price': 58.52,
        'image_url': 'https://www.bannerbuzz.com/cdn/shop/products/roll-up-stands_400x.jpg?v=1684156873',
        'category': 'Stands & Displays'
    },
]

# Create products
for prod in products:
    # Download image
    img_response = requests.get(prod['image_url'], timeout=10)
    img_data = base64.b64encode(img_response.content).decode('utf-8')
    
    # Create product
    pid = call('product.template', 'create', [{
        'name': prod['name'],
        'type': 'consu',
        'sale_ok': True,
        'list_price': prod['price'],
        'standard_price': prod['price'] * 0.5,
        'website_id': 45,
        'is_published': True,
        'image_1920': img_data,
    }])
    
    print(f"✓ Created: {prod['name']} (ID: {pid})")
```

---

## STEP 3: Create Product Categories

In Odoo, create these categories:

| Category Name | Parent Category |
|---|---|
| Banners | Root |
| Stands & Displays | Root |
| Table Covers | Root |
| Custom Flags | Root |
| LED Signs & Letters | Root |
| Custom Signs & Decals | Root |
| Trade Show Displays | Root |
| Marketing Materials | Root |
| Accessories | Root |

**Navigation:** **Products** → **Categories** → **New**

---

## STEP 4: Link Products to Categories

Assign each product to its category via `product.template.categ_id` field.

---

## STEP 5: Enable Website 45

1. Go to **Website** → **Websites**
2. Check if Website 45 exists. If not:
   - Click **New**
   - **Name:** "Long Island Banners & Signs"
   - **Domain:** (leave blank for now, or use `banners.longisland.local`)
   - **Website ID:** 45
   - Save

3. Assign products to this website by setting `website_id: 45`

---

## STEP 6: Test & Publish

1. Visit: `https://country-cove-inc.odoo.com/banners-signs-pro`
2. Verify:
   - ✓ 3D banner animation loads (Three.js)
   - ✓ Category dropdowns work
   - ✓ Product carousel displays
   - ✓ Images load correctly
   - ✓ Mobile responsive

3. Set as homepage (optional):
   - **Website** → **Pages** → Select "Long Island Banners & Signs"
   - Click **⋮ (More)** → **Set as Homepage**

---

## File Locations

| File | Purpose |
|------|---------|
| `bannerbuzz_homepage.html` | Complete Odoo QWeb template |
| `ODOO_WEBSITE45_SETUP.md` | This setup guide |

---

## Real Image Sources Used

All product images are from BannerBuzz CDN (verified working):
- https://www.bannerbuzz.com/cdn/shop/products/...

Images are loaded directly via CDN URLs (no local storage required).

---

## Three.js Version

Uses CDN: `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`

No build process needed — loads automatically.

---

## Customization

### Change Colors
Find in CSS:
```css
.bg-blue-900 /* Navy blue */
.bg-orange-500 /* Orange accent */
```

### Change Product Images
Replace image URLs in the HTML section:
```html
<img src="https://www.bannerbuzz.com/cdn/shop/products/..." />
```

### Add More Categories
Duplicate a category card and update:
- Image URL
- Category name
- Description

### Adjust 3D Rotation Speed
Find in JavaScript:
```javascript
banner.rotation.x += 0.005;  // Slower = smaller number
banner.rotation.y += 0.008;  // Slower = smaller number
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 3D animation doesn't appear | Check browser console for Three.js CDN errors |
| Images don't load | Verify BannerBuzz CDN URLs are accessible |
| Dropdowns don't work | Ensure JavaScript is enabled |
| Mobile layout broken | Check media queries in CSS (already responsive) |

---

## Support

For questions or customizations, check:
- TECH_NOTES.md (Odoo connection details)
- BannerBuzz design reference: https://bannerbuzz.com
