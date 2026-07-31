# GadgetHub

GadgetHub is a simple e-commerce web application built with Django. It was created as a semester project to show how a basic online store can work, from browsing products to placing orders.

## What the project includes

- A product catalog with different gadget categories
- Product search and filtering
- User registration and login
- A shopping cart for selected items
- Order placement and order-related views
- A basic dashboard for managing the store

## Tech stack

- Python
- Django
- MySQL
- HTML, CSS, and Bootstrap-based templates
- Pillow for product images

## Getting started

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the required packages:
   - Django
   - Pillow
   - mysqlclient
4. Set up your MySQL database and update the database settings in the project config.
5. Run the development server:

```bash
python manage.py runserver
```

## Project structure

The main app is organized into separate modules for:

- accounts
- products
- cart
- orders
- dashboard

This keeps the project easier to manage and makes it simple to expand later.

## Notes

This is a learning project, so the features are focused on the core flow of an online store rather than full production-level complexity.
