
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth import login, get_user_model
from django.contrib import messages

User = get_user_model()

def google_login_init_view(request):
    google_auth_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
    scope = "openid email profile"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": scope,
        "access_type": "offline",
        "prompt": "select_account",
    }
    # ساخت URL با پارامترها
    url = requests.Request('GET', google_auth_endpoint, params=params).prepare().url
    return redirect(url)


def google_callback_view(request):
    code = request.GET.get("code")
    if not code:
        messages.error(request, "کد مجوز از گوگل دریافت نشد.")
        return redirect("login")  # یا هر صفحه‌ای که می‌خوای

    # تبادل کد با توکن دسترسی
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_response = requests.post(token_url, data=data)
    if token_response.status_code != 200:
        messages.error(request, "دریافت توکن از گوگل ناموفق بود.")
        return redirect("login")

    token_json = token_response.json()
    access_token = token_json.get("access_token")

    # گرفتن اطلاعات کاربر
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {"alt": "json", "access_token": access_token}
    user_info_response = requests.get(user_info_url, params=params)

    if user_info_response.status_code != 200:
        messages.error(request, "دریافت اطلاعات کاربر از گوگل ناموفق بود.")
        return redirect("login")

    user_info = user_info_response.json()
    email = user_info.get("email")
    name = user_info.get("name")

    if not email:
        messages.error(request, "ایمیل کاربر دریافت نشد.")
        return redirect("login")

    # بررسی وجود کاربر و ورود
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # ایجاد کاربر جدید
        user = User.objects.create_user(username=email.split("@")[0], email=email)
        user.first_name = name
        user.save()

    login(request, user)
    return redirect("home")  # یا هر صفحه‌ای که می‌خوای

