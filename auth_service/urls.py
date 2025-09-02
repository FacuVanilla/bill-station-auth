"""
URL configuration for auth_service project.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect   # ✅ Needed for redirect
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

DEBUG = settings.DEBUG
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Health check view for Render
@csrf_exempt
def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django Auth Service is running',
    }, status=200)

# Simple ping endpoint
@csrf_exempt
def ping(request):
    return JsonResponse({'pong': True}, status=200)

# Debug endpoint
@csrf_exempt
def debug(request):
    return JsonResponse({
        'status': 'ok',
        'message': 'Django is working',
        'debug': DEBUG,
        'allowed_hosts': ALLOWED_HOSTS
    }, status=200)

# Swagger / ReDoc schema view
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
    # ✅ Root → redirect to ReDoc
    path('', lambda request: redirect('schema-redoc')),

    # Admin + API
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),

    # Health/debug endpoints
    path('health/', health_check, name='health_check'),
    path('ping/', ping, name='ping'),
    path('debug/', debug, name='debug'),

    # API docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
