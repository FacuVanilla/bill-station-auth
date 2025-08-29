# 🚂 Railway Deployment Troubleshooting Guide

## 🚨 Common Railway Deployment Issues

### Issue 1: "$PORT' is not a valid port number"

**Problem:** Railway can't resolve the `$PORT` environment variable.

**Solutions:**

#### Solution A: Use the Startup Script (Recommended)
1. **Railway will use the `railway_start.sh` script**
2. **The script properly handles the PORT variable**
3. **Redeploy your application**

#### Solution B: Manual Environment Variable
1. **In Railway dashboard, go to your service**
2. **Click on "Variables" tab**
3. **Add a new variable:**
   - **Name:** `PORT`
   - **Value:** `8000`
4. **Redeploy your service**

#### Solution C: Use Procfile Instead
1. **Railway can also use the `Procfile`**
2. **The Procfile is already updated for Railway compatibility**
3. **Redeploy your application**

### Issue 2: Database Connection Errors

**Problem:** Django can't connect to PostgreSQL.

**Solutions:**
1. **Ensure PostgreSQL service is added to your Railway project**
2. **Check that `DATABASE_URL` is automatically set by Railway**
3. **Verify the database service is running**

### Issue 3: Redis Connection Errors

**Problem:** Django can't connect to Redis.

**Solutions:**
1. **Ensure Redis service is added to your Railway project**
2. **Check that `REDIS_URL` is automatically set by Railway**
3. **Verify the Redis service is running**

## 🔧 Railway Deployment Steps

### Step 1: Create Railway Project
1. **Go to [Railway.app](https://railway.app)**
2. **Sign in with GitHub**
3. **Click "New Project"**

### Step 2: Deploy from GitHub
1. **Select "Deploy from GitHub repo"**
2. **Choose your `auth_service` repository**
3. **Railway will auto-detect Django**

### Step 3: Add PostgreSQL
1. **In your project dashboard, click "New"**
2. **Select "Database" → "PostgreSQL"**
3. **Railway will automatically set `DATABASE_URL`**

### Step 4: Add Redis
1. **Click "New" again**
2. **Select "Database" → "Redis"**
3. **Railway will automatically set `REDIS_URL`**

### Step 5: Set Environment Variables
1. **Go to your web service settings**
2. **Click "Variables" tab**
3. **Add these variables:**
   ```
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app.railway.app
   ```

### Step 6: Deploy
1. **Railway will automatically deploy**
2. **Check the deployment logs for any errors**
3. **Your app will be available at the provided URL**

## 🐛 Debugging Deployment Issues

### Check Railway Logs
1. **Go to your service in Railway dashboard**
2. **Click on "Deployments" tab**
3. **Click on the latest deployment**
4. **Check the logs for error messages**

### Common Error Messages and Fixes

#### "Module not found" errors
- **Fix:** Ensure all dependencies are in `requirements.txt`
- **Fix:** Check that the build process completed successfully

#### "Database connection failed"
- **Fix:** Verify PostgreSQL service is running
- **Fix:** Check `DATABASE_URL` environment variable

#### "Redis connection failed"
- **Fix:** Verify Redis service is running
- **Fix:** Check `REDIS_URL` environment variable

#### "Permission denied" errors
- **Fix:** The startup script handles permissions automatically
- **Fix:** Check that the script is executable

## 🔄 Redeployment Process

If you need to redeploy:

1. **Make changes to your code**
2. **Commit and push to GitHub**
3. **Railway will automatically redeploy**
4. **Monitor the deployment logs**
5. **Test your application**

## 📱 Testing Your Railway Deployment

### Health Check
- **Visit:** `https://your-app.railway.app/`
- **Expected:** Swagger UI documentation

### API Endpoints
- **Registration:** `POST /api/v1/users/register/`
- **Login:** `POST /api/v1/users/login/`
- **Documentation:** `/swagger/` and `/redoc/`

### Database Test
- **Create a test user through the API**
- **Verify the user appears in your PostgreSQL database**

### Redis Test
- **Request a password reset**
- **Verify the token is stored in Redis**

## 🆘 Getting Help

### Railway Support
- **Documentation:** [Railway Docs](https://docs.railway.app/)
- **Discord:** [Railway Discord](https://discord.gg/railway)
- **GitHub Issues:** [Railway GitHub](https://github.com/railwayapp/railway)

### Common Solutions
1. **Always check the deployment logs first**
2. **Verify all environment variables are set**
3. **Ensure database services are running**
4. **Check that the PORT variable is properly handled**

---

## 🎯 Quick Fix for PORT Issue

**Immediate Solution:**
1. **Add `PORT=8000` to your Railway environment variables**
2. **Redeploy your application**
3. **The startup script will handle the rest**

**Long-term Solution:**
- **Use the `railway_start.sh` script (already configured)**
- **Railway will automatically handle the PORT variable**

---

**🚀 Your Django app should deploy successfully on Railway!**
