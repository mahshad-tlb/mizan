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
            user = Users(
                username=username,
                email=email,
                phone_number=cleaned_phone_number,
                password=make_password(password),  # ← رمز عبور هش‌شده مستقیم ذخیره میشه
            )
            user.save()

            # ذخیره رمز دوم
            def hash_secondary_password(password: str) -> str:
                return hashlib.sha256(password.encode('utf-8')).hexdigest()

            # در جای مناسب در ویو یا تابع ذخیره‌سازی:
            hashed_secondary = hash_secondary_password(secondary_password)

            SecondaryPassword.objects.create(
                user=user,
                password=hashed_secondary
            )

            secondary_logger.debug(f"{username}: {hashed_secondary}")
            secondary_logger.info(f" {username} با موفقیت ذخیره شد.")

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

                # بررسی فقط برای تست، مقایسه مستقیم (خطرناک برای تولیدی!)
                from django.contrib.auth.hashers import make_password
                hashed_input = make_password(password)
                print("رمز ورودی هش شده:", hashed_input)
                print("رمز کاربر در DB:", user.password)

                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    return redirect('home')
                else:
                    return render(request, "login.html", {
                        "form": form,
                        "custom_error": "❌ check_password مقدار False داده است.",
                        "hashed_input": hashed_input,
                        "stored_password": user.password,
                    })

            except Users.DoesNotExist:
                return render(request, "login.html", {
                    "form": form,
                    "custom_error": "کاربر وجود ندارد."
                })
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})
