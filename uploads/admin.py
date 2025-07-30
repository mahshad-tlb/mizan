from django.contrib import admin
from django.utils.html import format_html
from .models import MediaFile
from .forms import MediaFileAdminForm
from .utils.upload import delete_file_from_arvan, generate_presigned_url


class MediaFileAdmin(admin.ModelAdmin):
    form = MediaFileAdminForm
    list_display = ['file_link', 'is_minified', 'uploaded_at', 'download_link']
    readonly_fields = ['download_link']

    def file_link(self, obj):
        return obj.file.name
    file_link.short_description = "نام فایل"

    def download_link(self, obj):
        if obj.file and obj.file.name:
            url = generate_presigned_url(obj.file.name)
            if url:
                return format_html(f"<a href='{url}' target='_blank'>دانلود</a>")
            else:
                return "خطا در دریافت لینک"
        return "فایلی وجود ندارد"
    download_link.short_description = "دانلود فایل"

    def delete_model(self, request, obj):
        if obj.file and obj.file.name:
            delete_file_from_arvan(obj.file.name)
        super().delete_model(request, obj)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(MediaFile, MediaFileAdmin)
