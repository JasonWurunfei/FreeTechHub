from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('post/<int:user_id>/', views.post, name='post'),
    path('show/', views.show, name='show'),
    path('show_blog/<int:post_id>/', views.show_blog, name='post_detail'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]