# Universal — Full Website Builder
Scripts that create or rebuild any Odoo website from scratch.

## MASTER SCRIPT
```bash
python odoo_website_builder.py --help
```

| Script | What It Does |
|--------|-------------|
| `odoo_website_builder.py` | **MASTER** — full site builder for any category (agency/ecommerce/tech/local_business/restaurant/nonprofit) |
| `create_odoo_websites.py` | Create new Odoo website records |
| `configure_new_domains.py` | Set up domain routing for new sites |
| `discover_odoo_sites.py` | List all websites + domains in Odoo |
| `list_all_domains.py` | List all registered domains |
| `clean_setup.py` | Initial database cleanup for new site |
| `setup_odoo_stores.py` | Set up store configuration |
| `fix_websites.py` | Fix website configuration issues |
| `fix_domains_odoo.py` | Fix domain mapping in Odoo |
| `rebrand_remove_hiren.py` | Remove Hiren branding, apply new brand |
| `nuclear_fix.py` | Last-resort fix for catastrophic site issues |
| `production_all_sites.py` | Apply changes across all production sites |
| `fix_500_issue.py` | Diagnose and fix Odoo 500 server errors |

## Usage — Build any site category
```bash
# E-commerce store
python odoo_website_builder.py --site 36 --category ecommerce \
  --name "Long Island Cards" --domain "https://www.longislandcards.com" \
  --phone "+1 (516) 555-0100" --location "Plainview, NY"

# Agency site
python odoo_website_builder.py --site 41 --category agency \
  --name "JHD Advisor" --domain "https://www.jhdadvisor.com" \
  --phone "+1 (917) 338-7086" --location "Long Island, NY"

# Local business
python odoo_website_builder.py --site 38 --category local_business \
  --name "LI Balloons & Decor" --domain "https://www.longislandballoonsdecor.com" \
  --phone "+1 (516) 555-0200" --location "Nassau County, NY"
```

## Available Categories
| Category | Best For | Colors |
|----------|---------|--------|
| `agency` | IT/marketing/consulting firms | Purple + Cyan |
| `ecommerce` | Online stores, retail | Green + Amber |
| `tech` | SaaS/software products | Blue + Purple |
| `local_business` | Contractors, salons, clinics | Red + Amber |
| `restaurant` | Food service, cafes | Brown + Red |
| `nonprofit` | Charities, community orgs | Teal + Amber |
