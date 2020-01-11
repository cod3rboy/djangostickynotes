from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.template.defaultfilters import slugify


# Note Model
class Note(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notes',
    )
    slug = models.SlugField(blank=False, unique=True, null=True)

    class BackgroundColors(models.TextChoices):
        MAGENTA = '#17A2B8'
        RED = '#DC3545'
        GREEN = '#28A745'
        DARK_GRAY = '#343A40'
        BLUE = '#007BFF'
        GRAY = '#6C757D'

    bg_color = models.CharField(
        max_length=7,
        choices=BackgroundColors.choices,
        default=BackgroundColors.DARK_GRAY,
        blank=False,
        null=False,
    )

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title) + "-" + get_random_string(25)
        else:
            self.slug = slugify(self.title) + self.slug[-26:]
        super(Note, self).save(*args, **kwargs)

    def get_short_title(self):
        title = str(self.title)
        length = 25
        short_title = str(title)[0:min(len(title), length)]
        return short_title + ' ...'

    def get_short_text(self):
        text = str(self.text)
        length = 40
        short_text = str(text)[0:min(len(text), length)]
        return short_text + ' ...'

    def get_background_color(self):
        return self.bg_color

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
        return reverse('note_detail', kwargs={'slug': self.slug})
