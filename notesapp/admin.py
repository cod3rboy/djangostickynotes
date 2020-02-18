from django.contrib import admin
from . import models


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'bg_color', 'font', 'created_on', 'updated_on', ]


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'featured']


class FontAdmin(admin.ModelAdmin):
    list_display = ['font_name', 'font_url', 'font_alt', ]


# Register your models here.
admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.Font, FontAdmin)
admin.site.register(models.Color, ColorAdmin)
