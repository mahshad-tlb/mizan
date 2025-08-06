import secrets
import hashlib
import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from users.models import Users, SecondaryPassword, ActivationToken
from users.forms.signup_forms import SignupForm, LoginForm
from users.utils.email import send_email

# Loggers
secondary_logger = logging.getLogger('users.secondary_password')
logger = logging.getLogger('users.account')


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            secondary_password = form.cleaned_data['secondary_password']

            cleaned_phone_number = f'+98{phone_number}'

            if Users.objects.filter(email=email).exists():
                messages.error(request, "این ایمیل قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            if Users.objects.filter(username=username).exists():
                messages.error(request, "این نام کاربری قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            if Users.objects.filter(phone_number=cleaned_phone_number).exists():
                messages.error(request, "این شماره موبایل قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            # Create user with hashed password
            user = Users(
                username=username,
                email=email,
                phone_number=cleaned_phone_number,
                password=make_password(password),
            )
            user.save()

            # Hash secondary password
            hashed_secondary = hashlib.sha256(secondary_password.encode('utf-8')).hexdigest()
            SecondaryPassword.objects.create(user=user, password=hashed_secondary)

            secondary_logger.info(f"Secondary password set for user {username}")
            logger.info(f"User {username} created and pending activation.")

            # Generate activation token
            token = secrets.token_urlsafe(32)
            ActivationToken.objects.create(user=user, token=token)

            activation_link = request.build_absolute_uri(
                reverse("activate_account", kwargs={"token": token})
            )

            # Send activation email
            send_email(
                subject="Account Activation",
                message=f"Click the following link to activate your account:\n{activation_link}",
                recipient_email=email
            )

            messages.success(request, "ثبت‌نام انجام شد. لطفاً ایمیل خود را برای فعال‌سازی حساب بررسی کنید.")
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = Users.objects.get(username=username)

                # Avoid using non-ASCII characters in print/log
                # print("Hashed input password:", make_password(password))  ← remove if not needed

                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    logger.info(f"User {username} logged in successfully.")
                    return redirect('home')
                else:
                    logger.warning(f"Login failed for user {username}: incorrect password.")
                    return render(request, "login.html", {
                        "form": form,
                        "custom_error": "رمز عبور اشتباه است.",
                    })

            except Users.DoesNotExist:
                logger.warning(f"Login failed: username '{username}' not found.")
                return render(request, "login.html", {
                    "form": form,
                    "custom_error": "کاربر وجود ندارد."
                })
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})
