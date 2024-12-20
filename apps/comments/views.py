from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Comment
from .serializers import CommentSerializer
from apps.core.permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').prefetch_related('replies')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'author', 'is_active']
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """Create a new comment"""
        serializer.save(author=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned comments to a given post,
        by filtering against a `post` query parameter in the URL.
        """
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset.filter(parent=None)  # Only return top-level comments

    @action(detail=True, methods=['POST'])
    def reply(self, request, pk=None):
        """Add a reply to a comment"""
        parent_comment = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                author=request.user,
                parent=parent_comment,
                post=parent_comment.post
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['GET'])
    def my_comments(self, request):
        """List authenticated user's comments"""
        queryset = self.get_queryset().filter(author=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
