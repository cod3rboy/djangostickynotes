from django.db import models
from django.conf import settings
from django.urls import reverse


# Note Model
class Note(models.Model):
    title = models.CharField(max_length=126)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
    )

    def get_short_title(self):
        title = str(self.title)
        length = 15
        short_title = str(title)[0:min(len(title), length)]
        return short_title + ' ...'

    def get_short_text(self):
        text = str(self.text)
        length = 20
        short_text = str(text)[0:min(len(text), length)]
        return short_text + ' ...'

    def __str__(self):
        """
        Returns string representation of Note Model Object
        :return: title of the note
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the absolute URL for model object
        :return: Absolute URL of model object
        """
        return reverse('note_detail', args=[self.pk])
