from rest_framework import serializers
from apps.posts.models import Post, Tag

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'tags']

class PostDetailSerializer(PostSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ['views_count', 'likes_count']
