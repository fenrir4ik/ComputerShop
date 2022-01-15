from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


def login_(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user=authenticate(username=username, password=password)
    login(request, user)
    return redirect('/')


@login_required
def logout_(request):
    logout(request)
    return redirect('/')


def index(request):
    return HttpResponse(f'User if authenticated: {request.user.is_authenticated}')
