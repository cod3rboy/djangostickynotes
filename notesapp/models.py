from django.db import models
from django.conf import settings


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

    def __str__(self):
        """
        Returns string representation of Note Model Object
        :return: title of the note
        """
        return self.title
