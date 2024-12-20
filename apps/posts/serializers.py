from rest_framework import serializers
from .models import Post, Tag
from apps.users.serializers import UserSerializer
from apps.categories.models import Category
from django.utils.text import slugify

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

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value

    def validate_content(self, value):
        if len(value) < 20:
            raise serializers.ValidationError("Content must be at least 20 characters long")
        return value

    def validate(self, data):
        # Cross-field validation
        title = data.get('title', '')
        content = data.get('content', '')
        
        if title and content and title.lower() in content.lower():
            raise serializers.ValidationError({
                "title": "Title should not be contained within the content"
            })
        
        return data

    def generate_unique_slug(self, title):
        """
        Generate a unique slug from the given title
        """
        base_slug = slugify(title)
        unique_slug = base_slug
        n = 1
        
        # Keep checking until we find a unique slug
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{n}"
            n += 1
        
        return unique_slug

    def create(self, validated_data):
        # Separate tags and categories
        tags_data = validated_data.pop('tags', [])
        categories = validated_data.pop('categories', [])

        # Auto-generate slug if not provided
        if not validated_data.get('slug'):
            validated_data['slug'] = self.generate_unique_slug(validated_data['title'])

        # Create post
        post = Post.objects.create(**validated_data)

        # Set categories
        if categories:
            post.categories.set(categories)

        # Handle tags
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            post.tags.add(tag)

        return post

    def update(self, instance, validated_data):
        # Handle slug update if title changes
        if 'title' in validated_data and not validated_data.get('slug'):
            validated_data['slug'] = self.generate_unique_slug(validated_data['title'])

        # Handle tags and categories
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.clear()
            for tag_data in tags_data:
                tag, _ = Tag.objects.get_or_create(**tag_data)
                instance.tags.add(tag)

        if 'categories' in validated_data:
            categories = validated_data.pop('categories')
            instance.categories.set(categories)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
