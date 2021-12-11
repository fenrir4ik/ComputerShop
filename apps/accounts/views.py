import requests
from django.contrib.auth import logout as django_logout, login as django_login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import LoginForm, RegisterForm
from .utils import login_excluded
from ..api.utils import create_api_request_url


@login_excluded('index')
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            user = authenticate(username=user_data['username'], password=user_data['password'])
            if user:
                django_login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Неправильный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    django_logout(request)
    return redirect('index')


@login_excluded('index')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            url = create_api_request_url(request, reverse('User API:Registration'))
            response = requests.post(url, user_data)
            if response.status_code == 200:
                return redirect('login')
            else:
                json_body = response.json()
                if 'username' in json_body:
                    form.add_error('username', 'Пользователь с таким логином уже существует')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
