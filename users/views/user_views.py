from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from users.models import Users
from comments.models import Comment
from comments.forms import CommentForm
from comments.email_utils import notify_admins
from django.contrib.auth.models import User

def home_view(request):
    print("User:", request.user)
    print("Is Authenticated:", request.user.is_authenticated)
    user = None

    # کاربر لاگین کرده با سشن (سیستم خودت)
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            user = None

    # کاربر گوگل
    elif request.user.is_authenticated:
        try:
            user = Users.objects.get(email=request.user.email)  # 👈 اتصال بر اساس ایمیل
        except Users.DoesNotExist:
            user = None

    if not user:
        return redirect("login")



    # ارسال کامنت
    # if request.method == "POST":
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.user = user
    #         comment.is_approved = False
    #         comment.save()
    #         notify_admins(comment)
    #         return redirect("home")
    # else:
    #     form = CommentForm()

    return render(request, "home.html", {
        "user": user,
        # "form": form,
        # ← اینجا ویرگول اضافه شد
    })


def user_detail(request, slug):
    user = get_object_or_404(Users, slug=slug)
    return render(request, 'user_detail.html', {'user': user})

# -----------------------------------------------------------------------------------------------------------
def ticket_view(request):
    user = None

    # کاربر لاگین کرده با سشن (سیستم خودت)
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            user = None

    # کاربر گوگل
    elif request.user.is_authenticated:
        try:
            user = Users.objects.get(email=request.user.email)  # 👈 اتصال بر اساس ایمیل
        except Users.DoesNotExist:
            user = None

    if not user:
        return redirect("login")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.is_approved = False
            comment.save()
            notify_admins(comment)
            return redirect("home")
    else:
        form = CommentForm()

    return render(request, "ticket.html", {
        "form": form,
    })