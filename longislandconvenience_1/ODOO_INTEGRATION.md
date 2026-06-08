# Odoo Integration Guide

This document provides step-by-step instructions for integrating the advanced Long Island Convenience store display into your Odoo website.

## Odoo Instance Details

- **URL**: https://country-cove-inc.odoo.com
- **Database**: country-cove-inc
- **User Email**: countrycoveinc@gmail.com
- **Web ID**: 1

## Integration Methods

### Method 1: Custom HTML Page (Recommended)

#### Step 1: Access Odoo Website Editor
1. Log in to https://country-cove-inc.odoo.com
2. Go to **Website** > **Pages**
3. Create a new page or edit existing homepage

#### Step 2: Add Body Content
1. Click **Edit** on the page
2. Go to **Customize > HTML Editor**
3. Locate the `<body>` section
4. Copy the entire content from `index.html` between `<body>` and `</body>` tags
5. Paste it into your Odoo page

#### Step 3: Add Styling
1. In the HTML editor, find the `<style>` block in `index.html`
2. Copy all CSS content
3. In Odoo, go to **Customize > CSS**
4. Paste the CSS styling

#### Step 4: Add JavaScript
1. Copy the JavaScript code from the `<script>` tag in `index.html`
2. In Odoo, go to **Customize > JavaScript**
3. Paste the code

#### Step 5: Configure Image Paths
Update all image paths in the `stores` array:
- Replace `./images/` with `/website/image/`
- Or use absolute URLs: `https://country-cove-inc.odoo.com/images/`

### Method 2: Odoo Module (Advanced)

If you prefer a more integrated approach, create an Odoo module:

#### File Structure
```
website_longisland_stores/
├── __init__.py
├── __manifest__.py
├── views/
│   └── website_templates.xml
└── static/
    ├── src/
    │   ├── css/
    │   │   └── stores.css
    │   ├── js/
    │   │   └── stores.js
    │   └── img/
    │       └── [all images]
    └── description/
        └── icon.png
```

#### __manifest__.py
```python
{
    'name': 'Long Island Convenience - Store Display',
    'version': '1.0.0',
    'category': 'Website',
    'summary': 'Advanced store showcase with 3D animations',
    'author': 'Long Island Convenience Inc',
    'website': 'https://longislandconvenience.com',
    'depends': ['website'],
    'data': [
        'views/website_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
```

#### views/website_templates.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <template id="stores_showcase" name="Store Showcase">
            <t t-call="website.layout">
                <div class="container-fluid stores-section">
                    <!-- Your HTML content here -->
                </div>
            </t>
        </template>
    </data>
</odoo>
```

### Method 3: Iframe Embed

If you want to keep the files separate:

```html
<iframe 
    src="https://your-domain.com/longislandconvenience_1/index.html"
    width="100%"
    height="auto"
    frameborder="0"
    allow="fullscreen">
</iframe>
```

## Image Management in Odoo

### Option A: Use Odoo Media Library
1. Go to **Website > Media**
2. Upload all images from `images/` folder
3. Get the image URLs from media library
4. Update image paths in the stores array

### Option B: Self-Hosted Images
1. Keep images in your web directory
2. Reference with full URLs: `https://country-cove-inc.odoo.com/images/sports-cards-center.png`

### Option C: CDN Integration
1. Upload images to a CDN (CloudFront, Cloudflare, etc.)
2. Update image paths to CDN URLs

## Meta Tags Configuration

### In Odoo Website Settings:
1. Go to **Website > Settings**
2. Under **SEO**, set:
   - **Title**: "Long Island Convenience - Premium Gifts & Products"
   - **Description**: "Your one-stop gift shop for sports cards, gift baskets, balloons, and more with same-day delivery across Nassau & Suffolk County, NY."
   - **Keywords**: "gift shop, sports cards, gift baskets, balloons, Long Island"

### Open Graph Tags (for social sharing):
These are already included in the HTML file's head section.

## API Integration

### Odoo Product Integration
To fetch products directly from Odoo:

```javascript
// Add to the stores data initialization
fetch('/api/products/sale.product.template', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer YOUR_TOKEN'
    }
})
.then(response => response.json())
.then(data => {
    // Process and populate stores
});
```

### Odoo Event/Holiday Integration
Fetch upcoming events for the timer:

```python
# In your Odoo module
@http.route('/api/upcoming-events', auth='public', type='json')
def get_upcoming_events(self):
    events = request.env['calendar.event'].search([
        ('start', '>', fields.Datetime.now())
    ], limit=1)
    return {'target_date': events[0].start if events else False}
```

