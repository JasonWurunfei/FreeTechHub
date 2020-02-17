from django.db import models

from POST.models import Post

def user_directory_path(instance, filename):
    print(instance)
    return 'media/photos/users/user_{0}/{1}'.format(instance.user.id, filename)

class Pic(models.Model):
    pic_post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    pic_comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path)
