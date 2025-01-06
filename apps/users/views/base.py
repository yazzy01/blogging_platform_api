from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from ..models import Profile
from ..serializers import UserSerializer, UserProfileSerializer, ProfileSerializer
from ..tokens import account_activation_token
from ..emails import send_verification_email, send_password_reset_email, send_login_alert_email
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    View for user registration with email verification
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False  # Deactivate user until email is verified
        user.save()
        send_verification_email(self.request, user)

class ActivateAccountView(APIView):
    """
    View for activating user account via email verification
    """
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_verified = True
            user.save()
            return Response({'detail': 'Account activated successfully'})
        return Response({'error': 'Invalid activation link'}, 
                       status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetView(APIView):
    """
    View for requesting password reset email
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            send_password_reset_email(request, user)
            return Response({'detail': 'Password reset email sent'})
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, 
                          status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    """
    View for confirming password reset
    """
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            new_password = request.data.get('new_password')
            if new_password:
                user.set_password(new_password)
                user.save()
                return Response({'detail': 'Password reset successful'})
            return Response({'error': 'New password is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid reset link'}, 
                       status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        # Record IP address for security tracking
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        
        user = serializer.save()
        user.profile.record_login(ip)

class UserListView(generics.ListAPIView):
    """
    View for listing users (admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating and deleting user details (admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Regular users can only see their own profile
        if not self.request.user.is_staff:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Profile.objects.none()
        # Regular users can only see their own profile
        if not self.request.user.is_staff:
            return Profile.objects.filter(user=self.request.user)
        return Profile.objects.all()

    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
