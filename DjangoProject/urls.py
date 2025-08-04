# DjangoProject/urls.py
from django.contrib import admin
from django.urls import path, include
from .limited_admin_site import limited_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('limited-admin/', limited_admin_site.urls),
    path('comments/', include('comments.urls')), # خطی که comments/urls را include می‌کند
    path('accounts/google/', include('google.urls')),
]