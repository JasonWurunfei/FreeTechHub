from users.models import User
from django import forms

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('college_major', 'grade', 'avatar', 'bio')

class RechargeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('coins',)
