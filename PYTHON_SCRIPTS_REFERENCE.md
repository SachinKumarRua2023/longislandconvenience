# Python Scripts Reference Guide

Complete explanation of all Python scripts created for the Long Island Cards homepage redesign.

---

## Overview

We created several Python scripts to automate:
1. **Image cleanup** - Remove duplicates, organize by category
2. **Base64 conversion** - Convert images to base64 for embedding
3. **HTML generation** - Create homepage with proper CSS and structure
4. **Hero section updates** - Add Pokemon card overlays
5. **Category matching** - Match images to product categories

---

## Script 1: complete_image_cleanup.py

### Purpose
Delete all old/duplicate base64 files and create clean, organized files from scratch.

### What It Does

```
STEP 1: Delete all existing base64 files
   - Removes all *_base64.txt files
   - Cleans up old/duplicate files
   - Starts fresh

STEP 2: Define image organization by category
   - Sports: 3 position files (left/center/right)
   - Pokemon: 3 unique position files
   - MTG: 3 position files
   - Yu-Gi-Oh: 3 position files
   - Graded: 3 position files
   - Products: 4 unique product images
   - Hero: 3 special Pokemon card overlays
   - Bundle: 1 special collection image

STEP 3: Convert each image to base64
   - Reads PNG file from assets folder
   - Encodes to base64 text
   - Saves as *_base64.txt file

STEP 4: Verify no duplicates
   - Counts total base64 files created
   - Confirms all images are unique
```

### Input (From Assets Folder)
```
assets/
├── SportCardsReady2Use.png
├── PokemonAncientSolRing.png
├── pokemon-cards-center.png
├── PokemonDragon.png
├── BundleOfMg.png
├── mtg-cards-center.png
├── mtg-cards-right.png
├── yugioh-cards-right.png
├── graded-cards-left.png
├── product-exclusive-collection.png
├── product-graded-slabbed.png
├── product-rare-editions.png
├── bulk-dragon-collection.png
└── (and more...)
```

### Output
```
base_directory/
├── sports-cards-left_base64.txt        (50KB)
├── sports-cards-center_base64.txt      (50KB)
├── sports-cards-right_base64.txt       (50KB)
├── pokemon-cards-left_base64.txt       (60KB)
├── pokemon-cards-center_base64.txt     (60KB)
├── pokemon-cards-right_base64.txt      (60KB)
├── (... and more for each category)
└── (Total: 16 files)
```

### Key Code Section
```python
# Convert image to base64
with open(image_path, 'rb') as f:
    b64_data = base64.b64encode(f.read()).decode('utf-8')

# Save base64 to text file
with open(output_file, 'w') as f:
    f.write(b64_data)
```

### Why This Script?
- **Avoids duplicates**: Each image has 1 base64 file
- **Organized**: Files named by category and position
- **Clean restart**: Deletes old files before creating new ones
- **Verification**: Confirms no duplicates were created

---

## Script 2: update_homepage_complete.py

### Purpose
Load all base64 files and generate complete homepage HTML with animations.

### What It Does

```
STEP 1: Load all base64 files
   - Reads 16 base64 text files
   - Stores in memory as dictionary

STEP 2: Create CSS animations
   - Fire glow animation (2.5s cycle)
   - Floating animation (4s up/down)
   - Brightness pulsing
   - Border circulate effect

STEP 3: Build HTML structure
   - Hero section with "Trading Card Paradise" title
   - Category cards grid (Sports, Pokemon, MTG, Yu-Gi-Oh, Graded)
   - Product showcase cards
   - Bundle showcase at bottom

STEP 4: Embed base64 images
   - For each category image:
     <img src="data:image/png;base64,{BASE64_DATA_HERE}">
   - Images embedded directly in HTML

STEP 5: Add animations to elements
   - Apply fire-glow to bundle images
   - Apply floating effect to cards
   - Apply hover effects to category cards

STEP 6: Save complete HTML
   - Writes all HTML + CSS + embedded images to file
   - Final size: ~39 MB (large because of embedded images)
```

