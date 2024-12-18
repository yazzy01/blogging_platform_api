from rest_framework import viewsets, permissions
from .models import Category
from .serializers import CategorySerializer
from django.utils.text import slugify

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if not serializer.validated_data.get('slug'):
            name = serializer.validated_data.get('name')
            serializer.validated_data['slug'] = slugify(name)
        serializer.save()
