# -*- encoding: utf-8 -*-

from itertools import groupby

from django.http import HttpResponseRedirect
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import (
    ModelForm,
    ValidationError,
    MediaDefiningClass,
    TextInput,
    DateInput,
    )
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import conditional_escape
from django.db import models
from .forms import (
    allocation_form_factory,
    )    
from sigma.candidatures.models import (
    Dossier,
    )
from .models import (
    Allocation,
    AllocationAccueil,
    AllocationOrigine,
    Allocataire,
    FicheFinanciere,
    DepensePrevisionnelle,
    VueEnsemble,
    EcritureCODA
    )
from sigma.custom_admin.util import (
    GuardedStackedInline,
    GuardedTabularInline,
    GuardedModelAdmin,
    )
from sigma.candidatures.workflow import DOSSIER_ETAT_RETENU
from sigma.lib.views import bad_request


class AllocationAdminMixin(object):
    def field_dossier(self, allocation):
        return '<a href="%s">%s</a>' % (
            reverse('admin:candidatures_dossier_change', args=(allocation.dossier.pk,)),
            conditional_escape(allocation.dossier)
        )
    field_dossier.allow_tags = True
    field_dossier.short_description = 'Dossier de candidature'


    def has_add_permission(self, request):
        # L'ajout de allocation n'est jamais manuel
        return False
    

class DeviseMixin(object):
    def _devise(self, obj):
        return '€'
    _devise.short_description = 'Devise'


class DepensePrevisionnelleInline(GuardedTabularInline, DeviseMixin):
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


class VueEnsembleInline(GuardedTabularInline, DeviseMixin):
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


class FicheFinanciereAdmin(GuardedModelAdmin, AllocationAdminMixin):
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
    readonly_fields = (
        'nom_complet',
        'field_dossier',
        'pays_origine',
        'code_bureau',
        'responsable_budgetaire',
        'code_operation',
        'date_debut',
        'date_fin',
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

        
        allocation = self.model.objects.get(pk=object_id)
        nb_mois = None
        dossier_mobilite = allocation.dossier.get_mobilite()
        if dossier_mobilite:
            nb_mois = dossier_mobilite.duree_totale.mois

        ecritures = EcritureCODA.objects \
                .filter(boursier_id=allocation.code_operation) \
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
                'montant': allocation.montant(lieu),
                'implantation': allocation.implantation(lieu),
            }
            for lieu, debut, fin
            in getattr(
                dossier_mobilite,
                'periodes_mobilite',
                lambda: [])()
            ]

        extra_context.update({
                'groupes_ecritures': groupes_ecritures,
                'allocation': allocation,
                'periodes_mobilite': periodes_mobilite,
                })

        return super(FicheFinanciereAdmin, self).change_view(
            request,
            object_id,
            form_url,
            extra_context,
            )


class AllocationOrigineInline(GuardedStackedInline):
    # TODO: make this more generic, since it's practically a copy of DossierOrigineInline
    max_num = 1
    template = "admin/candidatures/edit_inline/single-stack.html"
    can_delete = False
    model = AllocationOrigine
    verbose_name = verbose_name_plural = "Origine " \
            "(établissement d'inscription ou d'activité " \
            "à la date de la candidature)"

    fieldsets = (
        (None, {'fields': ('etablissement',)}),
        ('Autre établissement si non membre de l\'AUF', {
            'fields': (
                ('autre_etablissement_nom', 'autre_etablissement_adresse'),
                ('autre_etablissement_ville',
                 'autre_etablissement_code_postal'),
                ('autre_etablissement_region', 'autre_etablissement_pays')
            )
        }),
        ('Responsable institutionnel à l\'origine', {
            'fields': (
                ('resp_inst_civilite', 'resp_inst_nom', 'resp_inst_prenom'),
                ('resp_inst_fonction', 'resp_inst_courriel'),
                ('resp_inst_telephone', 'resp_inst_fax')
            )
        }),
        ('Responsable scientifique à l\'origine', {
            'fields': (('resp_sc_civilite', 'resp_sc_nom', 'resp_sc_prenom'),
                       ('resp_sc_fonction', 'resp_sc_courriel'),
                       ('resp_sc_telephone', 'resp_sc_fax'),
                       ('faculte_nom', 'faculte_adresse'),
                       ('faculte_ville', 'faculte_code_postal'))
        }),
        ("Directeur de thèse à l'origine", {
            'fields': ('dir_civilite',
                       ('dir_nom', 'dir_prenom'),
                       ('dir_courriel', 'dir_telephone'))
        }),
    )


class AllocationAccueilInline(GuardedStackedInline):
    # TODO: make this more generic, since it's practically a copy of DossierAccueilInline
    max_num = 1
    template = "admin/candidatures/edit_inline/single-stack.html"
    can_delete = False
    model = AllocationAccueil
    verbose_name = verbose_name_plural = "Accueil " \
            "(établissement de destination de la mobilité)"

    fieldsets = (
        (None, {'fields': ('etablissement',)}),
        ('Autre établissement si non membre de l\'AUF', {
            'fields': (
                ('autre_etablissement_nom', 'autre_etablissement_adresse'),
                ('autre_etablissement_ville',
                 'autre_etablissement_code_postal'),
                ('autre_etablissement_region', 'autre_etablissement_pays')
            )
        }),
        ('Responsable scientifique à l\'accueil', {
            'fields': (('resp_sc_civilite', 'resp_sc_nom', 'resp_sc_prenom'),
                       ('resp_sc_fonction', 'resp_sc_courriel'),
                       ('resp_sc_telephone', 'resp_sc_fax'),
                       ('faculte_nom', 'faculte_adresse'),
                       ('faculte_ville', 'faculte_code_postal'))
        }),
        ("Directeur de thèse à l'accueil", {
            'fields': ('dir_civilite',
                       ('dir_nom', 'dir_prenom'),
                       ('dir_courriel', 'dir_telephone'))
        }),
    )


