from django import forms
from markdownx.fields import MarkdownxFormField
from blog.models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=100)
    text = MarkdownxFormField()

    class Meta:
        model = Post
        fields = ['title', 'text']
    
