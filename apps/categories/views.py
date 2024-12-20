from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Category
from .serializers import CategorySerializer
from apps.core.permissions import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'parent']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order', 'created_at']
    ordering = ['order', 'name']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Category.objects.annotate(
            post_count=Count('posts', filter=models.Q(posts__status='published'))
        )
        if self.action == 'list':
            # Only return top-level categories for list action
            queryset = queryset.filter(parent=None)
        return queryset

    @action(detail=True)
    def subcategories(self, request, slug=None):
        """Get all subcategories of a category"""
        category = self.get_object()
        subcategories = Category.objects.filter(parent=category)
        serializer = self.get_serializer(subcategories, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def posts(self, request, slug=None):
        """Get all posts in a category"""
        category = self.get_object()
        posts = category.posts.filter(status='published')
        from apps.posts.serializers import PostSerializer
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
