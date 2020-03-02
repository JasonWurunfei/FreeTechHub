from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# Create your views here.
def index(request):
    return render(request, 'home/index.html')
