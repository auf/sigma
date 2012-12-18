# -*- encoding: utf-8 -*-

from itertools import groupby

from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import conditional_escape
from django.db import models
from .models import (
    Boursier,
    FicheFinanciere,
    DepensePrevisionnelle,
    VueEnsemble,
    EcritureCODA
    )
from sigma.custom_admin.util import GuardedModelAdmin


class BoursierAdminForm(ModelForm):

    class Meta:
        model = Boursier

    def __init__(self, *args, **kwargs):
        super(BoursierAdminForm, self).__init__(*args, **kwargs)
        if self.instance is not None and \
           self.instance.dossier.appel.code_budgetaire:
            code_budgetaire = self.instance.dossier.appel.code_budgetaire
            max_code_boursier = Boursier.objects \
                    .filter(code_operation__startswith=code_budgetaire) \
                    .order_by('-code_operation')[:1]
            if len(max_code_boursier) > 0:
                max_code = max_code_boursier[0].code_operation
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
        boursier = self.instance
        if boursier and code_operation and \
           self.instance.dossier.appel.code_budgetaire:
            code_budgetaire = boursier.dossier.appel.code_budgetaire

            # Vérifier le format du code opération
            if not code_operation.startswith(code_budgetaire) or \
               not code_operation.endswith('L'):
                raise ValidationError(
                    u"Code d'opération invalide: "
                    u"il devrait avoir la forme %sXXXL" %
                    code_budgetaire
                )

            # Vérifier que ce code d'opération n'est pas déjà utilisé
            conflits = Boursier.objects \
                    .filter(code_operation=code_operation) \
                    .exclude(pk=boursier.pk)
            if len(conflits) > 0:
                raise ValidationError(
                    u"Code d'opération déjà attribué au boursier %s." %
                    conflits[0]
                )

        return code_operation


class DeviseMixin(object):
    def _devise(self, obj):
        return '€'
    _devise.short_description = 'Devise'


class DepensePrevisionnelleInline(admin.TabularInline, DeviseMixin):
    model = DepensePrevisionnelle
    template = 'admin/edit_inline/tabular_compact.html'
    ordering = ('date',)
    extra = 0
    formfield_overrides = {
        models.DecimalField: {'localize': True},
    }
    fields = (
        'commentaires',
        'date',
        'montant_eur',
        '_devise',
        )
    readonly_fields = (
        '_devise',
        )


class VueEnsembleInline(admin.TabularInline, DeviseMixin):
    model = VueEnsemble
    template = 'admin/edit_inline/tabular_compact.html'
    formfield_overrides = {
        models.DecimalField: {'localize': True},
    }
    extra = 0

    fields = (
        '_description',
        'code_document',
        'code_sigma',
        '_montant',
        '_devise',
        )
    readonly_fields = [
        '_description',
        'vue_type',
        'code_document',
        '_montant',
        '_devise',
        ]

    def _description(self, obj):
        return obj.get_vue_type_display()
    _description.short_description = 'Description'

    def _montant(self, obj):
        return obj.montant
    _montant.short_description = 'Montant'

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True


class BoursierAdminMixin(object):
    def field_dossier(self, boursier):
        return '<a href="%s">%s</a>' % (
            reverse('admin:candidatures_dossier_change', args=(boursier.dossier.pk,)),
            conditional_escape(boursier.dossier)
        )
    field_dossier.allow_tags = True
    field_dossier.short_description = 'Dossier de candidature'


    def field_fiche(self, boursier):
        fiche_financiere_info = 'Fiche financière'
        return '<a href="%s">%s</a>' % (
            reverse('admin:boursiers_fichefinanciere_change',
                    args=(boursier.pk,)),
            fiche_financiere_info,
            )
    field_fiche.short_description = 'Fiche financière'
    field_fiche.allow_tags = True


    def field_actions(self, obj):
        return self.field_fiche(obj)
    field_actions.short_description = 'Actions'
    field_actions.allow_tags = True

    def has_add_permission(self, request):
        # L'ajout de boursier n'est jamais manuel
        return False
    

