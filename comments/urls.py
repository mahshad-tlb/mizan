from django.contrib import admin
from django.urls import path, include
from comments.admin_limited import limited_admin_site
from comments.views import admin_panel_views as comment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('limited-admin/', limited_admin_site.urls),
    path('review-comments/', comment_views.review_comments, name='review_comments'),
    path('approve-comment/<int:comment_id>/', comment_views.approve_comment, name='approve_comment'),
    path('delete-comment/<int:comment_id>/', comment_views.delete_comment, name='delete_comment'),
    path('edit-comment/<int:comment_id>/', comment_views.edit_comment, name='edit_comment'),
]