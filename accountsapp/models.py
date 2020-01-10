from django.db import models
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password', ]