### CSS Animations Included

#### Fire-Glow Animation
```css
@keyframes fire-glow {
    0% { box-shadow: 0 0 80px rgba(255, 69, 0, 0.8); }
    50% { box-shadow: 0 0 120px rgba(255, 20, 0, 1); }
    100% { box-shadow: 0 0 80px rgba(255, 69, 0, 0.8); }
}
```

#### Floating Animation
```css
@keyframes floating-enhanced {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}
```

#### Brightness Pulsing
```css
@keyframes brightness-pulse {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.2); }
}
```

### HTML Structure Created

```html
<header> ... Navigation ... </header>

<section class="hero">
    <h1>Trading Card Paradise</h1>
    <p>Explore premium collectibles...</p>
</section>

<section class="categories">
    <div class="category-card">
        <img src="data:image/png;base64,{SPORTS_IMAGE}" alt="Sports">
        <h3>Sports Cards</h3>
    </div>
    <div class="category-card">
        <img src="data:image/png;base64,{POKEMON_IMAGE}" alt="Pokemon">
        <h3>Pokemon Cards</h3>
    </div>
    <!-- ... more categories ... -->
</section>

<section class="products">
    <!-- Product cards with images -->
</section>

<section class="bundle-showcase" style="animation: fire-glow 2.5s infinite;">
    <img src="data:image/png;base64,{BUNDLE_IMAGE}" style="animation: floating-enhanced 4s infinite;">
</section>
```

### Output
- **File**: `homepage_base64.html`
- **Size**: 39.77 MB
- **Contains**: All HTML, CSS, and images
- **Problem**: Too large for Odoo's Embed Code field (10-15 MB limit)

### Why This Script?
- **Complete automation**: Generates entire homepage at once
- **Consistency**: All animations applied uniformly
- **Testable**: HTML can be opened in browser immediately
- **Problem solves**: Shows the size limitation issue clearly

---

## Script 3: fix_hero_pokemon_overlay.py

### Purpose
Update hero section to overlay Pokemon cards on top (3D perspective effect).

### What It Does

```
STEP 1: Read current HTML
   - Load homepage_base64.html
   - Find hero section

STEP 2: Load Pokemon card images
   - Read 3 Pokemon base64 files:
     - PokemonAncientSolRing
     - PokemonDeoxys
     - PokemonDragon

STEP 3: Create hero with overlay
   - Hero section has title + description
   - OVERLAID on top: 3 Pokemon cards
   - Cards positioned absolutely on right side
   - Cards have 3D perspective transform

STEP 4: Apply 3D transforms
   - Left card: rotateY(-15deg) - perspective tilt
   - Center card: scale(1.1) - emphasized/highlighted
   - Right card: rotateY(15deg) - perspective tilt
   - All cards: white background, shadow, rounded corners

STEP 5: Clean up duplicates
   - Remove any duplicate Pokemon gallery
   - Keep only the hero overlay version
```

### HTML Created

```html
<section class="hero" style="position: relative; overflow: visible;">
    <!-- Hero Content (Title, Description, Button) -->
    <div class="hero-content">
        <h1>Trading Card Paradise</h1>
        <p>Explore premium collectibles from your favorite brands</p>
        <a href="/shop" class="hero-btn">Shop Now</a>
    </div>

    <!-- Pokemon Cards OVERLAID on Hero -->
    <div class="pokemon-cards-overlay" style="
        position: absolute;
        right: 60px;
        top: 50%;
        transform: translateY(-50%);
        display: flex;
        gap: 20px;
        z-index: 10;">

        <!-- Card 1: Left (tilted left) -->
        <div style="transform: perspective(1000px) rotateY(-15deg);">
            <img src="data:image/png;base64,{ANCIENT_SOLRING_BASE64}">
        </div>

        <!-- Card 2: Center (highlighted) -->
        <div style="transform: scale(1.1); box-shadow: 0 12px 32px rgba(0,0,0,0.4);">
            <img src="data:image/png;base64,{DEOXYS_BASE64}">
        </div>

        <!-- Card 3: Right (tilted right) -->
        <div style="transform: perspective(1000px) rotateY(15deg);">
            <img src="data:image/png;base64,{DRAGON_BASE64}">
        </div>
    </div>
</section>
```

