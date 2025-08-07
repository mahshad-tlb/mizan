from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import ActivationToken


def activate_account(request, token):
    try:
        activation_token = ActivationToken.objects.get(token=token)
    except ActivationToken.DoesNotExist:
        messages.error(request, "The activation link is invalid.")
        return render(request, "invalid_token.html")

    if activation_token.is_valid():
        user = activation_token.user

        if user.is_active:
            messages.info(request, "Your account is already activated.")
            return redirect("login")

        user.is_active = True
        user.save()
        activation_token.delete()  # Optional: delete token after activation

        messages.success(request, "Your account has been successfully activated. You can now log in.")
        return redirect("login")
    else:
        messages.error(request, "The activation link has expired or is invalid.")
        return render(request, "invalid_token.html")


