from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from apps.user.forms import RegistrationForm, LoginForm, ProfileChangeForm


class UserRegisterView(CreateView):
    """
    View is used to register a user
    """
    template_name = 'user/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')


class UserLoginView(LoginView):
    """
    View is used to authorize user
    """
    template_name = 'user/login.html'
    form_class = LoginForm


class UserLogoutView(LoginRequiredMixin, View):
    """
    View is used to logout user
    """
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class ProfileChangeView(LoginRequiredMixin, UpdateView):
    """
    View is used to change user profile information in 'profile' section
    """
    form_class = ProfileChangeForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('profile')
    success_message = "Профиль успешно изменен"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data()
        context['user_data'] = {'name': user.name, 'surname': user.surname, 'email': user.email}
        return context
