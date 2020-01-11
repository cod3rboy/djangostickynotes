from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class SiteUser(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False,)
    email = models.EmailField(blank=False, unique=True,)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('profile')
