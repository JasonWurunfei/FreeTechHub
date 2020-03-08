from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class Likes(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    like_type = models.BooleanField()
    date= models.DateTimeField(auto_now_add=True)

    content_type= models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id= models.PositiveIntegerField()
    content_object= GenericForeignKey('content_type', 'object_id')
