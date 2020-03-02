from django.urls import path, include

from django.contrib import admin
from . import views

from django.contrib.auth.views import LoginView
from django.conf.urls import url
app_name='accounts'
urlpatterns = [
    path('resigister/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
] 
