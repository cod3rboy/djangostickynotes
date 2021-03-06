from django.contrib.auth import forms
from django.forms import ModelForm
from .models import SiteUser


class SiteUserCreationForm(forms.UserCreationForm):
    class Meta:
        model = SiteUser
        fields = ('first_name', 'last_name', 'gender', 'email', 'username')


class SiteUserChangeForm(ModelForm):
    class Meta:
        model = SiteUser
        fields = ('first_name', 'last_name', 'gender', 'email')
