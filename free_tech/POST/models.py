from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.CharField(max_length=200)
    post_date = models.DateTimeField(auto_now_add=True)