"""
URL configuration for auth_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Health check view for Railway
@csrf_exempt
def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django Auth Service is running',
        'timestamp': '2025-01-29T00:00:00Z'
    }, status=200)

# Simple ping endpoint for healthchecks
@csrf_exempt
def ping(request):
    return JsonResponse({'pong': True}, status=200)

# Debug endpoint to test basic functionality
@csrf_exempt
def debug(request):
    return JsonResponse({
        'status': 'ok',
        'message': 'Django is working',
        'timestamp': '2025-01-29T00:00:00Z',
        'debug': DEBUG,
        'allowed_hosts': ALLOWED_HOSTS
    }, status=200)

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Django Auth Service API",
        default_version='v1',
        description="A comprehensive authentication service built with Django",
        terms_of_service="https://www.billstation.com/terms/",
        contact=openapi.Contact(email="contact@billstation.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('api/v1/', include('users.urls'))],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('health/', health_check, name='health_check'),
    path('ping/', ping, name='ping'),
    path('debug/', debug, name='debug'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
