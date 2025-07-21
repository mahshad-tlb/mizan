from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django. db import  models
from datetime import timedelta
from django.utils import  timezone
from django_jalali.db import models as jmodels
import logging

logger = logging.getLogger('users')

try:

    ...

except Exception as e:
    logger.error(f"خطا رخ داد: {e}")


class Users(models.Model) :
    username = models.CharField(max_length=14, unique=True, verbose_name="نام کاربری")
    email = models.EmailField(unique=True, verbose_name="ایمیل ")
    phone_number = models.CharField(max_length=12, unique=True, verbose_name="شماره موبایل")
    password = models.CharField(max_length=9, verbose_name="رمز عبور")
    slug = models.SlugField(max_length=16, unique=True, blank=True, null=True, verbose_name="اسلاگ")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد ")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی ")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

def __str__(self):
        return self.username
    def __str__(self):
        return  self.username

class LoginToken(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

def __str__(self):
         return f"{self.user.username} - {self.token}"
#gvhbnj