from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import request
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.views import generic

from main.forms import ProfileForm, UserForm, ProfileFormset
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


@login_required
@transaction.atomic
def update_profile(request, pk):
    user = User.objects.get(id=pk)
    #ProfileFormset = inlineformset_factory(User, Profile, fields=('birth_date',), can_delete=False)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        formset = ProfileFormset(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and formset.is_valid():
            u = user_form.save()
            for form in formset.forms:
                up = form.save(commit=False)
                up.user = u
                up.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        user_form = UserForm(instance=request.user)
        formset = ProfileFormset(instance=request.user.profile)
    return render(request, 'main/profile_update.html', locals())

