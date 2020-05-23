import json
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from users.models import User
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from blog.models import Post
from .forms import ProfileForm, RechargeForm
from .models import Relationship, Coins_Operation
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
    user = get_object_or_404(User, id=id)
    user_info = get_object_or_404(User, id=id)
    self_user = request.user
    to_follow_user = get_object_or_404(User, id=id)

    if not Relationship.objects.filter(follower=request.user, following=to_follow_user).exists():
        show_button = "follow"
        if request.method == "POST":
            relationship = Relationship()
            relationship.following = User.objects.get(username=to_follow_user)
            relationship.follower = User.objects.get(username=self_user)
            relationship.save()

            return redirect('accounts:profile_account', id)
        else:
         #   all_lists = Relationship.objects.get(following_id=id)
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
    initial_data = {
        'user': user,
    }

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return render(request, 'registration/profile_account.html', {'user': user})
        else:
            return HttpResponse("The input of registration form is wrong. Please re-enter")
    elif request.method == 'GET':
        form = ProfileForm(initial=initial_data, instance=user)
        context = {'form': form,  'user': user}
        return render(request, 'registration/edit.html', context)
    else:
        return HttpResponse("ERROR")

def coins(request, id):
    user = User.objects.get(id=id)
    balance = user.coins
    return render(request, 'registration/profile_coins.html', locals())

def recharge_coins(request, id):
    profile = User.objects.get(id=id)
    if request.method == "POST":
        recharge_form = RechargeForm(request.POST)
        if recharge_form.is_valid():
            balance = profile.coins
            recharge_money = recharge_form.cleaned_data['coins']
            profile.coins = balance + recharge_money
            profile.save()

            Coins_Operation.objects.create(related_profile=profile, money=+recharge_money, reason="Recharge")
            return redirect('accounts:coins', id)
    else:
        recharge_form = RechargeForm()
        balance = profile.coins
        context = {
            'recharge_form': recharge_form,
            'user': profile,
            'balance': balance,
        }
        return render(request, 'registration/recharge_coins.html', context)

def transaction_records(request, id):
    user = User.objects.get(id=id)
    balance = user.coins
    operations = Coins_Operation.objects.filter(related_profile=user)
    return render(request, 'registration/coins_record.html', locals())
