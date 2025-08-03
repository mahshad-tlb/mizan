# urls.py
from django.urls import path
from .views import google_login_init_view, google_callback_view

urlpatterns = [
    path("auth/google/login/", google_login_init_view, name="google-login-init"),
    path("auth/google/callback/", google_callback_view, name="google-callback"),
]
