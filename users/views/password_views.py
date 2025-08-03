from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail

from users.models import Users, LoginToken
from users.forms.password_forms import ResetPasswordForm, NewPasswordForm
from users.forms.verification_forms import EmailForm
import secrets


def send_reset_link(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                messages.error(request, "کاربری با این ایمیل وجود ندارد.")
                return render(request, "reset_password_request.html", {"form": form})

            token = secrets.token_urlsafe(32)
            LoginToken.objects.create(user=user, token=token)

            link = request.build_absolute_uri(f"/reset-pass/{token}/")

            send_mail(
                subject="بازیابی رمز عبور",
                message=f"برای تغییر رمز عبور روی این لینک کلیک کنید:\n{link}",
                from_email="mahshad@mtlb.erfann31dev.ir",
                recipient_list=[email],
                fail_silently=False
            )

            messages.success(request, "لینک بازیابی رمز عبور ارسال شد.")
            return redirect("login")
    else:
        form = EmailForm()
    return render(request, "reset_password_request.html", {"form": form})

def reset_password_confirm(request, token):
    try:
        token_obj = LoginToken.objects.get(token=token, is_used=False)
    except LoginToken.DoesNotExist:
        return HttpResponse("لینک منقضی یا نامعتبر است.")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "رمز عبور و تکرار آن یکسان نیستند.")
            return render(request, "reset_password_confirm.html")

        user = token_obj.user
        user.password = new_password
        user.save()

        token_obj.is_used = True
        token_obj.save()

        messages.success(request, "رمز عبور با موفقیت تغییر یافت.")
        return redirect("login")

    return render(request, "reset_password_confirm.html")
