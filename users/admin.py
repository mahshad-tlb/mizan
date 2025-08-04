# admin.py

from django.contrib import admin
from .models import AdminEmail, Users, SecondaryPassword, ActivationToken, Notification
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import openpyxl
import datetime
import os
from django.contrib.admin import SimpleListFilter
from comments.models import Comment, Message
from comments.admin import CommentInline, CommentAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


class HasCommentFilter(SimpleListFilter):
    title = 'وضعیت نظر'
    parameter_name = 'has_comment'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'دارای نظر'),
            ('no', 'بدون نظر'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(id__in=Comment.objects.values_list('user_id', flat=True))
        elif self.value() == 'no':
            return queryset.exclude(id__in=Comment.objects.values_list('user_id', flat=True))
        return queryset


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'is_active', 'is_staff']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['username', 'email', 'phone_number']
    list_filter = ['created_at', 'updated_at', HasCommentFilter]
    list_editable = ['email', 'phone_number', 'is_active', 'is_staff']
    inlines = [CommentInline]
    actions = ['export_as_excel', 'export_as_pdf']

    def export_as_excel(self, request, queryset):
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "کاربران"
        columns = ['شناسه', 'نام کاربری', 'ایمیل', 'شماره موبایل', 'رمز عبور', 'تاریخ ایجاد', 'تاریخ بروزرسانی']
        worksheet.append(columns)
        for user in queryset:
            worksheet.append([
                user.id,
                user.username,
                user.email,
                user.phone_number,
                user.password,
                user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"users_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename={filename}'
        workbook.save(response)
        return response

    export_as_excel.short_description = "خروجی اکسل فارسی"

    def export_as_pdf(self, request, queryset):
        users = list(queryset)
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'DejaVuSans.ttf')
        context = {
            'users': users,
            'font_path': font_path.replace('\\', '/'),
        }
        html = render_to_string("users_pdf_template.html", context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=users.pdf'
        pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
        if pisa_status.err:
            return HttpResponse('خطا در تولید فایل PDF', status=500)
        return response

    export_as_pdf.short_description = "خروجی PDF فارسی"


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


class SuperuserMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('subject', 'content', 'sender__username', 'recipient__username')
    ordering = ('-created_at',)

    def has_permission(self, request):
        return request.user.is_superuser

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['sender'].initial = request.user
        form.base_fields['sender'].widget.attrs['disabled'] = True
        limited_admins = User.objects.filter(groups__name='Limited Admin')
        form.base_fields['recipient'].queryset = limited_admins
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(recipient=request.user) | qs.filter(sender=request.user)
        return qs.none()


admin.site.register(Message, SuperuserMessageAdmin)
