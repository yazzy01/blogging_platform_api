from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from core.exceptions import ResourceNotFoundError, PermissionDeniedError
from .models import Post, Tag, PostLike
from .serializers import PostSerializer, PostDetailSerializer, TagSerializer
import logging

logger = logging.getLogger('apps')

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing blog posts.
    
    Provides CRUD operations and additional actions for post management.
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'categories', 'tags']
    search_fields = ['title', 'content', 'meta_keywords']
    ordering_fields = ['created_at', 'updated_at', 'views_count', 'likes_count']
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return PostDetailSerializer
        return PostSerializer

    def get_queryset(self):
        """
        Get the list of posts based on user's authentication status.
        Authenticated users can see their own drafts.
        """
        queryset = Post.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        elif not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        return queryset

    def perform_create(self, serializer):
        """Create a new post with the current user as author."""
        serializer.save(author=self.request.user)
        logger.info(f"User {self.request.user.username} created post: {serializer.instance.title}")

    def perform_update(self, serializer):
        """Update post and handle status changes."""
        instance = self.get_object()
        if instance.author != self.request.user and not self.request.user.is_staff:
            logger.warning(f"User {self.request.user.username} attempted to update post: {instance.title}")
            raise PermissionDeniedError("You can only edit your own posts.")
        
        # Handle publication status change
        if instance.status != 'published' and serializer.validated_data.get('status') == 'published':
            serializer.validated_data['published_at'] = timezone.now()
        
        serializer.save()
        logger.info(f"User {self.request.user.username} updated post: {instance.title}")

    def perform_destroy(self, instance):
        """Delete post after permission check."""
        if instance.author != self.request.user and not self.request.user.is_staff:
            logger.warning(f"User {self.request.user.username} attempted to delete post: {instance.title}")
            raise PermissionDeniedError("You can only delete your own posts.")
        
        logger.info(f"User {self.request.user.username} deleted post: {instance.title}")
        instance.delete()

    @action(detail=True, methods=['post'])
    def toggle_like(self, request, slug=None):
        """Toggle like status for the current user."""
        post = self.get_object()
        action = post.toggle_like(request.user)
        return Response({'status': f'Post {action}', 'likes_count': post.likes_count})

    @action(detail=True, methods=['get'])
    def related_posts(self, request, slug=None):
        """Get posts related to the current post based on categories and tags."""
        post = self.get_object()
        related_posts = Post.objects.filter(
            Q(categories__in=post.categories.all()) | Q(tags__in=post.tags.all())
        ).exclude(id=post.id).distinct()[:5]
        
        serializer = PostSerializer(related_posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def view(self, request, slug=None):
        """Record a view for the post."""
        post = self.get_object()
        post.increment_views()
        return Response({'status': 'view recorded', 'views_count': post.views_count})

class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing post tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        """Get tags with optional filtering."""
        queryset = Tag.objects.all()
        if self.action == 'list':
            # Optionally filter by usage count
            min_posts = self.request.query_params.get('min_posts', None)
            if min_posts and min_posts.isdigit():
                queryset = queryset.filter(posts_count__gte=int(min_posts))
        return queryset