class AllocationAdmin(GuardedModelAdmin):

    change_form_template = 'admin/boursiers/allocation/change_form.html'

    # TODO: Make this work.
    # inlines = (
    #     AllocationOrigineInline,
    #     AllocationAccueilInline,
    #     )

    readonly_fields = ()

    def get_form(self, request, obj=None, **kw):
        return allocation_form_factory(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
                'dossier',
                'allocation_originale',
                'allocataire',
                )

    def add_view(self, request, form_url='', extra_context={}):
        dossier_qs = Dossier.objects.filter(id=request.GET.get('dossier'))
        if (request.method == 'GET' and (
                'dossier' not in request.GET or
                dossier_qs.count()
                == 0)):
            return bad_request(request, 'Dossier manquant, ou invalide')
        elif (request.method == 'GET'
              and 'dossier' in request.GET
              and dossier_qs.get().etat != DOSSIER_ETAT_RETENU):
            return bad_request(request, 'Le dossier doit être retenu '
                               'pour créer une allocation.')
        
        return self.return_to_allocataires(
            super(AllocationAdmin, self).add_view(
            request, form_url=form_url, extra_context=extra_context))

    def change_view(self, *a, **kw):
        res = super(AllocationAdmin, self).change_view(*a, **kw)
        return self.return_to_allocataires(res)

    def delete_view(self, *a, **kw):
        return self.return_to_allocataires(
            super(AllocationAdmin, self).delete_view(*a, **kw))

    def return_to_allocataires(self, res):
        # Au lieu de ramener a la liste d'allocation, ramener a la
        # list d'allocataires, apres l'ajout.
        if (isinstance(res, HttpResponseRedirect)
            and res['location'] == '/boursiers/allocation/'):
            return HttpResponseRedirect(
                reverse('admin:boursiers_allocataire_changelist'))
        return res
        

    def get_fieldsets(self, request, obj=None):
        if not obj:
            # If instance.
            return [(
                'Sélection de l\'allocataire', {
                    'fields': (
                        'creer_nouvel_allocataire',
                        'allocataire',
                        )}
                )] + [(
                    'Détails', {
                        'fields': (
                            'dossier',
                            'allocation_originale',
                            ('code_operation', 'numero_police_assurance'),
                            ('date_debut', 'date_fin'),
                            )
                        })]
        else:
            # If no instance.
            return [(
                    'Détails', {
                        'fields': (
                            'dossier',
                            'allocataire',
                            'allocation_originale',
                            # 'desiste',
                            ('code_operation', 'numero_police_assurance'),
                            ('date_debut', 'date_fin'),
                            )
                        })]


class AllocataireAdmin(GuardedModelAdmin, AllocationAdminMixin):
    search_fields = (
        'nom',
        'prenom',
        'courriel',
        )
    readonly_fields = (
        '_age',
        )
    list_display_links = ('_nom_si_actif', '_prenom_si_actif')
    list_filter = (
        'civilite',
        'pays',
        'nationalite',
        'allocations__dossier__appel',
        )

    def _si_actif(self, attr, obj):
        if obj.actif():
            tpl = '%s'
        else:
            tpl = '<span class="inactif">%s</span>'
        return tpl % getattr(obj, attr)

    def _nom_si_actif(self, obj):
        return self._si_actif('nom', obj)
    _nom_si_actif.allow_tags = True
    _nom_si_actif.short_description = u'Nom'

    def _prenom_si_actif(self, obj):
        return self._si_actif('prenom', obj)
    _prenom_si_actif.allow_tags = True
    _prenom_si_actif.short_description = u'Prénom'

    def _naissance_si_actif(self, obj):
        return self._si_actif('naissance_date', obj)
    _naissance_si_actif.allow_tags = True
    _naissance_si_actif.short_description = u'Date de naissance'


    list_display = (
        '_nom_si_actif',
        '_prenom_si_actif',
        '_naissance_si_actif',
    )
    fieldsets = (
        (None, {
            'fields': (
                    'civilite', ('nom', 'prenom'),
                    'nationalite',
                    'naissance_date',
                    '_age',
                    )
        }),
        ('Coordonnées', {
            'fields': (
                'adresse',
                'adresse_complement',
                ('ville', 'code_postal'),
                'pays',
                ('telephone', 'telephone_portable'),
                'courriel')
            }),
        )

    def _age(self, obj):
        return obj.candidat.age()
    _age.short_description = u'Âge'

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('adresse', 'adresse_complement'):
            kwargs['widget'] = TextInput(attrs={'size': 80})
        elif db_field.name == 'naissance_date':
            kwargs['widget'] = DateInput(format='%d/%m/%Y')
        return super(AllocataireAdmin, self) \
                .formfield_for_dbfield(db_field, **kwargs)

    change_form_template = (
        'admin/boursiers/allocataire/change_form.html')

    def change_view(self,
                    request,
                    object_id,
                    form_url='',
                    extra_context={}
                    ):
        res = super(AllocataireAdmin, self).change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
            )
        return res


admin.site.register(Allocation, AllocationAdmin)
admin.site.register(Allocataire, AllocataireAdmin)
admin.site.register(FicheFinanciere, FicheFinanciereAdmin)
