from django.contrib import admin
from .models import UserSkillFile

@admin.register(UserSkillFile)
class UserSkillFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


