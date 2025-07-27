from django.utils.text import slugify
from django. db import  models
from datetime import timedelta
from django.utils import  timezone
from django_jalali.db import models as jmodels
import logging
from users.utils.image_utils import minify_image
from ckeditor.fields import RichTextField
logger = logging.getLogger('users')

try:

    ...

except Exception as e:
    logger.error(f"خطا رخ داد: {e}")


class Users(models.Model) :
    username = models.CharField(max_length=14, unique=True, verbose_name="نام کاربری")
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    phone_number = models.CharField(max_length=12, unique=True, verbose_name="شماره موبایل")
    password = models.CharField(max_length=9, verbose_name="رمز عبور")
    slug = models.SlugField(max_length=16, unique=True, blank=True, null=True, verbose_name="اسلاگ")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return  self.username

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


class LoginToken(models.Model) :
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="کاربر")
    token = models.CharField(max_length=50, unique=True, verbose_name="توکن")
    created_at = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    is_used = models.BooleanField(default=False, verbose_name="استفاده شده")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return f"{self.user.username} - {self.token}"

    class Meta:
        verbose_name = "توکن ورود"
        verbose_name_plural = "توکن‌های ورود"


class SMSVerificationCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره موبایل")
    code = models.CharField(max_length=10, verbose_name="کد تایید")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def is_expired(self):
        expiration_time = self.created_at + timedelta(minutes=5)
        return timezone.now() > expiration_time

    def __str__(self):
        return f"{self.phone_number} - {self.code} (created: {self.created_at})"

    class Meta:
        verbose_name = "کد تأیید پیامکی"
        verbose_name_plural = "کدهای تأیید پیامکی"
        #fgh






class AdminEmail(models.Model):
    subject = models.CharField(max_length=200, verbose_name="عنوان ایمیل")
    body = RichTextField(verbose_name="متن ایمیل (HTML)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "ایمیل ادمین"
        verbose_name_plural = "ایمیل‌های ادمین"

    def __str__(self):
        return self.subject
