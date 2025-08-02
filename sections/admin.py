from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Section
from .forms import SectionAdminForm

@admin.register(Section)
class SectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = SectionAdminForm
    list_display = ['title', 'parent', 'order']
    list_filter = ['parent']
