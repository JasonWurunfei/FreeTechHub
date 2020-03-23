from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth.views import LoginView
from django.conf.urls import url
from django.contrib.auth import views as auth_views
app_name='accounts'
urlpatterns = [
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] 
