from datetime import datetime

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import request
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import generic

from main.forms import ProfileForm, ProfileFormset
from main.models import *


def index(request):
    return render(request, 'main/index.html',
                  context={'username': auth.get_user(request).username, 'turn_on_block': True})


class GoodListView(generic.ListView):
    model = Good
    template_name = 'main/goodlist.html'
    paginate_by = 10
    context_object_name = "searchres"

    def get_context_data(self, **kwargs):
        context = super(GoodListView, self).get_context_data(**kwargs)
        context['username'] = "123"
        tag = self.request.GET.get('tag')
        context['tag'] = tag
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.GET.get('tag')
        if tag:
            return queryset.filter(tag__tag_name=tag)
        return queryset


class GoodDetailView(generic.DetailView):
    model = Good


def about(request):
    return render(request, 'pages/about.html')


def contacts(request):
    return render(request, 'pages/contacts.html')


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    template_name = 'main/profile_update.html'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

