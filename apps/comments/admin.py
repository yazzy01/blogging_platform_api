from django.contrib import admin
from .models import Comment
from django.utils import timezone

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'status', 'is_active', 'created_at']
    list_filter = ['status', 'is_active', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    raw_id_fields = ['author', 'post', 'parent', 'moderated_by']
    readonly_fields = ['created_at', 'updated_at', 'moderated_at']
    list_per_page = 25
    actions = ['approve_comments', 'reject_comments']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post', 'moderated_by')

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new comment
            obj.author = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(
            status='approved',
            moderated_by=request.user,
            moderated_at=timezone.now()
        )

    @admin.action(description='Reject selected comments')
    def reject_comments(self, request, queryset):
        queryset.update(
            status='rejected',
            is_active=False,
            moderated_by=request.user,
            moderated_at=timezone.now()
        )
