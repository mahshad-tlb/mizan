from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CommentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comments'
    verbose_name = "مدیریت نظرات و پیام‌ها"  # 👈 فارسی‌سازی نام اپلیکیشن

    def ready(self):
        post_migrate.connect(self.create_limited_admin_group, sender=self)

    def create_limited_admin_group(self, sender, **kwargs):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Comment, Message

        group, created = Group.objects.get_or_create(name="Limited Admin")

        # پرمیشن‌های Comment
        ct_comment = ContentType.objects.get_for_model(Comment)
        perm_change_comment = Permission.objects.get(codename="change_comment", content_type=ct_comment)
        perm_delete_comment = Permission.objects.get(codename="delete_comment", content_type=ct_comment)

        # پرمیشن‌های Message
        ct_message = ContentType.objects.get_for_model(Message)
        perm_view_message = Permission.objects.get(codename="view_message", content_type=ct_message)
        perm_change_message = Permission.objects.get(codename="change_message", content_type=ct_message)
        perm_add_message = Permission.objects.get(codename="add_message", content_type=ct_message)

        group.permissions.set([
            perm_change_comment, perm_delete_comment,
            perm_view_message, perm_change_message, perm_add_message
        ])
