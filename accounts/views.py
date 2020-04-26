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
from .models import Profile, Relationship
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q

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
    id = id
    user = User.objects.get(id=id)
    user_info = User.objects.get(id=id)
    self_user = request.user
    to_follow_user = User.objects.get(id=id)

    if not Relationship.objects.filter(follower=request.user, following=to_follow_user).exists():
        show_button = "follow"
        if request.method == "POST":
            relationship = Relationship()
            relationship.following = User.objects.get(username=to_follow_user)
            relationship.follower = User.objects.get(username=self_user)
            relationship.save()

            return redirect('accounts:profile_account', id)
        else:
        #    all_lists = Relationship.objects.get(following_id=id)
         #   all_lists = user.following_users.all()
         #   relationship = Relationship.objects.all()
            all_lists = Relationship.objects.filter(following_id=id)
            followings =Relationship.objects.filter(follower_id=id)
         #   users = User.objects.all()
            return render(request, 'registration/profile_account.html', locals())
    else:
        show_button = "Unfollow"
        if request.method == "POST":
            relationship = Relationship.objects.get(Q(follower=self_user) & Q(following=to_follow_user))
            relationship.delete()
            return redirect('accounts:profile_account', id)
        else:
        #    all_lists = Relationship.objects.get(following_id=id)
         #   all_lists = user.following_users.all()
         #   relationship = Relationship.objects.all()
            all_lists = Relationship.objects.filter(following_id=id)
            followings = Relationship.objects.filter(follower_id=id)
         #   users = User.objects.all()
            return render(request, 'registration/profile_account.html', locals())



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
