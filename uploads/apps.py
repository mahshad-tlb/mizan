from django.apps import AppConfig

class UploadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uploads'
    verbose_name = "مدیریت فایل‌های آپلود شده"  # 👈 نام فارسی برای نمایش در پنل ادمین
