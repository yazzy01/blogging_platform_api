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
    # Documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Health Check - must be before other routes
    path('api/health/', health_check, name='health_check'),
    path('health/', health_check, name='health_check_alt'),  # Alternative health check URL

    # Admin
    path('admin/', admin.site.urls),

    # API Endpoints
    path('api/', include([
        path('posts/', include('apps.posts.urls')),
        path('users/', include('apps.users.urls')),
        path('categories/', include('apps.categories.urls')),
        path('comments/', include('apps.comments.urls')),
    ])),
]
