# LUMINA — Django E-Commerce

A full-featured Django e-commerce store with user auth, admin dashboard, and REST API.

## Quick Start

```bash
# 1. Install dependencies
pip install django djangorestframework pillow

# 2. Apply migrations
python manage.py migrate

# 3. Seed demo data + create admin (optional)
python manage.py loaddata  # or run the seed script

# 4. Create your own superuser
python manage.py createsuperuser

# 5. Run the dev server
python manage.py runserver
```

Open http://localhost:8000

## Demo Credentials (pre-seeded)
- **Admin:** `admin` / `admin123`  →  http://localhost:8000/admin/
- Register a new user at http://localhost:8000/register/

## Pages
| URL | Description |
|-----|-------------|
| `/` | Homepage with featured & latest products |
| `/products/` | Full catalog with filtering + sorting |
| `/products/<slug>/` | Product detail page |
| `/cart/` | Shopping cart |
| `/checkout/` | Order placement |
| `/orders/` | Order history |
| `/login/` | Sign in |
| `/register/` | New account |
| `/admin/` | Django admin dashboard |

## REST API
| Endpoint | Description |
|----------|-------------|
| `GET /api/` | API root |
| `GET /api/products/` | All products |
| `GET /api/products/<slug>/` | Single product |
| `GET /api/categories/` | All categories |
| `GET /api/orders/` | User's orders (auth required) |

**Query params:** `?search=query`, `?category=slug`, `?ordering=price`

## Project Structure
```
ecommerce/          # Django project config
store/              # Main app (models, views, templates)
  models.py         # Category, Product, Order, Cart
  views.py          # All page views
  admin.py          # Admin configuration
  urls.py           # URL patterns
api/                # REST API app
  serializers.py    # DRF serializers
  views.py          # API viewsets
  urls.py           # API routes
templates/
  base.html         # Base layout (dark luxury theme)
  store/            # Page templates
```

## Models
- **Category** — product groupings with slugs
- **Product** — name, price, stock, image_url, featured flag
- **Order** + **OrderItem** — user orders with status tracking
- **Cart** + **CartItem** — per-user persistent cart

## Customisation
- Add products via `/admin/`
- Change theme colours in `base.html` `:root` CSS variables
- Extend API with `api/serializers.py` + `api/views.py`