class FicheFinanciereAdmin(GuardedModelAdmin, BoursierAdminMixin):
    list_display = (
        'nom',
        'prenom',
        'code_operation',
        'naissance_date',
        'appel',
        'debut_mobilite',
    )
    list_display_links = ('nom', 'prenom')
    list_filter = ('dossier__appel',)
    form = BoursierAdminForm
    readonly_fields = (
        'nom_complet',
        'field_dossier',
        'pays_origine',
        'code_bureau',
        'responsable_budgetaire',
        'depenses_reelles_totales',
        'depenses_totales',
        )
    fieldsets = (
        (None, {
            'fields': (
                'nom_complet',
                'pays_origine',
                'code_bureau',
                'responsable_budgetaire',
                'field_dossier',
                'depenses_reelles_totales',
                'depenses_totales',
                'code_operation',
                ('date_debut', 'date_fin')
            )
        }),
    )
    inlines = [VueEnsembleInline, DepensePrevisionnelleInline]
    change_form_template = 'admin/boursiers/fichefinanciere/change_form.html'

    def change_view(self,
                    request,
                    object_id,
                    form_url='',
                    extra_context={}
                    ):

        boursier = self.model.objects.get(pk=object_id)
        nb_mois = None
        dossier_mobilite = boursier.dossier.get_mobilite()
        if dossier_mobilite:
            nb_mois = dossier_mobilite.duree_totale.mois

        ecritures = EcritureCODA.objects \
                .filter(boursier_id=boursier.code_operation) \
                .order_by('numero_pcg', 'nom_pcg', '-date_document')

        groupes_ecritures = []
        for pcg, lignes in groupby(
            ecritures, lambda x: (x.numero_pcg, x.nom_pcg)
        ):
            lignes = list(lignes)
            groupes_ecritures.append({
                    'pcg': pcg,
                    'lignes': lignes,
                    'sous_total': sum(l.montant for l in lignes)
                    })

        periodes_mobilite = [
            {
                'lieu': lieu.title(),
                'debut': debut,
                'fin': fin,
                'nb_mois': nb_mois,
                'montant': boursier.montant(lieu),
                'implantation': boursier.implantation(lieu),
            }
            for lieu, debut, fin
            in getattr(
                dossier_mobilite,
                'periodes_mobilite',
                lambda: [])()
            ]

        extra_context.update({
                'groupes_ecritures': groupes_ecritures,
                'boursier': boursier,
                'periodes_mobilite': periodes_mobilite,
                })

        return super(FicheFinanciereAdmin, self).change_view(
            request,
            object_id,
            form_url,
            extra_context,
            )

    # Permissions



class BoursierAdmin(GuardedModelAdmin, BoursierAdminMixin):
    list_display = (
        'nom',
        'prenom',
        'code_operation',
        'naissance_date',
        'appel',
        'debut_mobilite',
        'field_actions',
    )
    list_display_links = ('nom', 'prenom')
    list_filter = ('dossier__appel',)
    form = BoursierAdminForm
    readonly_fields = (
        'nom_complet',
        'field_dossier',
        'field_fiche',
        'pays_origine',
        'code_bureau',
        'responsable_budgetaire',
        'depenses_reelles_totales',
        'depenses_totales',
        )
    fieldsets = (
        (None, {
            'fields': (
                'nom_complet',
                'pays_origine',
                'code_bureau',
                'responsable_budgetaire',
                'field_dossier',
                'depenses_reelles_totales',
                'depenses_totales',
                'code_operation',
                'numero_police_assurance',
                ('date_debut', 'date_fin')
            )
        }),
    )
    change_form_template = 'admin/boursiers/boursier/change_form.html'


admin.site.register(Boursier, BoursierAdmin)
admin.site.register(FicheFinanciere, FicheFinanciereAdmin)
