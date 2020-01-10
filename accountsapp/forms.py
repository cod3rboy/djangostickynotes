from django.contrib.auth import forms
from .models import SiteUser


class SiteUserCreationForm(forms.UserCreationForm):
    class Meta:
        model = SiteUser
        fields = ('first_name', 'last_name', 'email', 'username')
