# GadgetHub

An e-commerce platform for electronics, built with Django, with an AI layer for product automation and a conversational shopping assistant.

## What it does

- Browse, search, and buy electronics (smartphones, laptops, audio, gaming, etc.)
- Cart, checkout, and simulated payment (eSewa, Khalti, Card, Cash on Delivery)
- Staff dashboard to manage products and orders
- AI tools for staff: auto-generate product descriptions and suggest categories
- AI chatbot for customers: search products by natural language, add to cart, and place orders through conversation

## Tech Stack

- **Backend:** Django, MySQL
- **AI service:** FastAPI, LangGraph, OpenAI (gpt-4o-mini)
- **Search:** ChromaDB (vector search for the chatbot)
- **Frontend:** HTML, CSS, JavaScript (no framework)

## Project Structure

```
gadgethub/          → Django app (main website + dashboard)
ai-service/          → FastAPI app (AI chatbot + tools)
```

## Setup

### 1. Django app

```bash
cd gadgethub
python -m venv venv
venv\Scripts\activate          # or source venv/bin/activate on Mac/Linux
pip install -r requirements.txt
```

Create a `.env` file in the `gadgethub` folder:

```
INTERNAL_API_KEY=<a random secret string>
AI_SERVICE_URL=http://localhost:8010
```

Set up the database, then run:

```bash
python manage.py migrate
python manage.py seed_products
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://localhost:8000`

### 2. AI service

```bash
cd ai-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `ai-service` folder:

```
OPENAI_API_KEY=<your OpenAI key>
DJANGO_INTERNAL_API_URL=http://localhost:8000/api/internal
DJANGO_INTERNAL_API_KEY=<same value as INTERNAL_API_KEY above>
```

Build the product search index, then run the service:

```bash
python build_index.py
uvicorn main:app --reload --port 8010
```

**Both servers need to be running at the same time** for the AI features (description generator, category suggester, chatbot) to work.

## Using It

- **Shop:** go to `http://localhost:8000`, sign up, and browse
- **Chat with the assistant:** click the chat bubble (bottom-right) after logging in
- **Staff dashboard:** log in with a superuser account, go to `http://localhost:8000/dashboard/`

## Notes

- Payment is simulated — no real money moves, no real payment gateway is connected
- The AI service must be running for the "Generate with AI" buttons and chatbot to work; if it's off, the rest of the site still works normally
