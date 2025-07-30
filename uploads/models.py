from django.db import models
from django.utils.text import slugify
from .utils.upload import delete_file_from_arvan
import os  # برای جدا کردن نام فایل از مسیر

class MediaFile(models.Model):
    file = models.FileField(upload_to='uploads/', verbose_name="نام فایل")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="اسلاگ")
    is_minified = models.BooleanField(default=False, verbose_name="مینیفای")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ آپلود")

    def save(self, *args, **kwargs):
        # اگر اسلاگ خالی است، مقداردهی کن
        if not self.slug and self.file:
            filename = os.path.basename(self.file.name)
            name, _ = os.path.splitext(filename)  # حذف پسوند فایل
            base_slug = slugify(name)
            slug = base_slug
            i = 1
            while MediaFile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            delete_file_from_arvan(self.file.name)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'فایل'
        verbose_name_plural = 'فایل‌ها'
