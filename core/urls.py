from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from apps.core.views import health_check

# Swagger/OpenAPI schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Blog Platform API",
        default_version='v1',
        description="A modern blogging platform API with features including posts, categories, comments, and user management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@blogapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def redirect_to_swagger(request):
    return redirect('schema-swagger-ui')

urlpatterns = [
    # Root redirect to Swagger
    path('', redirect_to_swagger, name='api-root'),

    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API Endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/posts/', include('apps.posts.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/health/', health_check, name='health_check'),

    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), 
         name='schema-redoc'),
    
    # Optional: API Root View
    path('api/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom 404 and 500 handlers
handler404 = 'apps.core.views.custom_404'
handler500 = 'apps.core.views.custom_500'
