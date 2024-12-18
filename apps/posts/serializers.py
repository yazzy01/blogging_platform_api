from rest_framework import serializers
from .models import Post, Tag
from apps.users.serializers import UserSerializer
from apps.categories.models import Category

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    slug = serializers.SlugField(required=False)
    categories = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'author', 'featured_image',
                 'excerpt', 'categories', 'tags', 'status', 'view_count',
                 'created_at', 'updated_at', 'published_at']
        read_only_fields = ['author', 'view_count', 'created_at', 'updated_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        categories = validated_data.pop('categories', [])

        # Auto-generate slug if not provided
        if not validated_data.get('slug'):
            from django.utils.text import slugify
            validated_data['slug'] = slugify(validated_data['title'])

        post = Post.objects.create(**validated_data)
        
        # Set categories
        if categories:
            post.categories.set(categories)
        
        # Handle tags if needed
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            post.tags.add(tag)
        
        return post
