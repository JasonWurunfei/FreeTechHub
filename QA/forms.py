from django import forms
from markdownx.fields import MarkdownxFormField
from QA.models import Question, Answer, Rewarded_question, Rewarded_answer


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

class Rewarded_QuestionForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=50)
    body = MarkdownxFormField()
    reward_money = forms.IntegerField(label='rewarded_money')
    note = forms.CharField(label='note', max_length=50)

    class Meta:
        model = Rewarded_question
        fields = ['title',
                  'tags',
                  'body',
                  'reward_money',
                  'note', ]

class Rewarded_AnswerForm(forms.ModelForm):
    content = MarkdownxFormField()

    class Meta:
        model = Rewarded_answer
        fields = ['content', ]
