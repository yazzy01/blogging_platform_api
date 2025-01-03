from django_filters import rest_framework as filters
from .models import Post

class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    content = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(field_name='author__username')
    category = filters.CharFilter(field_name='category__slug')
    tag = filters.CharFilter(field_name='tags__name')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    status = filters.ChoiceFilter(choices=Post.STATUS_CHOICES)

    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'category', 'tag', 'status', 
                 'created_after', 'created_before']
