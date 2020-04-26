from django import  forms
from markdownx.fields import MarkdownxFormField
from Q&A.

class QuestionForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=50)
    body = MarkdownxFormField()

    class Meta:
        model = Question
        fields = ['title', 'text']