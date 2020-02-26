from django.urls import path ,include
from . import views
from django.contrib.auth.views import LoginView
from django.contrib import admin
from django.conf.urls import url
app_name = 'home'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='home/login.html'), name='login'),  
    path('', views.index, name='index'),
    path('register/', views.register, name='register'), 
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
   
]
