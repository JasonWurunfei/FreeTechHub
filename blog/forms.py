from django import forms
from markdownx.fields import MarkdownxFormField
from blog.models import Post, Category

class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=100)
    text = MarkdownxFormField()

    class Meta:
        model = Post
        fields = ['title', 'text']

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='category', max_length=250)
    content = forms.CharField(label='Introduction', max_length=500)

    class Meta:
        model = Category
        fields = ['name', 'content']
        
