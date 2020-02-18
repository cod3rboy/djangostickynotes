from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.template.defaultfilters import slugify


# Color Model to represent background color of a sticky note
class Color(models.Model):
    """
    name - Human readable name of color to support visually impaired users.
    code - Hexadecimal representation of color
    """
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Font Model
class Font(models.Model):
    """
    name - Name of the font
    url - Link for the font file on Google Fonts Website
    alt - Name of alternate font to use in case first font fails to load
    """
    font_name = models.CharField(max_length=50, blank=False, null=False)
    font_url = models.URLField(blank=False, null=False)
    font_alt = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.font_name


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
    shared = models.BooleanField(blank=False, null=False, default=False)

    bg_color = models.ForeignKey(
        'Color',
        on_delete=models.DO_NOTHING,
    )

    font = models.ForeignKey(
        'Font',
        on_delete=models.DO_NOTHING,
        default="",
    )

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title) + "-" + get_random_string(25)
        else:
            self.slug = slugify(self.title) + self.slug[-26:]
        super(Note, self).save(*args, **kwargs)

    def get_short_title(self):
        title = str(self.title)
        length = 40
        short_title = str(title)[0:min(len(title), length)]
        if len(title) <= length:
            return short_title
        return short_title + ' ...'

    def get_short_text(self):
        text = str(self.text)
        length = 100
        short_text = str(text)[0:min(len(text), length)]
        if len(text) <= length:
            return short_text
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
