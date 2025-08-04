# comments/urls.py
from django.urls import path
from comments.views import admin_panel_views as comment_views

urlpatterns = [
    # URL‌های مربوط به اپلیکیشن comments
    path('review-comments/', comment_views.review_comments, name='review_comments'),
    path('approve-comment/<int:comment_id>/', comment_views.approve_comment, name='approve_comment'),
    path('delete-comment/<int:comment_id>/', comment_views.delete_comment, name='delete_comment'),
    path('edit-comment/<int:comment_id>/', comment_views.edit_comment, name='edit_comment'),
]