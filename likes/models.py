from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class Likes(models.Model):
    user = models.ForeignKey(User,models.CASCADE, null=True)
    like_type = models.BooleanField()     # 0 >>>likes  1 >>>undo
    date= models.DateTimeField(auto_now_add=True)

    content_type= models.ForeignKey(ContentType, on_delete=models.CASCADE) # ForeignKey(关联类，on_delete类型)，返回一个类，而ContentType(app_label,model_name)
                                                                            # 来取出一个类
    object_id= models.PositiveIntegerField()
    content_object= GenericForeignKey('content_type', 'object_id')        #对象 + object_id ，genreicF 返回一个实例—— 实例化

# 所以创建一个Likes实例，需要
# user = user
# ContentType = ContentType(app_label,model_name) -- 从而得到contenttype
# content_object = object_id + contenttype
