from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer
from django.utils.text import slugify

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def perform_create(self, serializer):
        # Auto-generate slug from title
        if not serializer.validated_data.get('slug'):
            title = serializer.validated_data.get('title', '')
            serializer.validated_data['slug'] = slugify(title)
        serializer.save(author=self.request.user)
