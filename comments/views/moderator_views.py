# comments/views/moderator_views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.apps import apps

from comments.forms import MessageForm
from comments.models import Message, Comment  # فرض بر وجود مدل Comment

User = get_user_model()
Notification = apps.get_model('user', 'Notification')


def is_moderator(user):
    return user.is_authenticated and not user.is_superuser


@user_passes_test(is_moderator)
def send_message_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = User.objects.filter(is_superuser=True).first()
            message.save()

            Notification.objects.create(
                recipient=message.recipient,
                message=f"New message from moderator: {message.subject}",
            )
            return redirect('moderator_dashboard')
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form})


@user_passes_test(is_moderator)
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()

    Notification.objects.create(
        recipient=User.objects.filter(is_superuser=True).first(),
        message=f"نظر ارسال‌شده توسط {comment.user} توسط {request.user} تأیید شد.",
        link=f"/admin/comments/comment/{comment.id}/change/"
    )

    return redirect('moderator_dashboard')
