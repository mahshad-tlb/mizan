from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from comments.models import Comment
from comments.forms import CommentForm


def is_limited_admin(user):
    return user.is_authenticated and user.groups.filter(name="Limited Admin").exists()


@user_passes_test(is_limited_admin)
def review_comments(request):
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'comments/review_comments.html', {'comments': comments})


@user_passes_test(is_limited_admin)
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    return redirect('review_comments')


@user_passes_test(is_limited_admin)
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('review_comments')


@user_passes_test(is_limited_admin)
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('review_comments')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comments/edit_comment.html', {'form': form})