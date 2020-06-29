import datetime
from django.contrib.auth.decorators import login_required
from users.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from markdown import markdown
from taggit.models import Tag
from blog.forms import PostForm, CategoryForm
from blog.models import Post, Video, Category
from accounts.models import Relationship
from comment.forms import CommentForm
from comment.models import Comments
from django.db.models import Q

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
            form.save_m2m()

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
    common_tags = Post.tags.most_common()[:4]
    user = request.user
    users = User.objects.all()

    context = {
        'texts': texts,
        'user': user,
        'users': users,
        'common_tags': common_tags,
    }

    return render(request, 'blog/blogs.html', context)

@login_required
def show_blog(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    markdown_extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ]
    post_detail.text = markdown(post_detail.text, extensions=markdown_extensions)
    post_type = ContentType.objects.get(app_label='blog', model='post')

    comments = Comments.objects.filter(object_id=post_id, parent=None)
    for comment in comments:
        comment.text = markdown(comment.text, extensions=markdown_extensions)
        child_comments = comment.children()
        print(child_comments)
        for child_comment in child_comments:
            child_comment.text = markdown(child_comment.text, extensions=markdown_extensions)
    comment_form = CommentForm()

    post = Post.objects.get(id=post_id)
    id = post.user_id
    user = User.objects.get(id=id)
    self_user = request.user
    user_info = User.objects.get(id=id)
    to_follow_user = User.objects.get(id=id)

    context = {
        'post_detail': post_detail,
        'post_type_id': post_type.id,
        'comments': comments,
        'comment_form': comment_form,
        'post': post,
        'user': user,
        'self_user':self_user,
        'user_info': user_info,
    }

    if not Relationship.objects.filter(follower=request.user, following=to_follow_user).exists():
        show_button = "follow"
        if request.method == "POST":
            relationship = Relationship()
            relationship.following = User.objects.get(username=to_follow_user)
            relationship.follower = User.objects.get(username=self_user)
            relationship.save()
            return redirect('blog:post_detail', post_id)
        else:
            all_lists = Relationship.objects.filter(following_id=id)
            followings = Relationship.objects.filter(follower_id=id)
            context.update({
                'show_button': show_button,
                'all_lists': all_lists,
                'followings': followings,
            })
            return render(request, 'blog/blogDetail.html', context)

    else:

        show_button = "Unfollow"
        if request.method == "POST":
            relationship = Relationship.objects.get(Q(follower=self_user) & Q(following=to_follow_user))
            relationship.delete()
            context.update({
                'show_button': show_button,
            })
            return redirect('blog:post_detail', post_id)

        else:
            all_lists = Relationship.objects.filter(following_id=id)
            followings = Relationship.objects.filter(follower_id=id)

            context.update({
                'show_button': show_button,
                'all_lists': all_lists,
                'followings': followings,
            })
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
    return redirect(reverse('blog:show'))

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

@login_required
def blogs_tagged(request, tag_slug=None):
    blogs = Post.objects.all()
    # tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        blog_list = blogs.filter(tags__in=[tag])

        context = {
            'tag': tag,
            'blog_list': blog_list,
        }
        return render(request, 'blog/tags_list.html', context)