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
from django.urls import reverse_lazy
from django.views import generic

from main.forms import ProfileForm, UserForm, ProfileFormset, GoodAddForm, GoodUpdateForm
from main.models import Seller, Tag, Category, Good, Profile


def index(request):
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


class GoodAddView(generic.CreateView):
    model = Good
    form_class = GoodAddForm
    success_url = reverse_lazy('goods')


class GoodUpdateView(generic.UpdateView):
    model = Good
    form_class = GoodUpdateForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('goods')


def about(request):
    return render(request, 'pages/about.html')


def contacts(request):
    return render(request, 'pages/contacts.html')


def login(request):
    return render(request, 'main/login.html')


@login_required
@transaction.atomic
def update_profile(request, pk):
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

