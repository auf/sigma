# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget, AdminDateWidget
from django.contrib import admin
from form_utils.forms import BetterModelForm
from sigma.candidatures.models import Dossier
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


def allocation_form_factory(request, instance):
    # Todo: Turn this into proper factory.
    #
    # S'il y a une instance, ça retourne AllocationForm (sans les
    # champs creet_nouvel_allocataire et allocataire
    # Sinon, retourne un callable qui creer une instance de
    # AllocationForm, en fournissant dossier_id au constructeur,
    # permettant alors de creer les help text du champs
    # code_operation.

    def inner_nouvelle_form_factory(*a, **kw):
        return NouvelleAllocation(
            *a,
             dossier_id=request.GET.get('dossier'),
             **kw)

    if instance:
        form = AllocationForm
    else:
        return inner_nouvelle_form_factory

    return form


class AllocationForm(forms.ModelForm):
    # def _get_dossier(self, dossier_id):
    #     return self.found_dossier

    def __init__(self, *args, **kwargs):
        dossier_id = kwargs.pop('dossier_id', None)
        super(AllocationForm, self).__init__(*args, **kwargs)
        self.fields['date_debut'].widget = AdminDateWidget()
        self.fields['date_fin'].widget = AdminDateWidget()

        # Get dossier.
        try:
            dossier = self.instance.dossier
            if dossier == None:
                raise AttributeError()
        except (Dossier.DoesNotExist, AttributeError):
            dossier = Dossier.objects.get(id=dossier_id)

        if dossier.appel.code_budgetaire:
            code_budgetaire = dossier.appel.code_budgetaire
            max_code_allocation = Allocation.objects \
                    .filter(code_operation__startswith=code_budgetaire) \
                    .order_by('-code_operation')[:1]
            if len(max_code_allocation) > 0:
                max_code = max_code_allocation[0].code_operation
                numero = max_code[len(code_budgetaire):-1]
            else:
                numero = 0
            try:
                numero_int = int(numero)
            except ValueError:
                pass
            else:
                prochain_numero = '%03d' % (numero_int + 1)
                prochain_code = code_budgetaire + prochain_numero + 'L'
                self.fields['code_operation'].help_text = \
                        u"Prochain code disponible: %s" % prochain_code

    def clean_code_operation(self):
        code_operation = self.cleaned_data['code_operation']
        dossier = self.cleaned_data['dossier']
        allocation = self.instance
        if code_operation and dossier.appel.code_budgetaire:
            code_budgetaire = dossier.appel.code_budgetaire

            # Vérifier le format du code opération
            if not code_operation.startswith(code_budgetaire) or \
               not code_operation.endswith('L'):
                raise forms.ValidationError(
                    u"Code d'opération invalide: "
                    u"il devrait avoir la forme %sXXXL" %
                    code_budgetaire
                )

            # Vérifier que ce code d'opération n'est pas déjà utilisé
            conflits = Allocation.objects \
                    .filter(code_operation=code_operation) \
                    .exclude(pk=allocation.pk)
            if len(conflits) > 0:
                raise forms.ValidationError(
                    u"Code d'opération déjà attribué à l'allocation %s." %
                    conflits[0]
                )

        return code_operation

    class Meta:
        exclude = []
        model = Allocation


class NouvelleAllocation(AllocationForm):
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
        if (not self.data.get('creer_nouvel_allocataire', None) ==
            'on' and not self.cleaned_data.get('allocataire', None)):
            raise forms.ValidationError(
                'Veuillez choisir un allocataire, ou choisir d\'en '
                'creer un.'
                )
        elif (self.data.get('creer_nouvel_allocataire', None) == 'on'
              and self.cleaned_data.get('allocataire', None)):
            raise forms.ValidationError(
                'Vous ne pouvez pas créer un allocataire si un '
                'allocataire est déjà sélectionné.'
                )
        else:
            return self.cleaned_data.get('allocataire', None)

    def clean(self):
        if (self.cleaned_data.get('creer_nouvel_allocataire', None) and not
              self.cleaned_data.get('allocataire', None)):
            self.cleaned_data['allocataire'] = (
                Allocataire.from_dossier(dossier=self.cleaned_data['dossier']))
        return self.cleaned_data
        

    def save(self, commit=True):
        # Pour une raison ou pour une autre, si on veut que save_m2m
        # soit appelé, il faut changer commit = True (et l'admin par
        # défaut set commit=False). La documentation Django semble
        # dire le contraire, il doit me manquer un detail..
        if not self.instance.id:
            commit = True
        return super(NouvelleAllocation, self).save(commit=commit)
        
    def save_m2m(self):
        # C'est ici que sont crees les related objects.
        self.instance.create_mobilite()
        self.instance.create_vues_ensemble()
        self.instance.create_depenses_previsionelles()
