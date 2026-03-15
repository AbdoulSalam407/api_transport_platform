# 🐛 TROUBLESHOOTING GUIDE

## Common Issues & Solutions

---

## ❌ Django/Python Issues

### Issue: `ModuleNotFoundError: No module named 'django'`

**Cause:** Django not installed in your environment

**Solution:**

```bash
pip install django==6.0.3
pip install -r requirements.txt
```

### Issue: `django.core.exceptions.ImproperlyConfigured: Requested setting DATABASES`

**Cause:** Django settings not properly configured

**Solution:**

```bash
# Verify settings.py exists and DJANGO_SETTINGS_MODULE is set
export DJANGO_SETTINGS_MODULE=api_transport_platform.settings

# For Windows (PowerShell):
$env:DJANGO_SETTINGS_MODULE = "api_transport_platform.settings"

# Then try again:
python manage.py runserver
```

### Issue: `No module named 'rest_framework'`

**Cause:** Django REST Framework not installed

**Solution:**

```bash
pip install djangorestframework==3.14.0
pip install -r requirements.txt
```

---

## 🗄️ Database Issues

### Issue: `django.db.utils.OperationalError: no such table: users_customuser`

**Cause:** Database migrations not applied

**Solution:**

```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: PostgreSQL Connection Error

**Cause:** PostgreSQL not running or connection credentials wrong

**Solution:**

```bash
# Check if PostgreSQL is running
# Windows:
Get-Service PostgreSQL
# or use Services application

# Linux/Mac:
sudo systemctl status postgresql

# Check .env file has correct credentials:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=transport_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Test connection:
psql -U postgres -d transport_db -h localhost
```

### Issue: `psycopg2 is the psycopg package`

**Cause:** psycopg2 not installed for PostgreSQL

**Solution:**

```bash
pip install psycopg2-binary==2.9.9
```

### Issue: Database locked (SQLite)

**Cause:** Django testing or multiple processes accessing database

**Solution:**

```bash
# Close all Django instances
# Delete SQLite database and start fresh:
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🔐 Authentication Issues

### Issue: `detail": "Invalid token."`

**Cause:** Token missing, invalid, or expired

**Solution:**

```bash
# 1. Get a new token
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-password"}'

# 2. Use token in Authorization header
Authorization: Token abc123def456
```

### Issue: `"detail": "Authentication credentials were not provided."`

**Cause:** Missing Authorization header

**Solution:**

```bash
# Add this header to every request:
Authorization: Token YOUR_TOKEN

# In Postman:
# Go to Authorization tab
# Select "Bearer Token"
# Paste your token
```

### Issue: `"detail": "You do not have permission to perform this action."`

**Cause:** Insufficient permissions for user role

**Solution:**

```bash
# 1. Change user role in database:
python manage.py shell

# In shell:
from users.models import CustomUser
user = CustomUser.objects.get(username='username')
user.role = 'admin'  # or 'driver', 'client'
user.save()

# 2. Or get superuser token:
python manage.py createsuperuser
```

### Issue: `"detail": "Invalid username/password."`

**Cause:** Wrong credentials provided

**Solution:**

```bash
# Reset password:
python manage.py changepassword username

# Or create new superuser:
python manage.py createsuperuser
```

---

## 📡 API Endpoint Issues

### Issue: `404 Not Found`

**Cause:** Endpoint URL incorrect or resource doesn't exist

**Solution:**

```bash
# 1. Verify URL structure
Correct: http://localhost:8000/api/v1/users/users/
Wrong: http://localhost:8000/api/users/users/  (missing v1)
Wrong: http://localhost:8000/api/v1/users/  (missing second users)

# 2. Verify resource exists
# List all first:
GET http://localhost:8000/api/v1/users/users/

# 3. Then get specific by ID:
GET http://localhost:8000/api/v1/users/users/1/
```

### Issue: `400 Bad Request`

**Cause:** Invalid JSON or missing required fields

