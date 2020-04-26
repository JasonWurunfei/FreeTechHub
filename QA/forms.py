from django import forms
from markdownx.fields import MarkdownxFormField
from QA.models import Question, Answer


class QuestionForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=50)
    body = MarkdownxFormField()

    class Meta:
        model = Question
        fields = ['title',
                  'tags',
                  'body', ]

class AnswerForm(forms.ModelForm):
    content = MarkdownxFormField()

    class Meta:
        model = Answer
        fields = ['content', ]
