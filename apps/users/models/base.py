from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

User = get_user_model()

class Profile(models.Model):
    """Extended user profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.URLField(max_length=500, blank=True, null=True)  # Made nullable
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    
    # Security fields
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    # Social links
    twitter = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)

    class Meta:
        app_label = 'users'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s profile"

    def lock_account(self, duration_minutes=30):
        """Lock account for specified duration"""
        self.account_locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save()

    def reset_failed_attempts(self):
        """Reset failed login attempts counter"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save()

    def record_failed_attempt(self):
        """Record a failed login attempt"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:  # Lock after 5 failed attempts
            self.lock_account()
        self.save()

    def record_login(self, ip_address):
        """Record successful login"""
        self.last_login_ip = ip_address
        self.last_login = timezone.now()
        self.reset_failed_attempts()
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create Profile when User is created"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save Profile when User is saved"""
    instance.profile.save()
