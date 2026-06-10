# Universal — Header, Footer & Navigation
Scripts that manage site-wide header, footer, menus and navigation.

## Scripts

| Script | What It Does |
|--------|-------------|
| `fix_all_footers_favicons.py` | Fix footer layout + favicon paths across all sites |
| `cleanup_menus.py` | Remove duplicate or orphaned navigation menu items |
| `add_blog_menu.py` | Add Blog menu item to any site's navigation |
| `setup_header_footer_users.py` | Set up user-specific header/footer configurations |
| `fix_header_v2.py` | Header layout and styling fixes |
| `read_footer_views.py` | Read and inspect footer view HTML |
| `fix_footer_and_domain.py` | Footer content + domain corrections |
| `fix_homepage_layout.py` | Homepage section layout fixes |
| `fix_social_links.py` | Update social media links in footer |
| `fix_phone_numbers.py` | Update phone numbers across all pages |
| `fix_contact_all_views.py` | Fix contact info across all website views |
| `fix_contact_page.py` | Rebuild contact page from scratch |
| `fix_stores_page.py` | Fix store location page layout |
| `create_contact_page.py` | Create new contact/location pages with forms |
| `upload_logos_fix_jhd.py` | Upload logos + fix JHD Advisor branding |

## Add navigation to any site
```bash
# Add a Blog menu item to site 41
python add_blog_menu.py

# Fix all footers across all sites
python fix_all_footers_favicons.py
```

## Navigation structure used across sites
```
Home | Services/Shop | Blog | About | Contact
```
