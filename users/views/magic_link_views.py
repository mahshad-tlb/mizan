from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from users.models import Users, LoginToken
from users.forms.verification_forms import EmailForm
import secrets


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
                from_email="noreply@example.com",
                recipient_list=[email],
                fail_silently=False
            )

            messages.success(request, "لینک ورود به ایمیل شما ارسال شد.")
            return redirect("login")
    else:
        form = EmailForm()
    return render(request, "send_magic_link.html", {"form": form})