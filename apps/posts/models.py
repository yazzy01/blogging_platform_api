from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from apps.categories.models import Category
import logging

logger = logging.getLogger('apps')

User = get_user_model()

class Tag(models.Model):
    """
    Model representing a post tag.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def posts_count(self):
        """Get the number of posts using this tag."""
        return self.posts.count()


class Post(models.Model):
    """
    Model representing a blog post.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    featured_image = models.ImageField(upload_to='posts/', null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Log post creation/update
        is_new = not self.pk
        if is_new:
            logger.info(f"Creating new post: {self.title}")
        else:
            logger.info(f"Updating post: {self.title}")
            
        super().save(*args, **kwargs)

    def increment_views(self):
        """Increment the view count for this post."""
        self.views_count += 1
        self.save(update_fields=['views_count'])
        logger.info(f"Incremented views for post: {self.title}")

    def toggle_like(self, user):
        """Toggle like status for a user."""
        if self.likes.filter(user=user).exists():
            self.likes.filter(user=user).delete()
            self.likes_count -= 1
            action = "unliked"
        else:
            self.likes.create(user=user)
            self.likes_count += 1
            action = "liked"
        
        self.save(update_fields=['likes_count'])
        logger.info(f"User {user.username} {action} post: {self.title}")
        return action

    @property
    def reading_time(self):
        """Calculate estimated reading time in minutes."""
        words_per_minute = 200
        word_count = len(self.content.split())
        return max(1, round(word_count / words_per_minute))


class PostLike(models.Model):
    """
    Model representing a post like.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
