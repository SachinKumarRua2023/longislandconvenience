# Odoo Iframe Embed Code - GitHub Page Integration

## 🔗 Direct Copy-Paste Odoo Code

### **Option 1: Simple Iframe (Height Fixed)**

```html
<!-- Long Island Convenience Store Showcase -->
<div class="long-island-showcase">
    <iframe 
        src="https://sachinkulmarrua2023.github.io/longislandconvenience/"
        width="100%" 
        height="2800px" 
        frameborder="0"
        style="border: none; margin: 0; padding: 0; display: block;">
    </iframe>
</div>
```

**Use this when:** You want fixed height, simple embed

---

### **Option 2: Responsive Iframe (Recommended) ⭐**

```html
<!-- Long Island Convenience - Responsive Iframe -->
<div class="li-showcase-wrapper" style="position: relative; width: 100%; padding-bottom: 150%; overflow: hidden;">
    <iframe 
        src="https://sachinkulmarrua2023.github.io/longislandconvenience/"
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; margin: 0; padding: 0;"
        frameborder="0"
        allow="fullscreen">
    </iframe>
</div>

<style>
    @media (max-width: 768px) {
        .li-showcase-wrapper {
            padding-bottom: 200%;
        }
    }
</style>
```

**Use this when:** You want responsive, mobile-friendly embed

---

### **Option 3: Full Page Height (Auto-Adjust)**

```html
<!-- Long Island Convenience - Auto Height -->
<iframe 
    id="li-showcase-iframe"
    src="https://sachinkulmarrua2023.github.io/longislandconvenience/"
    width="100%" 
    height="800px"
    frameborder="0"
    style="border: none; margin: 0; padding: 0; display: block; min-height: 100vh;">
</iframe>

<script>
    // Auto-adjust iframe height
    document.getElementById('li-showcase-iframe').onload = function() {
        try {
            var iframeDoc = this.contentDocument || this.contentWindow.document;
            this.height = iframeDoc.documentElement.scrollHeight + 'px';
        } catch(e) {
            console.log('Iframe cross-origin - using fixed height');
            this.height = '2800px';
        }
    };
    
    // Fallback height if auto-adjust fails
    setTimeout(function() {
        document.getElementById('li-showcase-iframe').height = '2800px';
    }, 3000);
</script>
```

**Use this when:** You want auto-adjusting height

---

## 📍 How to Use in Odoo

### Step 1: Create New Page in Odoo
1. Go to **Website > Pages**
2. Click **+ New**
3. Set:
   - **Page Title**: "Store Showcase" or "Home"
   - **URL**: "/showcase" or "/"

### Step 2: Edit Page

1. Click **Edit**
2. Find **HTML Editor** or **<> Code**
3. Click **</> Code View** or **HTML Editor**

### Step 3: Paste Iframe Code

**Clear all existing content**, then paste ONE of the iframe codes above.

### Step 4: Save & Publish

1. Click **Save**
2. Click **Publish**
3. Click **View** to see live

---

## 🔗 Redirect Functionality

The website already has **built-in redirect links** for each store:

### Store Links Configuration

Each store card has a "Visit Store" button that redirects to:

```javascript
const stores = [
    {
        id: 1,
        name: 'Sports Cards',
        url: 'https://longislandcards.com'  // ← Click redirects here
    },
    {
        id: 2,
        name: 'Gift Baskets',
        url: 'https://ligiftbasket.com'  // ← Click redirects here
    },
    {
        id: 3,
        name: 'Balloons & Décor',
        url: 'https://longislandbaloonsdecor.com'  // ← Click redirects here
    },
    {
        id: 4,
        name: 'Print & Mail',
        url: 'https://longislandprintandmail.com'  // ← Click redirects here
    },
    {
        id: 5,
        name: 'Game Cards',
        url: '#'  // Update with actual URL
    },
    {
        id: 6,
        name: 'Greeting Cards',
        url: '#'  // Update with actual URL
    }
];
```

### ✅ How It Works

1. User sees store card in iframe
2. User clicks **"Visit Store →"** button
3. Browser redirects to store website
4. **Works across cross-origin!** (iframe to external website)

---

## 🎯 Update Store URLs

To change where users are directed, update the URLs in the GitHub file:

### Step 1: Edit index.html on GitHub

1. Go to: https://github.com/SachinKumarRua2023/longislandconvenience
2. Click `index.html`
3. Click Edit (pencil icon)
4. Find the `stores` array in the JavaScript section

### Step 2: Update URLs

```javascript
{
    id: 5,
    name: 'Game Cards',
    url: 'https://yourgamecards.com'  // ← Change this
},
{
    id: 6,
    name: 'Greeting Cards',
    url: 'https://yourgreetingcards.com'  // ← Change this
}
```

### Step 3: Commit Changes

1. Scroll down
2. Enter commit message: "Update store URLs"
3. Click **Commit changes**
4. Changes live automatically!

