from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Users
from users.forms.signup_forms import SignupForm, LoginForm
import logging
from django.contrib.auth.hashers import make_password, check_password

logger = logging.getLogger(__name__)

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            cleaned_phone_number=f'+98{phone_number}'


            # چک کردن وجود ایمیل یا نام‌کاربری
            if Users.objects.filter(email=email).exists():
                logger.warning(f"Signup failed due to duplicate email: {email}")
                messages.error(request, "این ایمیل قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            if Users.objects.filter(username=username).exists():
                logger.warning(f"Signup failed due to duplicate username: {username}")
                messages.error(request, "این نام کاربری قبلاً ثبت شده است.")
                return render(request, "signup.html", {"form": form})

            # ذخیره‌سازی پسورد هش شده
            hashed_password = make_password(password)

            user = Users.objects.create(
                username=username,
                password=hashed_password,
                email=email,
                phone_number=cleaned_phone_number
            )
            logger.info(f"User signed up successfully: {user.email}")
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
                # بررسی پسورد هش شده
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    logger.info(f"User logged in successfully: {user.email}")
                    return redirect('home')
                else:
                    messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
                    logger.warning(f"Failed login attempt for user: {username} due to wrong password")
            except Users.DoesNotExist:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
                logger.warning(f"Failed login attempt for non-existent user: {username}")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})
