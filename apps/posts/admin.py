from django.contrib import admin
from .models import Post, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'category']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author', 'category']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
