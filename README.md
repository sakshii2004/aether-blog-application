# Aether Blog Application

Aether is a blog application where users can:

- Read blog posts
- Write and publish their own blogs
- Like and comment on other users' blogs

---

## Getting Started

### Requirements

- Python 3.x
- pip
- Virtual environment support (`venv`)

---

## Setting Up the Project Locally

### Linux / Windows / macOS

#### 1. Clone the repository
```
git clone https://github.com/sakshii2004/aether-blog-application.git
cd aether-blog-application
```

#### 2. Create a virtual environment

**Linux/macOS:**
```
python3 -m venv env
```

**Windows:**
```
python -m venv env
```

#### 3. Activate the virtual environment

**Linux/macOS:**
```
source env/bin/activate
```

**Windows:**
```
env\Scripts\activate
```

#### 4. Install dependencies
```
pip install django ipython
```

#### 5. Navigate into the Django project folder
```
cd aether
```

#### 6. Run the server
```
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to see the app running.

---

## Features

- Create and manage blog posts
- Comment on posts
- Like your favorite blogs
- Authentication system
```

