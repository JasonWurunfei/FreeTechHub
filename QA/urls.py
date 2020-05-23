from django.urls import path
from QA import views

app_name = 'QA'
urlpatterns = [
    path('post_question/<int:user_id>/', views.post_question, name='post_question'),
    path('reward_question/<int:user_id>/', views.reward_question, name='reward_question'),
    path('questions/', views.Questions, name='questions'),
    path('show_question/<int:question_id>/', views.show_question, name='show_question'),
    path('show_r_question/<int:question_id>/', views.show_r_question, name='show_r_question'),
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('edit_r_question/<int:question_id>/', views.edit_r_question, name='edit_r_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('delete_r_question/<int:question_id>/', views.delete_r_question, name='delete_r_question'),
    path('post_answer/<int:question_id>/', views.post_answer, name='post_answer'),
    path('post_r_answer/<int:question_id>/', views.post_r_answer, name='post_r_answer'),
    path('edit_r_answer/<int:r_answer_id>/', views.edit_r_answer, name="edit_r_answer"),
    path('delete_r_answer/<int:r_answer_id>/', views.delete_r_answer, name="delete_r_answer"),
    path('accept/<int:r_answer_id>/', views.accept_answer, name='accept_answer'),
    path('tag_list/<slug:tag_slug>', views.questions_tagged, name='tag_list'),
]