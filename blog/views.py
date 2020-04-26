import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from markdown import markdown
from blog.forms import PostForm, CategoryForm
from blog.models import Post, Video, Category
from comment.forms import CommentForm
from comment.models import Comments

def is_post_owner(func):
    def check(request, *args, **kwargs):
        post_id = kwargs["post_id"]
        post = Post.objects.get(id=post_id)
        if post.user_id != request.user.id:
            return HttpResponse("It is not yours ! You are not permitted !",
                                status=403)
        return func(request, *args, **kwargs)

    return check

def is_category_owner(func):
    def check(request, *args, **kwargs):
        category_id = kwargs["category_id"]
        category = Category.objects.get(id=category_id)
        if category.user_id != request.user.id:
            return HttpResponse("It is not yours ! You are not permitted !",
                                status=403)
        return func(request, *args, **kwargs)

    return check

def is_user_owner(func):
    def check(request, *args, **kwargs):
        user_id = kwargs["user_id"]
        if user_id != request.user.id:
            return HttpResponse("It is not yours ! You are not permitted !",
                                status=403)
        return func(request, *args, **kwargs)

    return check

@login_required
@is_user_owner
def post(request, user_id):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.text = form.cleaned_data['text']
            post.title = form.cleaned_data['title']
            post.user_id = user_id
            post.save()

            files2 = request.FILES.getlist('video')
            for file in files2:
                vid = Video(content=file, post=post)
                vid.save()

        return redirect('blog:show')

    else:
        form = PostForm()
        user = User.objects.get(id=user_id)
        context = {
            'user': user,
            'form': form,
        }
        return render(request, 'blog/blogEdit.html', context)

@login_required
def show(request):
    texts = Post.objects.all().order_by('-mod_date')
    video = []
    user = request.user
    users = User.objects.all()
    for i in range(len(texts)):
        videos = Video.objects.filter(post=texts[i].id)
        if len(videos) == 1:
            video.append(videos[0])
        if len(videos) == 0:
            video.append(None)
        if len(videos) >= 2:
            for q in range(len(videos)):
                video.append(videos[q])
    context = {
        'texts': texts,
        'user': user,
        'users': users,
        'video': video,
    }

    return render(request, 'blog/blogs.html', context)

@login_required
def show_blog(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    post_detail.total_views += 1
    post_detail.text = markdown(post_detail.text, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post_type = ContentType.objects.get(app_label='blog', model='post')
    users = User.objects.all()
    video = []
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
        'users': users,
        'post_detail': post_detail,
        'post_type_id': post_type.id,
        'video': video,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/blogDetail.html', context)

@login_required
@is_post_owner
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        new_post_form = PostForm(request.POST, instance=post)
        if new_post_form.is_valid():
            post = new_post_form.save(commit=False)
            post.title = new_post_form.cleaned_data['title']
            post.text = new_post_form.cleaned_data['text']
            post.mod_date = datetime.datetime.now()
            post.save()

            files2 = request.FILES.getlist('video')
            for file in files2:
                vid = Video(content=file, post_id=post_id)
                vid.save()

            return redirect(reverse('blog:post_detail', args=(post_id,)))
    else:
        new_post_form = PostForm(instance=post)
        context = {
            'new_post_form': new_post_form,
            'post_id': post_id,
        }
        return render(request, 'blog/blogEdit.html', context)

@login_required
@is_post_owner
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('blog:show')

@login_required
@is_post_owner
def remove_blog(request, post_id):
    removed_blog = Post.objects.get(user_id=request.user.id, id=post_id)
    category_id = removed_blog.category_id
    removed_blog.category_id = None
    removed_blog.save()
    return redirect(reverse('blog:post_by_category', args=(category_id,)))

@login_required
@is_user_owner
def categories(request, user_id):
    categories = Category.objects.filter(user_id=user_id)
    context = {
        'categories': categories,
        'user_id': user_id,
    }
    return render(request, 'blog/categories.html', context)

@login_required
@is_category_owner
def post_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if category.user_id == request.user.id:
        posts = Post.objects.filter(category_id=category_id)
        user = request.user

        context = {
            'posts': posts,
            'category': category,
            'user': user
        }
        return render(request, 'blog/post_by_category.html', context)

@login_required
@is_user_owner
def add_category(request, user_id):
    if request.method == 'POST':
        blog_title_list = request.POST.getlist('blog_title_list')
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.user_id = user_id
            category.name = category_form.cleaned_data['name']
            category.content = category_form.cleaned_data['content']
            category_exist = Category.objects.filter(name=category.name)
            if len(category_exist) == 1:
                warning = 'The category you have already created!'
                context = {
                    'category_form': category_form,
                    'warning': warning,
                }
                return render(request, 'blog/addCategory.html', context)
            elif len(category_exist) == 0:
                category.save()
                for blog_title in blog_title_list:
                    blog = Post.objects.get(user_id=user_id, title=blog_title)
                    blog.category_id = category.id
                    blog.save()
                return redirect(reverse('blog:categories', args=(user_id,)))

    else:
        category_form = CategoryForm()
        Blogs = Post.objects.filter(user_id=user_id)
        context = {
            'category_form': category_form,
            'user_id': user_id,
            'Blogs': Blogs,
        }
        return render(request, 'blog/addCategory.html', context)

@login_required
@is_category_owner
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    blog_title_list = request.POST.getlist('blog_title_list')
    user_id = request.user.id
    if request.method == 'POST':
        new_category_form = CategoryForm(request.POST, instance=category)
        if new_category_form.is_valid():
            new_category = new_category_form.save(commit=False)
            new_category.user_id = user_id
            new_category.name = new_category_form.cleaned_data['name']
            new_category.content = new_category_form.cleaned_data['content']
            new_category.save()
            for blog_title in blog_title_list:
                blog = Post.objects.get(user_id=user_id, title=blog_title)
                blog.category_id = new_category.id
                blog.save()
            return redirect(reverse('blog:categories', args=(user_id,)))
    else:
        new_category_form = CategoryForm(instance=category)
        Blogs = Post.objects.filter(user_id=user_id, category_id=None)
        context = {
            'new_category_form': new_category_form,
            'category_id': category_id,
            'Blogs': Blogs,
        }
        return render(request, 'blog/addCategory.html', context)

@login_required
@is_category_owner
def delete_category(request, category_id):
    user = request.user
    category = Category.objects.get(id=category_id)
    category.delete()
    return redirect(reverse('blog:categories', args=(user.id, )))
