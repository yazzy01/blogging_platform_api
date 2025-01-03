from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Profile, UserActivity

User = get_user_model()

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        """Test user registration"""
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_profile_view(self):
        """Test user profile retrieval"""
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_profile_update(self):
        """Test user profile update"""
        url = reverse('user-profile')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'profile': {
                'bio': 'Test bio',
                'location': 'Test location'
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['profile']['bio'], 'Test bio')

class UserActivityViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_activity_list(self):
        """Test activity list retrieval"""
        UserActivity.objects.create(
            user=self.user,
            activity_type='login',
            ip_address='127.0.0.1'
        )
        url = reverse('user-activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_activity_stats(self):
        """Test activity statistics"""
        for _ in range(3):
            UserActivity.objects.create(
                user=self.user,
                activity_type='login',
                ip_address='127.0.0.1'
            )
        
        url = reverse('user-activity-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('activity_counts' in response.data)
        self.assertTrue('recent_activities' in response.data)
