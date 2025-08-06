from django.db import models
from django.utils.text import slugify
from users.models import Users
from django.contrib.auth import get_user_model

User = get_user_model()


class Comment(models.Model):
    content = models.TextField(verbose_name="متن نظر")
    is_approved = models.BooleanField(default=False, verbose_name="آیا تأیید شده؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    slug = models.SlugField(verbose_name="اسلاگ", blank=True, null=True, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='comments', null=True, verbose_name="کاربر")

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']

    def __str__(self):
        return f"نظر شماره {self.pk}"

    def save(self, *args, **kwargs):
        if not self.slug and self.content:
            base_slug = slugify(self.content[:30])  # فقط ۳۰ کاراکتر اول متن
            unique_slug = base_slug
            num = 1
            while Comment.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', null=True, verbose_name="فرستنده")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, verbose_name="گیرنده")
    subject = models.CharField(max_length=255, verbose_name="موضوع")
    content = models.TextField(verbose_name="متن پیام")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return f"پیام از {self.sender} به {self.recipient}"
