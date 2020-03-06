from . import views
from django.urls import path ,include
from django.contrib import admin
app_name = 'home'
urlpatterns = [
	path('', views.index, name='index'),
]
