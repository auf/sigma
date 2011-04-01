# -*- encoding: utf-8 -*-

import os
from django import forms
from django.contrib import admin
from form_utils.forms import BetterModelForm
from datamaster_modeles.models import Discipline
from models import UserProfile, Note, Commentaire, Dossier, TypePiece, Piece
from dynamo.forms import PropertyForm
from dynamo.fields import FILE

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

################################################################################
# DOSSIER - PIECES
################################################################################

class TypePieceForm(BetterModelForm):
    """
    Il n'y a qu'un type possible de pièces dans ce cas : fichier.
    """
    class Meta:
        exclude = ('field_type',)
        model = TypePiece

    def save(self, commit=True):
        instance = super(TypePieceForm, self).save(commit)
        instance.field_type = FILE
        return instance

class PieceForm(PropertyForm):
    """
    Dans l'admin inline, on préserve le type défini par l'appel.
    """
    class Meta:
        exclude = ('type', )
        model = Piece
