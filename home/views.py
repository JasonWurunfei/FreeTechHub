from django.shortcuts import render, redirect

from accounts.models import Profile
from blog.models import Post, Video, Category
from users.models import User
from django.core.paginator import Paginator
# Create your views here.
def index(request):
	texts = Post.objects.all()
	video = []
	user = request.user
	coins = Profile.objects.get(user=user).coins
	users = User.objects.all()
	paginator = Paginator(texts, 3)
	page = request.GET.get('page')
	articles = paginator.get_page(page)

	context = {
		'texts': texts,
		'user': user,
		'users': users,
		'video': video,
		'articles': articles,
		'coins': coins,
	}

	return render(request, 'home/index.html', context)
