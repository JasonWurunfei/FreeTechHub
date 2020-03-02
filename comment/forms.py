from django import forms

from comment.models import Comments


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comments
        fields = ('text',)