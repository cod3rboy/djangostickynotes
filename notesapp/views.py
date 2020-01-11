from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Note
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class HomepageView(LoginRequiredMixin, ListView):
    template_name = 'notesapp/home.html'
    model = Note

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user).order_by('-created_on')


class NoteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'notesapp/notes_new.html'
    model = Note
    fields = ('title', 'text',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'notesapp/notes_detail.html'
    model = Note
    slug_field = 'slug'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user, slug=self.kwargs['slug'])


class NoteEditView(LoginRequiredMixin, UpdateView):
    template_name = 'notesapp/notes_edit.html'
    model = Note
    fields = ('title', 'text')
    slug_field = 'slug'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user, slug=self.kwargs['slug'])


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'notesapp/notes_delete.html'
    model = Note
    slug_field = 'slug'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user, slug=self.kwargs['slug'])
