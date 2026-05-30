# Scholarship Eligibility Checker

A Django + SQLite scholarship eligibility checker for Indian central and state government schemes.

## Features

- Student registration and login with Django auth
- Student profile capture
- Structured scholarship rule fields
- Eligibility results with matched and missing criteria
- Scheme browsing and details
- Django Admin for managing schemes
- Seed data for practical demo/testing
- Browser print/download report support
- Render-ready deployment files

## Local Setup

Install Python, then run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_schemes
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

## Render Deployment

Set these environment variables in Render:

```text
SECRET_KEY=<generated secure value>
DEBUG=False
ALLOWED_HOSTS=<your-render-domain>.onrender.com
CSRF_TRUSTED_ORIGINS=https://<your-render-domain>.onrender.com
```

Use:

```bash
./build.sh
gunicorn scholarship_site.wsgi:application
```

SQLite works for a demo deployment, but production scholarship data should be backed up regularly or moved to a managed database.

## Static Portfolio Demo

If you want a recruiter-friendly version that does not need Python, Django, or a server, open:

```text
static-demo/index.html
```

That static version runs fully in the browser and can be hosted on GitHub Pages. It includes profile entry, scheme browsing, eligibility matching, localStorage, and print/download reports.
