# Deployment Guide - Auth Service

This guide provides step-by-step instructions for deploying the Auth Service to Railway and Render platforms.

## 🚀 Railway Deployment

### Prerequisites
- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))

### Step 1: Prepare Your Repository
1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Django Auth Service"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

### Step 2: Deploy on Railway
1. **Visit [Railway Dashboard](https://railway.app/dashboard)**
2. **Click "New Project" → "Deploy from GitHub repo"**
3. **Select your repository**
4. **Wait for the build to complete**

### Step 3: Configure Environment Variables
In your Railway project dashboard, go to the "Variables" tab and add:

```env
DATABASE_URL=postgresql://username:password@host:port/database
REDIS_URL=redis://username:password@host:port
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.railway.app
```

### Step 4: Add PostgreSQL Database
1. **In Railway dashboard, click "New" → "Database" → "PostgreSQL"**
2. **Copy the DATABASE_URL from the database service**
3. **Update your DATABASE_URL environment variable**

### Step 5: Add Redis Service
1. **In Railway dashboard, click "New" → "Database" → "Redis"**
2. **Copy the REDIS_URL from the Redis service**
3. **Update your REDIS_URL environment variable**

### Step 6: Deploy
1. **Railway will automatically redeploy when you push changes**
2. **Your app will be available at: `https://your-app-name.railway.app`**

---

## 🌐 Render Deployment

### Prerequisites
- GitHub account
- Render account (sign up at [render.com](https://render.com))

### Step 1: Prepare Your Repository
1. **Push your code to GitHub** (same as Railway step 1)

### Step 2: Deploy on Render
1. **Visit [Render Dashboard](https://dashboard.render.com)**
2. **Click "New" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**

   **Name**: `auth-service` (or your preferred name)
   
   **Environment**: `Python 3`
   
   **Build Command**: `pip install -r requirements.txt`
   
   **Start Command**: `gunicorn auth_service.wsgi:application`

### Step 3: Configure Environment Variables
In your Render service settings, add these environment variables:

```env
DATABASE_URL=postgresql://username:password@host:port/database
REDIS_URL=redis://username:password@host:port
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com
```

### Step 4: Add PostgreSQL Database
1. **In Render dashboard, click "New" → "PostgreSQL"**
2. **Choose your plan and region**
3. **Copy the DATABASE_URL from the database service**
4. **Update your DATABASE_URL environment variable**

### Step 5: Add Redis Service
1. **In Render dashboard, click "New" → "Redis"**
2. **Choose your plan and region**
3. **Copy the REDIS_URL from the Redis service**
4. **Update your REDIS_URL environment variable**

### Step 6: Deploy
1. **Click "Create Web Service"**
2. **Render will build and deploy your application**
3. **Your app will be available at: `https://your-service-name.onrender.com`**

---

## 🔧 Environment Variables Reference

### Required Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Redis connection string | `redis://host:6379/0` |
| `SECRET_KEY` | Django secret key | `your-super-secret-key-here` |

### Optional Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `False` (production) |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |
| `JWT_ACCESS_TOKEN_LIFETIME` | JWT access token lifetime (minutes) | `5` |
| `JWT_REFRESH_TOKEN_LIFETIME` | JWT refresh token lifetime (days) | `1` |

---

## 🧪 Testing Your Deployment

### 1. Health Check
Visit your deployed URL to see the Swagger documentation:
```
https://your-app.railway.app/
https://your-service.onrender.com/
```

### 2. API Endpoints Test
Test the registration endpoint:
```bash
curl -X POST https://your-app.railway.app/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

### 3. Admin Interface
Visit `/admin/` to access the Django admin interface:
```
https://your-app.railway.app/admin/
```

---

## 🚨 Common Issues & Solutions

### Issue: Database Connection Failed
**Solution**: 
- Check your `DATABASE_URL` format
- Ensure the database service is running
- Verify network access between services

### Issue: Redis Connection Failed
**Solution**:
- Check your `REDIS_URL` format
- Ensure the Redis service is running
- Verify network access between services

### Issue: Static Files Not Loading
**Solution**:
- Ensure `DEBUG=False` in production
- Check that `STATIC_ROOT` is properly configured
- Verify WhiteNoise is working correctly

### Issue: JWT Tokens Not Working
**Solution**:
- Check your `SECRET_KEY` is set
- Verify JWT settings in `settings.py`
- Ensure token expiration times are reasonable

---

## 📊 Monitoring & Maintenance

### Railway
- **Logs**: Available in the service dashboard
- **Metrics**: Built-in monitoring and alerts
- **Scaling**: Automatic scaling based on traffic

### Render
- **Logs**: Available in the service dashboard
- **Metrics**: Basic monitoring included
- **Scaling**: Manual scaling configuration

---

## 🔄 Continuous Deployment

Both platforms support automatic deployments:

1. **Push changes to your main branch**
2. **Platform automatically detects changes**
3. **Builds and deploys new version**
4. **Zero-downtime deployment**

---

## 💰 Cost Considerations

### Railway
- **Free Tier**: $5/month credit
- **PostgreSQL**: $5/month
- **Redis**: $5/month
- **Web Service**: $5/month

### Render
- **Free Tier**: Limited (sleeps after inactivity)
- **PostgreSQL**: $7/month
- **Redis**: $7/month
- **Web Service**: $7/month

---

## 🎯 Next Steps

After successful deployment:

1. **Set up custom domain** (optional)
2. **Configure SSL certificates** (automatic on both platforms)
3. **Set up monitoring and alerts**
4. **Implement CI/CD pipeline**
5. **Add production logging**
6. **Set up backup strategies**

---

## 📞 Support

- **Railway**: [Discord Community](https://discord.gg/railway)
- **Render**: [Documentation](https://render.com/docs)
- **Project Issues**: Create an issue in the GitHub repository

---

**Happy Deploying! 🚀**
