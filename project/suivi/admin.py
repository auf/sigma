# -*- encoding: utf-8 -*-

from itertools import groupby

from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import conditional_escape

from sigma.workflow import DOSSIER_ETAT_BOURSIER
from suivi.models import Boursier


class BoursierAdminForm(ModelForm):

    class Meta:
        model = Boursier

    def clean_code_operation(self):
        code_operation = self.cleaned_data['code_operation']
        boursier = self.instance
        if boursier and code_operation:
            code_budgetaire = boursier.dossier.appel.code_budgetaire

            # Vérifier le format du code opération
            if not code_operation.startswith(code_budgetaire) or \
               not code_operation.endswith('L'):
                raise ValidationError(
                    u"Code d'opération invalide: il devrait avoir la forme %sXXXL" % 
                    code_budgetaire
                )

            # Vérifier que ce code d'opération n'est pas déjà utilisé
            conflits = Boursier.objects \
                    .filter(code_operation=code_operation) \
                    .exclude(pk=boursier.pk)
            if len(conflits) > 0:
                raise ValidationError(
                    u"Code d'opération déjà attribué au boursier %s." % conflits[0]
                )
            
        return code_operation


class BoursierAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'code_operation', 'field_actions')
    form = BoursierAdminForm
    readonly_fields = ('nom_complet', 'field_dossier')
    fields = ('nom_complet', 'field_dossier', 'code_operation', 'numero_police_assurance')

    # Champs calculés

    def field_dossier(self, boursier):
        return '<a href="%s">%s</a>' % (
            reverse('admin:sigma_dossier_change', args=(boursier.dossier.pk,)),
            conditional_escape(boursier.dossier)
        )
    field_dossier.allow_tags = True
    field_dossier.short_description = 'Dossier de candidature'

    def field_actions(self, obj):
        return '<a href="%s">Suivi</a>' % reverse('admin:suivi_boursier_suivi', args=(obj.pk,))
    field_actions.short_description = ''
    field_actions.allow_tags = True

    # Vues additionnelles

    def get_urls(self):
        admin_urls = super(BoursierAdmin, self).get_urls()
        additional_urls = patterns('',
            url(r'^(\d+)/suivi/$', self.admin_site.admin_view(self.view_suivi),
                name='suivi_boursier_suivi'),
        )
        return additional_urls + admin_urls

    def view_suivi(self, request, id):
        boursier = Boursier.objects.get(pk=id)
        lignes_ecritures = boursier.lignes_ecritures_coda() \
                .exclude(montant_eur=0) \
                .order_by('compte_comptable__code', '-ecriture__date') \
                .select_related('compte_comptable', 'ecriture')
        groupes_ecritures = []
        for compte_comptable, lignes in groupby(lignes_ecritures, lambda x: x.compte_comptable):
            lignes = list(lignes)
            groupes_ecritures.append({
                'compte_comptable': compte_comptable,
                'lignes': lignes,
                'sous_total': sum(l.montant_eur for l in lignes)
            })
        return render_to_response('admin/suivi/boursier/suivi.html', {
            'boursier': boursier,
            'groupes_ecritures': groupes_ecritures
        }, context_instance=RequestContext(request))

    # Permissions

    def has_add_permission(self, request):
        # L'ajout de boursier n'est jamais manuel
        return False

admin.site.register(Boursier, BoursierAdmin)
