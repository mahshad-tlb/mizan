# superuser_views.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from comments.models import Message
from users.models import Notification
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@superuser_required
def notifications_view(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-created_at')
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {
        'messages': messages,
        'notifications': notifications,
    })
