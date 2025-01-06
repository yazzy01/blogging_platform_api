from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from apps.core.views import health_check
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger documentation setup
schema_view = get_schema_view(
    openapi.Info(
        title="Blogging Platform API",
        default_version='v1',
        description="API for the Blogging Platform",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Health Check - must be before other routes
    path('health/', health_check, name='health_check'),
    path('api/health/', health_check, name='health_check_alt'),

    # Documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Admin
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('apps.blog.urls')),
]

# Custom error handlers
handler404 = 'apps.core.views.custom_404'
handler500 = 'apps.core.views.custom_500'
