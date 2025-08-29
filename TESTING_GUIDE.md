# 🧪 Testing Guide - Auth Service API

This guide shows you how to test the Django Authentication Service API using different methods.

## 🚀 **Quick Start - Server Status**

First, ensure your Django server is running:
```bash
# In your project directory
source venv/bin/activate
python manage.py runserver
```

The server will start at: `http://localhost:8000`

---

## 🌐 **Method 1: Swagger UI (Easiest)**

### **Step 1: Open Swagger Interface**
1. **Open your browser**
2. **Go to:** `http://localhost:8000/`
3. **You'll see the interactive Swagger documentation**

### **Step 2: Test Endpoints**
1. **Click on any endpoint** (e.g., "User Registration")
2. **Click "Try it out"**
3. **Fill in the required parameters**
4. **Click "Execute"**
5. **View the response**

### **Step 3: Test User Registration**
```json
{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123",
    "password_confirm": "testpass123"
}
```

### **Step 4: Test User Login**
```json
{
    "email": "test@example.com",
    "password": "testpass123"
}
```

---

## 📮 **Method 2: Postman (Professional)**

### **Step 1: Import Collection**
1. **Download the file:** `Auth_Service_API.postman_collection.json`
2. **Open Postman**
3. **Click "Import" → "Upload Files"**
4. **Select the downloaded collection file**

### **Step 2: Set Environment Variables**
In Postman, create a new environment with these variables:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `http://localhost:8000` | `http://localhost:8000` |
| `access_token` | `your_access_token_here` | (leave empty) |
| `refresh_token` | `your_refresh_token_here` | (leave empty) |
| `reset_token` | `your_reset_token_here` | (leave empty) |

### **Step 3: Test the API Flow**

#### **1. User Registration**
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/users/register/`
- **Body (raw JSON):**
```json
{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123",
    "password_confirm": "testpass123"
}
```

**Expected Response:**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "email": "test@example.com",
        "full_name": "Test User",
        "date_joined": "2024-01-01T00:00:00Z",
        "last_login": null
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### **2. User Login**
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/users/login/`
- **Body (raw JSON):**
```json
{
    "email": "test@example.com",
    "password": "testpass123"
}
```

**Expected Response:**
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "email": "test@example.com",
        "full_name": "Test User",
        "date_joined": "2024-01-01T00:00:00Z",
        "last_login": "2024-01-01T00:00:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

**⚠️ Important:** Copy the `access` and `refresh` tokens from the response!

#### **3. Update Environment Variables**
After login, update your Postman environment:
- **`access_token`:** Copy the access token from login response
- **`refresh_token`:** Copy the refresh token from login response

#### **4. Test Protected Endpoints**

**Get User Profile:**
- **Method:** GET
- **URL:** `{{base_url}}/api/v1/users/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Update User Profile:**
- **Method:** PUT
- **URL:** `{{base_url}}/api/v1/users/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
    "full_name": "Updated User Name"
}
```

#### **5. Test Password Reset**

**Request Password Reset:**
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/users/password/reset/`
- **Body (raw JSON):**
```json
{
    "email": "test@example.com"
}
```

**Copy the reset token** from the response and update `reset_token` variable.

**Confirm Password Reset:**
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/users/password/reset/confirm/`
- **Body (raw JSON):**
```json
{
    "token": "{{reset_token}}",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
}
```

#### **6. Test Token Refresh**
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/users/token/refresh/`
- **Body (raw JSON):**
```json
{
    "refresh": "{{refresh_token}}"
}
```

#### **7. Test Logout**
- **Method:** POST
- **URL:** `{{base_url}}/api/v1/users/logout/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
    "refresh": "{{refresh_token}}"
}
```

---

## 💻 **Method 3: cURL Commands (Command Line)**

