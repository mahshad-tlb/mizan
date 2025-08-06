from django.utils.text import slugify
from django.db import models
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.contrib.auth.models import PermissionsMixin, Group, Permission, BaseUserManager
import logging
from jdatetime import timedelta

logger = logging.getLogger('users')


class UserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("ایمیل باید وارد شود")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, phone_number, password, **extra_fields)


class Users(PermissionsMixin, models.Model):
    username = models.CharField(max_length=14, unique=True, verbose_name="نام کاربری")
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="شماره موبایل")
    password = models.CharField(max_length=256, verbose_name="رمز عبور")
    slug = models.SlugField(max_length=16, unique=True, blank=True, null=True, verbose_name="اسلاگ")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    is_active = models.BooleanField(default=False, verbose_name="فعال")
    is_staff = models.BooleanField(default=False, verbose_name="عضو کادر")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="آخرین ورود")

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="custom_users",
        verbose_name="گروه‌ها"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="custom_users",
        verbose_name="دسترسی‌ها"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    @classmethod
    def get_email_field_name(cls):
        return 'email'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


class ActivationToken(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="activation_tokens", verbose_name="کاربر")
    token = models.CharField(max_length=64, unique=True, verbose_name="توکن")
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="تاریخ ایجاد")

    def is_valid(self):
        if self.created_at is None:
            return False
        expiration_time = self.created_at + timedelta(days=1)
        return timezone.now() <= expiration_time

    class Meta:
        verbose_name = "توکن فعال‌سازی"
        verbose_name_plural = "توکن‌های فعال‌سازی"


class LoginToken(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="کاربر")
    token = models.CharField(max_length=50, unique=True, verbose_name="توکن")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_used = models.BooleanField(default=False, verbose_name="استفاده شده")
    updated_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return f"{self.user.username} - {self.token}"

    class Meta:
        verbose_name = "توکن ورود"
        verbose_name_plural = "توکن‌های ورود"


class SMSVerificationCode(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="شماره موبایل")
    code = models.CharField(max_length=6, verbose_name="کد تأیید")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")
    is_verified = models.BooleanField(default=False, verbose_name="تأیید شده")

    def __str__(self):
        return f"{self.phone_number} - {self.code}"

    def is_expired(self):
        expiration_time = self.created_at + timedelta(minutes=5)
        return timezone.now() > expiration_time

    class Meta:
        verbose_name = "کد تأیید پیامکی"
        verbose_name_plural = "کدهای تأیید پیامکی"


class AdminEmail(models.Model):
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    body = models.TextField(verbose_name="متن")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "ایمیل ادمین"
        verbose_name_plural = "ایمیل‌های ادمین"


class SecondaryPassword(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, verbose_name="کاربر")
    password = models.CharField(max_length=256, verbose_name="رمز دوم")

    def __str__(self):
        return f"{self.user.username} - رمز دوم"

    class Meta:
        verbose_name = "رمز دوم"
        verbose_name_plural = "رمزهای دوم"


class Notification(models.Model):
    recipient = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="دریافت‌کننده")
    message = models.CharField(max_length=255, verbose_name="پیام")
    link = models.URLField(null=True, blank=True, verbose_name="لینک")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"اعلان برای {self.recipient}"

    class Meta:
        verbose_name = "اعلان"
        verbose_name_plural = "اعلان‌ها"
