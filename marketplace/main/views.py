from datetime import datetime

from django.contrib import auth
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import generic

from main.models import Good


def index(request):
    return render(request, 'main/index.html',
                  context={'username': auth.get_user(request).username, 'turn_on_block': True})


class GoodListView(generic.ListView):
    model = Good
    template_name = 'main/goodlist.html'
    queryset = Good.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context['username'] = "123"
        return context


class GoodDetailView(generic.DetailView):
    model = Good


def about(request):
    return render(request, 'pages/about.html')


def contacts(request):
    return render(request, 'pages/contacts.html')
