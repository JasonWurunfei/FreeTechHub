from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Likes
from django.contrib.contenttypes.models import ContentType
import datetime

def Postlikes(request,post_id,like_type):
    user = request.user
    post_type = ContentType.objects.get(app_label="blog", model="post")
    date = datetime.datetime.now()

    if like_type == "like":
        like_type = True
    else:
        like_type = False

    if user.is_authenticated:
        hasbeen_liked = Likes.objects.filter(        # 这里必须用filter来实现，get，filter区别
            user=user,
            content_type=post_type,
            object_id=post_id,
        )
        if hasbeen_liked:
            if like_type:
                hasbeen_liked.delete()
            else:
                obj = hasbeen_liked.get()
                obj.like_type = False
                obj.save()
        else:
            Likes.objects.create(
                user=user,
                content_type=post_type,
                object_id=post_id,
                date=date,
                like_type=like_type,
            )

        return HttpResponseRedirect(reverse('blog:post_detail', args=(post_id,)))

    else:
        return HttpResponseRedirect('accounts:login')
