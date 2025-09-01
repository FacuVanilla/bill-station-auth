# Render Deployment Guide

## Quick Setup for Render

### 1. Create a new Web Service on Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the `auth_service` repository

### 2. Configure the Web Service

**Name:** `auth-service` (or any name you prefer)

**Environment:** `Python 3`

**Build Command:** `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear`

**Start Command:** Leave blank (uses Procfile)

### 3. Environment Variables

Add these environment variables in Render dashboard:

```
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://username:password@host:5432/database_name
REDIS_URL=redis://username:password@host:6379/0
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=7
```

### 4. Database Setup

1. Create a new PostgreSQL database in Render
2. Copy the database URL to your environment variables
3. The migrations will run automatically on deployment

### 5. Deploy

Click "Create Web Service" and Render will:
- Build your application
- Run migrations
- Start the server
- Provide you with a URL

## Advantages of Render over Railway

- ✅ **More reliable deployment**
- ✅ **Better error messages**
- ✅ **Simpler configuration**
- ✅ **Automatic HTTPS**
- ✅ **Better logging**

## Your API Endpoints

Once deployed, your API will be available at:
- **Swagger UI:** `https://your-app-name.onrender.com/`
- **API Base:** `https://your-app-name.onrender.com/api/v1/users/`
- **Health Check:** `https://your-app-name.onrender.com/health/`
- **Ping:** `https://your-app-name.onrender.com/ping/`

## Troubleshooting

If you encounter issues:
1. Check the Render logs in the dashboard
2. Verify environment variables are set correctly
3. Ensure the database URL is valid
4. Check that all dependencies are in requirements.txt
