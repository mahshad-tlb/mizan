from .models import Message

def unread_messages_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_messages_count': unread_count}
    return {'unread_messages_count': 0}