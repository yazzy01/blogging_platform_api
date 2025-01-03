from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Tag, PostLike
from apps.users.serializers import UserProfileSerializer
from apps.categories.serializers import CategorySerializer

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    """
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'description', 'posts_count', 'created_at']
        read_only_fields = ['slug', 'posts_count']

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for basic post information.
    Used for list views and related posts.
    """
    author = UserProfileSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='post-detail',
        lookup_field='slug'
    )

    class Meta:
        model = Post
        fields = [
            'url', 'title', 'slug', 'author', 'categories', 'tags',
            'status', 'featured_image', 'views_count', 'likes_count',
            'is_liked', 'created_at', 'reading_time'
        ]
        read_only_fields = ['slug', 'views_count', 'likes_count']

    def get_is_liked(self, obj):
        """Check if the current user has liked the post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class PostDetailSerializer(PostSerializer):
    """
    Serializer for detailed post information.
    Used for retrieve, create and update operations.
    """
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        required=False,
        source='categories'
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        required=False,
        source='tags'
    )

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + [
            'content', 'meta_description', 'meta_keywords',
            'published_at', 'category_ids', 'tag_ids'
        ]
        read_only_fields = PostSerializer.Meta.read_only_fields + ['published_at']

    def validate(self, attrs):
        """
        Validate the post data.
        Ensure required fields are present when publishing.
        """
        if attrs.get('status') == 'published':
            required_fields = ['title', 'content', 'categories']
            missing_fields = [field for field in required_fields if not attrs.get(field)]
            if missing_fields:
                raise serializers.ValidationError({
                    'error': f"The following fields are required for publishing: {', '.join(missing_fields)}"
                })
            
            # Validate content length
            if len(attrs.get('content', '')) < 100:
                raise serializers.ValidationError({
                    'content': "Content must be at least 100 characters long for published posts."
                })
            
            # Validate meta description
            if not attrs.get('meta_description'):
                # Auto-generate meta description from content
                content = attrs.get('content', '')
                attrs['meta_description'] = content[:157] + '...' if len(content) > 160 else content
        
        return attrs

    def create(self, validated_data):
        """Create a new post with associated categories and tags."""
        categories = validated_data.pop('categories', [])
        tags = validated_data.pop('tags', [])
        
        post = Post.objects.create(**validated_data)
        
        if categories:
            post.categories.set(categories)
        if tags:
            post.tags.set(tags)
        
        return post

    def update(self, instance, validated_data):
        """Update a post with associated categories and tags."""
        categories = validated_data.pop('categories', None)
        tags = validated_data.pop('tags', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if categories is not None:
            instance.categories.set(categories)
        if tags is not None:
            instance.tags.set(tags)
        
        instance.save()
        return instance
