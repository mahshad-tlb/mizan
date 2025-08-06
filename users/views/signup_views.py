
import secrets
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
import logging

# Import مدل‌ها
from users.models import Users, SecondaryPassword, ActivationToken
from users.forms.signup_forms import SignupForm, LoginForm

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
            secondary_password = form.cleaned_data['secondary_password']

            cleaned_phone_number = f'+98{phone_number}'

            secondary_logger.debug(f"🔐 رمز دوم وارد شده برای {username}: {secondary_password}")

            # چک کردن تکراری نبودن
            if Users.objects.filter(email=email).exists():
                messages.error(request, "این ایمیل قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            if Users.objects.filter(username=username).exists():
                messages.error(request, "این نام کاربری قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            if Users.objects.filter(phone_number=cleaned_phone_number).exists():
                messages.error(request, "این شماره موبایل قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            try:
                # ساخت کاربر با hash کردن رمز
                hashed_password = make_password(password)
                user = Users.objects.create(
                    username=username,
                    password=hashed_password,
                    email=email,
                    phone_number=cleaned_phone_number,
                    is_active=True  # غیرفعال در ابتدا
                )

                # ذخیره رمز دوم
                hashed_secondary = make_password(secondary_password)
                SecondaryPassword.objects.create(
                    user=user,
                    password=hashed_secondary
                )

                secondary_logger.debug(f"🔑 رمز دوم هش‌شده برای {username}: {hashed_secondary}")
                secondary_logger.info(f"✅ رمز دوم برای کاربر {username} با موفقیت ذخیره شد.")

                # ساخت توکن فعال‌سازی
                token = secrets.token_urlsafe(32)
                ActivationToken.objects.create(user=user, token=token)

                # ساخت لینک فعال‌سازی
                activation_link = request.build_absolute_uri(
                    reverse("activate_account", kwargs={"token": token})
                )

                # ارسال ایمیل فعال‌سازی
                try:
                    send_mail(
                        subject="فعالسازی حساب کاربری",
                        message=f"برای فعالسازی حساب کاربری‌تان روی لینک زیر کلیک کنید:\n{activation_link}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False
                    )
                    messages.success(request, "ثبت‌نام انجام شد. لطفاً ایمیل خود را برای فعال‌سازی حساب بررسی کنید.")
                except Exception as e:
                    logger.error(f"Error sending email: {e}")
                    messages.warning(request, "ثبت‌نام انجام شد، اما ایمیل ارسال نشد.")

                return redirect('login')

            except Exception as e:
                logger.error(f"Error creating user: {e}")
                messages.error(request, "خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.")
                return render(request, "signup.html", {"form": form})

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
                # جستجوی کاربر
                user = Users.objects.get(username=username)

                # بررسی فعال بودن کاربر
                if not user.is_active:
                    # بررسی اینکه آیا کاربر در انتظار فعال‌سازی هست
                    pending_id = request.session.get('pending_activation_user_id')
                    if pending_id and int(pending_id) == user.id:
                        user.is_active = True
                        user.save()
                        del request.session['pending_activation_user_id']
                        messages.success(request, "حساب شما فعال شد.")
                    else:
                        messages.error(request, "حساب شما فعال نیست. لطفاً ایمیل خود را چک کنید.")
                        logger.warning(f"Inactive user tried to login: {username}")
                        return render(request, "login.html", {"form": form})

                # بررسی رمز عبور
                if check_password(password, user.password):
                    # ورود موفق - ذخیره در session
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username

                    # به‌روزرسانی last_login
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])

                    logger.info(f"User logged in successfully: {user.username} ({user.email})")
                    messages.success(request, "ورود موفق بود.")
                    return redirect('home')
                else:
                    messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
                    logger.warning(f"Wrong password for user: {username}")

            except Users.DoesNotExist:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
                logger.warning(f"Login attempt for non-existent user: {username}")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# def logout_view(request):
#     """خروج از سیستم"""
#     # پاک کردن session
#     if 'user_id' in request.session:
#         username = request.session.get('username', 'Unknown')
#         logger.info(f"User logged out: {username}")
#         del request.session['user_id']
#
#     if 'username' in request.session:
#         del request.session['username']
#
#     # پاک کردن کل session (اختیاری)
#     request.session.flush()
#
#     messages.success(request, "با موفقیت خارج شدید.")
#     return redirect('login')


def activate_account(request, token):
    """فعال‌سازی حساب کاربری"""
    try:
        activation_token = ActivationToken.objects.get(token=token)
        user = activation_token.user

        if not user.is_active:
            user.is_active = True
            user.save()
            activation_token.delete()  # حذف توکن بعد از استفاده
            messages.success(request, "حساب شما با موفقیت فعال شد.")
            # برای ورود خودکار بعد از فعال‌سازی
            request.session['pending_activation_user_id'] = user.id
            logger.info(f"Account activated: {user.username}")
        else:
            messages.info(request, "حساب شما قبلاً فعال شده است.")

    except ActivationToken.DoesNotExist:
        messages.error(request, "لینک فعال‌سازی نامعتبر یا منقضی شده است.")
        logger.warning(f"Invalid activation token used: {token}")

    return redirect('login')


# تابع کمکی برای گرفتن کاربر فعلی از session
def get_current_user(request):
    """گرفتن کاربر فعلی از session"""
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return Users.objects.get(id=user_id, is_active=True)
        except Users.DoesNotExist:
            # اگه کاربر وجود نداشت، session رو پاک کن
            if 'user_id' in request.session:
                del request.session['user_id']
            if 'username' in request.session:
                del request.session['username']
    return None


# Middleware یا Decorator برای چک کردن login (اختیاری)
def login_required_custom(view_func):
    """Decorator برای چک کردن ورود کاربر"""

    def wrapper(request, *args, **kwargs):
        if not get_current_user(request):
            messages.error(request, "برای دسترسی به این صفحه باید وارد شوید.")
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper