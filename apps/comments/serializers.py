from rest_framework import serializers
from .models import Comment

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    replies = RecursiveSerializer(many=True, read_only=True)
    moderated_by = serializers.ReadOnlyField(source='moderated_by.username')
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'content', 'created_at', 
            'updated_at', 'parent', 'replies', 'is_active',
            'status', 'moderated_by', 'moderated_at'
        ]
        read_only_fields = [
            'author', 'created_at', 'updated_at', 
            'status', 'moderated_by', 'moderated_at'
        ]

    def validate_parent(self, value):
        if value and value.parent:
            raise serializers.ValidationError("Nested replies are not allowed.")
        return value
