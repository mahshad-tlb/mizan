# limited_admin_site.py

from django.contrib import admin
from django.contrib.admin import AdminSite
from comments.models import Comment, Message
from comments.admin import CommentAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class LimitedAdminSite(AdminSite):
    site_header = "پنل ناظر"
    site_title = "پنل محدود"
    index_title = "فقط تایید نظرات و پیام‌ها"

    def has_permission(self, request):
        # فقط اعضای گروه Limited Admin اجازه ورود دارند
        return request.user.is_authenticated and request.user.groups.filter(name="Limited Admin").exists()

    def index(self, request, extra_context=None):
        # بررسی وجود پیام‌ خوانده‌نشده
        unread_messages_count = Message.objects.filter(recipient=request.user, is_read=False).count()

        extra_context = extra_context or {}
        extra_context['unread_messages_count'] = unread_messages_count

        return super().index(request, extra_context=extra_context)


class LimitedMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('subject', 'content', 'sender__username', 'recipient__username')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # فقط پیام‌هایی که کاربر فرستاده یا دریافت کرده
        return qs.filter(sender=request.user) | qs.filter(recipient=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # مقدار پیش‌فرض فرستنده = کاربر فعلی، و غیرفعال کردن فیلد
        form.base_fields['sender'].initial = request.user
        form.base_fields['sender'].disabled = True

        # دریافت کاربران مجاز برای دریافت پیام
        admin_users = User.objects.filter(is_superuser=True)
        limited_admins = User.objects.filter(groups__name='Limited Admin')
        allowed_recipients = (admin_users | limited_admins).exclude(id=request.user.id)

        form.base_fields['recipient'].queryset = allowed_recipients
        return form

    def save_model(self, request, obj, form, change):
        # فیلد sender را با کاربر لاگین‌شده تنظیم می‌کنیم حتی اگر فیلد قفل باشد
        obj.sender = request.user
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        # فقط اگر کاربر پرمیشن اضافه‌کردن پیام را داشته باشد
        return request.user.has_perm('comments.add_message')


limited_admin_site = LimitedAdminSite(name="limited_admin")
limited_admin_site.register(Comment, CommentAdmin)
limited_admin_site.register(Message, LimitedMessageAdmin)
