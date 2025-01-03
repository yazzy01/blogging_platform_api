from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.exceptions import PermissionDeniedError
from apps.posts.models import Post
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer
import logging

logger = logging.getLogger('apps')

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing blog comments.
    
    Provides CRUD operations and additional actions for comment management.
    """
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Get the list of comments.
        Filter by post and optionally by parent for replies.
        """
        post_id = self.kwargs.get('post_pk')
        queryset = Comment.objects.filter(post_id=post_id, is_approved=True)

        # Filter by parent for replies
        parent_id = self.request.query_params.get('parent', None)
        if parent_id is not None:
            if parent_id == '':
                queryset = queryset.filter(parent=None)
            else:
                queryset = queryset.filter(parent_id=parent_id)

        return queryset.select_related('author', 'parent')

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return CommentDetailSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        """Create a new comment."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        comment = serializer.save(author=self.request.user, post=post)
        logger.info(f"User {self.request.user.username} created comment on post: {post.title}")

    def perform_update(self, serializer):
        """Update a comment."""
        instance = self.get_object()
        if instance.author != self.request.user and not self.request.user.is_staff:
            logger.warning(f"User {self.request.user.username} attempted to update comment on post: {instance.post.title}")
            raise PermissionDeniedError("You can only edit your own comments.")
        
        serializer.save(is_edited=True)
        logger.info(f"User {self.request.user.username} updated comment on post: {instance.post.title}")

    def perform_destroy(self, instance):
        """Delete a comment."""
        if instance.author != self.request.user and not self.request.user.is_staff:
            logger.warning(f"User {self.request.user.username} attempted to delete comment on post: {instance.post.title}")
            raise PermissionDeniedError("You can only delete your own comments.")
        
        logger.info(f"User {self.request.user.username} deleted comment on post: {instance.post.title}")
        instance.delete()

    @action(detail=True, methods=['post'])
    def toggle_like(self, request, post_pk=None, pk=None):
        """Toggle like status for the current user."""
        comment = self.get_object()
        action = comment.toggle_like(request.user)
        return Response({
            'status': f'Comment {action}',
            'likes_count': comment.likes_count
        })

    @action(detail=True, methods=['get'])
    def replies(self, request, post_pk=None, pk=None):
        """Get replies to this comment."""
        comment = self.get_object()
        replies = comment.replies.filter(is_approved=True)
        serializer = CommentSerializer(replies, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_comments(self, request, post_pk=None):
        """Get all comments by the current user on this post."""
        comments = Comment.objects.filter(
            post_id=post_pk,
            author=request.user
        ).select_related('author', 'parent')
        
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
