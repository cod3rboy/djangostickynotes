from django.forms import ModelForm
from . import models


class NoteCreateForm(ModelForm):
    class Meta:
        model = models.Note
        fields = ('title', 'text', 'shared', 'bg_color', 'font')


class NoteUpdateForm(ModelForm):
    class Meta:
        model = models.Note
        fields = ('title', 'text', 'shared', 'bg_color', 'font')
