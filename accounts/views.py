from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("accounts:login")
	else:
		form = RegisterForm(request.POST)
	return render(request, 'registration/register.html', context={'form': form})
