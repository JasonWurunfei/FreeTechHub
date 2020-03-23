from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth.views import LoginView
from django.conf.urls import url
<<<<<<< HEAD
from django.contrib.auth import views as auth_views
app_name='accounts'
urlpatterns = [
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
=======
app_name='accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('profile/<int:user_id>/',views.profile, name='profile'),
>>>>>>> 2ce616dfa3705438a07010d20711c384ed26b064
] 
