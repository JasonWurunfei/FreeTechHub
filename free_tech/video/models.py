from django.db import models

from POST.models import Post


def user_directory_path(instance, filename):
    print(instance)
    return 'media/videos/users/user_{0}/{1}'.format(instance.user.id, filename)

class Video(models.Model):
    vid_post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.FileField(upload_to=user_directory_path)