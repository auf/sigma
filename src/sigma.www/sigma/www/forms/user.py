# -=- encoding: utf-8 -=-
from django import forms
from django.db import models
from django.forms.util import ValidationError, ErrorList
from django.forms.models import modelform_factory, modelformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class UserEditForm(forms.ModelForm):
    """Formulaire de modification des informations d'un utilisateur"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]
        
