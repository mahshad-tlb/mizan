from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('table/', views.skills_table, name='table'),  # صفحه جدول مهارت‌ها
    path('update/<int:skill_id>/', views.update_skill, name='update_skill'),
    path('user_skills/<str:filename>/', views.download_user_skill, name='download_user_skill'),
]
