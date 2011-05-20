# -*- encoding: utf-8 -*-

import os
from django import forms
from django.contrib import admin
from form_utils.forms import BetterModelForm
from django.forms import ModelForm
from datamaster_modeles.models import Discipline
from models import UserProfile, Note, Commentaire, Dossier, Expert

################################################################################
# PROFIL - DISCIPLINES
################################################################################

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

################################################################################
# DOSSIER - EVALUATION
################################################################################

class NoteForm(BetterModelForm):
    class Meta:
        exclude = ('user', )
        model = Note

class CommentaireForm(BetterModelForm):
    class Meta:
        exclude = ('user', )
        model = Commentaire

class EvaluationForm(BetterModelForm):
    class Meta:
        fields = ('moyenne_academique', 'opportunite_regionale', )
        model = Dossier
        
class ExpertForm(forms.Form):
    expert = forms.ModelMultipleChoiceField(queryset=Expert.objects.all())
