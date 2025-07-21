
from django.contrib import admin

from users.models import Users



@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'created_at', 'updated_at', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at', 'created_at', 'updated_at']