### CSS Transforms Explained

```css
/* Perspective - creates 3D depth */
perspective: 1000px;

/* Rotate around Y axis (tilt left/right) */
rotateY(-15deg);  /* Tilt towards camera on left */
rotateY(15deg);   /* Tilt away from camera on right */

/* Scale - make bigger/smaller */
scale(1.1);  /* 10% larger */

/* Shadow - depth effect */
box-shadow: 0 12px 32px rgba(0,0,0,0.4);
```

### Visual Result

```
BEFORE: Hero just has text
┌─────────────────────────────────┐
│     Trading Card Paradise       │
│  Explore premium collectibles   │
│          [Shop Now]             │
└─────────────────────────────────┘

AFTER: Hero has Pokemon cards overlaid
┌─────────────────────────────────────────────────────────┐
│     Trading Card Paradise    /[Card]\[Card]\[Card]      │
│  Explore premium collectibles     3D Effect Floating    │
│          [Shop Now]                                      │
└─────────────────────────────────────────────────────────┘
```

### Why This Script?
- **Visual impact**: Cards float over hero section
- **3D effect**: Professional-looking depth with perspective
- **Professional**: Matches modern trading card site designs
- **Responsive**: Overlay scales with screen size

---

## Script 4: update_hero_and_categories.py

### Purpose
Match category images to their product type (Pokemon category shows Pokemon cards, etc.).

### What It Does

```
STEP 1: Load Pokemon card base64 files
   - Read 4 Pokemon image files
   - Store in memory

STEP 2: Update Hero Section
   - Add Pokemon cards showcase
   - Display 3 Pokemon cards side-by-side
   - Right-aligned in hero

STEP 3: Update Category Images
   - Sports category → use sports-cards-* images
   - Pokemon category → use pokemon-cards-* images
   - MTG category → use mtg-cards-* images
   - Yu-Gi-Oh category → use yugioh-cards-* images
   - Graded category → use graded-cards-* images

STEP 4: Image mapping
   For each category:
   - Left image: category-name-cards-left.png
   - Center image: category-name-cards-center.png
   - Right image: category-name-cards-right.png
```

### Category Updates

```
BEFORE: All categories used same generic card image

AFTER:
├── Sports Category
│   ├── Left: sports-cards-left.png
│   ├── Center: sports-cards-center.png
│   └── Right: sports-cards-right.png
│
├── Pokemon Category
│   ├── Left: pokemon-cards-left.png (PokemonAncientSolRing)
│   ├── Center: pokemon-cards-center.png (pokemon-cards-center)
│   └── Right: pokemon-cards-right.png (PokemonDragon)
│
├── MTG Category
│   ├── Left: mtg-cards-left.png (BundleOfMg)
│   ├── Center: mtg-cards-center.png (mtg-cards-center)
│   └── Right: mtg-cards-right.png (mtg-cards-right)
│
└── (etc for other categories)
```

### Why This Script?
- **Visual consistency**: Each category shows relevant images
- **Better UX**: Users see what they're looking for
- **Professional**: Organized, themed sections
- **Engagement**: Matching images increase click-through

---

## Script 5: reorganize_homepage_structure.py

### Purpose
Move Pokemon gallery to TOP and keep bundle showcase at BOTTOM.

### What It Does

```
STEP 1: Extract sections
   - Find Pokemon cards gallery section
   - Find bundle showcase section

STEP 2: Reorder structure
   - Remove both from current location
   - Insert Pokemon gallery at TOP (after header)
   - Insert bundle showcase at BOTTOM (before footer)

STEP 3: New order
   1. Header & Navigation
   2. POKEMON CARDS GALLERY (TOP) ← Moved here
   3. Hero Section
   4. Features
   5. Categories
   6. Products
   7. BUNDLE SHOWCASE (BOTTOM) ← Stays here
   8. Footer
```

