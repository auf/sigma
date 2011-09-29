# -*- encoding: utf-8 -*-

import os
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from form_utils.forms import BetterModelForm
from django.forms import ModelForm
from dynamo.forms import PropertyForm
from dynamo.fields import TEXT
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

    def clean_note(self):
        note = self.cleaned_data['note']

        from models import NOTE_MIN, NOTE_MAX

        if note < NOTE_MIN or note > NOTE_MAX:
            raise forms.ValidationError("Vous devez spécifier une note entre 1 et 100")

        return note

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

class ExpertChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        disciplines = ', '.join([d.code for d in obj.disciplines.all()])
        return "%s, %s (%s)" % (obj.nom, obj.prenom, disciplines)

class ExpertForm(forms.Form):
    experts = ExpertChoiceField(queryset=Expert.objects.all(),
                                help_text="Maintenez appuyé « Ctrl », ou « Commande (touche pomme) » sur un Mac, pour en sélectionner plusieurs.")

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


################################################################################
# Dynamo - ADMIN
################################################################################
class ConformiteForm(PropertyForm):
   """
   Dans l'admin inline, on préserve le type défini par l'appel.
   """
   class Meta:
       exclude = ('type', 'value', )
       model = Conformite

class TypeConformiteForm(BetterModelForm):
    """
    Il n'y a qu'un type possible de pièces dans ce cas : boolean.
    """
    class Meta:
        exclude = ('field_type',)
        model = TypeConformite

    def save(self, commit=True):
        instance = super(TypeConformiteForm, self).save(commit)
        instance.field_type = TEXT
        return instance















