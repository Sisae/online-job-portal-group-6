Project name: Job Portal (Django)

Purpose & audience

Purpose: Provide a secure, maintainable platform for employers to publish jobs and for job seekers to discover roles, submit applications, and track hiring progress.

Primary users: Job seekers, Employers, Site administrators.

High-level goals

Let employers create and manage company profiles and job listings.

Let job seekers register, upload resumes, search jobs, apply, and monitor application status.

Provide an employer dashboard to review, filter, and update application statuses.

Be modular, secure, and ready for scaling (follow Django conventions and enable later API, async, and caching integrations).

Core technical stack

Backend: Python + Django (MVT), Django REST Framework (for future APIs)

Frontend: Django templates + Bootstrap (static files) for the MVP

Database: SQLite for development (migrate to PostgreSQL in production)

Background tasks: Celery + Redis (planned)

File storage: local MEDIA/ for dev; S3 or cloud storage for production

CI: GitHub Actions (run tests, lint, basic checks)

Core features (MVP)

Custom user model: is_employer flag to separate flows.

Company model & employer dashboard.

Job model with CRUD (title, company FK, description, location, job_type, closing_date, is_active).

Public job listings with pagination, keyword search, and basic filters (location, company, remote).

Application model linking job + applicant, with resume FileField and application status lifecycle (Applied → Under Review → Interview → Offer → Rejected).

Resume upload validation (file type & size).

Email notifications (console backend for dev).

Admin customizations for managing core models.

Non-functional requirements

Security: CSRF protection, input validation, file-type checking, access control on employer actions.

Maintainability: Modular apps (accounts, companies, jobs, applications, core), PEP8-compliant code, documented models and views.

Performance: Use select_related/prefetch_related for related queries; cache frequently-read pages (optional Redis).

Scalability: ASGI-ready, Celery-ready for background jobs, abstracted storage configuration for switching to cloud storage.

Acceptance criteria / success metrics

A registered employer can create a company and post a job that appears in public listings.

A job seeker can register, upload a resume, apply to a job, and view the application status.

Employers can view and change application statuses; status changes trigger notifications to applicants.

Tests: core models and key views have unit tests and pass on CI.

The app can be run locally using the documented steps in README (venv, pip install -r requirements.txt, python manage.py migrate, runserver).

Extensibility & next steps

Add REST API endpoints with DRF for mobile clients.

Add resume parsing / NLP for skill extraction and matching.

Integrate Celery for email and heavy tasks; use Redis for caching.

Deploy to a production-ready platform (Docker, Kubernetes, Render, Heroku, or similar) and switch to PostgreSQL + cloud storage.