from django.shortcuts import render
from django.contrib import auth
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def my_profile_view(request):
    current_user = auth.get_user(request)
    profile = Profile.objects.get(user = current_user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance = profile)

    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        "profile":profile,
        "form":form,
        "confirm":confirm
    }
    return render(request, "profiles/main.html", context)