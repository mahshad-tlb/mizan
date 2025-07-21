import django_jalali.db.models as jmodels
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import logging

logger = logging.getLogger(__name__)

class Email(models.Model):
    عنوان = models.CharField("عنوان", max_length=100)
    متن = RichTextField("متن")
    اسلاگ = models.SlugField("اسلاگ", unique=True, blank=True)
    تاریخ_ایجاد = jmodels.jDateTimeField("تاریخ ایجاد", auto_now_add=True)
    تاریخ_بروزرسانی = jmodels.jDateTimeField("تاریخ بروزرسانی", auto_now=True)

    def save(self, *args, **kwargs):
        if not self.اسلاگ:
            self.اسلاگ = slugify(self.عنوان)
        is_new = False
        if self.pk is None:
                is_new = True
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"ایمیل جدید با عنوان '{self.عنوان}' ایجاد شد.")
        else:
            logger.info(f"ایمیل با عنوان '{self.عنوان}' به‌روزرسانی شد.")

    def __str__(self):
        return self.عنوان
