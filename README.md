# CarZest - Django Car Rental System

CarZest is a Django-based car rental web application originally built as a collaborative hackathon project and later shared on a teammate's GitHub repository. This repository is a refreshed version of that project, with the original concept retained while the backend, booking flow, security hygiene and frontend have been cleaned up for portfolio use.

> **Project note:** This is a student/portfolio project, not a production rental marketplace. Payment processing, live vehicle availability, deployment infrastructure and real-world fleet operations are intentionally outside the current scope.

## What changed in the refreshed version

- Modern responsive UI with a new landing page, fleet cards and authentication screens
- Database-driven vehicle listings instead of hard-coded vehicle choices
- Login-protected fleet and booking pages
- User-owned booking history via **My Bookings**
- Server-side rental-price calculation
- Booking validation for rental duration and pickup dates
- Django admin improvements for vehicles, bookings and contact messages
- Environment-based Django secret key and host configuration
- Clean `.gitignore` so local databases, media and Python cache files stay out of Git
- Automated tests covering authentication, vehicle access and booking calculations

## Features

- User registration and login
- Vehicle fleet browsing
- Vehicle-specific booking flow
- Rental duration and pickup-date validation
- Automatic rental total calculation
- Booking history for authenticated users
- Contact form stored in the Django admin
- Django admin dashboard for fleet and booking management
- Responsive frontend for desktop and mobile screens

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap 5, Bootstrap Icons, JavaScript
- **Database:** SQLite for local development
- **Image handling:** Pillow
- **Testing:** Django TestCase

## Project Structure

```text
Car-Rental-System/
├── MyApp/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── vehicles/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── static/
├── templates/
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Car-Rental-System
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Use `.env.example` as a reference and export the variables in your shell or set them in your deployment platform. The project intentionally avoids a dotenv dependency.

The current Django settings read:

```text
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS
```

The project does not require a third-party environment-variable package for local use. Export the variables in your shell or load them through your deployment platform.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create an admin account

```bash
python manage.py createsuperuser
```

### 7. Load the sample fleet

The repository includes a small fixture containing the original demo fleet.

```bash
python manage.py loaddata fixtures/cars.json
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

Admin dashboard: `http://127.0.0.1:8000/admin/`

The sample vehicle images are kept in `static/` so the repository stays self-contained without committing a development `media/` directory.

## Testing

Run the automated test suite with:

```bash
python manage.py test
```

## Adding Vehicles

Vehicle records are managed through the Django admin panel. Each vehicle can have:

- Vehicle ID
- Name
- Description
- Daily rental price
- Vehicle image

The public booking form reads vehicle names and prices directly from the database. The final rental total is recalculated server-side before the booking is stored.

## Security / Repository Hygiene

The repository intentionally does **not** include:

- `db.sqlite3`
- `.env` files
- Python `__pycache__` directories
- `.pyc` files
- Django `staticfiles/` build output
- Local uploaded media

Never commit production credentials, API keys or real customer information to Git.

## Original Project Context

The initial application was created collaboratively during a hackathon and was later hosted by a teammate. This refreshed repository preserves the original CarZest concept while documenting and improving the codebase rather than presenting the original work as a brand-new solo project.

## Future Improvements

Potential next steps include:

- Real-time vehicle availability
- Payment gateway integration
- Booking cancellation and refund workflows
- Email/SMS booking confirmations
- PostgreSQL for production deployment
- Docker-based deployment
- REST API for a mobile client
- Automated CI/CD with GitHub Actions

## License

Add the appropriate license and attribution information from the original project before publishing if the original repository's license requires it.
