from datetime import datetime

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms import TextInput, EmailInput, formset_factory

from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date',)

    def __init__(self, *args, user, **kwargs):
        self.fields['birth_date'] = forms.DateField(widget=forms.SelectDateWidget(), label='Дата рождения')

class ProfileFormset (forms.inlineformset_factory(User, Profile, fields=('birth_date',), can_delete=False)):
    def __init__(self, *args, **kwargs):
        self.__initial = kwargs.pop('initial', [])
        super(ProfileFormset, self).__init__(*args, **kwargs)

    def clean(self):
        super(ProfileFormset, self).clean()

        for form in self.forms:
            data = form.cleaned_data['birth_date']
            birth_date_delta = datetime.now().date().year - data.year
            if birth_date_delta < 18:
                form.add_error('birth_date', 'Сайт доступен от 18 лет')
                raise forms.ValidationError('Доступ ограничен !')
            return data
