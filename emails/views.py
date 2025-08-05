from django.shortcuts import render, redirect
from .forms import EmailForm
from django.core.mail import send_mail
from users.models import Users
from premailer import transform
import logging

logger = logging.getLogger(__name__)

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()
            subject = email.title
            raw_html = email.body
            from_email = 'mahshad@mtlb.erfann31dev.ir'
            users = Users.objects.filter(is_active=True).exclude(email='').values_list('email', flat=True)
            recipient_list = list(users)

            html_message = transform(raw_html)

            logger.info(f"شروع ارسال ایمیل '{subject}' به {len(recipient_list)} کاربر فعال.")
            try:
                send_mail(subject, '', from_email, recipient_list, html_message=html_message, fail_silently=False)
                logger.info(f"ایمیل '{subject}' با موفقیت ارسال شد.")
            except Exception as e:
                logger.error(f"خطا در ارسال ایمیل '{subject}': {e}")

            return redirect('send_email')
    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form})
