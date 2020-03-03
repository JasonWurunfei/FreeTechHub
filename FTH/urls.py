"""FTH URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog.views import post, show, show_blog, edit_post, delete_post
from comment.views import comment
from likes.views import Postlikes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/<int:user_id>/', post),
    path('accounts/',include('accounts.urls', namespace='accounts')),
    path('',include('home.urls', namespace='home')),
    path('show/', show, name='show'),
    path('show_blog/<int:post_id>/', show_blog, name='post_detail'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', delete_post),
    path('<int:post_id>/<str:like_type>', Postlikes),
    path('<int:post_id>/', comment, name="comment_page"),
    path('markdownx/', include('markdownx.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

