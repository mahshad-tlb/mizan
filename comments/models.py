from django.db import models
from django.utils.text import slugify
from users.models import Users


class Comment(models.Model):
    content = models.TextField(verbose_name="متن نظر")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    slug = models.SlugField(verbose_name="اسلاگ", blank=True, null=True, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ['-created_at']

    def __str__(self):
        return f"نظر #{self.pk}"

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
