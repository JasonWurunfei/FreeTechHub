from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.safestring import mark_safe
from markdown import markdown


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    #text = models.TextField()
    text = RichTextUploadingField()
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['date']

    def get_comment_text_md(self):
        return mark_safe(markdown(self.text))

    def __str__(self):
        return self.text

    def children(self):
        return Comments.objects.filter(parent=self)
    
