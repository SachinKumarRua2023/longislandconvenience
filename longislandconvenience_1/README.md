# Long Island Convenience - Advanced Store Display

A professional, responsive website showcasing Long Island Convenience's six store brands with advanced Three.js animations, seasonal countdown timers, and premium UI/UX design.

## Features

### 🎨 Advanced UI/UX
- **Three.js 3D Animations**: Dynamic geometric shapes and smooth transitions
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Modern Glassmorphism**: Contemporary design with semi-transparent panels
- **Smooth Transitions**: CSS animations and transform effects
- **Professional Color Scheme**: Gold and burgundy accents with dark theme

### ⏱️ Seasonal Reminder Timer
- Countdown to upcoming holidays (Christmas 2026)
- Real-time updates with days, hours, minutes, and seconds
- Eye-catching display with gradient backgrounds

### 🏪 Store Showcase
Displays all six Long Island Convenience brands:
1. **Sports Cards** - Rare and vintage sports card collections
2. **Gift Baskets** - Beautifully curated gift baskets for all occasions
3. **Balloons & Décor** - Premium balloon arrangements and event decorations
4. **Print & Mail** - Professional printing and nationwide shipping
5. **Game Cards** - Trading card games (Yu-Gi-Oh, Magic: The Gathering, etc.)
6. **Greeting Cards** - Custom and personalized greeting cards

### ✨ Interactive Elements
- Hover effects on store cards with shadow and transform animations
- Floating balloon background animations
- Dynamic image brightness and scale effects
- Status badges (LIVE/COMING SOON) for each store

### 🔍 SEO Optimization
- Full meta tags for search engines
- Open Graph support for social media sharing
- Semantic HTML structure
- Mobile-friendly viewport configuration

## Folder Structure

```
longislandconvenience_1/
├── index.html              # Main standalone HTML file
├── images/                 # All product and store images
│   ├── BalloonsCenter.png
│   ├── balloon_left.jfif
│   ├── balloon_right.jfif
│   ├── cards_left.png
│   ├── cards_right.png
│   ├── giftbasket_center.jpg
│   ├── giftbasket_left.jpg
│   ├── giftbasket_right.jpg
│   ├── printmail_center.jpeg
│   ├── printmail_left.jpeg
│   ├── printmail_right.jpeg
│   └── sports-cards-center.png
├── README.md               # This file
└── ODOO_INTEGRATION.md     # Odoo integration guide
```

## Usage

### Standalone View
Simply open `index.html` in a web browser. No installation required.

```bash
# Option 1: Direct open
open index.html

# Option 2: Local server
python -m http.server 8000
# Then visit http://localhost:8000
```

### Odoo Integration
For integration with Odoo website:

1. Extract the body content (everything between `<body>` tags)
2. Create an Odoo Website Page with custom HTML
3. Keep Odoo's header/footer intact
4. Include the `<style>` block in Odoo's custom CSS
5. Include the `<script>` block in Odoo's custom JS

See `ODOO_INTEGRATION.md` for detailed instructions.

## Technologies Used

- **Three.js**: 3D graphics library for animations
- **HTML5**: Semantic markup with SEO optimization
- **CSS3**: Advanced styling with gradients, animations, and transforms
- **Vanilla JavaScript**: No dependencies required for core functionality

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Customization

### Colors
Edit CSS variables in the `<style>` section:
```css
:root {
    --primary-dark: #1a0f15;
    --primary-burgundy: #6b3e4a;
    --accent-pink: #e94b7f;
    --accent-gold: #d4af37;
    /* ... more variables ... */
}
```

### Stores Data
Modify the `stores` array in the JavaScript section to update store information:
```javascript
const stores = [
    {
        name: 'Store Name',
        category: 'Category',
        description: 'Description',
        status: 'LIVE', // or 'COMING'
        image: './images/image.png',
        url: 'store-link'
    },
    // ... more stores
];
```

### Timer Target Date
Update the target date in the `initializeTimer()` function:
```javascript
let target = new Date(2026, 11, 25); // Month is 0-indexed
```

## Performance

- **Optimized Images**: Compressed and properly formatted
- **Lazy Loading**: Images load on demand
- **WebGL Rendering**: Hardware-accelerated 3D graphics
- **Minimal Dependencies**: Only Three.js external library
- **Responsive Canvas**: Scales with window resizing

## SEO Features

- Open Graph meta tags for social sharing
- Comprehensive meta descriptions
- Keywords and author information
- Mobile viewport configuration
- Schema-ready structure

## Odoo Compatibility

- **Instance**: https://country-cove-inc.odoo.com
- **Database**: country-cove-inc
- **Module**: Custom HTML Integration
- **Web ID**: 1

## Future Enhancements

- [ ] Add product search functionality
- [ ] Implement shopping cart integration
- [ ] Add customer testimonials section
- [ ] E-mail subscription form
- [ ] Advanced analytics tracking
- [ ] Multi-language support
- [ ] Accessibility improvements (WCAG 2.1)

## Support

For issues or questions, contact:
- **Email**: sachin@longislandconvenience.com
- **Phone**: +1 (917) 338-7086
- **Address**: 605 Old Country Road, Plainview, NY 11803

## License

This project is proprietary to Long Island Convenience Inc. All rights reserved.

---

**Last Updated**: June 9, 2026
**Version**: 1.0.0
