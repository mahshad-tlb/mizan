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

# لاگرها
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

            # ساخت کاربر (رمز هش شده در فیلد password)
            user = Users(
                username=username,
                email=email,
                phone_number=cleaned_phone_number,
                password=make_password(password),  # هش امن رمز عبور
            )
            user.save()
            logger.info(f"User {username} saved to database.")

            # هش رمز دوم با sha256
            logger.debug(f"User {username} entered secondary password: {secondary_password}")
            hashed_secondary = hashlib.sha256(secondary_password.encode('utf-8')).hexdigest()
            logger.debug(f"SHA256 hash of secondary password for user {username}: {hashed_secondary}")
            SecondaryPassword.objects.create(user=user, password=hashed_secondary)
            secondary_logger.info(f"Secondary password set for user {username}")

            secondary_logger.info(f"Secondary password set for user {username}")
            logger.info(f"User {username} created and pending activation.")

            # ساخت توکن فعال‌سازی
            token = secrets.token_urlsafe(32)
            ActivationToken.objects.create(user=user, token=token)

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

                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    logger.info(f"User {username} logged in.")
                    return redirect('home')
                else:
                    logger.warning(f"Login failed for {username}: incorrect password.")
                    return render(request, "login.html", {
                        "form": form,
                        "custom_error": "رمز عبور اشتباه است.",
                    })

            except Users.DoesNotExist:
                logger.warning(f"Login attempt with unknown username: {username}")
                return render(request, "login.html", {
                    "form": form,
                    "custom_error": "کاربر وجود ندارد."
                })
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

#def login_view(request):
    #if request.method == "POST":
        #form = LoginForm(request.POST)
        #if form.is_valid():
            #username = form.cleaned_data['username']
            #password = form.cleaned_data['password']

            #try:
                #user = Users.objects.get(username=username)

                #if not user.is_active:
                    #logger.warning(f"Login failed for {username}: account not activated.")
                    #return render(request, "login.html", {
                        #"form": form,
                        #"custom_error": "حساب شما هنوز فعال نشده است.",
                    #})

                #if check_password(password, user.password):
                    #request.session['user_id'] = user.id
                    #logger.info(f"User {username} logged in.")
                    #return redirect('home')
                #else:
                    #logger.warning(f"Login failed for {username}: incorrect password.")
                    #return render(request, "login.html", {
                        #"form": form,
                        #"custom_error": "رمز عبور اشتباه است.",
                    #})

            #except Users.DoesNotExist:
                #logger.warning(f"Login attempt with unknown username: {username}")
                #return render(request, "login.html", {
                    #"form": form,
                    #"custom_error": "کاربر وجود ندارد."
                #})
    #else:
        #form = LoginForm()

    #return render(request, "login.html", {"form": form})

def logout_view(request):
    # پاک کردن session مربوط به کاربر
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "با موفقیت خارج شدید.")
    else:
        messages.info(request, "شما وارد نشده‌اید.")

    return render(request, 'logout.html')