import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger("users.email_service")

def send_email(subject, message, recipient_email, fail_silently=False, from_email=None):
    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[recipient_email],
            fail_silently=fail_silently
        )
        logger.info(f"ایمیل با موضوع '{subject}' به {recipient_email} ارسال شد.")
        return True
    except Exception as e:
        logger.error(f"ارسال ایمیل به {recipient_email} با خطا مواجه شد: {e}")
        return False