## Performance Optimization

### Image Optimization
```bash
# Use ImageMagick to optimize images
convert input.png -quality 80 -resize 800x600 output.png

# Or use online tools
# - TinyPNG
# - Compressor.io
```

### Caching
In Odoo, enable caching:
1. **Settings > Technical > System Parameters**
2. Add: `web.base.url.freeze` = `True`

### CDN Configuration
1. Go to **Settings > Website > CDN**
2. Enable CDN for static content

## Customization Examples

### Change Color Scheme
Update CSS variables in the `<style>` block:

```css
:root {
    --primary-dark: #1a0f15;        /* Change to your dark color */
    --primary-burgundy: #6b3e4a;    /* Change to your brand color */
    --accent-pink: #e94b7f;         /* Change accent color */
    --accent-gold: #d4af37;         /* Change highlight color */
}
```

### Add More Stores
Update the `stores` array:

```javascript
{
    name: 'New Store',
    category: 'Category Name',
    description: 'Store description here',
    status: 'LIVE', // or 'COMING'
    image: './images/new-store.png',
    url: 'link-to-store'
}
```

### Change Timer Target Date
Update in `initializeTimer()`:

```javascript
let target = new Date(2026, 11, 25); // Year, Month (0-11), Day
```

### Adjust Animation Speed
Modify the Three.js animation loop:

```javascript
// Slower rotation
mesh.rotation.x += 0.0005; // Was 0.001
mesh.rotation.y += 0.001;  // Was 0.002
```

## Troubleshooting

### Images Not Loading
- Check image paths are correct
- Verify image file names match exactly (case-sensitive)
- Ensure CORS is enabled if using external URLs
- Check browser console for 404 errors

### Three.js Not Loading
- Verify CDN link is accessible: `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`
- Check browser version (requires ES6 support)
- Ensure JavaScript is enabled

### Styling Issues
- Check for CSS conflicts with Odoo theme
- Add `!important` if styles are being overridden
- Verify all color variables are defined
- Check for missing closing tags

### Performance Issues
- Reduce number of floating balloons (change loop count)
- Lower Three.js shader quality
- Enable browser caching
- Use image compression

## Odoo Automation

### n8n Workflow Integration
Connect this page with your n8n automation:

1. **Trigger**: New product added in Odoo
2. **Action**: Update stores array automatically
3. **Webhook**: POST to update store information

Example n8n node configuration:
```json
{
    "resource": "odoo",
    "operation": "read",
    "module": "sale.product.template",
    "filters": {
        "category_id": ["=", "Stores"],
        "active": ["=", true]
    }
}
```

### Auto-Update Store Information
Create a cron job to sync:

```python
@api.model
def update_store_display(self):
    # Fetch products
    products = self.env['sale.product.template'].search([
        ('category_id.name', '=', 'Stores')
    ])
    # Update JSON file or database
    # Trigger page refresh
```

## Monitoring & Analytics

### Track Page Views
Add Google Analytics:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

### Monitor Performance
1. Use Chrome DevTools Performance tab
2. Check Web Vitals:
   - Largest Contentful Paint (LCP)
   - First Input Delay (FID)
   - Cumulative Layout Shift (CLS)

## Security Considerations

### Content Security Policy
Add to Odoo:
```html
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' cdnjs.cloudflare.com;
    style-src 'self' 'unsafe-inline';
    img-src 'self' data:;
">
```

### Image Validation
Verify all images before upload:
- Max file size: 5MB
- Allowed formats: PNG, JPG, GIF
- Scan for malware

### Data Protection
Ensure compliance:
- [ ] GDPR compliance
- [ ] SSL/TLS encryption
- [ ] Regular backups
- [ ] Access controls

## Support & Maintenance

### Regular Updates
- Update Three.js library monthly
- Review browser compatibility
- Test on mobile devices
- Monitor performance metrics

### Backup
```bash
# Backup Odoo configuration
pg_dump country-cove-inc > backup.sql

# Backup files
tar -czf longisland_backup.tar.gz longislandconvenience_1/
```

## Additional Resources

- [Odoo Website Module Documentation](https://www.odoo.com/documentation/16.0/applications/websites/website/website.html)
- [Three.js Documentation](https://threejs.org/docs/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [Web Performance Guide](https://web.dev/)

---

**Contact for Support**:
- Email: countrycoveinc@gmail.com
- Phone: +1 (917) 338-7086
- Address: 605 Old Country Road, Plainview, NY 11803

**Last Updated**: June 9, 2026
**Version**: 1.0.0
