from . import views
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views


app_name='accounts'
urlpatterns = [
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('LOGOUT/', auth_views.LogoutView.as_view(), name='Logout'),
    path('profile/edit/<int:id>/', views.profile_edit, name='edit'),
    path('profile/show/<int:id>/', views.profile_account, name='profile_account'),
]

