from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Skill(models.Model):
    """
    مهارت‌های موجود در سیستم
    """
    name = models.CharField(max_length=100, verbose_name='مهارت')

    class Meta:
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت‌ها'

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    """
    امتیاز هر کاربر برای هر مهارت
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'مهارت کاربر'
        verbose_name_plural = 'مهارت‌های کاربران'
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user} - {self.skill}: {self.score}"


class UserSkillFile(models.Model):
    """
    فایل اکسل اولیه برای پر کردن جدول مهارت‌ها
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='skill_file',
        verbose_name='کاربر'
    )
    file = models.FileField(
        upload_to='user_skills/', blank=True, verbose_name='فایل مهارت‌ها'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین به‌روزرسانی')

    class Meta:
        verbose_name = 'فایل مهارت کاربر'
        verbose_name_plural = 'فایل‌های مهارت کاربران'

    def __str__(self):
        return f'فایل مهارت {self.user}'
