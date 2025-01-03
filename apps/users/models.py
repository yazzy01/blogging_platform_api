from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    website = models.URLField(max_length=200, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def lock_account(self, duration=30):
        """Lock account for specified minutes after too many failed attempts"""
        from django.utils import timezone
        self.account_locked_until = timezone.now() + timezone.timedelta(minutes=duration)
        self.save()

    def reset_failed_attempts(self):
        """Reset failed login attempts counter"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save()

    def record_login(self, ip_address):
        """Record successful login"""
        from django.utils import timezone
        self.last_login_ip = ip_address
        self.last_login_at = timezone.now()
        self.reset_failed_attempts()
        self.save()

    def record_failed_attempt(self):
        """Record failed login attempt and lock account if necessary"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:  # Lock after 5 failed attempts
            self.lock_account()
        self.save()

    def is_locked(self):
        """Check if account is currently locked"""
        from django.utils import timezone
        if self.account_locked_until and self.account_locked_until > timezone.now():
            return True
        return False

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
