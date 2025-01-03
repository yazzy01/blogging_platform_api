from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from django.conf import settings
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend
from ..models.activity import UserActivity

class SocialAuthRedirectView(APIView):
    """
    Redirect users to social auth provider
    """
    permission_classes = [AllowAny]

    def get(self, request, provider):
        """Get social auth URL and redirect"""
        strategy = load_strategy(request)
        try:
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
        except MissingBackend:
            return Response(
                {'error': f'Provider {provider} not supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get authorization URL
        auth_url = backend.auth_url()
        return redirect(auth_url)

class SocialAuthCallbackView(APIView):
    """
    Handle social auth callback
    """
    permission_classes = [AllowAny]

    def get(self, request, provider):
        """Handle social auth callback"""
        strategy = load_strategy(request)
        try:
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
        except MissingBackend:
            return Response(
                {'error': f'Provider {provider} not supported'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Complete social auth process
            user = backend.complete(request=request)
            
            # Log social login activity
            UserActivity.log_activity(
                user=user,
                activity_type='login',
                request=request,
                metadata={'provider': provider}
            )
            
            # Return success response with token
            return Response({
                'token': user.auth_token.key,
                'user_id': user.id,
                'email': user.email
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class SocialAuthErrorView(APIView):
    """
    Handle social auth errors
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """Handle social auth error"""
        error = request.GET.get('message', 'Unknown error')
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

class SocialAuthSuccessView(APIView):
    """
    Handle social auth success
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """Handle social auth success"""
        return Response({'message': 'Authentication successful'})
