# Auth Service - Django Authentication System

A robust Django-based authentication service built for Bill Station's Fintech platform, featuring JWT authentication, PostgreSQL database, Redis caching, and comprehensive user management.

## 🚀 Features

- **User Registration & Authentication**: Secure user registration with email verification
- **JWT Authentication**: Stateless authentication with access and refresh tokens
- **Password Reset**: Redis-backed password reset functionality with secure tokens
- **User Profile Management**: Complete user profile CRUD operations
- **Rate Limiting**: Built-in rate limiting for security
- **API Documentation**: Swagger/OpenAPI documentation
- **Docker Support**: Containerized development environment
- **PostgreSQL Integration**: Production-ready database setup
- **Redis Caching**: High-performance caching for password reset tokens

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7 + Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Cache**: Redis (Production) / Local Memory (Development)
- **Documentation**: Swagger/OpenAPI (drf-yasg)
- **Deployment**: Gunicorn + WhiteNoise
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL (for production)
- Redis (for production)
- Docker & Docker Compose (optional, for containerized development)

## 🚀 Quick Start

### Option 1: Local Development (with PostgreSQL & Redis)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd auth_service
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your PostgreSQL and Redis configuration
   ```

5. **Set up PostgreSQL and Redis**
   - Start PostgreSQL service
   - Start Redis service
   - Create database: `createdb auth_service_db`

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### Option 2: Docker Development

1. **Clone and navigate to project**
   ```bash
   git clone <repository-url>
   cd auth_service
   ```

2. **Start services with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Run migrations (in a new terminal)**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

The application will be available at `http://localhost:8000`

## 🔧 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=your-domain.railway.app,your-domain.onrender.com

# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://username:password@host:5432/database_name

# Redis Configuration
REDIS_URL=redis://username:password@host:6379/0

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1
```

## 📚 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/users/register/` | User registration | No |
| POST | `/api/v1/users/login/` | User login | No |
| POST | `/api/v1/users/logout/` | User logout | Yes |
| POST | `/api/v1/users/token/refresh/` | Refresh JWT token | No |

### Password Reset Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/users/password/reset/` | Request password reset | No |
| POST | `/api/v1/users/password/reset/confirm/` | Confirm password reset | No |

### User Profile Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/users/profile/` | Get user profile | Yes |
| PUT | `/api/v1/users/profile/` | Update user profile | Yes |

### Documentation Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/swagger/` | Swagger UI documentation |
| GET | `/redoc/` | ReDoc documentation |
| GET | `/` | API root (Swagger UI) |

## 🔐 API Usage Examples

### User Registration
```bash
curl -X POST http://localhost:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### User Login
```bash
curl -X POST http://localhost:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Password Reset Request
```bash
curl -X POST http://localhost:8000/api/v1/users/password/reset/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com"
  }'
```

### Password Reset Confirmation
```bash
curl -X POST http://localhost:8000/api/v1/users/password/reset/confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "reset_token_from_email",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
  }'
```

### Get User Profile (Authenticated)
```bash
curl -X GET http://localhost:8000/api/v1/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 🚀 Deployment

### Railway Deployment

1. **Connect your GitHub repository to Railway**
2. **Set environment variables in Railway dashboard:**
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `REDIS_URL`: Your Redis connection string
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: Set to `False` for production
   - `ALLOWED_HOSTS`: Your domain(s)

3. **Deploy automatically on git push**

### Render Deployment

1. **Connect your GitHub repository to Render**
2. **Create a new Web Service**
3. **Set environment variables:**
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `REDIS_URL`: Your Redis connection string
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: Set to `False` for production
   - `ALLOWED_HOSTS`: Your domain(s)

4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `gunicorn auth_service.wsgi:application`

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Validation**: Django's built-in password strength validation
- **Rate Limiting**: Prevents brute force attacks
- **CORS Protection**: Configurable cross-origin resource sharing
- **Secure Headers**: Security middleware enabled
- **Redis Token Storage**: Secure password reset token storage with expiration

## 📁 Project Structure

```
auth_service/
├── auth_service/          # Main project settings
├── users/                 # User management app
│   ├── migrations/        # Database migrations
│   ├── admin.py          # Admin interface
│   ├── apps.py           # App configuration
│   ├── models.py         # User model
│   ├── serializers.py    # API serializers
│   ├── urls.py           # App URL patterns
│   └── views.py          # API views
├── manage.py             # Django management script
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── railway.json          # Railway deployment
├── Procfile              # Render deployment
├── env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── setup_local.py        # Local setup script
├── start_dev.sh          # Development startup
├── README.md             # This file
├── DEPLOYMENT.md         # Deployment guide
└── PROJECT_SUMMARY.md    # Project summary
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the BSD License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Email: contact@billstation.com
- Create an issue in the GitHub repository

## 🔮 Future Enhancements

- [ ] Email verification for user registration
- [ ] Two-factor authentication (2FA)
- [ ] Social authentication (Google, Facebook, etc.)
- [ ] User roles and permissions
- [ ] Audit logging
- [ ] API versioning
- [ ] Webhook support
- [ ] Advanced rate limiting strategies

---

**Built with ❤️ for Bill Station's Fintech Platform**
