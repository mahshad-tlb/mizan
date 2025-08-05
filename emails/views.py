from django.shortcuts import render, redirect
from .forms import EmailForm
from django.core.mail import send_mail
from users.models import Users  # اگر مدل کاربر سفارشی دارید
import logging

logger = logging.getLogger(__name__)

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()

            subject = email.عنوان
            message = email.متن
            from_email = 'https://mtlb.erfann31dev.ir/'

            # دریافت ایمیل همه کاربران فعال
            users = Users.objects.filter(is_active=True).exclude(email='').values_list('email', flat=True)
            recipient_list = list(users)
            logger.info(f"شروع ارسال ایمیل '{subject}' به {len(recipient_list)} کاربر فعال.")

            # ارسال ایمیل به همه کاربران
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                logger.info(f"ایمیل '{subject}' با موفقیت به همه کاربران ارسال شد.")
            except Exception as e:
                logger.error(f"ارسال ایمیل '{subject}' شکست خورد. خطا: {e}")

            return redirect('send_email')
    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form})
