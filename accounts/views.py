from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login, logout, authenticate
import datetime
def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("accounts:login")
	else:
		form = RegisterForm(request.POST)
	return render(request, 'registration/register.html', context={'form': form})