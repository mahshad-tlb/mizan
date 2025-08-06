from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = "مدیریت کاربران"  # 👈 نمایش نام فارسی در پنل ادمین
