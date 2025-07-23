from django.shortcuts import render, get_object_or_404, redirect
from users.models import Users
from comments.models import Comment
from comments.forms import CommentForm
from comments.email_utils import notify_admins

def home_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect("login")

    user = Users.objects.get(id=user_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user  # فرض شده که فیلد user در مدل Comment به مدل Users اشاره دارد
            comment.is_approved = False  # کامنت تا تایید ناظر غیر فعال باشد
            comment.save()
            notify_admins(comment)

            return redirect("home")
    else:
        form = CommentForm()

    return render(request, "home.html", {
        "username": user.username,
        "form": form
    })


def user_detail(request, slug):
    user = get_object_or_404(Users, slug=slug)
    return render(request, 'user_detail.html', {'user': user})
