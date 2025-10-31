# Job Portal API Documentation

This is the backend API for the Job Portal application, built with Django REST Framework. The API provides endpoints for employers to manage their job postings, company profiles, and applications programmatically.

## Base URL
```
http://127.0.0.1:8000/api/v1/
```

## Authentication

The API uses Token Authentication. Include the token in the Authorization header:

```
Authorization: Token your_token_here
```

### Getting a Token

1. **Register a new user:**
   ```bash
   POST /api/v1/auth/register/
   Content-Type: application/json
   
   {
       "username": "employer1",
       "first_name": "John",
       "last_name": "Doe",
       "email": "john@example.com",
       "password1": "securepassword123",
       "password2": "securepassword123",
       "user_type": "employer"
   }
   ```

2. **Login:**
   ```bash
   POST /api/v1/auth/login/
   Content-Type: application/json
   
   {
       "username": "employer1",
       "password": "securepassword123"
   }
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - Register a new user
- `POST /api/v1/auth/login/` - Login and get token
- `POST /api/v1/auth/logout/` - Logout and delete token

### Companies
- `GET /api/v1/companies/` - List user's company
- `POST /api/v1/companies/` - Create company profile
- `GET /api/v1/companies/{id}/` - Get company details
- `PUT /api/v1/companies/{id}/` - Update company
- `PATCH /api/v1/companies/{id}/` - Partial update company
- `DELETE /api/v1/companies/{id}/` - Delete company
- `GET /api/v1/companies/my_company/` - Get current user's company

### Jobs
- `GET /api/v1/jobs/` - List jobs (employer sees their jobs, job seekers see all active)
- `POST /api/v1/jobs/` - Create a new job (employer only)
- `GET /api/v1/jobs/{id}/` - Get job details
- `PUT /api/v1/jobs/{id}/` - Update job (employer only)
- `PATCH /api/v1/jobs/{id}/` - Partial update job (employer only)
- `DELETE /api/v1/jobs/{id}/` - Delete job (employer only)
- `GET /api/v1/jobs/search/` - Search jobs with filters
- `GET /api/v1/jobs/{id}/applications/` - Get applications for a job (employer only)

### Applications
- `GET /api/v1/applications/` - List applications (employer sees job applications, job seekers see their applications)
- `GET /api/v1/applications/{id}/` - Get application details
- `PATCH /api/v1/applications/{id}/update_status/` - Update application status (employer only)

### Dashboard
- `GET /api/v1/dashboard/stats/` - Get dashboard statistics (employer only)

## Example Usage

### 1. Create Company Profile

```bash
POST /api/v1/companies/
Authorization: Token your_token_here
Content-Type: application/json

{
    "name": "Tech Solutions Inc",
    "website": "https://techsolutions.com",
    "description": "Leading technology company",
    "location": "San Francisco, CA",
    "contact_email": "hr@techsolutions.com"
}
```

### 2. Create a Job

```bash
POST /api/v1/jobs/
Authorization: Token your_token_here
Content-Type: application/json

{
    "title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer...",
    "location": "San Francisco, CA",
    "remote": true,
    "job_type": "full-time",
    "salary": 120000,
    "closing_date": "2024-12-31T23:59:59Z",
    "is_active": true
}
```

### 3. Search Jobs

```bash
GET /api/v1/jobs/search/?search=python&job_type=full-time&location=San Francisco&remote=true
Authorization: Token your_token_here
```

### 4. Update Application Status

```bash
PATCH /api/v1/applications/1/update_status/
Authorization: Token your_token_here
Content-Type: application/json

{
    "status": "under_review",
    "notes": "Candidate looks promising, schedule interview"
}
```

### 5. Get Dashboard Statistics

```bash
GET /api/v1/dashboard/stats/
Authorization: Token your_token_here
```

Response:
```json
{
    "total_jobs": 5,
    "active_jobs": 3,
    "total_applications": 25,
    "pending_applications": 8,
    "recent_applications": [...],
    "recent_jobs": [...]
}
```

## Job Search Filters

The `/api/v1/jobs/search/` endpoint supports the following query parameters:

- `search` - Search in title, description, company name, or location
- `job_type` - Filter by job type (full-time, part-time, contract, internship, temporary)
- `location` - Filter by location
- `remote` - Filter by remote work availability (true/false)
- `min_salary` - Minimum salary filter
- `max_salary` - Maximum salary filter

## Application Status Values

- `applied` - Application submitted
- `under_review` - Application being reviewed
- `interview` - Interview scheduled
- `offer` - Job offer made
- `rejected` - Application rejected

## Error Responses

The API returns standard HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

Error responses include a JSON object with error details:

```json
{
    "error": "Error message",
    "field_errors": {
        "field_name": ["Specific error message"]
    }
}
```

## Rate Limiting

The API implements basic rate limiting to prevent abuse. If you exceed the rate limit, you'll receive a `429 Too Many Requests` response.

## Pagination

List endpoints support pagination with the following query parameters:

- `page` - Page number (default: 1)
- `page_size` - Number of items per page (default: 20, max: 100)

Paginated responses include:

```json
{
    "count": 100,
    "next": "http://api.example.com/endpoint/?page=2",
    "previous": null,
    "results": [...]
}
```


