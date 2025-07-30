from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from comments.models import Comment
from comments.admin import CommentAdmin

class LimitedAdminSite(AdminSite):
    site_header = _("پنل مدیریت ناظر محدود")
    site_title = _("ناظر محدود")
    index_title = _("داشبورد ناظر")

    def has_permission(self, request):
        user = request.user
        # فقط اگر کاربر وارد شده و عضو گروه "Limited Admin" باشد اجازه می‌دهد
        if user.is_authenticated and user.groups.filter(name="Limited Admin").exists():
            return True
        return False


limited_admin_site = LimitedAdminSite(name='limited_admin')
limited_admin_site.register(Comment, CommentAdmin)