### Why This Script?
- **Content flow**: Important Pokemon section visible first
- **Balancing**: Bundle showcase at bottom for call-to-action
- **Engagement**: User sees premium products as they scroll
- **Storytelling**: Top = showcase, Bottom = sale/bundle push

---

## Script 6: replace_product_images.py

### Purpose
Replace generic product card images with actual card images.

### What It Does

```
STEP 1: Find product cards in HTML
   - Premium Trading Card Boxes
   - Graded & Slabbed Cards
   - Rare & Limited Editions

STEP 2: Load product images from base64 files
   - product-premium-boxes_base64.txt
   - product-graded-slabbed_base64.txt
   - product-rare-editions_base64.txt

STEP 3: Replace URLs with base64 images
   - From: <img src="https://pexels.com/...">
   - To: <img src="data:image/png;base64,{BASE64_DATA}">

STEP 4: Verify replacements
   - Count total replacements made
   - Confirm all products have images
```

### HTML Before & After

```html
<!-- BEFORE -->
<div class="product-card">
    <img src="https://pexels.com/photos/123456">
    <h3>Premium Boxes</h3>
</div>

<!-- AFTER -->
<div class="product-card">
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA...">
    <h3>Premium Boxes</h3>
</div>
```

### Why This Script?
- **Consistency**: All images from same source (your assets)
- **No external dependencies**: Doesn't rely on Pexels
- **Control**: Complete control over product images
- **Brand**: Shows your actual cards, not generic images

---

## Script 7: enhance_bundle_showcase.py

### Purpose
Add fire animations and styling to bundle showcase section.

### What It Does

```
STEP 1: Find bundle showcase section
   - Locate the bundle/special collection area

STEP 2: Add fire-themed CSS
   - Fire-colored border: #ff4500 (orange-red)
   - Fire glow animation: 2.5s cycle
   - Color transitions: orange → red → orange

STEP 3: Style bundle images
   - Size: 400px width, auto height
   - Border: 6px solid fire-orange
   - Shadow: 0 0 80px rgba(255, 69, 0, 0.8)
   - Animation: fire-glow 2.5s infinite

STEP 4: Add floating animation
   - Bundle image floats up/down
   - Duration: 4s smooth cycle
   - Timing: ease-in-out (smooth acceleration)

STEP 5: Create fire effect
   - Gradient background
   - Fire colors (orange, red, yellow)
   - Glowing shadows
   - Pulsing brightness
```

### CSS Created

```css
/* Fire Border */
border: 4px solid #ff4500;
box-shadow: 0 0 80px rgba(255, 69, 0, 0.4);

/* Fire Glow Animation */
@keyframes fire-border-circulate {
    0% { 
        border-color: #ff8c00;
        box-shadow: 0 0 80px rgba(255, 140, 0, 0.8);
    }
    50% { 
        border-color: #ff0000;
        box-shadow: 0 0 120px rgba(255, 0, 0, 1);
    }
    100% { 
        border-color: #ff8c00;
        box-shadow: 0 0 80px rgba(255, 140, 0, 0.8);
    }
}

/* Floating Animation */
@keyframes floating-enhanced {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Apply to bundle image */
.bundle-image {
    animation: fire-border-circulate 2.5s ease-in-out infinite,
              floating-enhanced 4s ease-in-out infinite;
}
```

### Visual Effect

```
BEFORE: Static bundle image
┌──────────────────┐
│   [Bundle Img]   │
└──────────────────┘

AFTER: Animated with fire glow + floating
        ↑ [Bundle Img] ↑    (floating)
    (fire glow pulsing)
    Orange → Red → Orange cycle
    (2.5s animation loop)
```

### Why This Script?
- **Draws attention**: Fire animation catches the eye
- **Premium feel**: Professional animation style
- **Promotes bundles**: Call-to-action via visual effect
- **Brand personality**: Fire theme matches trading cards energy

---

## How All Scripts Work Together

### Execution Order

