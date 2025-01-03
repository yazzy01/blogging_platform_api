from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView,
    UserProfileView,
    UserListView,
    UserDetailView,
    UserViewSet,
    ProfileViewSet,
    ActivateAccountView,
    RequestPasswordResetView,
    PasswordResetConfirmView
)
from .views.activity import UserActivityViewSet
from .views.auth import (
    SocialAuthRedirectView,
    SocialAuthCallbackView,
    SocialAuthErrorView,
    SocialAuthSuccessView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'activities', UserActivityViewSet, basename='user-activity')

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
    path('password/reset/', RequestPasswordResetView.as_view(), name='password-reset'),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', 
         PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Social Authentication
    path('social/login/<str:provider>/', SocialAuthRedirectView.as_view(), name='social-login'),
    path('social/callback/<str:provider>/', SocialAuthCallbackView.as_view(), name='social-callback'),
    path('social/error/', SocialAuthErrorView.as_view(), name='social-error'),
    path('social/success/', SocialAuthSuccessView.as_view(), name='social-success'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    
    # Profile Management
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # ViewSet URLs
    path('', include(router.urls)),
]
