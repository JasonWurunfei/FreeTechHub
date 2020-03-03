from django.shortcuts import render
from django.http import HttpResponseRedirect
from blog.models import Post

def searchView(request):
    keywords = request.GET.get('search')
    if not keywords:
        return HttpResponseRedirect('home:index')

    post_requested = Post.objects.filter(title__icontains=keywords)
    context ={
        'post_requested':post_requested
    }
    return render(request,'blog/searchResult.html',context=context)