---

## 📱 Mobile Optimization

### For Mobile-Friendly Iframe

Use **Option 2 (Responsive)** for best mobile experience:

```html
<div class="li-showcase-wrapper" style="position: relative; width: 100%; padding-bottom: 150%; overflow: hidden;">
    <iframe 
        src="https://sachinkulmarrua2023.github.io/longislandconvenience/"
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
        frameborder="0"
        allow="fullscreen">
    </iframe>
</div>
```

---

## 🎨 Customize Iframe Style in Odoo

Add custom CSS in Odoo to style the iframe:

```css
/* Odoo Custom CSS */
iframe {
    border: 1px solid #ddd;
    border-radius: 10px;
    margin: 20px 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.long-island-showcase {
    background: #f5f5f5;
    padding: 20px;
    margin: 20px 0;
    border-radius: 15px;
}

/* On desktop */
@media (min-width: 768px) {
    iframe {
        height: 2800px;
    }
}

/* On mobile */
@media (max-width: 768px) {
    iframe {
        height: 3500px;
    }
}
```

---

## ✅ Testing Checklist

After embedding in Odoo:

- [ ] Page loads without errors
- [ ] All 6 store cards visible
- [ ] Event/coupon section shows
- [ ] Images display correctly
- [ ] Hover effects work
- [ ] Clicking "Visit Store →" redirects to correct website
- [ ] Mobile layout looks good
- [ ] No console errors (F12)
- [ ] Links open in new tab (or same window)

---

## 🔍 Troubleshooting

### **Iframe Not Loading**

**Problem**: Blank iframe or error message

**Solutions**:
1. Check internet connection
2. Verify GitHub page is live: https://sachinkulmarrua2023.github.io/longislandconvenience/
3. Clear browser cache
4. Try different browser
5. Check Odoo console (F12)

### **Links Not Working**

**Problem**: Clicking "Visit Store" doesn't redirect

**Solutions**:
1. Check if URLs are correct in `index.html`
2. Verify URLs start with `https://`
3. Try opening URL directly in browser
4. Check firewall/security settings

### **Layout Broken**

**Problem**: Images/text misaligned

**Solutions**:
1. Try **Option 2 (Responsive)** code
2. Adjust padding-bottom percentage (150%, 200%)
3. Add custom CSS in Odoo
4. Test on mobile device directly

### **Height Issues**

**Problem**: Content cut off or too much white space

**Solutions**:
1. Increase height: `height="3500px"`
2. Try auto-height option (Option 3)
3. Use responsive wrapper (Option 2)

---

## 🔄 Keep It Updated

### Auto-Updates from GitHub

The iframe automatically pulls latest changes from GitHub!

**To update website:**
1. Edit `index.html` on GitHub
2. Commit changes
3. **Wait 30 seconds** for GitHub Pages to rebuild
4. Refresh Odoo page
5. See updates live!

No need to re-embed or change Odoo code!

---

## 📝 Complete Odoo Page Code

Here's a complete page template for Odoo:

```html
<section class="section">
    <div class="container">
        <h1 style="text-align: center; color: #d4af37; margin-bottom: 30px;">
            ✨ Long Island Convenience - Premium Gifts & Services
        </h1>
        
        <!-- Iframe Embed -->
        <div class="li-showcase-wrapper" style="position: relative; width: 100%; padding-bottom: 150%; overflow: hidden; margin: 20px 0; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <iframe 
                src="https://sachinkulmarrua2023.github.io/longislandconvenience/"
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 15px;"
                frameborder="0"
                allow="fullscreen">
            </iframe>
        </div>

        <!-- Contact Info Below -->
        <div style="text-align: center; margin-top: 40px; padding: 20px; background: #f5f5f5; border-radius: 10px;">
            <h3>📞 Contact Us</h3>
            <p>
                <strong>Phone:</strong> +1 (917) 338-7086<br>
                <strong>Email:</strong> countrycoveinc@gmail.com<br>
                <strong>Address:</strong> 605 Old Country Road, Plainview, NY 11803
            </p>
        </div>
    </div>
</section>

<style>
    @media (max-width: 768px) {
        .li-showcase-wrapper {
            padding-bottom: 200%;
        }
    }
</style>
```

---

## 🚀 Final Steps

1. **Copy the iframe code** (choose Option 1, 2, or 3)
2. **Login to Odoo** (country-cove-inc.odoo.com)
3. **Create new page** (Website > Pages > + New)
4. **Paste code** into HTML editor
5. **Save & Publish**
6. **View page** to verify
7. **Test all links** (make sure redirects work)
8. **Share with team!** 🎉

---

## 📞 Support

If iframe not working:
- Email: kahpk1933@gmail.com
- Phone: +1 (917) 338-7086
- Check: https://sachinkulmarrua2023.github.io/longislandconvenience/ (direct access)

---

**Ready to embed?** Choose Option 2 (Responsive) - it's the best! ⭐
