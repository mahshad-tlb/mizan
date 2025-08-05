from django.contrib import admin
from .models import Email
from django.core.mail import send_mail
from users.models import Users
from premailer import transform


@admin.action(description="ارسال ایمیل انتخاب شده به همه کاربران")
def send_email_to_all(modeladmin, request, queryset):
    for email in queryset:
        subject = email.title
        raw_html = email.body
        from_email = 'mahshad@mtlb.erfann31dev.ir'
        users = Users.objects.exclude(email='').values_list('email', flat=True)
        recipient_list = list(users)

        html_message = transform(raw_html)

        send_mail(
            subject=subject,
            message='',
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
            html_message=html_message
        )
    modeladmin.message_user(request, "ایمیل‌ها با موفقیت ارسال شدند!")


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at', 'updated_at']
    search_fields = ['title', 'body']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    ordering = ['-created_at']
    actions = [send_email_to_all]
