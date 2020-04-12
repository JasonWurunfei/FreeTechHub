from django.contrib.auth.models import User
from django.db import models
from markdownx.utils import markdownify
from markdownx.models import MarkdownxField
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=500, null=True)

    class Meta:
        verbose_name = 'Category'
        # A human-readable name for the object, singular;
        # If this isn’t given, Django will use a munged version of the class name: CamelCase becomes camel case.
        verbose_name_plural = "Categories"
        # If this isn’t given, Django will use verbose_name + "s".
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('blog:post_by_category', args=[self.name])

    def __str__(self):
        return self.name

class DateCreateModMixin(models.Model):
    class Meta:
        abstract=True

    mod_date = models.DateTimeField(auto_now_add=True)

class Post(DateCreateModMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.SET_NULL, null=True)
    text = MarkdownxField()
    total_views = models.PositiveIntegerField(default=0)

    def body_summary(self):
        return markdownify(self.text[:300] + "...")

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

def user_vid_directory_path(instance, filename):
    return 'videos/users/user_{0}/{1}'.format(instance.post.user.id, filename)

class Video(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.FileField(upload_to=user_vid_directory_path)
