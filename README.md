# Scholarship Eligibility Checker

SchemeSetu is a scholarship eligibility checker built to help students identify government scholarship schemes that may match their personal, academic, and financial profile. The project includes both a full Django backend version and a static portfolio demo that can be opened directly from GitHub Pages.

## Live Demo

Portfolio website:

[https://gnanenderchinnu.github.io/scholorship-eligibility-checker/](https://gnanenderchinnu.github.io/scholorship-eligibility-checker/)

GitHub repository:

[https://github.com/GnanenderChinnu/scholorship-eligibility-checker](https://github.com/GnanenderChinnu/scholorship-eligibility-checker)

## Index

1. [Project Overview](#project-overview)
2. [Objectives](#objectives)
3. [Key Features](#key-features)
4. [Technology Stack](#technology-stack)
5. [Project Structure](#project-structure)
6. [Static Portfolio Demo](#static-portfolio-demo)
7. [Django Application](#django-application)
8. [Eligibility Logic](#eligibility-logic)
9. [Database and Seed Data](#database-and-seed-data)
10. [Local Setup](#local-setup)
11. [Demo Credentials](#demo-credentials)
12. [Deployment](#deployment)
13. [Testing](#testing)
14. [Future Scope](#future-scope)
15. [Disclaimer](#disclaimer)

## Project Overview

Many students miss scholarship opportunities because scheme rules are spread across multiple portals and are difficult to compare. This project demonstrates a centralized eligibility-checking workflow where a student enters profile details and receives scheme matches with clear explanations.

The application is designed as a realistic portfolio project. The database contains sample schemes, but the system is structured so that more real schemes can be added later through Django Admin or CSV import.

## Objectives

- Provide a clean scholarship eligibility checking experience.
- Collect relevant student profile details such as category, income, domicile state, education level, marks, certificates, and bank readiness.
- Compare profile information against structured scheme rules.
- Show matched and missing eligibility conditions.
- Provide a printable/downloadable eligibility report.
- Support future expansion of the scheme database.
- Offer a static GitHub Pages version for recruiters and portfolio review.

## Key Features

- Student registration and login using Django built-in authentication.
- Student profile form with personal, academic, income, document, and eligibility-related fields.
- Structured scholarship scheme model.
- Rule-based eligibility matching.
- Results page with eligibility percentage, matched criteria, and missing criteria.
- Scheme browsing and filtering.
- Django Admin support for scheme management.
- CSV export/import commands for scheme data expansion.
- Seed data command for sample schemes.
- Static browser-only demo for GitHub Pages.
- Print/download report support using browser print.
- Render-ready deployment files.

## Technology Stack

| Area | Technology |
| --- | --- |
| Backend | Django |
| Frontend | Django Templates, HTML, CSS |
| Database | SQLite |
| Authentication | Django built-in auth |
| Admin Panel | Django Admin |
| Static Demo | HTML, CSS, JavaScript, localStorage |
| Deployment Target | Render for Django, GitHub Pages for static demo |
| Styling | Plain custom CSS |

## Project Structure

```text
scholorship site/
├── checker/                 # Django app for profiles, schemes, eligibility, commands
├── scholarship_site/        # Django project settings and URL config
├── templates/               # Django HTML templates
├── static/                  # Django CSS assets
├── static-demo/             # Local no-server static version
├── docs/                    # GitHub Pages static website
├── manage.py
├── requirements.txt
├── render.yaml
├── Procfile
├── build.sh
└── README.md
```

## Static Portfolio Demo

The static version is intended for recruiters and portfolio visitors. It does not require Python, Django, SQLite, or a running server.

Live static demo:

[https://gnanenderchinnu.github.io/scholorship-eligibility-checker/](https://gnanenderchinnu.github.io/scholorship-eligibility-checker/)

Main static files:

```text
docs/index.html
docs/styles.css
docs/app.js
```

The static demo supports:

- Student profile entry.
- Demo profile loading.
- Scheme browsing.
- Scheme filtering.
- Eligibility calculation in the browser.
- Matched and missing criteria.
- Printable report.
- Browser localStorage for saving demo profile data.

## Django Application

The Django version demonstrates the backend architecture for a real scholarship checker.

Main modules:

- `checker/models.py`: student profile and scholarship scheme models.
- `checker/eligibility.py`: rule-based eligibility engine.
- `checker/forms.py`: registration and profile forms.
- `checker/views.py`: page views and filtering logic.
- `checker/admin.py`: Django Admin configuration.
- `checker/management/commands/`: seed, demo, import, and export commands.

Important pages:

- `/` - homepage
- `/register/` - student registration
- `/login/` - login
- `/dashboard/` - user dashboard
- `/profile/` - student profile form
- `/results/` - eligibility results
- `/schemes/` - scheme browsing
- `/admin/` - admin panel

## Eligibility Logic

The eligibility engine compares a student's profile with each scheme's structured rule fields.

Examples of checked conditions:

- Domicile/state requirement
- Category requirement
- Gender requirement
- Education level
- Course stream
- Family income limit
- Minimum marks
- Age limit
- Disability condition
- BPL condition
- Bank account requirement
- Aadhaar-linked bank readiness
- Income certificate availability
- Caste/category certificate availability
- Previous-year pass requirement
- Hosteller/day scholar condition

Each scheme result includes:

- Eligibility status
- Match percentage
- Matched criteria
- Missing criteria
- Official portal link

## Database and Seed Data

The project uses SQLite for simple local development and demo deployment.

Seed schemes can be loaded with:

```bash
python manage.py seed_schemes
```

Scheme data can be exported with:

```bash
python manage.py export_schemes_csv schemes_export.csv
```

Scheme data can be imported with:

```bash
python manage.py import_schemes_csv path/to/file.csv
```

The included scheme data is sample/demo data. It is suitable for demonstrating functionality, but real production use requires verified and regularly updated official scheme data.

## Local Setup

Install Python, then run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_schemes
python manage.py create_demo
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

## Demo Credentials

The demo account can be created with:

```bash
python manage.py create_demo
```

Credentials:

```text
Username: demo_student
Password: Demo@12345
```

## Deployment

### GitHub Pages

The static portfolio demo is deployed from the `docs` folder.

GitHub Pages settings:

```text
Source: Deploy from a branch
Branch: main
Folder: /docs
```

Published site:

[https://gnanenderchinnu.github.io/scholorship-eligibility-checker/](https://gnanenderchinnu.github.io/scholorship-eligibility-checker/)

### Render

The Django version includes Render deployment files:

```text
render.yaml
Procfile
build.sh
requirements.txt
```

Recommended environment variables:

```text
SECRET_KEY=<secure generated value>
DEBUG=False
ALLOWED_HOSTS=<your-render-domain>.onrender.com
CSRF_TRUSTED_ORIGINS=https://<your-render-domain>.onrender.com
```

Build command:

```bash
./build.sh
```

Start command:

```bash
gunicorn scholarship_site.wsgi:application
```

## Testing

Run Django tests with:

```bash
python manage.py test
```

The test suite covers:

- Eligibility rule matching.
- Validation of structured scheme fields.
- Scheme filtering.
- Profile submission flow.

## Future Scope

Possible future improvements:

- Add a larger verified scholarship database.
- Add state-wise scheme coverage for all Indian states.
- Add multilingual support.
- Add PDF generation.
- Add student document upload and verification workflow.
- Add admin import templates with validation previews.
- Move production database from SQLite to PostgreSQL.
- Add dashboard analytics for admins.

## Disclaimer

This project is created for academic, portfolio, and demonstration purposes. Eligibility results are based on stored rule fields and should be treated as guidance only. Students must verify final eligibility, deadlines, benefits, and application requirements on the official government portals before applying.
