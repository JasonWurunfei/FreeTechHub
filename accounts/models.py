from django.db import models
from users.models import User
from django.conf import settings

class Relationship(models.Model):
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_users', on_delete=models.CASCADE)
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower_users', on_delete=models.CASCADE)

class Coins_Operation(models.Model):
    related_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    money = models.IntegerField()
    operated_time = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=20, blank=True)
