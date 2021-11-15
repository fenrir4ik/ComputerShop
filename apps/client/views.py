import requests
from django.contrib.auth import authenticate, logout, login as django_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect

from apps.client.forms import LoginForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                django_login(request, user)
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_user(request):
    if request.user.is_active:
        logout(request)
    return redirect('/')

@login_required
def index(request):
    ses_id = request.session.session_key
    token = get_token(request)
    cookies = {'csrftoken': token,
               'sessionid': ses_id}
    response = requests.get('', cookies=cookies)
    return HttpResponse(f'CSRFToken {token} SessiongId {ses_id}')