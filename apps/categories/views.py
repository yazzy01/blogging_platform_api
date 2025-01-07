from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.exceptions import ResourceNotFoundError
from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer
import logging

logger = logging.getLogger('apps')

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing blog categories.
    
    Provides CRUD operations and additional actions for category management.
    """
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order', 'created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action in ['retrieve', 'create', 'update', 'partial_update']:
            return CategoryDetailSerializer
        return CategorySerializer

    def get_queryset(self):
        """
        Get the list of categories.
        Optionally filter by parent or active status.
        """
        queryset = Category.objects.all()
        
        # Filter by parent
        parent_slug = self.request.query_params.get('parent', None)
        if parent_slug == 'root':
            queryset = queryset.filter(parent=None)
        elif parent_slug:
            try:
                parent = Category.objects.get(slug=parent_slug)
                queryset = queryset.filter(parent=parent)
            except Category.DoesNotExist:
                raise ResourceNotFoundError(f"Parent category '{parent_slug}' not found")

        # Filter by active status
        active = self.request.query_params.get('active', None)
        if active is not None:
            queryset = queryset.filter(is_active=active.lower() == 'true')

        return queryset

    def perform_create(self, serializer):
        """Create a new category."""
        category = serializer.save()
        logger.info(f"Created new category: {category.name}")

    def perform_update(self, serializer):
        """Update a category."""
        category = serializer.save()
        logger.info(f"Updated category: {category.name}")

    def perform_destroy(self, instance):
        """Delete a category after checking for posts."""
        if instance.posts.exists():
            logger.warning(f"Attempted to delete category '{instance.name}' with existing posts")
            raise ValidationError("Cannot delete category with existing posts")
        
        logger.info(f"Deleted category: {instance.name}")
        instance.delete()

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """Get hierarchical category tree."""
        categories = Category.get_category_tree()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get category statistics."""
        categories = Category.get_active_categories()
        total_categories = categories.count()
        total_posts = sum(category.total_posts for category in categories)
        
        data = {
            'total_categories': total_categories,
            'total_posts': total_posts,
            'categories': [{
                'name': category.name,
                'slug': category.slug,
                'posts_count': category.total_posts,
                'has_children': category.has_children
            } for category in categories]
        }
        
        return Response(data)
