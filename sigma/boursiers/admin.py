# -*- encoding: utf-8 -*-

from itertools import groupby

from auf.django.permissions.admin import GuardedModelAdmin
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import conditional_escape
from django.db import models

from sigma.boursiers.models import (
    Boursier, DepensePrevisionnelle, EcritureCODA
)


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


class DepensePrevisionnelleInline(admin.TabularInline):
    model = DepensePrevisionnelle
    template = 'admin/edit_inline/tabular_compact.html'
    formfield_overrides = {
        models.DecimalField: {'localize': True},
    }


class BoursierAdmin(GuardedModelAdmin):
    list_display = (
        'nom', 'prenom', 'code_operation', 'naissance_date', 'appel',
        'debut_mobilite', 'field_actions'
    )
    list_display_links = ('nom', 'prenom')
    list_filter = ('dossier__appel',)
    form = BoursierAdminForm
    readonly_fields = ('nom_complet', 'field_dossier')
    fieldsets = (
        (None, {
            'fields': (
                'nom_complet', 'field_dossier', 'code_operation',
                'numero_police_assurance', 'responsable_budgetaire',
                ('date_debut', 'date_fin')
            )
        }),
    )
    inlines = [DepensePrevisionnelleInline]

    # Champs calculés

    def field_dossier(self, boursier):
        return '<a href="%s">%s</a>' % (
            reverse('admin:candidatures_dossier_change', args=(boursier.dossier.pk,)),
            conditional_escape(boursier.dossier)
        )
    field_dossier.allow_tags = True
    field_dossier.short_description = 'Dossier de candidature'

    def field_actions(self, obj):
        return '<a href="%s">Suivi</a>' % \
                reverse('admin:boursiers_boursier_suivi', args=(obj.pk,))
    field_actions.short_description = ''
    field_actions.allow_tags = True

    # Vues additionnelles

    def get_urls(self):
        admin_urls = super(BoursierAdmin, self).get_urls()
        additional_urls = patterns('',
            url(r'^(\d+)/suivi/$', self.admin_site.admin_view(self.view_suivi),
                name='boursiers_boursier_suivi'),
        )
        return additional_urls + admin_urls

    def view_suivi(self, request, id):
        boursier = Boursier.objects.get(pk=id)

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
                'nb_mois': (fin.month - debut.month +
                            12 * (fin.year - debut.year)),
                'montant': boursier.montant(lieu),
                'implantation': boursier.implantation(lieu),
            }
            for lieu, debut, fin
            in boursier.dossier.mobilite.periodes_mobilite()
        ]

        return render_to_response('admin/boursiers/boursier/suivi.html', {
            'title': "Suivi de %s" % boursier,
            'boursier': boursier,
            'groupes_ecritures': groupes_ecritures,
            'periodes_mobilite': periodes_mobilite,
        }, context_instance=RequestContext(request))

    # Permissions

    def has_add_permission(self, request):
        # L'ajout de boursier n'est jamais manuel
        return False

admin.site.register(Boursier, BoursierAdmin)