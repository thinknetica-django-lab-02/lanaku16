from django.contrib import auth
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html', context={'username': auth.get_user(request).username, 'turn_on_block': True})


def about(request):
    return render(request, 'pages/about.html')


def contacts(request):
    return render(request, 'pages/contacts.html')