from django import forms
from comment.models import Comments
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Comments
        fields = ('text',)
