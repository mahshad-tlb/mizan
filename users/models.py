from django.db import models
from django.utils import timezone


class Users(models.Model):
    username = models.CharField(max_length=15, unique=True, verbose_name="نام کاربری")
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره موبایل")
    password = models.CharField(max_length=8, verbose_name="رمز عبور")
    slug = models.SlugField(max_length=15, unique=True, blank=True, null=True, verbose_name="اسلاگ")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")



def __str__(self):
        return self.username

class LoginToken(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

def __str__(self):
         return f"{self.user.username} - {self.token}"