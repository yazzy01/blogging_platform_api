from rest_framework import viewsets, permissions
from apps.posts.models import Tag
from apps.posts.serializers import TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
