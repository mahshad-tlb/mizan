import secrets
from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Users, SecondaryPassword, ActivationToken
from users.forms.signup_forms import SignupForm, LoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import logging
from django.urls import reverse
from users.utils.email import send_email
import hashlib

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
            def hash_secondary_password(password: str) -> str:
                return hashlib.sha256(password.encode('utf-8')).hexdigest()

            # در جای مناسب در ویو یا تابع ذخیره‌سازی:
            hashed_secondary = hash_secondary_password(secondary_password)

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
            send_email(
                subject="فعالسازی حساب کاربری",
                message=f"برای فعالسازی حساب کاربری‌تان روی لینک زیر کلیک کنید:\n{activation_link}",
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

                if not user.is_active:
                    pending_id = request.session.get('pending_activation_user_id')
                    if pending_id and int(pending_id) == user.id:
                        user.is_active = True
                        user.save()
                        del request.session['pending_activation_user_id']
                        messages.success(request, "حساب شما فعال شد.")
                    else:
                        messages.error(request, "حساب شما فعال نیست.")
                        return render(request, "login.html", {"form": form})

                # ✅ چک کردن رمز عبور با check_password
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    user.last_login = timezone.now()
                    user.save()
                    messages.success(request, "ورود موفق بود.")
                    return redirect('home')
                else:
                    messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
            except Users.DoesNotExist:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

