from django.contrib import admin
from . import models


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_on', 'updated_on', ]


# Register your models here.
admin.site.register(models.Note, NoteAdmin)
