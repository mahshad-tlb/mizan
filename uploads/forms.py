from django import forms
from .models import MediaFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from .utils.upload import upload_file_to_arvan, delete_file_from_arvan


class MediaFileAdminForm(forms.ModelForm):
    upload = forms.FileField(required=False, label="آپلود فایل جدید")

    class Meta:
        model = MediaFile
        fields = ['is_minified']

    def recursive_minify(self, image_file, max_kb=300):
        image = Image.open(image_file)
        image = image.convert("RGB")
        qualities = (85, 40, 10)

        for q in qualities:
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=q)
            size_kb = buffer.getbuffer().nbytes / 1024

            if size_kb <= max_kb:
                buffer.seek(0)
                return InMemoryUploadedFile(
                    buffer,
                    None,
                    f"min_{getattr(image_file, 'name', 'image.jpg')}",
                    'image/jpeg',
                    buffer.getbuffer().nbytes,
                    None
                )

        buffer.seek(0)
        return InMemoryUploadedFile(
            buffer,
            None,
            f"min_{getattr(image_file, 'name', 'image.jpg')}",
            'image/jpeg',
            buffer.getbuffer().nbytes,
            None
        )

    def save(self, commit=True):
        upload_file = self.cleaned_data.get("upload")
        is_minified = self.cleaned_data.get("is_minified")
        instance = super().save(commit=False)

        if upload_file:
            # حذف فایل قبلی از آروان در صورت وجود
            if instance.pk and instance.file:
                delete_file_from_arvan(instance.file.name)

            # مینیفای تصویر اگر گزینه فعال باشد و نوع فایل تصویر باشد
            if is_minified and upload_file.name.lower().endswith(('jpg', 'jpeg', 'png', 'webp')):
                upload_file = self.recursive_minify(upload_file)

            path = f"uploads/{upload_file.name}"
            success = upload_file_to_arvan(upload_file, path)
            if success:
                instance.file.name = path
            else:
                raise forms.ValidationError("خطا در آپلود فایل")

        if commit:
            instance.save()
        return instance
