from django.contrib import admin
from django.urls import path, include

from users.urls import urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('emails.urls')),
]
