from . import views
from django.urls import path ,include
from django.contrib import admin
from blog.views import searchView

app_name = 'home'
urlpatterns = [
	path('', views.index, name='index'),
	path('search_result_page/',searchView,name='search')

]
