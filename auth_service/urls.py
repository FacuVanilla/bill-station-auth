from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('schema-redoc')),   # ✅ Root → ReDoc
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('health/', health_check, name='health_check'),
    path('ping/', ping, name='ping'),
    path('debug/', debug, name='debug'),

    # Only keep ReDoc (Swagger optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Optional: still allow raw schema (JSON/YAML)
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
