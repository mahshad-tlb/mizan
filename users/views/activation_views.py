from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.contrib import messages

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        login(request, user)
        user.is_active = True
        user.save()
        messages.success(request, "حساب شما با موفقیت فعال شد و وارد شدید.")
        return redirect("home")  # مسیر صفحه اصلی پروژه‌ات
    else:
        messages.error(request, "لینک نامعتبر یا منقضی شده است.")
        return render(request, "invalid_token.html")
