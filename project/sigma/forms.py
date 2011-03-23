# -*- encoding: utf-8 -*-

from django import forms
from django.contrib import admin
from form_utils.forms import BetterModelForm
from datamaster_modeles.models import Discipline
from models import UserProfile

class DisciplineForm(BetterModelForm):
    """
    """
    disciplines = forms.ModelMultipleChoiceField(
        queryset=Discipline.objects.all(),
        label="Disciplines", 
        widget=admin.widgets.FilteredSelectMultiple("disciplines", False),
        required=False,
        )

    class Meta:
        exclude = ('user', )
        model = UserProfile

