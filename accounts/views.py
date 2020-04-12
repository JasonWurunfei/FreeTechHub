import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from blog.models import Post
from .forms import ProfileForm
from .models import Profile
from django.views.decorators.csrf import csrf_protect


def is_owner(func):
    def check(request, *args, **kwargs):
        id = kwargs["id"]
        user = User.objects.get(id=id)
        if not (user.id == request.user.id):
            return render(request, 'permission.html')
        return func(request, *args, **kwargs)
    return check


@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    contents = Post.objects.filter(user=user)
    context = {
        'user': user,
        'contents': contents,
    }
    return render(request, 'registration/profile.html', context)


@login_required
def profile_account(request, id):
    user = User.objects.get(id=id)
    return render(request, 'registration/profile_account.html', {'user': user})


@login_required
@is_owner
def profile_edit(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)
    initial_data = {
        'user': user,
        'college_major': profile.college_major,
        'grade': profile.grade,
        'bio': profile.bio,
        'avatar': profile.avatar,
    }

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'registration/profile_account.html', {'user': user})
        else:
            return HttpResponse("The input of registration form is wrong. Please re-enter")
    elif request.method == 'GET':
        form = ProfileForm(initial=initial_data, instance=profile)
        context = {'form': form, 'profile': profile, 'user': user }
        return render(request, 'registration/edit.html', context)
    else:
        return HttpResponse("ERROR")
