from django.shortcuts import render, redirect
from blog.models import Post, Video, Category
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# Create your views here.
def index(request):
	texts = Post.objects.all()
	video = []
	user = request.user
	users = User.objects.all()
	paginator = Paginator(texts, 3)
	page = request.GET.get('page')
	articles = paginator.get_page(page)

	context = {
		'texts': texts,
		'user': user,
		'users': users,
		'video': video,
		'articles': articles
	}

	return render(request, 'home/index.html', context)
