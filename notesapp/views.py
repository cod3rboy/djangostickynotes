from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Note, Color, Font
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site


class HomepageView(LoginRequiredMixin, ListView):
    template_name = 'notesapp/home.html'
    model = Note

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user).order_by('-created_on')

    def get_context_data(self, **kwargs):
        kwargs.update({
            'fonts': Font.objects.all(),
        })
        return super().get_context_data(**kwargs)


class NoteCreateView(LoginRequiredMixin, CreateView):
    template_name = 'notesapp/notes_new.html'
    model = Note
    form_class = forms.NoteCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        all_colors = Color.objects.all()
        kwargs.update({
            'featured_colors': all_colors.filter(featured=True),
            'colors': all_colors.filter(featured=False),
            'fonts': Font.objects.all(),
        })
        return super().get_context_data(**kwargs)


class NoteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'notesapp/notes_detail.html'
    model = Note
    slug_field = 'slug'

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        kwargs.update({
            'domain': get_current_site(request=self.request).domain,
            'protocol': 'https' if self.request.is_secure() else 'http',
        })
        return super().get_context_data(**kwargs)


class NoteEditView(LoginRequiredMixin, UpdateView):
    template_name = 'notesapp/notes_edit.html'
    model = Note
    form_class = forms.NoteUpdateForm
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        all_colors = Color.objects.all()
        kwargs.update({
            'featured_colors': all_colors.filter(featured=True),
            'colors': all_colors.filter(featured=False),
            'fonts': Font.objects.all(),
        })
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user, slug=self.kwargs['slug'])


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'notesapp/notes_delete.html'
    model = Note
    slug_field = 'slug'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user, slug=self.kwargs['slug'])


class SharedNoteDetailView(DetailView):
    template_name = 'notesapp/shared_note_detail.html'
    model = Note
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'domain': get_current_site(request=self.request).domain,
            'protocol': 'https' if self.request.is_secure() else 'http',
        })
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.model.objects.filter(slug=self.kwargs['slug'], shared=True)
