from datetime import datetime

from django.contrib import auth
from django.contrib.auth import logout, login
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.views import LoginView
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


class GoodAddView(PermissionRequiredMixin, generic.CreateView):
    def has_permission(self):
        return self.request.user.groups.filter(name='sellers').exists()

    model = Good
    form_class = GoodAddForm
    success_url = reverse_lazy('goods')


class GoodUpdateView(PermissionRequiredMixin, generic.UpdateView):
    def has_permission(self):
        return self.request.user.groups.filter(name='sellers').exists()

    model = Good
    form_class = GoodUpdateForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('goods')


def about(request):
    return render(request, 'pages/about.html')


def contacts(request):
    return render(request, 'pages/contacts.html')


class RegisterUser(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'main/register.html'

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name='common users')
        user.groups.add(group)
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'


def logout_user(request):
    logout(request)
    return redirect('login')


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

