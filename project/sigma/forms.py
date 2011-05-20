# -*- encoding: utf-8 -*-

import os
from django import forms
from django.contrib import admin
from django.forms.models import inlineformset_factory
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
        exclude = ('expert', )
        model = Note

class NoteExpertForm(inlineformset_factory(Dossier, Note,  extra=0, form=NoteForm)):
    pass


class CommentaireForm(BetterModelForm):
    class Meta:
        exclude = ('user', )
        model = Commentaire

class EvaluationForm(BetterModelForm):
    class Meta:
        fields = ('moyenne_academique', 'opportunite_regionale', )
        model = Dossier
        
class ExpertForm(forms.Form):
    experts = forms.ModelMultipleChoiceField(queryset=Expert.objects.all())

    def __init__(self, *args, **kwargs):
        self.dossiers = kwargs.pop('dossiers')
        super(ExpertForm, self).__init__(*args, **kwargs)


    def save(self):
        for d in self.dossiers:
            d.experts = self.cleaned_data.get('experts', [])
            d.save()
    


