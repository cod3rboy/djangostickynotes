from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from .models import Note


class HomepageView(ListView):
    template_name = 'notesapp/home.html'
    model = Note


class NoteCreateView(CreateView):
    template_name = 'notesapp/notes_new.html'
    model = Note
    fields = ('title', 'text', 'author')


class NoteDetailView(DetailView):
    template_name = 'notesapp/notes_detail.html'
    model = Note
