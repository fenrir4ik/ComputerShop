from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from apps.user.forms import RegistrationForm


class UserRegister(CreateView):
    """View for user registrations"""
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')


def login_(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect(reverse('index'))


@login_required
def logout_(request):
    logout(request)
    return redirect(reverse('index'))
