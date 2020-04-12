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
from comment.views import comment
from likes.views import Postlikes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('allauth.urls')),
    path('account/',include('accounts.urls', namespace='accounts')),
    path('', include('home.urls', namespace='home')),
    path('blog/', include(('blog.urls', 'blog' ), namespace='blog')),
    path('<int:post_id>/', comment, name="comment_page"),
    path('<int:post_id>/<str:like_type>', Postlikes),
    path('markdownx/', include('markdownx.urls')),
    path('search/',include('haystack.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
