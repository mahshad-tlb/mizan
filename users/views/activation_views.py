from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.contrib import messages

from users.models import ActivationToken


def activate_account(request, token):
    try:
        activation_token = ActivationToken.objects.get(token=token)
    except ActivationToken.DoesNotExist:
        messages.error(request, "لینک نامعتبر است.")
        return render(request, "invalid_token.html")

    if activation_token.is_valid():
        user = activation_token.user
        user.is_active = False
        user.save()

        activation_token.is_used = True
        activation_token.save()

        login(request, user)
        messages.success(request, "حساب شما با موفقیت فعال شد.")
        return redirect("home")
    else:
        messages.error(request, "لینک منقضی شده یا قبلاً استفاده شده است.")
        return render(request, "invalid_token.html")
