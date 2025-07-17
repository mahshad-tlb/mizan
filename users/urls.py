from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path("magic-link/", views.send_magic_link, name="send_magic_link"),
    path("magic-login/<str:token>/", views.magic_login, name="magic_login"),

    path("send-reset-link/", views.send_reset_link, name="send_reset_link"),
    path("reset-pass/<str:token>/", views.reset_password_confirm, name="reset_password_confirm"),


]

