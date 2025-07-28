from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Users, SecondaryPassword
from users.forms.signup_forms import SignupForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password
import logging
secondary_logger = logging.getLogger('secondary_password')

logger = logging.getLogger(__name__)
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            secondary_password = form.cleaned_data['secondary_password']  # ✅ اصلاح شد

            cleaned_phone_number = f'+98{phone_number}'

            # لاگ گرفتن از رمز دوم خام
            secondary_logger.debug(f"🔐 رمز دوم وارد شده برای {username}: {secondary_password}")  # ✅ اصلاح شد

            # چک کردن تکراری بودن
            if Users.objects.filter(email=email).exists():
                messages.error(request, "این ایمیل قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            if Users.objects.filter(username=username).exists():
                messages.error(request, "این نام کاربری قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            if Users.objects.filter(phone_number=cleaned_phone_number).exists():
                messages.error(request, "این شماره موبایل قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            # ساخت کاربر
            hashed_password = make_password(password)
            user = Users.objects.create(
                username=username,
                password=hashed_password,
                email=email,
                phone_number=cleaned_phone_number
            )

            # هش کردن رمز دوم
            hashed_secondary = make_password(secondary_password)
            secondary_logger.debug(f"🔑 رمز دوم هش‌شده برای {username}: {hashed_secondary}")  # ✅ اصلاح شد

            # ذخیره رمز دوم
            SecondaryPassword.objects.create(
                user=user,
                password=hashed_secondary
            )
            secondary_logger.info(f"✅ رمز دوم برای کاربر {username} با موفقیت ذخیره شد.")

            messages.success(request, "ثبت‌نام با موفقیت انجام شد.")
            return redirect('login')
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
