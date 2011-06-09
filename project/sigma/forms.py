# -*- encoding: utf-8 -*-

import os
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from form_utils.forms import BetterModelForm
from django.forms import ModelForm
from datamaster_modeles.models import Discipline
from models import *

class RequiredInlineFormSet(BaseInlineFormSet):
  """
  Generates an inline formset that is required
  """

  def _construct_form(self, i, **kwargs):
    """
    Override the method to change the form attribute empty_permitted
    """
    form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
    form.empty_permitted = False
    return form

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
    

################################################################################
# Groupe Régional - ADMIN
################################################################################

class GroupeRegionalAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        label="Membres",
        queryset=User.objects.filter(is_active=True).order_by('username'), 
        widget=admin.widgets.FilteredSelectMultiple("Membres", False),
        required=False,
        )
    
    class Meta:
        model = GroupeRegional

    def __init__(self, *args, **kwargs):
        super(GroupeRegionalAdminForm, self).__init__(*args, **kwargs)

        # cas édition, on prépopule les users déjà membre
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            user_ids = [u.id for u in instance.users.all().order_by('username')]
            self.fields['users'].initial = user_ids
