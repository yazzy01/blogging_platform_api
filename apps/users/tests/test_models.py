from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..models import Profile, UserActivity

User = get_user_model()

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile

    def test_profile_creation(self):
        """Test profile is created automatically with user"""
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertEqual(str(self.profile), "testuser's profile")

    def test_profile_fields(self):
        """Test profile fields can be set"""
        self.profile.bio = "Test bio"
        self.profile.location = "Test location"
        self.profile.save()
        
        self.assertEqual(self.profile.bio, "Test bio")
        self.assertEqual(self.profile.location, "Test location")

    def test_failed_login_attempts(self):
        """Test failed login attempts tracking"""
        self.profile.record_failed_attempt()
        self.assertEqual(self.profile.failed_login_attempts, 1)

        # Test account locking after 5 attempts
        for _ in range(4):
            self.profile.record_failed_attempt()
        
        self.assertTrue(self.profile.account_locked_until is not None)
        self.assertEqual(self.profile.failed_login_attempts, 5)

    def test_successful_login(self):
        """Test successful login resets failed attempts"""
        self.profile.failed_login_attempts = 3
        self.profile.record_login('127.0.0.1')
        
        self.assertEqual(self.profile.failed_login_attempts, 0)
        self.assertEqual(self.profile.last_login_ip, '127.0.0.1')
        self.assertTrue(self.profile.last_login is not None)

class UserActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_activity_creation(self):
        """Test activity can be created"""
        activity = UserActivity.objects.create(
            user=self.user,
            activity_type='login',
            ip_address='127.0.0.1'
        )
        
        self.assertTrue(isinstance(activity, UserActivity))
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'login')
        self.assertEqual(activity.ip_address, '127.0.0.1')

    def test_activity_log_method(self):
        """Test activity logging helper method"""
        activity = UserActivity.log_activity(
            user=self.user,
            activity_type='post_create',
            metadata={'post_id': 1}
        )
        
        self.assertEqual(activity.activity_type, 'post_create')
        self.assertEqual(activity.metadata, {'post_id': 1})
