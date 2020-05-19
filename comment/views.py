from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import CommentForm
from .models import Comments
from django.contrib.contenttypes.models import ContentType
import datetime

def create_comment(request, post_id):
    user = request.user

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = comment_form.cleaned_data.get('text')
            date = datetime.datetime.now()
            post_type = ContentType.objects.get(app_label="blog", model="post")

            Comments.objects.create(
            user=user,
            content_type=post_type,
            object_id=post_id,
            text=text,
            date=date,
            parent=None,
            )
            return redirect(reverse('blog:post_detail', args=(post_id,)))


def create_c_comment(request, comment_id):
    user = request.user
    comment = Comments.objects.get(id=comment_id)
    post_id = comment.object_id

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            text = comment_form.cleaned_data.get('text')
            date = datetime.datetime.now()
            post_type = ContentType.objects.get(app_label="blog", model="post")

            comment.status = False
            comment.save()
        
            Comments.objects.create(
                user=user,
                content_type=post_type,
                object_id=post_id,
                text=text,
                date=date,
                parent=comment,
            )
            return redirect(reverse('blog:post_detail', args=(post_id,)))
    else:
        comment.status = True
        comment.save()
        return redirect(reverse('blog:post_detail', args=(post_id,)))
