# Complete Odoo Integration Guide - Step by Step

## 📋 Overview

Integrate the advanced Long Island Convenience website into your Odoo instance with full functionality including:
- Image galleries with 3 product images per store
- Dynamic special events and coupons calendar
- Real-time discount offers
- Professional store showcase

---

## 🔐 Odoo Login Details

```
URL: https://country-cove-inc.odoo.com
Database: country-cove-inc
Email: countrycoveinc@gmail.com
Password: M@nhattan1234
Web ID: 1
```

---

## 📑 Table of Contents

1. [Method 1: Create Custom HTML Page (Easiest)](#method-1-custom-html-page)
2. [Method 2: Embed as Iframe (Quick)](#method-2-iframe-embed)
3. [Method 3: Full Module Integration (Advanced)](#method-3-odoo-module)
4. [Image Management](#image-management)
5. [Real-Time Offers Integration](#real-time-offers)
6. [Testing & Troubleshooting](#testing--troubleshooting)

---

## Method 1: Custom HTML Page (EASIEST) ⭐

### Step 1: Log in to Odoo

1. Visit: https://country-cove-inc.odoo.com
2. Login with your credentials
3. Go to **Website** > **Pages**

### Step 2: Create New Page

1. Click **+ New**
2. Fill in:
   - **Page Title**: "Home" or "Store Showcase"
   - **URL**: "/" (if making homepage) or "/stores"
   - **Website**: Select your website

### Step 3: Edit Page Content

1. Click **Edit**
2. Look for **HTML Editor** or **<> Code** button
3. **Clear all existing content**

### Step 4: Copy & Paste HTML (Body Only)

Copy everything from the `<body>` section of `index.html`:

```html
<!-- Hero Section -->
<div class="hero-section">
    <h1 class="hero-title">✨ Long Island Convenience</h1>
    <p class="hero-subtitle">7 Brands. One Neighborhood. Premium Gifts & Services</p>
</div>

<!-- Main Container -->
<div class="container">
    <!-- Special Events & Coupons Section -->
    <div class="offers-section">
        <h2 class="section-title">🎉 Special Events & Best Offers</h2>
        <div class="calendar-grid" id="eventsGrid">
            <!-- Events will be dynamically inserted here -->
        </div>
    </div>

    <!-- Stores with Image Galleries -->
    <div class="stores-section">
        <h2 class="section-title">🏪 Our Stores</h2>
        <div class="stores-grid" id="storesGrid">
            <!-- Store cards will be dynamically inserted here -->
        </div>
    </div>

    <!-- Features Section -->
    <h2 class="section-title">Why Choose Long Island Convenience?</h2>
    <div class="features-grid">
        <!-- Features content -->
    </div>

    <!-- CTA Banner -->
    <div class="cta-banner">
        <!-- CTA content -->
    </div>
</div>
```

### Step 5: Add CSS Styling

1. In the Odoo page editor, find **Customize > CSS** or **Custom CSS**
2. Paste all CSS from the `<style>` block in `index.html`
3. **Key CSS Variables:**
   ```css
   :root {
       --primary-dark: #1a0f15;
       --primary-burgundy: #6b3e4a;
       --accent-pink: #e94b7f;
       --accent-gold: #d4af37;
       --text-light: #e0e0e0;
       --text-gray: #b0b0b0;
       --success-green: #2ecc71;
   }
   ```

### Step 6: Add JavaScript

1. Find **Customize > JavaScript** or **Custom JS**
2. Paste all JavaScript from the `<script>` block
3. This includes:
   - Events data array
   - Stores data array
   - Render functions
   - Gallery functions

### Step 7: Update Image Paths

**CRITICAL**: Update all image paths in the JavaScript

Replace:
```javascript
// OLD
images: ['./images/sports-cards-center.png', './images/cards_left.png', './images/cards_right.png']

// NEW - Use Odoo Media URLs
images: ['/web/image/ir.attachment/12345/sports-cards-center.png', ...]
```

Or use absolute GitHub URLs:
```javascript
images: [
    'https://raw.githubusercontent.com/SachinKumarRua2023/longislandconvenience/main/images/sports-cards-center.png',
    'https://raw.githubusercontent.com/SachinKumarRua2023/longislandconvenience/main/images/cards_left.png',
    'https://raw.githubusercontent.com/SachinKumarRua2023/longislandconvenience/main/images/cards_right.png'
]
```

### Step 8: Save & Publish

1. Click **Save**
2. Click **Publish** to make live
3. Click **View** to see your page

---

## Method 2: Iframe Embed (QUICK)

If you want to keep it as a separate static page:

### Step 1: Create Page

1. Go to **Website > Pages > + New**
2. Name: "Store Showcase"
3. URL: "/showcase"

### Step 2: Add Iframe Code

In the page HTML editor, add:

```html
<iframe 
    src="https://sachinkulmarrua2023.github.io/longislandconvenience/"
    width="100%" 
    height="2000px" 
    frameborder="0"
    style="border: none; margin: 0; padding: 0;">
</iframe>
```

### Advantages:
✅ No code duplication
✅ Auto-updates from GitHub
✅ Easy maintenance
✅ Fast deployment

### Disadvantages:
❌ Separate from Odoo styling
❌ Not fully integrated

---

## Method 3: Odoo Module (ADVANCED)

### Step 1: Create Module Structure

```
longisland_web/
├── __init__.py
├── __manifest__.py
├── views/
│   └── website_templates.xml
├── static/
│   └── src/
│       ├── css/
│       │   └── website.css
│       ├── js/
│       │   └── website.js
│       └── images/
│           ├── BalloonsCenter.png
│           ├── cards_left.png
│           └── ... (all images)
└── controllers/
    └── website.py
```

### Step 2: Create __manifest__.py

```python
{
    'name': 'Long Island Convenience - Web Store',
    'version': '1.0.0',
    'category': 'Website',
    'summary': 'Advanced store showcase with image galleries and coupon calendar',
    'author': 'Long Island Convenience Inc',
    'website': 'https://longislandconvenience.com',
    'depends': ['website', 'website_form'],
    'data': [
        'views/website_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'longisland_web/static/src/css/website.css',
            'longisland_web/static/src/js/website.js',
        ],
    },
    'installable': True,
    'auto_install': False,
}
```

### Step 3: Create website_templates.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <template id="store_showcase" name="Store Showcase">
            <t t-call="website.layout">
                <div class="o_longiland_web">
                    <!-- Your HTML content here -->
                </div>
            </t>
        </template>
    </data>
</odoo>
```

---

## Image Management

### Option A: Odoo Media Library (BEST FOR ODOO)

**Step 1: Upload Images**
1. Go to **Website > Media**
2. Create folder: "Long Island Convenience"
3. Upload all 12 images

**Step 2: Get Image URLs**
1. Click each image
2. Copy the media URL: `/web/image/ir.attachment/12345/image-name.png`

**Step 3: Update JavaScript**
```javascript
const stores = [
    {
        id: 1,
        name: 'Sports Cards',
        images: [
            '/web/image/ir.attachment/123/sports-cards-center.png',
            '/web/image/ir.attachment/124/cards_left.png',
            '/web/image/ir.attachment/125/cards_right.png'
        ]
    },
    // ... more stores
];
```

### Option B: GitHub Raw URLs (EASIEST FOR TESTING)

No need to upload! Use GitHub URLs directly:

```javascript
const stores = [
    {
        id: 1,
        name: 'Sports Cards',
        images: [
            'https://raw.githubusercontent.com/SachinKumarRua2023/longislandconvenience/main/images/sports-cards-center.png',
            'https://raw.githubusercontent.com/SachinKumarRua2023/longislandconvenience/main/images/cards_left.png',
            'https://raw.githubusercontent.com/SachinKumarRua2023/longislandconvenience/main/images/cards_right.png'
        ]
    }
];
```

### Option C: CDN URLs (PRODUCTION)

Upload to Cloudflare or CloudFront:
```javascript
images: [
    'https://cdn.longislandconvenience.com/sports-cards-center.png',
    'https://cdn.longislandconvenience.com/cards_left.png',
    'https://cdn.longislandconvenience.com/cards_right.png'
]
```

---

## Real-Time Offers Integration

### Connect Events to Odoo

Fetch events from Odoo Calendar:

```javascript
// Replace the static events array with Odoo API call
async function loadEventsFromOdoo() {
    const response = await fetch('/api/calendar/event', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    const events = await response.json();
    renderEvents(events);
}

// Call on page load
document.addEventListener('DOMContentLoaded', loadEventsFromOdoo);
```

### Add Odoo Event Controller

In `controllers/website.py`:

```python
from odoo import http, fields
from odoo.http import request

class WebsiteEvents(http.Controller):
    @http.route('/api/calendar/event', auth='public', type='json')
    def get_events(self):
        events = request.env['calendar.event'].search([
            ('start', '>=', fields.Datetime.now()),
            ('start', '<=', fields.Datetime.add(fields.Datetime.now(), days=30))
        ], order='start')
        
        return [{
            'date': event.start.strftime('%b %d'),
            'title': event.name,
            'description': event.description,
            'discount': event.discount or 'Special Offer',
            'category': event.category_id.name if event.category_id else 'event'
        } for event in events]
```

---

## Update Store Information

### Connect to Odoo Products

Update store data from Odoo product categories:

```javascript
async function loadStoresFromOdoo() {
    const response = await fetch('/api/products/category', {
        method: 'GET'
    });
    const stores = await response.json();
    renderStores(stores);
}
```

### Odoo Controller for Products

```python
@http.route('/api/products/category', auth='public', type='json')
def get_categories(self):
    categories = request.env['product.category'].search([
        ('display_on_website', '=', True)
    ])
    
    return [{
        'id': cat.id,
        'name': cat.name,
        'category': cat.description,
        'status': 'LIVE',
        'images': [img.image_1920 for img in cat.product_ids[:3]],
        'url': cat.website_url
    } for cat in categories]
```

---

## Testing & Troubleshooting

### Test Checklist

- [ ] Images load correctly
- [ ] Events calendar displays
- [ ] Store cards show 3 images (left, center, right)
- [ ] Hover effects work
- [ ] All links work
- [ ] Mobile responsive
- [ ] Colors match brand
- [ ] No console errors

### Common Issues & Fixes

#### Images Not Loading
```
Problem: 404 errors for images
Solution: 
1. Check image path format
2. Verify images uploaded to Odoo Media
3. Use absolute URLs instead of relative
```

#### JavaScript Not Running
```
Problem: No events or stores showing
Solution:
1. Check browser console (F12)
2. Verify JavaScript is enabled
3. Check for syntax errors
4. Ensure jQuery loaded (if needed)
```

#### Styling Conflicts
```
Problem: Colors/layout broken
Solution:
1. Add !important to critical CSS
2. Check for Odoo theme overrides
3. Use CSS specificity
4. Clear browser cache
```

#### Mobile Issues
```
Problem: Layout broken on mobile
Solution:
1. Check media queries (max-width: 768px)
2. Verify viewport meta tag
3. Test on actual device
4. Use browser DevTools
```

---

## CSS Customization for Odoo

If Odoo colors conflict, customize:

```css
:root {
    --primary-dark: #1a0f15;           /* Dark background */
    --primary-burgundy: #6b3e4a;       /* Brand burgundy */
    --accent-pink: #e94b7f;            /* Highlight color */
    --accent-gold: #d4af37;            /* Gold accents */
    --text-light: #e0e0e0;             /* Light text */
    --text-gray: #b0b0b0;              /* Gray text */
    --success-green: #2ecc71;          /* Green badges */
}
```

Change these to match your Odoo theme!

---

## Meta Tags for SEO

Ensure these are in your Odoo page head:

```html
<meta name="description" content="Long Island Convenience - Your one-stop gift shop with same-day delivery across Nassau & Suffolk County, NY.">
<meta name="keywords" content="gift shop, sports cards, gift baskets, balloons, same-day delivery, Long Island">
<meta property="og:title" content="Long Island Convenience - Gifts & More">
<meta property="og:description" content="Premium gifts with daily coupons and special events.">
<meta property="og:image" content="/web/image/ir.attachment/123/BalloonsCenter.png">
```

---

## Deployment Checklist

- [ ] Page created in Odoo
- [ ] HTML content pasted
- [ ] CSS added
- [ ] JavaScript added
- [ ] Images uploaded or linked
- [ ] Image paths updated
- [ ] Page tested
- [ ] Mobile tested
- [ ] Links tested
- [ ] Page published
- [ ] Menu updated (if needed)
- [ ] Analytics configured (optional)

---

## Support & Maintenance

### Regular Updates

- **Weekly**: Monitor events calendar
- **Monthly**: Add new events/offers
- **Quarterly**: Update product images
- **Yearly**: Review design and UX

### Backup

```bash
# Backup Odoo database
pg_dump country-cove-inc > backup_$(date +%Y%m%d).sql

# Backup files
tar -czf odoo_backup_$(date +%Y%m%d).tar.gz /path/to/files
```

---

## Next Steps

1. **Choose Integration Method** (Method 1 recommended for quickest setup)
2. **Prepare Content** (Gather all images and event info)
3. **Test Locally** (Review at sachinkulmarrua2023.github.io)
4. **Login to Odoo** (country-cove-inc.odoo.com)
5. **Create Page** (Home or /showcase)
6. **Add Content** (HTML, CSS, JS)
7. **Upload Images** (Odoo Media or use GitHub URLs)
8. **Test & Publish** (Verify everything works)
9. **Update Menu** (Add navigation links if needed)
10. **Monitor & Maintain** (Update content regularly)

---

## Contact & Support

**Technical Support**:
- Email: kahpk1933@gmail.com
- Phone: +1 (917) 338-7086
- Address: 605 Old Country Road, Plainview, NY 11803

**Resources**:
- [Live Website](https://sachinkulmarrua2023.github.io/longislandconvenience/)
- [GitHub Repository](https://github.com/SachinKumarRua2023/longislandconvenience)
- [Odoo Documentation](https://www.odoo.com/documentation/)

---

**Last Updated**: June 9, 2026  
**Version**: 1.0.0  
**Status**: Ready for Odoo Integration ✅
