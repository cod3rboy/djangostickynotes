from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class SiteUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', ]


# Register your models here.
admin.site.register(models.SiteUser, SiteUserAdmin)
