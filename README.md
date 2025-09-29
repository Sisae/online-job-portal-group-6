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
   cd jobportal-fresh
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

## Deployment

For Heroku deployment, the project includes:
- `Procfile` for process management
- `runtime.txt` for Python version specification
- `whitenoise` for static file serving
