from django.shortcuts import render, get_object_or_404, redirect

from users.models import Users



def home_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect("login")

    user = Users.objects.get(id=user_id)
    return render(request, "home.html", {"username": user.username})


def user_detail(request, slug):
    user = get_object_or_404(Users, slug=slug)
    return render(request, 'user_detail.html', {'user': user})
