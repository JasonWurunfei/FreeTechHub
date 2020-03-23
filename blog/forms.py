from django import forms
from markdownx.fields import MarkdownxFormField
<<<<<<< HEAD
from blog.models import Post
=======
from blog.models import Post, Category
>>>>>>> 2ce616dfa3705438a07010d20711c384ed26b064

class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=100)
    text = MarkdownxFormField()

    class Meta:
        model = Post
        fields = ['title', 'text']
<<<<<<< HEAD
    
=======

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='category', max_length=250)

    class Meta:
        model = Category
        fields = ['name',]
>>>>>>> 2ce616dfa3705438a07010d20711c384ed26b064
