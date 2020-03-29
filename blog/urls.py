from django.urls import include, path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('post/<int:user_id>/', views.post, name='post'),
    path('show/', views.show, name='show'),
    path('show_blog/<int:post_id>/', views.show_blog, name='post_detail'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('category/<int:category_id>/', views.post_by_category, name='post_by_category'),
    path('categories/<int:user_id>/', views.categories, name='categories'),
    path('add_category/<int:user_id>/', views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('remove_blog/<int:post_id>/', views.remove_blog, name='remove_blog'),
]
