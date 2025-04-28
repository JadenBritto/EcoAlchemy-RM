# EcoAlchemy ♻️

EcoAlchemy is a Django-based web application that promotes eco-friendly living by offering sustainable products, green tips, and an environmental awareness platform.

---

## 🚀 Features

- User Authentication (Login/Signup)
- Eco-friendly Product Listings
- Tips and Resources for Sustainable Living
- Contact Form
- Clean and modern UI using Django templates
- Responsive Design
- Django Crispy Forms Integration

---

# Tech Stack

- Python 3
- Django 4
- Gunicorn (for WSGI server)
- Render.com (for deployment)
- Django Crispy Forms (for enhanced form styling)

---

## ⚙️ Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ecoalchemy.git
cd ecoalchemy

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

Deployment on Render
Requirements:
A requirements.txt file (already included)

A gunicorn server for production

ALLOWED_HOSTS = ['*'] (or your Render domain) in settings.py

pip install -r requirements.txt
python manage.py migrate

python manage.py runserver 0.0.0.0:$PORT




