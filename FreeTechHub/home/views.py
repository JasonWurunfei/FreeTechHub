from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    return render(request, 'home/index.html')
def register(request):
    if request.method  != 'POST':
       form = UserCreationForm()
    else:
       form = UserCreationForm(data=request.POST)
       if form.is_valid():
          new_user = form.save()
          authenticated_user =  authenticate(username=new_user.username,password=request.POST['password1'])
          login(request,authenticated_user)
          return HttpResponseRedirect(reverse('home:login'))
    context = {'form': form}
    return render(request, 'home/login.html', context)
