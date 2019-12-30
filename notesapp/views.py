from django.shortcuts import render
from django.views.generic import ListView
from .models import Note


class HomepageView(ListView):
    template_name = 'notesapp/home.html'
    model = Note

