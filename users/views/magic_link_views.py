import secrets
import logging
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import login
from django.utils import timezone
from users.models import Users, LoginToken
from users.forms.verification_forms import EmailForm

# تنظیم لاگر
logger = logging.getLogger("users.email")


def send_magic_link(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            logger.info(f"دریافت درخواست ارسال لینک ورود برای ایمیل: {email}")

            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                logger.warning(f"کاربر با ایمیل {email} یافت نشد.")
                messages.error(request, "کاربری با این ایمیل وجود ندارد.")
                return render(request, "send_magic_link.html", {"form": form})

            token = secrets.token_urlsafe(32)
            LoginToken.objects.create(user=user, token=token)
            logger.info(f"توکن ورود برای کاربر {user.email} ایجاد شد: {token}")

            link = request.build_absolute_uri(f"/magic-login/{token}/")
            logger.debug(f"لینک ساخته شده برای ورود: {link}")

            try:
                send_mail(
                    subject="ورود سریع به سایت",
                    message=f"برای ورود روی این لینک کلیک کنید:\n{link}",
                    from_email="mahshad@mtlb.erfann31dev.ir",
                    recipient_list=[email],
                    fail_silently=False
                )
                logger.info(f"ایمیل لینک ورود برای {email} ارسال شد.")
            except Exception as e:
                logger.error(f"خطا در ارسال ایمیل برای {email}: {e}")
                messages.error(request, "خطا در ارسال ایمیل. لطفاً بعداً دوباره تلاش کنید.")
                return render(request, "send_magic_link.html", {"form": form})

            messages.success(request, "لینک ورود به ایمیل شما ارسال شد.")
            return redirect("home")
        else:
            logger.warning("فرم ایمیل نامعتبر بود.")
    else:
        form = EmailForm()
        logger.debug("صفحه ارسال لینک ورود GET شد.")

    return render(request, "send_magic_link.html", {"form": form})


def magic_login(request, token):
    logger.info(f"درخواست ورود با توکن: {token}")

    try:
        login_token = LoginToken.objects.get(token=token)
    except LoginToken.DoesNotExist:
        logger.warning(f"توکن نامعتبر: {token}")
        messages.error(request, "لینک ورود نامعتبر است.")
        return render(request, "invalid_token.html")

    if login_token.is_used:
        logger.warning(f"توکن قبلاً استفاده شده: {token} برای کاربر {login_token.user.email}")
        messages.error(request, "این لینک قبلاً استفاده شده است.")
        return render(request, "invalid_token.html")

    if timezone.now() - login_token.created_at > timedelta(minutes=10):
        logger.warning(f"توکن منقضی شده: {token} برای کاربر {login_token.user.email}")
        messages.error(request, "لینک منقضی شده است.")
        return render(request, "invalid_token.html")

    user = login_token.user
    login(request, user)
    logger.info(f"کاربر {user.email} با موفقیت وارد شد با استفاده از توکن {token}")

    login_token.is_used = True
    login_token.save()
    logger.debug(f"توکن {token} به عنوان استفاده‌شده علامت‌گذاری شد.")

    messages.success(request, f"{user.username} عزیز، خوش آمدید.")
    return redirect("home")
