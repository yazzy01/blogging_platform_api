from django.contrib import admin
from django.db.models import Count, Q
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'order', 'is_active', 'post_count_display']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    list_editable = ['order', 'is_active']
    raw_id_fields = ['parent']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        )
        return queryset

    def post_count_display(self, obj):
        return obj.post_count
    post_count_display.short_description = 'Posts'
    post_count_display.admin_order_field = 'post_count'
