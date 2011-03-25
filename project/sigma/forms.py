# -*- encoding: utf-8 -*-

from django import forms
from django.contrib import admin
from form_utils.forms import BetterModelForm
from datamaster_modeles.models import Discipline
from models import UserProfile, Dossier, Note, Commentaire

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
