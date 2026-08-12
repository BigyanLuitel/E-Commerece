# GadgetHub

GadgetHub is an electronics e-commerce project built with Django. It includes a storefront, shopping cart, order flow, admin dashboard, and a conversational AI assistant for customer support and product guidance.

## Features

- Product catalog with categories such as smartphones, laptops, audio, wearables, and gaming
- Search and filtering for products
- Cart and checkout flow
- Simulated payment options: eSewa, Khalti, card, and cash on delivery
- Order tracking and order history
- Staff dashboard for managing products, orders, and users
- AI-powered staff tools for generating product descriptions and suggesting categories
- Customer chat assistant for help and ordering support
- Help Center page with support guidance and FAQs

## Tech Stack

- Backend: Django
- Database: PostgreSQL (configured in the project settings)
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Authentication: Django custom user model
- AI integration: external service running on localhost:8010

## Project Structure

```text
gadgethub/
├── accounts/
├── cart/
├── chatbot/
├── dashboard/
├── gadgethub/
├── internal_api/
├── orders/
├── products/
├── static/
├── templates/
├── manage.py
├── requirements.txt
└── .env
```

## Setup

### 1. Create and activate a virtual environment

```bash
cd d:\CollegeProjects\E-Commerece
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file inside the `gadgethub` folder with values such as:

```env
DB_PASSWORD=your_database_password
HOST=your_database_host
PORT=your_database_port
INTERNAL_API_KEY=your_internal_api_key
AI_SERVICE_URL=http://localhost:8010
```

### 3. Run database setup

```bash
cd gadgethub
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open:

- Storefront: http://localhost:8000
- Admin dashboard: http://localhost:8000/dashboard/

## Optional AI service

The app is designed to use an external AI service on `http://localhost:8010` for features like product description generation, category suggestion, and chat assistance.

If that service is not running, the core storefront and dashboard still work, but AI-powered features will not be available.

## Main User Flows

- Browse products from the home page and product listing pages
- Add products to the cart
- Proceed to checkout and choose a payment method
- View and track orders from the order history page
- Use the chat assistant for product and support help
- Access the Help Center for FAQs and support options
- Log in to the dashboard as a staff/superuser to manage products, orders, and users

## Notes

- Payment is simulated for this project and is not connected to a real payment provider.
- The project uses a custom user model based on email login.
- Passwords are not exposed in dashboard user views.
