from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Note
from django.urls import reverse_lazy


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


class NoteEditView(UpdateView):
    template_name = 'notesapp/notes_edit.html'
    model = Note
    fields = ('title', 'text')


class NoteDeleteView(DeleteView):
    template_name = 'notesapp/notes_delete.html'
    model = Note
    success_url = reverse_lazy('home')
