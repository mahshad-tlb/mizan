from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils import timezone

from .models import Users, LoginToken
from .forms import LoginForm, SignupForm, EmailForm

import secrets

# ---------- ورود ----------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = Users.objects.get(username=username, password=password)
                # ورود موفق
                return redirect('home')
            except Users.DoesNotExist:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

# ---------- ثبت نام ----------
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']

            user = Users(
                username=username,
                password=password,  # پروژه واقعی: هش کن
                email=email,
                phone_number=phone_number
            )
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})

# ---------- ارسال لینک لاگین با ایمیل (magic link) ----------
def send_magic_link(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                messages.error(request, "کاربری با این ایمیل وجود ندارد.")
                return render(request, "send_magic_link.html", {"form": form})

            token = secrets.token_urlsafe(31)
            LoginToken.objects.create(user=user, token=token)

            link = request.build_absolute_uri(f"/magic-login/{token}/")

            send_mail(
                "لینک ورود شما",
                f"برای ورود روی این لینک کلیک کنید:\n{link}",
                "your_email@gmail.com",
                [email],
                fail_silently=False,
            )

            messages.success(request, "لینک ورود به ایمیل شما ارسال شد.")
            return redirect('home')
    else:
        form = EmailForm()
    return render(request, "send_magic_link.html", {"form": form})

# ---------- ورود با لینک ایمیل ----------
def magic_login(request, token):
    try:
        token_obj = LoginToken.objects.get(token=token, is_used=False)
    except LoginToken.DoesNotExist:
        return HttpResponse("لینک نامعتبر یا منقضی شده است.")

    request.session['user_id'] = token_obj.user.id
    token_obj.is_used = True
    token_obj.save()

    return HttpResponse(f"خوش آمدید {token_obj.user.username}! شما وارد شدید ✅")

# ---------- ارسال لینک ریست پسورد ----------
def send_reset_link(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                messages.error(request, "کاربری با این ایمیل وجود ندارد.")
                return render(request, "reset_password_request.html", {"form": form})

            token = secrets.token_urlsafe(32)
            LoginToken.objects.create(user=user, token=token)

            link = request.build_absolute_uri(f"/reset/{token}/")

            send_mail(
                "لینک بازیابی رمز عبور",
                f"برای تغییر رمز عبور روی این لینک کلیک کنید:\n{link}",
                "your_email@gmail.com",
                [email],
                fail_silently=False,
            )

            messages.success(request, "لینک بازیابی به ایمیل شما ارسال شد.")
            return redirect('login')
    else:
        form = EmailForm()
    return render(request, "reset_password_request.html", {"form": form})

# ---------- تغییر رمز عبور با لینک ----------
def reset_password_confirm(request, token):
    try:
        token_obj = LoginToken.objects.get(token=token, is_used=False)
    except LoginToken.DoesNotExist:
        return HttpResponse("لینک نامعتبر یا منقضی شده است.")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "رمز عبور و تکرار آن یکسان نیستند.")
            return render(request, "reset_password_confirm.html")

        # ذخیره رمز جدید
        user = token_obj.user
        user.password = new_password  # پروژه واقعی: هش کن
        user.save()

        # غیرفعال کردن توکن
        token_obj.is_used = True
        token_obj.save()

        messages.success(request, "رمز عبور با موفقیت تغییر کرد. لطفاً وارد شوید.")
        return redirect("login")

    return render(request, "reset_password_confirm.html")
