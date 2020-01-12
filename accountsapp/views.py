from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from .forms import SiteUserCreationForm, SiteUserChangeForm


class SiteUserCreateView(CreateView):
    """
    View for user signup page
    """
    model = get_user_model()
    template_name = 'accountsapp/signup.html'
    success_url = reverse_lazy('home')
    form_class = SiteUserCreationForm


class SiteUserProfileView(LoginRequiredMixin, TemplateView):
    """
    View for user profile page
    """
    model = get_user_model()
    template_name = 'accountsapp/profile.html'

    def get_context_data(self, **kwargs):
        """
        Returns the context data to be passed to template
        :param kwargs: keyword arguments received from url
        :return: updated keyword arguments containing authenticated user object
        """
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            self.model.__name__.lower(): get_object_or_404(self.model, username=self.request.user.username)
        })
        return kwargs


class SiteUserProfileChangeView(LoginRequiredMixin, UpdateView):
    """
    View to change user profile
    """
    model = get_user_model()
    template_name = 'accountsapp/profile_change.html'
    success_url = reverse_lazy('profile')
    form_class = SiteUserChangeForm

    def get_object(self, queryset=None):
        """
        Return the user to be passed to template
        """
        return get_object_or_404(get_user_model(), username=self.request.user.username)
