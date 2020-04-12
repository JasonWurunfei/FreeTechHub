from ckeditor.widgets import CKEditorWidget
from django import forms
from comment.models import Comments

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Comments
        fields = ('text',)
