from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import CommentForm
from .models import Comments
from django.contrib.contenttypes.models import ContentType
import datetime

def comment(request,post_id):
    user = request.user
    post_type = ContentType.objects.get(app_label="blog", model="post")
    date = datetime.datetime.now()
    parent_obj = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            text = comment_form.cleaned_data.get('text')
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comments.objects.filter(id=parent_id)
                if parent_qs.exists():
                    parent_obj = parent_qs.first()

            Comments.objects.create(
                user=user,
                content_type=post_type,
                object_id=post_id,
                text=text,
                date=date,
                parent=parent_obj,
            )
            return redirect(reverse('blog:post_detail', args=(post_id,)))
