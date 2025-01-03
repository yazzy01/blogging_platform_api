from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from social_django.models import UserSocialAuth
from unittest.mock import patch

User = get_user_model()

class SocialAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('social_core.backends.google.GoogleOAuth2.auth_url')
    def test_google_login_redirect(self, mock_auth_url):
        """Test Google login redirect"""
        mock_auth_url.return_value = 'http://google.com/auth'
        url = reverse('social-login', kwargs={'provider': 'google-oauth2'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    @patch('social_core.backends.github.GithubOAuth2.auth_url')
    def test_github_login_redirect(self, mock_auth_url):
        """Test GitHub login redirect"""
        mock_auth_url.return_value = 'http://github.com/auth'
        url = reverse('social-login', kwargs={'provider': 'github'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_invalid_provider(self):
        """Test invalid provider handling"""
        url = reverse('social-login', kwargs={'provider': 'invalid'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class EmailVerificationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_active=False
        )

    def test_account_activation(self):
        """Test account activation"""
        # This is a basic test. In reality, you'd need to generate proper token and uidb64
        url = reverse('activate', kwargs={
            'uidb64': 'fake-uid',
            'token': 'fake-token'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_request(self):
        """Test password reset request"""
        url = reverse('password-reset')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_password_reset_request(self):
        """Test invalid password reset request"""
        url = reverse('password-reset')
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
