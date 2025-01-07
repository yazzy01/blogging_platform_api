from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from apps.core.views import health_check
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

# Swagger documentation setup
schema_view = get_schema_view(
    openapi.Info(
        title="Blogging Platform API",
        default_version='v1',
        description="API for the Blogging Platform",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=f"https://blogging-platform-api-748v.onrender.com",
)

urlpatterns = [
    # Health Check - must be before other routes
    path('api/health/', health_check, name='health_check'),
    path('api/health', health_check),  # Also match without trailing slash

    # Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Admin
    path('admin/', admin.site.urls),

    # API routes
    path('api/posts/', include('apps.posts.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/users/', include('apps.users.urls')),
]

# Custom error handlers
handler404 = 'apps.core.views.custom_404'
handler500 = 'apps.core.views.custom_500'
