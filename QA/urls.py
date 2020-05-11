from django.urls import path
from QA import views

app_name = 'QA'
urlpatterns = [
    path('post_question/<int:user_id>/', views.post_question, name='post_question'),
    path('questions/', views.Questions, name='questions'),
    path('show_question/<int:question_id>/', views.show_question, name='show_question'),
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('post_answer/<int:question_id>/', views.post_answer, name='post_answer'),
    path('tag_list/<slug:tag_slug>', views.questions_tagged, name='tag_list'),
]