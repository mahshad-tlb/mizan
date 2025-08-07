from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils import timezone
import logging

logger = logging.getLogger('send_evening_emails')

class Command(BaseCommand):
    help = 'Send good evening email to active users'

    def handle(self, *args, **kwargs):
        now = timezone.localtime(timezone.now())


        if True:
            User = get_user_model()
            users = User.objects.filter(is_active=True, email__isnull=False).exclude(email='')

            for user in users:
                try:
                    send_mail(
                        subject="عصر بخیر!",
                        message="عصر بخیر! امیدواریم روز خوبی را گذرانده باشید.",
                        from_email='https://mtlb.erfann31dev.ir/',
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                    logger.info(f"Email sent to {user.email}")
                except Exception as e:
                    logger.error(f"Failed to send to {user.email}: {str(e)}")

            self.stdout.write(self.style.SUCCESS('Evening emails sent.'))
        else:
            self.stdout.write('Not the right time. Skipping.')
