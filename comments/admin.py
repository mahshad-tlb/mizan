from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_content', 'is_approved', 'created_at']
    list_filter = ['is_approved']
    readonly_fields = ['created_at', 'slug']
    search_fields = ['content']
    fields = ['content', 'is_approved', 'created_at', 'slug']

    def short_content(self, obj):
        return obj.content[:50]
    short_content.short_description = "متن نظر"
