from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


class UserCreateView(CreateView):
    model = get_user_model()
    template_name = 'accountsapp/signup.html'
    success_url = reverse_lazy('home')
    fields = ('first_name', 'last_name', 'username', 'email', 'password')
