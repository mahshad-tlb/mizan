from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from users.models import Users, LoginToken
from users.forms.verification_forms import EmailForm
import secrets
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta


def send_magic_link(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                messages.error(request, "کاربری با این ایمیل وجود ندارد.")
                return render(request, "send_magic_link.html", {"form": form})

            token = secrets.token_urlsafe(32)
            LoginToken.objects.create(user=user, token=token)

            link = request.build_absolute_uri(f"/magic-login/{token}/")

            # ارسال ایمیل (در ترمینال چاپ می‌شود)
            send_mail(
                subject="ورود سریع به سایت",
                message=f"برای ورود روی این لینک کلیک کنید:\n{link}",
                from_email="mahshad@mtlb.erfann31dev.ir",
                recipient_list=[email],
                fail_silently=False
            )

            messages.success(request, "لینک ورود به ایمیل شما ارسال شد.")
            return redirect("login")
    else:
        form = EmailForm()
    return render(request, "send_magic_link.html", {"form": form})


def magic_login(request, token):
    try:
        login_token = LoginToken.objects.get(token=token)
    except LoginToken.DoesNotExist:
        messages.error(request, "لینک ورود نامعتبر است.")
        return render(request, "invalid_token.html")

    if login_token.is_used:
        messages.error(request, "این لینک قبلاً استفاده شده است.")
        return render(request, "invalid_token.html")

    # 🧪 Debug prints to check time difference
    now = timezone.now()
    token_time = login_token.created_at
    time_diff = now - token_time

    print("🕒 Now:", now)
    print("📨 Token created at:", token_time)
    print("⏱️ Time difference:", time_diff)

    # لینک فقط تا 10 دقیقه معتبر باشد
    if time_diff > timedelta(minutes=10):
        messages.error(request, "لینک منقضی شده است.")
        return render(request, "invalid_token.html")

    user = login_token.user

    # لاگین دستی
    login(request, user)

    # علامت‌گذاری لینک به عنوان استفاده‌شده
    login_token.is_used = True
    login_token.save()

    messages.success(request, f"{user.username} عزیز، خوش آمدید.")
    return redirect("home")