**Solution:**

```bash
# 1. Verify JSON is valid
# Use JSONLint.com to validate

# 2. Check required fields:
POST http://localhost:8000/api/v1/users/users/
{
  "username": "john",              # Required
  "email": "john@example.com",     # Required
  "password": "securepass123",     # Required
  "first_name": "John",            # Optional but recommended
  "last_name": "Doe",              # Optional
  "role": "client"                 # Optional (defaults to client)
}

# 3. Check data types
# phone_number must be string: "+33612345678" not 33612345678
```

### Issue: `405 Method Not Allowed`

**Cause:** Wrong HTTP method for endpoint

**Solution:**

```bash
# Reference which methods each endpoint accepts:
GET    /api/v1/users/users/              # List
POST   /api/v1/users/users/              # Create
GET    /api/v1/users/users/{id}/         # Detail
PUT    /api/v1/users/users/{id}/         # Update
DELETE /api/v1/users/users/{id}/         # Delete
```

### Issue: `412 Precondition Failed` or CORS errors

**Cause:** CORS configuration issue

**Solution:**

```bash
# Verify CORS is enabled in settings.py:
INSTALLED_APPS = [
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

# If still failing, allow all during development:
CORS_ALLOW_ALL_ORIGINS = True  # NOT for production!
```

---

## 📊 Data Issues

### Issue: `"status": ["\"planifie\" is not a valid choice."]`

**Cause:** Invalid choice value for field

**Solution:**

```bash
# Use valid choices only
Valid trajet statuses: "planifie", "en_cours", "termine", "annule"
Valid vehicule types: "bus", "minibus", "voiture", "van"
Valid vehicule status: "disponible", "en_trajet", "maintenance", "inactif"

# Check model choices in model files:
# trajets/models.py for Trajet.STATUS_CHOICES
# vehicules/models.py for Vehicule.TYPE_CHOICES
```

### Issue: `"phone_number": ["Enter a valid phone number."]`

**Cause:** Phone number format invalid

**Solution:**

```bash
# Use international format with +
# Valid: "+33612345678", "+33123456789"
# Invalid: "0612345678", "33612345678", "612345678"

# Regex in validators:
^\+?1?\d{9,15}$
```

### Issue: `"username": ["This field must be unique."]`

**Cause:** Username already exists in database

**Solution:**

```bash
# Use different username
# Or reset user:
python manage.py shell

from users.models import CustomUser
CustomUser.objects.filter(username='oldname').delete()
```

### Issue: `"email": ["This field must be unique."]`

**Cause:** Email already registered

**Solution:**

```bash
# Use different email
# Or delete user:
python manage.py shell

from users.models import CustomUser
CustomUser.objects.filter(email='test@example.com').delete()
```

---

## 🚀 Server/Runtime Issues

### Issue: `Address already in use`

**Cause:** Port 8000 already in use

**Solution:**

```bash
# Use different port:
python manage.py runserver 0.0.0.0:8001

# Or kill process using port 8000:
# Windows (PowerShell):
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Linux/Mac:
sudo lsof -ti:8000 | xargs kill -9
```

### Issue: `RuntimeError: Event loop is closed`

**Cause:** Async issue with Django

**Solution:**

```bash
# Restart Python
# If using Windows:
python manage.py runserver
# Then try again

# Or use:
python manage.py runserver --nothreading
```

### Issue: `ConnectionRefusedError` or timeout

**Cause:** Server not running

**Solution:**

```bash
# Make sure server is running in terminal:
python manage.py runserver

# Output should show:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C
```

---

## 🔍 Migration Issues

### Issue: `No changes detected in app 'users'`

**Cause:** Models not modified or migrations already exist

**Solution:**

```bash
# Show migration status:
python manage.py showmigrations users

# If migrations exist but not applied:
python manage.py migrate users

# If you need to reset migrations:
# BE CAREFUL - this deletes all data!
python manage.py migrate users zero  # Unapply all
rm users/migrations/0*.py            # Delete migration files
python manage.py makemigrations users
python manage.py migrate users
```

