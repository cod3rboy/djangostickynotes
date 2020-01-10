from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import SiteUserCreationForm


class SiteUserCreateView(CreateView):
    model = get_user_model()
    template_name = 'accountsapp/signup.html'
    success_url = reverse_lazy('home')
    form_class = SiteUserCreationForm