```
1. complete_image_cleanup.py
   ↓
   Creates: 16 clean base64 files (no duplicates)

2. update_homepage_complete.py
   ↓
   Creates: homepage_base64.html (39 MB with all images)

3. fix_hero_pokemon_overlay.py
   ↓
   Updates: Hero section with Pokemon 3D cards overlay

4. update_hero_and_categories.py
   ↓
   Updates: Categories to show matching images

5. reorganize_homepage_structure.py
   ↓
   Reorders: Pokemon gallery TOP, bundle showcase BOTTOM

6. replace_product_images.py
   ↓
   Updates: Product cards with actual images

7. enhance_bundle_showcase.py
   ↓
   Finalizes: Fire animations on bundle showcase
```

### Data Flow

```
PNG Images (Assets Folder)
    ↓ (cleanup_image_cleanup.py)
16 Base64 Text Files
    ↓ (all other scripts)
homepage_base64.html (39 MB)
    ↓ (Problem: Too large for Odoo)
GitHub Pages Solution
    ↓
Smaller HTML + GitHub-hosted images
    ↓ (Odoo Embed)
Live Website
```

---

## Key Concepts Explained

### Base64 Encoding
- **What**: Converts binary image data to text
- **Why**: Can embed images directly in HTML without image files
- **Trade-off**: Images become 33% larger as text, but more portable

### Absolute Positioning
```css
position: absolute;
right: 60px;    /* Distance from right edge */
top: 50%;       /* Distance from top */
transform: translateY(-50%);  /* Center vertically */
z-index: 10;    /* Layer on top of other elements */
```

### CSS Animations
- **`@keyframes`**: Define animation frames (0%, 50%, 100%)
- **`animation`**: Apply animation to element
- **`animation-duration`**: How long (e.g., 2.5s)
- **`animation-iteration-count: infinite`**: Repeat forever

### 3D Transforms
```css
perspective(1000px)  /* Creates 3D space */
rotateY(-15deg)      /* Rotate around vertical axis */
scale(1.1)           /* Make 10% larger */
```

---

## File Size Analysis

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| cleanup | Organize images | 16 PNGs | 16 base64 files |
| complete | Generate HTML | 16 base64 | 39 MB HTML |
| fix_hero | Update hero | 39 MB HTML | 39 MB HTML (updated) |
| update_categories | Match categories | 39 MB HTML | 39 MB HTML (updated) |
| reorganize | Reorder sections | 39 MB HTML | 39 MB HTML (updated) |
| replace_products | Product images | 39 MB HTML | 39 MB HTML (updated) |
| enhance_bundle | Fire animations | 39 MB HTML | 39 MB HTML (final) |

**Final Output**: `homepage_base64.html` (39.77 MB)

---

## Why GitHub Pages Instead?

**Problem with base64 embedding:**
- Odoo Embed Code field: ~10-15 MB limit
- Our file: 39.77 MB
- Result: "Request too large" error

**Solution with GitHub Pages:**
- HTML: ~500 KB (no embedded images)
- Images: Hosted on GitHub (free)
- Odoo file: Embed via iframe
- Result: Fast, reliable, updatable

---

## Running the Scripts

### Prerequisites
```
Python 3.x installed
Assets folder with PNG images
Base directory accessible
```

### Run One Script
```bash
python complete_image_cleanup.py
```

### Run All Sequentially
```bash
python complete_image_cleanup.py
python update_homepage_complete.py
python fix_hero_pokemon_overlay.py
python update_hero_and_categories.py
python reorganize_homepage_structure.py
python replace_product_images.py
python enhance_bundle_showcase.py
```

### Expected Output
- 16 base64 files created
- 1 homepage_base64.html file created (~39 MB)
- Console messages confirming each step

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "File not found" | Image path incorrect | Check assets folder path |
| "Permission denied" | Can't write file | Close file in editor first |
| "Base64 is empty" | Image not read correctly | Check file permissions |
| "HTML too large" | All images embedded | Use GitHub Pages instead |

---

**That's all the scripts!** Each one handles a specific part of the homepage redesign. Together, they create a professional, animated trading card website.

