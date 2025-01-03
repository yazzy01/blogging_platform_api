from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for basic user information in comments."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['email']

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for basic comment information.
    Used for list views and nested representations.
    """
    author = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    reply_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'content', 'created_at',
            'likes_count', 'is_liked', 'reply_count',
            'is_edited', 'is_approved'
        ]
        read_only_fields = [
            'author', 'created_at', 'likes_count',
            'is_edited', 'is_approved'
        ]

    def get_is_liked(self, obj):
        """Check if the current user has liked this comment."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for detailed comment information.
    Used for retrieve, create and update operations.
    """
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        required=False,
        allow_null=True
    )
    replies = CommentSerializer(many=True, read_only=True)

    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + [
            'parent', 'replies', 'updated_at'
        ]

    def validate_parent(self, value):
        """
        Validate the parent comment.
        Ensure it belongs to the same post and is not a reply itself.
        """
        if value:
            # Ensure parent belongs to the same post
            post_id = self.context['view'].kwargs.get('post_pk')
            if value.post_id != int(post_id):
                raise serializers.ValidationError(
                    "Parent comment must belong to the same post."
                )
            
            # Prevent deep nesting
            if value.parent:
                raise serializers.ValidationError(
                    "Cannot reply to a reply. Only one level of nesting is allowed."
                )
        
        return value

    def validate_content(self, value):
        """Validate comment content."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Comment content must be at least 3 characters long."
            )
        return value.strip()
