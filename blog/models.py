from django.contrib.auth.models import User
from django.db import models
from markdownx.utils import markdownify
from comment.models import Comments
from markdownx.models import MarkdownxField
from django.urls import reverse

class DateCreateModMixin(models.Model):
    class Meta:
        abstract=True

    mod_date = models.DateTimeField(auto_now_add=True)

class Post(DateCreateModMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    text = MarkdownxField()

    def formatted_markdown(self):
        return markdownify(self.text)

    def body_summary(self):
        return markdownify(self.text[:300] + "...")

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

def user_pic_directory_path(instance, filename):
    return 'photos/users/user_{0}/{1}'.format(instance.post.user.id, filename)

class Pic(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pic_comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=user_pic_directory_path)

def user_vid_directory_path(instance, filename):
    return 'videos/users/user_{0}/{1}'.format(instance.post.user.id, filename)

class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.FileField(upload_to=user_vid_directory_path)
