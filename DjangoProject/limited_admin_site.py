from django.contrib.admin import AdminSite
from comments.models import Comment
from comments.admin import CommentAdmin  # کلاس ادمین سفارشی که ساختی
import logging
from comments.email_utils import notify_admins

logger = logging.getLogger(__name__)

class LimitedAdminSite(AdminSite):
    site_header = "پنل ناظر"
    site_title = "پنل محدود"
    index_title = "فقط تایید نظرات"

    def has_permission(self, request):
        user = request.user
        if user.is_authenticated and user.groups.filter(name="Limited Admin").exists():
            logger.warning(f"✅ ناظر {user.username} وارد پنل محدود شد.")
            notify_admins(
                subject="ورود ناظر به پنل محدود",
                message=f"کاربر {user.username} وارد پنل محدود شد."
            )

            # ارسال ایمیل یا پیام به ادمین‌ها
            from django.contrib.auth.models import User
            admins = User.objects.filter(is_superuser=True, is_active=True)
            for admin in admins:
                logger.info(f"اطلاع رسانی: ناظر {user.username} وارد پنل محدود شد. به ادمین {admin.username}")

            return True
        return False

# نمونه شی برای ایمپورت در urls.py یا جاهای دیگر
limited_admin_site = LimitedAdminSite(name="limited_admin")
limited_admin_site.register(Comment, CommentAdmin)
