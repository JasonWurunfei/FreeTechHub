from django.urls import path
from comment import views

app_name = 'comment'
urlpatterns = [
    path('new_comment/<int:post_id>', views.create_comment, name="create_comment"),
    path('new_c_comment/<int:comment_id>', views.create_c_comment, name="create_c_comment"),
]
