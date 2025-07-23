from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


def notify_admins(comment=None, subject=None, message=None):
    User = get_user_model()

    # گرفتن ناظرها
    moderators = User.objects.filter(groups__name='Limited Admin', is_active=True)
    superusers = User.objects.filter(is_superuser=True, is_active=True)

    recipients = list(set(user.email for user in moderators.union(superusers) if user.email))

    if not recipients:
        logger.warning("هیچ ادمینی برای ارسال ایمیل یافت نشد.")
        return

    if comment:
        subject = f"نظر جدید از {comment.user.username}"
        message = f"یک نظر جدید توسط کاربر {comment.user.username} ثبت شده است:\n\n"
        message += f"{comment.content}\n\nمنتظر تایید شماست."
    elif not message:
        message = "پیام بدون محتوای مشخص ارسال شد."

    # لاگ بگیریم ببینیم قراره به کی‌ها ایمیل بفرسته
    logger.info(f"📧 ارسال ایمیل به: {recipients}")
    logger.info(f"📝 متن پیام: {message}")

    send_mail(
        subject=subject or "اعلان جدید",
        message=strip_tags(message),
        from_email="webmaster@example.com",
        recipient_list=recipients,
        fail_silently=False
    )

