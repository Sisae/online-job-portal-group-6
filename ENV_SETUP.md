# Environment Configuration

This project uses environment variables for sensitive configuration. Follow these steps to set up your environment.

## Setup Instructions

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file and add your credentials:**

### Required Settings

#### Django Settings
- `SECRET_KEY`: Django secret key (default is provided for development)
- `DEBUG`: Set to `True` for development, `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

#### Email Settings (Gmail)
To enable email notifications:

1. **Get your Gmail address:**
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   ```

2. **Generate a Gmail App Password:**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification if not already enabled
   - Go to "App passwords" section
   - Generate a new app password for "Mail"
   - Copy the 16-character password
   - Add it to `.env`:
   ```
   EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
   ```

### Example `.env` File

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Settings (Gmail)
EMAIL_HOST_USER=myemail@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

## Security Notes

- ⚠️ **Never commit the `.env` file to version control**
- The `.env` file is already included in `.gitignore`
- Share `.env.example` instead, which contains no sensitive data
- Use different credentials for development and production

## What Happens If Email Is Not Configured?

If you don't configure email settings, the application will still work, but:
- Email notifications for new jobs won't be sent
- Application status update emails won't be sent
- You'll see an SMTP error in the console when these events occur

For development, you can temporarily use Django's console email backend by changing in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