### **1. User Registration**
```bash
curl -X POST http://localhost:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

### **2. User Login**
```bash
curl -X POST http://localhost:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### **3. Get User Profile (with token)**
```bash
# Replace YOUR_ACCESS_TOKEN with the actual token from login
curl -X GET http://localhost:8000/api/v1/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### **4. Update User Profile**
```bash
curl -X PUT http://localhost:8000/api/v1/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated User Name"
  }'
```

### **5. Request Password Reset**
```bash
curl -X POST http://localhost:8000/api/v1/users/password/reset/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com"
  }'
```

### **6. Confirm Password Reset**
```bash
# Replace YOUR_RESET_TOKEN with the actual token from reset request
curl -X POST http://localhost:8000/api/v1/users/password/reset/confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_RESET_TOKEN",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
  }'
```

---

## 🔍 **Testing Checklist**

### **✅ Basic Functionality**
- [ ] User registration works
- [ ] User login returns JWT tokens
- [ ] Protected endpoints require authentication
- [ ] User profile can be retrieved and updated

### **✅ Authentication Flow**
- [ ] JWT tokens are valid
- [ ] Token refresh works
- [ ] Logout blacklists tokens
- [ ] Invalid tokens are rejected

### **✅ Password Reset**
- [ ] Reset request generates token
- [ ] Token expires after 10 minutes
- [ ] Password can be changed with valid token
- [ ] Invalid tokens are rejected

### **✅ Error Handling**
- [ ] Invalid credentials return proper errors
- [ ] Missing fields return validation errors
- [ ] Unauthorized access returns 401
- [ ] Rate limiting works (try multiple requests quickly)

---

## 🚨 **Common Testing Scenarios**

### **1. Test Rate Limiting**
```bash
# Make multiple requests quickly to see rate limiting in action
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/v1/users/login/ \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "wrongpass"}'
  echo "Request $i"
done
```

### **2. Test Token Expiration**
1. **Login and get tokens**
2. **Wait for access token to expire** (5 minutes by default)
3. **Try to access protected endpoint**
4. **Should get 401 Unauthorized**

### **3. Test Password Validation**
```bash
# Test weak password
curl -X POST http://localhost:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "123",
    "password_confirm": "123"
  }'
```

### **4. Test Email Validation**
```bash
# Test invalid email format
curl -X POST http://localhost:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "invalid-email",
    "full_name": "Test User",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

---

## 🎯 **Testing Tips**

### **1. Use Environment Variables**
- **Postman:** Set up environment variables for tokens
- **Swagger:** Copy tokens manually between requests
- **cURL:** Use shell variables for tokens

### **2. Test Error Cases**
- **Invalid credentials**
- **Missing required fields**
- **Invalid data formats**
- **Expired tokens**
- **Unauthorized access**

### **3. Monitor Server Logs**
```bash
# Watch Django server logs for debugging
python manage.py runserver --verbosity 2
```

### **4. Check Database**
```bash
# Access Django shell to check data
python manage.py shell
>>> from users.models import User
>>> User.objects.all()
>>> exit()
```

---

## 🔧 **Troubleshooting**

### **Issue: Server not starting**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

### **Issue: Database connection failed**
```bash
# Check PostgreSQL status
brew services list | grep postgresql

# Start PostgreSQL if needed
brew services start postgresql
```

### **Issue: Redis connection failed**
```bash
# Check Redis status
brew services list | grep redis

# Start Redis if needed
brew services start redis
```

### **Issue: Migration errors**
```bash
# Reset migrations if needed
python manage.py migrate --fake users zero
python manage.py makemigrations
python manage.py migrate
```

---

## 🎉 **Success Indicators**

You'll know everything is working when:

✅ **Registration:** Returns user data + JWT tokens  
✅ **Login:** Returns user data + JWT tokens  
✅ **Profile Access:** Works with valid JWT token  
✅ **Password Reset:** Generates and accepts reset tokens  
✅ **Rate Limiting:** Blocks excessive requests  
✅ **Error Handling:** Returns proper HTTP status codes  

---

**Happy Testing! 🚀**

Your API is now ready for comprehensive testing and development!
