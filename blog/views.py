import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from markdown import markdown

from blog.forms import PostForm, CategoryForm
from blog.models import Post, Pic, Video, Category
from comment.forms import CommentForm
from comment.models import Comments

def post(request, user_id):
    if request.method == "POST":
        form = PostForm(request.POST)
        category_form = CategoryForm(request.POST)
        if form.is_valid():
            if category_form.is_valid():
                category = category_form.save(commit=False)
                category.name = category_form.cleaned_data['name']
                category_exist = Category.objects.filter(name=category.name)
                if len(category_exist) == 1:
                    category_id = Category.objects.get(name=category.name)
                elif len(category_exist) == 0:
                    category_form.save()
                    category_id = Category.objects.get(name=category.name)

                post = form.save(commit=False)
                post.text = form.cleaned_data['text']
                post.title = form.cleaned_data['title']
                post.category = category_id
                post.user_id = user_id
                post.save()

                files1 = request.FILES.getlist('img')
                for file in files1:
                    img = Pic(image=file, post=post)
                    img.save()
                files2 = request.FILES.getlist('video')
                for file in files2:
                    vid = Video(content=file, post=post)
                    vid.save()

        return redirect('blog:show')

    else:
        form = PostForm()
        category_form = CategoryForm()
        user = User.objects.get(id=user_id)
        context = {
            'user': user,
            'form': form,
            'category_form': category_form,
        }
        return render(request, 'blog/blogEdit.html', context)

def edit_post(request, post_id, category_id):
    post = get_object_or_404(Post, pk=post_id)
    category = get_object_or_404(Category, pk=category_id)
    if request.method == "POST":
        new_post_form = PostForm(request.POST, instance=post)
        new_category_form = CategoryForm(request.POST, instance=category)
        if new_post_form.is_valid() and new_category_form.is_valid():
            category = new_category_form.save(commit=False)
            category.name = new_category_form.cleaned_data['name']
            category_exist = Category.objects.filter(name=category.name)
            if len(category_exist) == 1:
                category_id = Category.objects.get(name=category.name)
            elif len(category_exist) == 0:
                new_category_form.save()
                category_id = Category.objects.get(name=category.name)

            post = new_post_form.save(commit=False)
            post.title = new_post_form.cleaned_data['title']
            post.text = new_post_form.cleaned_data['text']
            post.category = category_id
            post.mod_date = datetime.datetime.now()
            post.save()

            files1 = request.FILES.getlist('img')
            for file in files1:
                img = Pic(image=file, post_id=post_id)
                img.save()
            files2 = request.FILES.getlist('video')
            for file in files2:
                vid = Video(content=file, post_id=post_id)
                vid.save()

            return redirect(reverse('blog:post_detail', args=(post_id,)))
    else:
        new_post_form = PostForm(instance=post)
        new_category_form = CategoryForm(instance=category)
        context = {
            'new_post_form': new_post_form,
            'post_id': post_id,
            'new_category_form': new_category_form,
            'category_id': category_id,
        }
        return render(request, 'blog/blogEdit.html', context)

def delete_post(reqeust, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('blog:show')

def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }

    return render(request, 'blog/categories.html', context)

def post_by_category(request, category_id):
    categories = Category.objects.all()
    posts = Post.objects.all()
    users = User.objects.all()
    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        post = posts.filter(category=category)

        context = {
            'categories': categories,
            'post': post,
            'category': category,
            'users': users,
        }
        return render(request, 'blog/post_by_category.html', context)

def show(request):
    texts = Post.objects.all().order_by('-mod_date')
    img=[]
    video=[]
    user = request.user
    users= User.objects.all()
    for i in range(len(texts)):
        imgs = Pic.objects.filter(post=texts[i].id)
        if len(imgs) == 1:
            img.append(imgs[0])
        if len(imgs) == 0:
            img.append(None)
        if len(imgs) >= 2:
            for p in range(len(imgs)):
                img.append(imgs[p])

        videos = Video.objects.filter(post=texts[i].id)
        if len(videos) == 1:
            video.append(videos[0])
        if len(videos) == 0:
            video.append(None)
        if len(videos) >= 2:
            for q in range(len(videos)):
                video.append(videos[q])
    context = {
        'img': img,
        'texts': texts,
        'user': user,
        'users': users,
        'video': video,
    }

    return render(request, 'blog/blogs.html', context)

def show_blog(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    post_detail.text = markdown(post_detail.text,extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post_type = ContentType.objects.get(app_label='blog', model='post')
    users = User.objects.all()
    user = User.objects.get(id = post_detail.user_id)
    img=[]
    video=[]

    imgs = Pic.objects.filter(post=post_detail.id)
    if len(imgs) == 1:
        img.append(imgs[0])
    if len(imgs) == 0:
        img.append(None)
    if len(imgs) >= 2:
        for p in range(len(imgs)):
            img.append(imgs[p])

    videos = Video.objects.filter(post=post_detail.id)
    if len(videos) == 1:
        video.append(videos[0])
    if len(videos) == 0:
        video.append(None)
    if len(videos) >= 2:
        for q in range(len(videos)):
            video.append(videos[q])

    comments = Comments.objects.filter(object_id=post_id, parent=None)
    comment_form = CommentForm()
    
    context = {
        'img': img,
        'user': user,
        'users': users,
        'post_detail': post_detail,
        'post_type_id': post_type.id,
        'video': video,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/blogDetail.html', context)

