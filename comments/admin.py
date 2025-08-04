# comments/admin.py

from django.contrib import admin
from .models import Comment, Message
from users.models import Users
# سایر ایمپورت‌ها...

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_content', 'is_approved', 'created_at']
    list_filter = ['is_approved']
    readonly_fields = ['created_at', 'slug']
    search_fields = ['content']
    fields = ['content', 'is_approved', 'created_at', 'slug']

    def short_content(self, obj):
        return obj.content[:50]
    short_content.short_description = "متن نظر"

admin.site.register(Comment, CommentAdmin) # ثبت مدل Comment در پنل اصلی


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['created_at', 'slug']
    fields = ['content', 'is_approved', 'created_at', 'slug']
    show_change_link = True

# این فایل نباید مدل Message را ثبت کند.
# بنابراین مطمئن شوید که هیچ خطی مانند admin.site.register(Message, ...) در اینجا وجود ندارد.