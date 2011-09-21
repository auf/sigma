# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
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
            if not code_operation.startswith(code_budgetaire) or \
               not code_operation.endswith('L'):
                raise ValidationError(
                    u"Code d'opération invalide: il devrait avoir la forme %sXXXL" % 
                    code_budgetaire
                )
        return code_operation


class BoursierAdmin(admin.ModelAdmin):

    # Champs calculés

    def dossier_link(boursier):
        return '<a href="%s">%s</a>' % (
            reverse('admin:sigma_dossier_change', args=(boursier.dossier.pk,)),
            conditional_escape(boursier.dossier)
        )
    dossier_link.allow_tags = True
    dossier_link.short_description = 'Dossier de candidature'

    # Configuration

    # XXX: La seule façon de faire référence à la méthode 'dossier_link' dans
    # l'objet admin ici est de passer la méthode elle-même. C'est pour ça que
    # sa définition est placée plus haut. Bug Django?
    form = BoursierAdminForm
    readonly_fields = ['nom_complet', dossier_link]
    fields = ['nom_complet', dossier_link, 'code_operation']

    # Queryset

    def queryset(self, request):
        # Cacher les fiches boursier dont le dossier de candidature n'indique
        # pas qu'ils sont boursiers.
        qs = super(BoursierAdmin, self).queryset(request)
        return qs.filter(dossier__etat=DOSSIER_ETAT_BOURSIER)

admin.site.register(Boursier, BoursierAdmin)
