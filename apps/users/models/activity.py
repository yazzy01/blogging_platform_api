from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class UserActivity(models.Model):
    """Model for tracking user activities"""
    ACTIVITY_TYPES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('post_create', 'Created Post'),
        ('post_update', 'Updated Post'),
        ('post_delete', 'Deleted Post'),
        ('comment_create', 'Created Comment'),
        ('comment_update', 'Updated Comment'),
        ('comment_delete', 'Deleted Comment'),
        ('profile_update', 'Updated Profile'),
        ('like', 'Liked Content'),
        ('view', 'Viewed Content'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    
    # For linking activity to any model (post, comment, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['activity_type', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"

    @classmethod
    def log_activity(cls, user, activity_type, request=None, obj=None, metadata=None):
        """
        Log a user activity
        :param user: User performing the activity
        :param activity_type: Type of activity (from ACTIVITY_TYPES)
        :param request: HTTP request object (optional)
        :param obj: Related object (optional)
        :param metadata: Additional metadata (optional)
        """
        activity = cls(
            user=user,
            activity_type=activity_type,
            metadata=metadata or {}
        )
        
        if request:
            activity.ip_address = request.META.get('REMOTE_ADDR')
            activity.user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        
        if obj:
            activity.content_type = ContentType.objects.get_for_model(obj)
            activity.object_id = obj.pk
        
        activity.save()
        return activity
