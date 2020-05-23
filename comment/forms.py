from django import forms
from comment.models import Comments
from markdownx.fields import MarkdownxFormField
# from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CommentForm(forms.ModelForm):
    text = MarkdownxFormField()

    class Meta:
        model = Comments
        fields = ('text',)
