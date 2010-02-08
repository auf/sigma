# -=- encoding: utf-8 -=-
from django import forms
from django.db import models
from django.forms.util import ValidationError, ErrorList
from django.forms.models import modelform_factory, modelformset_factory 

from sigma.www.forms import SigmaModelForm
from sigma.www.models import *

import unicodedata

class AppelStatutForm(forms.ModelForm):
    """Formulaire de modification des statut"""
    class Meta:
        model = Appel
        fields = ['statut']


class AppelAjoutForm(SigmaModelForm):
    """Formulaire d'ajout d'un appel d'offre"""
    debut_inscription = forms.DateTimeInput(format='%d/%m/%Y', attrs={
            'class':'campo',
            'readonly':'readonly',
            'size':'15'
        })

    fin_inscription = forms.DateTimeInput(format='%d/%m/%Y', attrs={
            'class':'campo',
            'readonly':'readonly',
            'size':'15'
        })

    date_reception_dossier = forms.DateTimeInput(format='%d/%m/%Y', attrs={
            'class':'campo',
            'readonly':'readonly',
            'size':'15'
        })

    class Meta:
        model = Appel
        exclude = [ 'statut',
                    'statut_id',
                    'actif',
                    'creation_date',
                    'creation_user',
                    'modif_date', 
                    'modif_user']

    def get_title(self):
        return "Ajouter un appel d'offre"
        
    def get_action_url(self):
        return "/appels/add/"

    def get_return_url(self):
        return "/appels/"

    def clean(self):
        """Gere la validation des donnees afin de dispenser de validations
        les champs conditionel"""
        forms.ModelForm.clean(self)

        cleaned_data = self.cleaned_data
        for field,field_dependent in Appel.field_dependencies.items():
            if cleaned_data[field]:
                if field_dependent in cleaned_data and \
                        not cleaned_data[field_dependent]:
                    self._errors[field_dependent] = \
                        [u"Ce champ est obligatoire."]
            else:
                if field_dependent in self._errors:
                    del self._errors[field_dependent]
        return self.cleaned_data


class AppelEditForm(SigmaModelForm):
    """Formulaire de modification d'un appel d'offre"""
    debut_inscription = forms.DateTimeInput(format='%d/%m/%Y', attrs={
            'class':'campo',
            'readonly':'readonly',
            'size':'15'
        })
    fin_inscription = forms.DateTimeInput(format='%d/%m/%Y', attrs={
            'class':'campo',
            'readonly':'readonly',
            'size':'15'
        })

    class Meta:
        model = Appel
        exclude = [
            'statut', 
            'statut_id',
            'piecesjointes',
            'criteres',
            'projetposte',
            'actif']
        
    def get_title(self):
        return "%s (%s) / modifier" % \
            (self.instance.nom, self.instance.id)
        
    def get_action_url(self):
        return "/appels/edit/%s/" % self.instance.id

    def get_return_url(self):
        return "/appels/detail/%s/" % self.instance.id

    def clean(self):
        """Gere la validation des donnees afin de dispenser de validations
        les champs conditionel"""
        cleaned_data = self.cleaned_data
        for dependency in Appel.field_dependencies:
            if Appel.field_dependencies[dependency] in self._errors:
                if not cleaned_data[dependency]:
                    del self._errors[Appel.field_dependencies[dependency]]
        return cleaned_data


class AppelCriteriaAjout(forms.ModelForm):
    """Formulaire d'ajout d'un critere de checklit par un appel d'offre"""
    class Meta:
        model = CritereSupplementaire
