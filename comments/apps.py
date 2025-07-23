
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CommentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comments'

    def ready(self):
        post_migrate.connect(self.create_limited_admin_group, sender=self)


    def create_limited_admin_group(self, sender, **kwargs):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType

        Comment = self.get_model('Comment')
        group, created = Group.objects.get_or_create(name="Limited Admin")
        ct = ContentType.objects.get_for_model(Comment)

        perm_change = Permission.objects.get(codename="change_comment", content_type=ct)
        perm_delete = Permission.objects.get(codename="delete_comment", content_type=ct)
        group.permissions.set([perm_change, perm_delete])

