# Job Portal Project

A Django-based job portal application with employer and job seeker functionality.

## Features

- User authentication and authorization
- Company profile management
- Job posting and management
- Application tracking with status updates
- Email notifications for application status changes
- Employer dashboard

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd online-job-portal-group-6
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Project Structure

- `accounts/` - User authentication and profiles
- `companies/` - Company management
- `jobs/` - Job posting and management
- `applications/` - Job application handling
- `core/` - Core utilities and shared functionality

## Environment Variables

Create a `.env` file in the project root with:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Notes

- The active settings module is `jobportal_project.settings` (used by `manage.py`).
- Default DB is SQLite (`db.sqlite3`).
- CORS is configured for local dev; adjust `CORS_ALLOWED_ORIGINS` as needed in `jobportal_project/settings.py`.

## Deployment

For Heroku or similar platforms, consider adding:

- `Procfile` for process management
- `runtime.txt` for Python version specification
- `whitenoise` for static file serving

## Notifications

### What changed

- We added a simple notifications feature to the site.
- It can send emails now, and it's set up so SMS can be added later.

### What it does now

- Emails when your application status changes
  - If an employer moves your application (like "Under Review" to "Interview"), you get an email showing the old and new status.

- Emails when a new job is posted
  - When a new job is added, all job seekers with an email on file get a "New job posted" email.

### How to try it out

- Add an email to a test job seeker in the Admin.
- Create a new job → the job seeker should get an alert email.
- Change an application's status → that applicant should get a status update email.

### Note for sending real emails

- Configure your email settings in the `.env` file:
  - `EMAIL_HOST` (SMTP server, e.g., smtp-relay.brevo.com)
  - `EMAIL_PORT` (usually 587)
  - `EMAIL_USE_TLS=True`
  - `EMAIL_HOST_USER` (your sending email)
  - `EMAIL_HOST_PASSWORD` (your email app password)
  - `DEFAULT_FROM_EMAIL` (sender address)
- Without these, emails won't actually send.
