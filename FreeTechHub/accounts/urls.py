from django.urls import path ,include
from . import views
from django.contrib.auth.views import LoginView
from django.contrib import admin
from django.conf.urls import url
app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  
    path('register/', views.register, name='register'), 
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
   
]
