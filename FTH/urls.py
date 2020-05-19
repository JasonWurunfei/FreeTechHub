from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from likes.views import Postlikes
from vote.views import QuestionVotes, AnswerVotes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('allauth.urls')),
    path('account/',include('accounts.urls', namespace='accounts')),
    path('', include('home.urls', namespace='home')),
    path('blog/', include(('blog.urls', 'blog' ), namespace='blog')),
    path('comment/', include(('comment.urls', 'comment'), namespace='comment')),
    path('like/<int:post_id>/<str:like_type>', Postlikes, name="post_like"),
    path('vote_question/<int:question_id>/<str:vote_type>', QuestionVotes, name="question_vote"),
    path('vote_answer/<int:answer_id>/<str:vote_type>', AnswerVotes, name="answer_vote"),
    path('markdownx/', include('markdownx.urls')),
    path('search/', include('haystack.urls')),
    path('QA/', include('QA.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

