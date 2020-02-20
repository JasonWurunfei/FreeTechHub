from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
app_name = 'home'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='home/login.html'), name='login'),  
    path('', views.index, name='index'),
    path('register/', views.register, name='register'), 
]
