import django_jalali.db.models as jmodels
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import logging

logger = logging.getLogger(__name__)

class Email(models.Model):
    title = models.CharField("عنوان", max_length=100)
    body = RichTextField("متن")
    slug = models.SlugField("اسلاگ", unique=True, blank=True)
    created_at = jmodels.jDateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = jmodels.jDateTimeField("تاریخ بروزرسانی", auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if not self.slug:
            base_slug = slugify(self.title or "")
            slug = base_slug
            counter = 1
            while Email.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

        if is_new:
            logger.info(f"ایمیل جدید با عنوان '{self.title}' ایجاد شد.")
        else:
            logger.info(f"ایمیل با عنوان '{self.title}' به‌روزرسانی شد.")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "ایمیل"
        verbose_name_plural = "ایمیل‌ها"
