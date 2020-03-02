from django.urls import path ,include
from . import views
from django.contrib.auth.views import LoginView
from django.contrib import admin
from django.conf.urls import url
app_name = 'home'
urlpatterns = [
   
    path('', views.index, name='index'),
 
   
]
