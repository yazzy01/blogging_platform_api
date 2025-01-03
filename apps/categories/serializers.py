from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for basic category information.
    Used for list views and nested representations.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='category-detail',
        lookup_field='slug'
    )
    posts_count = serializers.IntegerField(read_only=True)
    has_children = serializers.BooleanField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'url', 'name', 'slug', 'description', 'icon', 'color',
            'is_active', 'order', 'posts_count', 'has_children'
        ]
        read_only_fields = ['slug']

class CategoryDetailSerializer(CategorySerializer):
    """
    Serializer for detailed category information.
    Used for retrieve, create and update operations.
    """
    parent = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    children = CategorySerializer(many=True, read_only=True)
    breadcrumbs = serializers.SerializerMethodField()

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + [
            'parent', 'children', 'breadcrumbs',
            'created_at', 'updated_at'
        ]

    def get_breadcrumbs(self, obj):
        """Get category breadcrumbs."""
        breadcrumbs = []
        current = obj
        while current is not None:
            breadcrumbs.append({
                'name': current.name,
                'slug': current.slug
            })
            current = current.parent
        return list(reversed(breadcrumbs))

    def validate(self, attrs):
        """
        Validate the category data.
        Ensure proper parent-child relationships.
        """
        parent = attrs.get('parent')
        if parent:
            # Check for circular reference
            if self.instance and parent.pk == self.instance.pk:
                raise serializers.ValidationError({
                    'parent': "A category cannot be its own parent."
                })
            
            # Check for deep nesting
            if parent.parent:
                raise serializers.ValidationError({
                    'parent': "Categories can only be nested one level deep."
                })
            
            # Check for existing children when setting as child
            if self.instance and self.instance.children.exists():
                raise serializers.ValidationError({
                    'parent': "Cannot set a category with children as a child category."
                })
        
        return attrs
