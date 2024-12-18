from rest_framework import serializers
from .models import Category
from django.utils.text import slugify

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']
        read_only_fields = ['slug']  # Make slug read-only as we'll generate it

    def create(self, validated_data):
        # Auto-generate slug from name
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)
