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
        user.is_active = True
        user.save()

        activation_token.created_at = None
        activation_token.save()

        return redirect("home")
    else:
        return render(request, "invalid_token.html")
