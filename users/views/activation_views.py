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
        # حساب هنوز فعال نشود
        # فقط user_id را در session ذخیره می‌کنیم
        request.session['pending_activation_user_id'] = user.id

        messages.success(request, "اکنون می‌توانید وارد حساب خود شوید تا فعال‌سازی کامل شود.")
        return redirect("login")
    else:
        return render(request, "invalid_token.html")

