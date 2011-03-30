# -*- encoding: utf-8 -*-

import os
from django import forms
from django.contrib import admin
from form_utils.forms import BetterModelForm
from datamaster_modeles.models import Discipline
from models import UserProfile, Dossier, Note, Commentaire, Piece, TYPE_PIECES
from fields import PIECE_STORAGE

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

class PieceForm(forms.ModelForm):
    class Meta:
        fields = ('valeur', )
        model = Piece

    def __init__(self, *args, **kwargs):
        """
        Dynamically add each of the form fields for the given form model 
        instance and its related field model instances.
        """
        super(PieceForm, self).__init__(*args, **kwargs)
        try:
            code_type_champs = self.instance.type.field_type
            class_type = TYPE_PIECES[code_type_champs]['field']
            extra = TYPE_PIECES[code_type_champs]['extra']
            self.fields['valeur'] = class_type(**extra)
        except:
            # Si c'est une piece sans instance, on ne fait rien.
            # Ce cas ne devrait pas se produite car les instances 
            # Pieces sont prépopulées à partir de l'appel
            pass


    def save(self, **kwargs):
        piece = super(PieceForm, self).save(commit=False)

        if piece.type.field_type == 9:
            tmp_upload = self.cleaned_data['valeur']
            name = "%s/%s_%s" % (piece.dossier_id, piece.id, tmp_upload.name)
            PIECE_STORAGE.save(name, tmp_upload)
            piece.valeur = name
            piece.save()
  
        return piece
