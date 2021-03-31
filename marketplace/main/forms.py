from django import forms
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.forms import TextInput, EmailInput, formset_factory

from .models import *


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email')


ProfileFormset = inlineformset_factory(User, Profile, fields='__all__', can_delete=False)
