from django.contrib import admin
from .models import  AdminEmail, Users
from django.core.mail import send_mail
from django.contrib import messages
from django import forms
from .models import Users, SecondaryPassword


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']





@admin.register(AdminEmail)
class AdminEmailAdmin(admin.ModelAdmin):
    list_display = ["subject", "created_at"]
    actions = ["send_email_to_all_users"]

    def send_email_to_all_users(self, request, queryset):
        for email_obj in queryset:
            subject = email_obj.subject
            message = email_obj.body
            from_email = "admin@example.com"
            recipient_list = list(Users.objects.values_list("email", flat=True))

            for recipient in recipient_list:
                send_mail(
                    subject,
                    "",
                    from_email,
                    [recipient],
                    html_message=message,
                    fail_silently=False,
                )
        self.message_user(request, "ایمیل‌ها با موفقیت ارسال شدند.", messages.SUCCESS)

    send_email_to_all_users.short_description = "ارسال ایمیل به همه کاربران"

@admin.register(SecondaryPassword)
class SecondaryPasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'password')
    search_fields = ('user__username',)