### Issue: `Conflicting migrations detected`

**Cause:** Multiple migration branches

**Solution:**

```bash
# Show conflicts:
python manage.py showmigrations --plan

# Merge migrations:
python manage.py makemigrations --merge

# Or reset and start fresh:
python manage.py migrate zero
python manage.py makemigrations
python manage.py migrate
```

### Issue: `Application 'core' doesn't have a 'models' module`

**Cause:** Core app not properly configured

**Solution:**

```bash
# Create models.py in core/:
touch api_transport_platform/core/models.py

# Add to core/apps.py:
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    # Don't change default_auto_field for core
```

---

## 📝 Admin Issues

### Issue: `Page not found` at `/admin/`

**Cause:** Admin app not installed or migrations not run

**Solution:**

```bash
# Verify admin is in INSTALLED_APPS:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    ...
]

# Migrate:
python manage.py migrate
```

### Issue: `No such table: django_session`

**Cause:** Admin migrations not applied

**Solution:**

```bash
python manage.py migrate
```

### Issue: Admin page shows empty list

**Cause:** Admin not registered for model

**Solution:**

```bash
# Check app/admin.py has registration:
from django.contrib import admin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name']
```

---

## 🧪 Testing Issues

### Issue: `No tests were run`

**Cause:** Test files not found or not named correctly

**Solution:**

```bash
# Run tests:
python manage.py test

# Run specific app tests:
python manage.py test users

# Run specific test file:
python manage.py test users.tests

# Run with verbose output:
python manage.py test --verbosity=2

# Create test file if missing:
# Create: app/tests.py or app/tests/
# Write test class extending TestCase
```

---

## 📦 Dependency Issues

### Issue: `pip: command not found`

**Cause:** pip not in PATH

**Solution:**

```bash
# Use Python module:
python -m pip install package-name

# Or use anaconda:
conda install package-name
```

### Issue: `FileNotFoundError: [Errno 2] No such file or directory: 'requirements.txt'`

**Cause:** Not in project root directory

**Solution:**

```bash
# Navigate to project root:
cd c:\Users\DELL\Desktop\formation_python_force_n\transport_platform\api_transport_platform

# Then install:
pip install -r requirements.txt
```

### Issue: `Version conflict: requirement not found`

**Cause:** Package version incompatibility

**Solution:**

```bash
# Update pip, setuptools, wheel:
pip install --upgrade pip setuptools wheel

# Then reinstall requirements:
pip install --force-reinstall -r requirements.txt
```

---

## 🎯 Quick Diagnosis Commands

```bash
# Check Django setup
python manage.py check

# Check installed apps
python manage.py shell
>>> from django.apps import apps
>>> [app.name for app in apps.get_app_configs()]

# Check database connection
python manage.py dbshell

# Show all migrations
python manage.py showmigrations

# Check URLs
python manage.py show_urls

# Check settings
python manage.py shell
>>> from django.conf import settings
>>> settings.DATABASE_URL  # etc.

# Clear cache (if using Redis)
redis-cli FLUSHDB

# Check user count
python manage.py shell
>>> from users.models import CustomUser
>>> CustomUser.objects.count()
```

---

## 💬 Still Having Issues?

### Debug Steps:

1. **Check Logs** - Look at terminal output for errors
2. **Read Error Messages** - They often contain the solution
3. **Verify Prerequisites** - Python, pip, Django, DRF installed
4. **Test Incrementally** - Test each endpoint individually
5. **Use Shell** - `python manage.py shell` to test code directly
6. **Clear Cache** - Sometimes things get stuck

### Common Resources:

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Stack Overflow: Tag your question with `django` and `django-rest-framework`
- Project Docs: See README.md, PROJECT_DOCUMENTATION.md

---

**Last Updated:** 2026-03-20  
**Version:** 1.0
