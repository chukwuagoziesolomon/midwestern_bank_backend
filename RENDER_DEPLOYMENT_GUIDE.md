# 🚀 Render Deployment Guide - Midwestern Bank

## Overview

This guide explains how to deploy the Midwestern Bank backend to Render with automatic superuser creation.

---

## Step 1: Prepare for Deployment

### 1.1 Create Render Account
1. Go to https://render.com
2. Sign up for a free account
3. Connect your GitHub repository

### 1.2 Files Already in Place
✅ `build.sh` - Build script that runs during deployment
✅ `bankapp/management/commands/create_superuser_auto.py` - Auto-creates superuser
✅ `requirements.txt` - Python dependencies

---

## Step 2: Environment Variables on Render

Go to your Render service settings and add these environment variables:

### Database (PostgreSQL)
```
DATABASE_URL=postgres://user:password@host:5432/dbname
```

### Email Configuration (Gmail)
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@midwesternbank.com
```

### Admin Superuser Creation (Optional - Uses Defaults if Not Set)
```
ADMIN_EMAIL=admin@midwesternbank.com
ADMIN_PASSWORD=SecureAdminPassword123!
ADMIN_FIRST_NAME=Admin
ADMIN_LAST_NAME=User
```

### Django Settings
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com,localhost
CORS_ALLOWED_ORIGINS=http://localhost:5173,https://your-admin-dashboard.vercel.app,https://your-app.onrender.com
```

---

## Step 3: Create PostgreSQL Database on Render

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Fill in:
   - **Name:** midwestern-bank-db
   - **PostgreSQL Version:** Latest
   - **Region:** Same as your service
4. Click "Create Database"
5. Copy the `DATABASE_URL` and add to Web Service

---

## Step 4: Create Web Service on Render

### 4.1 Connect Repository
1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Select your GitHub repository

### 4.2 Configure Service
- **Name:** midwestern-bank-api
- **Environment:** Python 3
- **Region:** Your preferred region
- **Build Command:** `bash build.sh`
- **Start Command:** `gunicorn config.wsgi:application`

### 4.3 Add Environment Variables
Add all the variables from Step 2

### 4.4 Create Service
- Render will automatically run `build.sh` during deployment
- This will:
  1. ✅ Install dependencies
  2. ✅ Run migrations
  3. ✅ Collect static files
  4. ✅ **Create superuser automatically**

---

## Step 5: Verify Deployment

### Check Build Logs
1. Go to your Web Service
2. Click "Logs" tab
3. Look for:
   ```
   ✅ Superuser created successfully!
   Email: admin@midwesternbank.com
   ```

### Test API Endpoints
```bash
# Test signup
curl -X POST https://your-app.onrender.com/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@bank.com",
    "password": "testpass",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Test admin login
curl -X POST https://your-app.onrender.com/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@midwesternbank.com",
    "password": "SecureAdminPassword123!"
  }'
```

---

## Step 6: Connect Admin Frontend

Update your React/Vite admin dashboard API URL:

```javascript
// config or env file
const API_BASE = process.env.VITE_API_URL || 'https://your-app.onrender.com/api';
```

Update CORS_ALLOWED_ORIGINS in Django settings if needed:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'https://your-admin-dashboard.vercel.app',
    'https://your-app.onrender.com'
]
```

---

## Step 7: Deploy on Every Push

Once configured, every push to your GitHub repository will:
1. Trigger automatic deployment
2. Run `build.sh` which:
   - Installs dependencies
   - Runs migrations
   - Creates superuser (if doesn't exist)
3. Start the web service

---

## Troubleshooting

### Issue: "Superuser not created"
**Solution:** Check environment variables are set correctly
```bash
# View logs
# Look for error messages in the Build/Deploy logs
```

### Issue: "Database connection failed"
**Solution:** Verify DATABASE_URL is correct
```
# Should look like:
postgres://user:password@db-host:5432/dbname
```

### Issue: "Email not configured"
**Solution:** Add email environment variables
```
EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, etc.
```

### Issue: "CORS error from admin dashboard"
**Solution:** Update CORS_ALLOWED_ORIGINS
```python
CORS_ALLOWED_ORIGINS = [
    'https://your-admin-domain.vercel.app'
]
```

---

## What Happens During Deployment

```
1. 🔧 Push to GitHub
   ↓
2. 🚀 Render detects changes
   ↓
3. 📥 Clones repository
   ↓
4. 🏗️ Runs build.sh:
   - pip install -r requirements.txt
   - python manage.py migrate
   - python manage.py collectstatic --noinput
   - python manage.py create_superuser_auto
   ↓
5. ✅ Superuser created (if not exists)
   ↓
6. 🌐 Web service starts
   ↓
7. 🎉 API ready at https://your-app.onrender.com/api
```

---

## Post-Deployment Checklist

- ✅ Superuser account created automatically
- ✅ Database migrations applied
- ✅ Static files collected
- ✅ API endpoints accessible
- ✅ CORS configured for admin dashboard
- ✅ Email service configured
- ✅ Admin can login and manage users

---

## Default Admin Credentials

If you don't set environment variables, defaults are:

```
Email: admin@midwesternbank.com
Password: AdminPassword123!
```

⚠️ **CHANGE THESE IN PRODUCTION!** Set proper environment variables:

```
ADMIN_EMAIL=your-secure-email@company.com
ADMIN_PASSWORD=YourSecurePassword123!SecurePassword123!
```

---

## Monitoring Deployment

### View Live Logs
```bash
# In Render Dashboard
# Click on Web Service → Logs
# Watch real-time deployment progress
```

### Check Database
```bash
# Click on PostgreSQL instance
# Check "Connections" tab
```

### Monitor API Health
```bash
curl https://your-app.onrender.com/api/signup/
# Should return 200 OK
```

---

## Next Steps

1. **Deploy React admin dashboard** to Vercel/Netlify
2. **Update API_BASE_URL** in admin dashboard to point to production
3. **Create initial users** via signup endpoint
4. **Approve users** using admin dashboard
5. **Monitor logs** on Render dashboard

---

## Quick Commands Reference

**Create superuser locally:**
```bash
python manage.py create_superuser_auto
```

**Create superuser with custom credentials:**
```bash
ADMIN_EMAIL=admin@bank.com \
ADMIN_PASSWORD=MyPassword123! \
python manage.py create_superuser_auto
```

**Run migrations:**
```bash
python manage.py migrate
```

**Check if superuser exists:**
```bash
python manage.py shell -c "from django.contrib.auth.models import User; print('Superusers:', User.objects.filter(is_superuser=True).values('email'))"
```

---

**Your Midwestern Bank API is now ready for production on Render!** 🎉
