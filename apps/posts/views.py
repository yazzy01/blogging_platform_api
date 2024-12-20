from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostSerializer
from django.utils.text import slugify
from apps.core.permissions import IsAuthorOrReadOnly
from django.db.models import Prefetch
from django.core.cache import cache
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.utils import timezone

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories', 'author', 'status']
    search_fields = ['title', 'content', 'tags__name', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        """
        queryset = Post.objects.select_related(
            'author'  # Optimize author foreign key
        ).prefetch_related(
            'categories',  # Optimize categories many-to-many
            'tags'  # Optimize tags many-to-many
        )

        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(categories__name=category)

        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            try:
                # Parse dates in YYYY-MM-DD format
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                # Make them timezone aware
                start = timezone.make_aware(start)
                end = timezone.make_aware(end)
                queryset = queryset.filter(created_at__date__range=[start_date, end_date])
            except ValueError:
                pass

        # Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__name=tag)

        return queryset.distinct()

    def perform_create(self, serializer):
        """
        Handle post creation with automatic slug generation
        """
        if not serializer.validated_data.get('slug'):
            title = serializer.validated_data.get('title', '')
            base_slug = slugify(title)
            unique_slug = base_slug
            n = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{n}"
                n += 1
            serializer.validated_data['slug'] = unique_slug
        serializer.save(author=self.request.user)

    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        """
        Cached list view
        """
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        """
        Cached detail view
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Handle post updates
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Check if title is being updated
        if 'title' in request.data and not request.data.get('slug'):
            new_title = request.data['title']
            base_slug = slugify(new_title)
            unique_slug = base_slug
            n = 1
            while Post.objects.filter(slug=unique_slug).exclude(id=instance.id).exists():
                unique_slug = f"{base_slug}-{n}"
                n += 1
            request.data['slug'] = unique_slug

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Handle post deletion
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Post deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
