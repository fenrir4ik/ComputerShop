from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView

from apps.user.forms import RegistrationForm, LoginForm


class UserRegister(CreateView):
    """View is used to register a user"""
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')


class UserLogin(LoginView):
    """View is used to authorize user"""
    template_name = 'login.html'
    form_class = LoginForm


class UserLogout(LoginRequiredMixin, View):
    """View is used to logout user"""
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))
