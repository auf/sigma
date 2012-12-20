# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.contrib import admin
from form_utils.forms import BetterModelForm
from .models import (
    Allocation,
    Allocataire,
    )

ALLOC_HELP_TEXTS = {
    'creer_nouvel_allocataire': (
        'Les données du dossier seront utilisées pour créer un '
        'nouvel allocataire. Veuillez vérifier qu\'il n\'existe '
        'pas déjà un allocataire correspondant à ce dossier avant'
        ' de choisir cette option.'
        ),
    'allocataire': (
        'Cliquez sur l\'icône de recherche pour choisir un '
        'allocataire existant.'
        ),
    }

class NouvelleAllocation(forms.ModelForm):
    creer_nouvel_allocataire = forms.BooleanField(
        'Créer un nouvel allocataire à partir du dossier',
        )
    def __init__(self, *a, **kw):
        super(NouvelleAllocation, self).__init__(*a, **kw)
        self.fields['creer_nouvel_allocataire'].required = False
        self.fields['allocataire'].required = False
        self.fields['allocataire'].widget = ForeignKeyRawIdWidget(
            rel=Allocation.allocataire.field.rel,
            admin_site=admin.site,
            )

        # Assigner les help_text
        for key in ALLOC_HELP_TEXTS:
            self.fields[key].help_text = ALLOC_HELP_TEXTS[key]

    def clean_allocataire(self):
        print "Cleaning alloc"
        if (not self.cleaned_data['creer_nouvel_allocataire'] and not
            self.cleaned_data['allocataire']):
            raise forms.ValidationError(
                'Veuillez choisir un allocataire, ou choisir d\'en '
                'creer un.'
                )
        elif (self.cleaned_data['creer_nouvel_allocataire'] and
            self.cleaned_data['allocataire']):
            raise forms.ValidationError(
                'Vous ne pouvez pas créer un allocataire si un '
                'allocataire est déjà sélectionné.'
                )
        else:
            return self.cleaned_data['allocataire']


    def clean(self):
        if (self.cleaned_data['creer_nouvel_allocataire'] and not
              self.cleaned_data['allocataire']):
            self.cleaned_data['allocataire'] = (
                Allocataire.from_dossier(dossier=self.cleaned_data['dossier']))
        return self.cleaned_data
        

    #     if self.cleaned_data['creer_nouvel_allocataire']:
    #         raise forms.ValidationError(
    #             'Vous ne pouvez pas créer un allocataire si un '
    #             'allocataire est déjà sélectionné.'
    #             )
    #     return self.cleaned_data['allocataire']

    # def clean(self):
    #     if (self.cleaned_data['creer_nouvel_allocataire'] and
    #         self.cleaned_data['allocataire']):
    #     if (not self.cleaned_data['creer_nouvel_allocataire'] and
    #         not self.cleaned_data['allocataire']):
    #         raise forms.ValidationError('asdasdasd')
    #         raise forms.ValidationError(
    #             'Veuillez choisir un allocataire, ou choisir d\'en '
    #             'créer un.'
    #             )
        
        
    class Meta:
        # fields = (
        #     ('creer_nouvel_allocataire',
        #     'allocataire',)
        #     )
        exclude = []
        model = Allocation
