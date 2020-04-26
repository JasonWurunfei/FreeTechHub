from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager
# from .models import User

class Question(models.Model):
    title = models.TextField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = MarkdownxField()
    tags = TaggableManager(blank=True)
    views = models.PositiveIntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('uploaded_at',)

    def __str__(self):
        return self.title

    def answer_number(self):
        answers = Answer.objects.filter(question_id=self.id)
        return len(answers)

    def type_id(self):
        question_type = ContentType.objects.get(app_label='QA', model='question')
        return question_type.id

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class Answer(models.Model):
    content = MarkdownxField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('answer_time',)

    def __str__(self):
        return self.content

