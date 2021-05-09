from datetime import datetime, timedelta
from typing import Dict, Any, Union

from django.contrib import auth
from django.contrib.auth import logout, login
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.db import transaction
from django.db.models import QuerySet
from django.forms import inlineformset_factory
from django.http import request, HttpRequest, HttpResponse
from django.http.response import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone

from main.forms import ProfileForm, UserForm, ProfileFormset, GoodAddForm, GoodUpdateForm, UseRegistForm
from main.models import Seller, Tag, Category, Good, Profile, Subscriber

import time

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from main.tasks import send_mail_about_new_good

from marketplace.celery import debug_task


def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        username = auth.get_user(request).username
        user_id = User.objects.get(username=username)
        profile = Profile.objects.get(pk=user_id)
        context = {'username': username,
                   'turn_on_block': True,
                   'profile': profile
                  }
    else:
        context = {'username': '',
                   'turn_on_block': True,
                   'profile': ''
                   }

    return render(request, 'main/index.html',
                  context=context
                  )


class GoodListView(generic.ListView):
    model = Good
    template_name = 'main/goodlist.html'
    paginate_by = 9
    context_object_name = "searchres"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super(GoodListView, self).get_context_data(**kwargs)
        tag = self.request.GET.get('tag')
        context['tag'] = tag
        return context

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        tag = self.request.GET.get('tag')
        if tag:
            return queryset.filter(tag__tag_name=tag)
        return queryset


class Search(generic.ListView):
    model = Good
    template_name = 'main/goodlist.html'
    paginate_by = 5
    context_object_name = "searchres"

    def get_context_data(self, *args, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self) -> QuerySet[Any]:
        q = self.request.GET.get('q')
        query = SearchQuery(q)
        vector = SearchVector('good_name', 'description', 'brand', 'composition', 'tag__tag_name', 'category__category_name')
        queryset = Good.objects.annotate(search=vector).filter(search=query)
        return queryset


class GoodDetailView(generic.DetailView):
    model = Good

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super(GoodDetailView, self).get_context_data(**kwargs)
        view_counter = cache.get('view_counter')
        if not view_counter:
            cache.set('view_counter', 0)
        view_counter = cache.incr('view_counter', delta=1, version=None)
        context['view_counter'] = view_counter
        return context


class GoodAddView(PermissionRequiredMixin, generic.CreateView):
    model = Good
    form_class = GoodAddForm
    success_url = reverse_lazy('goods')

    def has_permission(self) -> Union[Any, bool]:
        return self.request.user.groups.filter(name='sellers').exists()

    def form_valid(self, form):
        form.save()
        send_mail_about_new_good.delay(form.instance.id)
        return super().form_valid(form)


class GoodUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Good
    form_class = GoodUpdateForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('goods')

    def has_permission(self) -> Union[Any, bool]:
        return self.request.user.groups.filter(name='sellers').exists()


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/about.html')


def contacts(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/contacts.html')


def delivery(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/delivery.html')


def pay(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/pay.html')


class RegisterUser(generic.CreateView):
    form_class = UseRegistForm
    template_name = 'main/register.html'

    def form_valid(self, form) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
        user = form.save()
        group = Group.objects.get(name='common users')
        user.groups.add(group)
        email = EmailMessage(
            'Спасибо за регистрацию на сайте',
            'Вы прошли регистрацию на сайте Marketplace',
            to=[user.email])
        email.send()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')


@login_required
@transaction.atomic
def update_profile(request: HttpRequest, pk: int) -> HttpResponse:
    user = User.objects.get(id=pk)
    #ProfileFormset = inlineformset_factory(User, Profile, fields=('birth_date',), can_delete=False)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        formset = ProfileFormset(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and formset.is_valid():
            data_user = user_form.save()
            for form in formset.forms:
                data_user_form = form.save(commit=False)
                data_user_form.user = data_user
                data_user_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        user_form = UserForm(instance=request.user)
        formset = ProfileFormset(instance=request.user.profile)
    return render(request, 'main/profile_update.html', locals())
