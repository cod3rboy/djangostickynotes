from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class SiteUser(AbstractUser):
    first_name = models.CharField(max_length=50, blank=False,)
    email = models.EmailField(blank=False, unique=True,)

    class Gender(models.TextChoices):
        MALE = 'm'
        FEMALE = 'f'
        TRANSGENDER = 't'

    gender = models.CharField(max_length=1, choices=Gender.choices, blank=False, default=Gender.MALE)

    def get_gender(self):
        if self.gender == SiteUser.Gender.MALE:
            return 'Male'
        elif self.gender == SiteUser.Gender.FEMALE:
            return 'Female'
        else:
            return 'Transgender'

    def is_male(self):
        return self.gender == SiteUser.Gender.MALE

    def is_female(self):
        return self.gender == SiteUser.Gender.FEMALE

    def is_transgender(self):
        return self.gender == SiteUser.Gender.TRANSGENDER

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('profile')
