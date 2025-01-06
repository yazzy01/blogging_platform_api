from django.contrib import admin
from django.urls import path, include
from apps.core.views import health_check

urlpatterns = [
    # Health Check - must be before other routes
    path('api/health/', health_check, name='health_check'),

    # Admin
    path('admin/', admin.site.urls),

    # API Endpoints
    path('api/', include('apps.blog.urls')),
]
