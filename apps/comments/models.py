from django.db import models
from django.contrib.auth import get_user_model
from apps.posts.models import Post
import logging

logger = logging.getLogger('apps')

User = get_user_model()

class Comment(models.Model):
    """
    Model representing a comment on a blog post.
    Supports nested comments (replies).
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['parent', '-created_at']),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def save(self, *args, **kwargs):
        # Log comment creation/update
        is_new = not self.pk
        if is_new:
            logger.info(f"User {self.author.username} created comment on post: {self.post.title}")
        else:
            logger.info(f"User {self.author.username} updated comment on post: {self.post.title}")
        
        super().save(*args, **kwargs)

    @property
    def is_reply(self):
        """Check if this comment is a reply to another comment."""
        return self.parent is not None

    @property
    def reply_count(self):
        """Get the number of replies to this comment."""
        return self.replies.count()

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
        logger.info(f"User {user.username} {action} comment on post: {self.post.title}")
        return action

class CommentLike(models.Model):
    """
    Model representing a like on a comment.
    """
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes comment on {self.comment.post.title}"
