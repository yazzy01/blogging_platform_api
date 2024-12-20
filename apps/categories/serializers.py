from rest_framework import serializers
from .models import Category

class RecursiveCategorySerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = CategorySerializer(value, context=self.context)
        return serializer.data

class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveCategorySerializer(many=True, read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'parent',
            'children', 'created_at', 'updated_at', 
            'is_active', 'order', 'post_count'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def validate_parent(self, value):
        if value and value.parent:
            raise serializers.ValidationError(
                "Categories can only be nested one level deep."
            )
        return value
