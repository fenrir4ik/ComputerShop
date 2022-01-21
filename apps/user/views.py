from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import UpdateView

from apps.user.forms import RegistrationForm, LoginForm, ProfileChangeForm
from apps.user.models import User


class UserRegisterView(CreateView):
    """View is used to register a user"""
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    """View is used to authorize user"""
    template_name = 'login.html'
    form_class = LoginForm


class UserLogoutView(LoginRequiredMixin, View):
    """View is used to logout user"""

    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class ProfileChangeView(LoginRequiredMixin, UpdateView):
    """View is used to change user profile information in 'profile' section"""
    form_class = ProfileChangeForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
