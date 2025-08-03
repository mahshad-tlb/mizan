import secrets

from allauth.socialaccount.providers.mediawiki.provider import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Users, SecondaryPassword, ActivationToken
from users.forms.signup_forms import SignupForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password
import logging

secondary_logger = logging.getLogger('secondary_password')
from django.conf import settings

logger = logging.getLogger(__name__)
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse


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

            secondary_logger.debug(f"🔐 رمز دوم وارد شده برای {username}: {secondary_password}")

            if Users.objects.filter(email=email).exists():
                messages.error(request, "این ایمیل قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            if Users.objects.filter(username=username).exists():
                messages.error(request, "این نام کاربری قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            if Users.objects.filter(phone_number=cleaned_phone_number).exists():
                messages.error(request, "این شماره موبایل قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            # ساخت کاربر (غیرفعال در ابتدا)
            hashed_password = make_password(password)
            user = Users.objects.create(
                username=username,
                password=hashed_password,
                email=email,
                phone_number=cleaned_phone_number,
            )

            # ذخیره رمز دوم
            hashed_secondary = make_password(secondary_password)
            SecondaryPassword.objects.create(
                user=user,
                password=hashed_secondary
            )
            secondary_logger.debug(f"🔑 رمز دوم هش‌شده برای {username}: {hashed_secondary}")
            secondary_logger.info(f"✅ رمز دوم برای کاربر {username} با موفقیت ذخیره شد.")

            # ساخت توکن و لینک فعال‌سازی
            token = secrets.token_urlsafe(32)
            ActivationToken.objects.create(user=user, token=token)

            # build link
            activation_link = request.build_absolute_uri(
                reverse("activate_account", kwargs={"token": token})
            )

            # ارسال ایمیل فعال‌سازی
            send_mail(
                subject="فعالسازی حساب کاربری",
                message=f"برای فعالسازی حساب کاربری‌تان روی لینک زیر کلیک کنید:\n{activation_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False
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
                if check_password(password, user.password):
                    # ورود موفق (بدون بررسی رمز دوم)
                    request.session['user_id'] = user.id
                    logger.info(f"User logged in successfully: {user.email}")
                    return redirect('home')
                else:
                    messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
                    logger.warning(f"Failed login for user: {username} due to wrong password")
            except Users.DoesNotExist:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
                logger.warning(f"Failed login attempt for non-existent user: {username}")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})
