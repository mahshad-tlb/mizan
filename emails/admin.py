from django.contrib import admin
from .models import Email
from django.core.mail import send_mail
from users.models import Users


@admin.action(description="ارسال ایمیل انتخاب شده به همه کاربران")
def send_email_to_all(modeladmin, request, queryset):
    for email in queryset:
        subject = email.عنوان
        message = email.متن
        from_email = 'mahshad@mtlb.erfann31dev.ir'
        users = Users.objects.exclude(email='').values_list('email', flat=True)
        recipient_list = list(users)
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    modeladmin.message_user(request, "ایمیل‌ها با موفقیت ارسال شدند!")



@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['عنوان', 'اسلاگ', 'تاریخ_ایجاد', 'تاریخ_بروزرسانی']
    search_fields = ['عنوان', 'متن']
    readonly_fields = ['تاریخ_ایجاد', 'تاریخ_بروزرسانی', 'اسلاگ']
    ordering = ['-تاریخ_ایجاد']
    actions = [send_email_to_all]
