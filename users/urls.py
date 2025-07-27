from django.urls import path
from .views.signup_views import signup_view, login_view
from .views.magic_link_views import send_magic_link
from .views.password_views import send_reset_link, reset_password_confirm
from .views.sms_views import send_code_view, verify_code_view
from .views.user_views import user_detail, home_view


urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path("magic-link/", send_magic_link, name="send_magic_link"),
   # path("magic-login/<str:token>/", views.magic_login, name="magic_login"),

    path("send-reset-link/", send_reset_link, name="send_reset_link"),
    path("reset-pass/<str:token>/", reset_password_confirm, name="reset_password_confirm"),
    path('home/', home_view, name='home'),  # 👈 اینو اضافه کن
    path("send-code/", send_code_view, name="send_code"),
    path("verify-code/", verify_code_view, name="verify_code"),
    path('users/<slug:slug>/', user_detail, name='user_detail'),




]

