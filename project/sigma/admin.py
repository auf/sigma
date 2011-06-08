# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import admin
from reversion.admin import VersionAdmin
from auf.django.workflow.admin import WorkflowAdmin
from models import *

class AppelAdmin(WorkflowAdmin):
    list_display = ('nom', 'code_budgetaire', 'date_debut', 'date_fin', 'etat', '_actions', )
    list_filter = ('region', )
    fields = ('nom',
        'region',
        'code_budgetaire',
        #'formulaire_wcs',
        'date_debut',
        'date_fin',
        'date_activation',
        'date_desactivation',
        'etat',
        )

    def _actions(self, obj):
        return "<a href='%s?appel__id__exact=%s'>Voir les dossiers</a>" % (reverse('admin:sigma_dossier_changelist'), obj.id)
    _actions.allow_tags = True
        

class CandidatAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('nom', 'prenom', 'nom_jeune_fille', 'sexe', 'civilite', )
        }),
        ('Identification', {
            'classes': ('collapse',),
            'fields': ('nationalite', 'naissance_ville', 'naissance_date', 'naissance_pays', )
        }),
        ('Coordonnées', {
            'classes': ('collapse',),
            'fields': (
                'pays',
                'adresse',
                'code_postal',
                'ville',
                'region',
                'telephone_perso',
                'fax_perso',
                'courriel_perso',
                'telephone_pro',
                'fax_pro',
                'courriel_pro',
                )
        }),
    )

class DossierOrigineInline(admin.StackedInline):
    model = DossierOrigine
    max_num = 1
    template = "admin/sigma/edit_inline/stacked.html"
    verbose_name = verbose_name_plural = "Origine"
    
class DossierAccueilInline(admin.StackedInline):
    model = DossierAccueil
    max_num = 1
    template = "admin/sigma/edit_inline/stacked.html"
    verbose_name = verbose_name_plural = "Accueil"

class DossierMobiliteInline(admin.StackedInline):
    model = DossierMobilite
    max_num = 1
    template = "admin/sigma/edit_inline/stacked.html"
    verbose_name = verbose_name_plural = "Mobilité"
    
class DossierCandidatInline(admin.StackedInline):
    model = Candidat
    max_num = 1
    template = "admin/sigma/edit_inline/stacked.html"
    verbose_name = verbose_name_plural = "Informations sur le candidat"


class DiplomeInline(admin.StackedInline):
    model = Diplome
    max_num = 1
    template = "admin/sigma/edit_inline/stacked.html"
    verbose_name = verbose_name_plural = "Diplômes"

def affecter_dossiers_expert(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    return HttpResponseRedirect(reverse('affecter_experts_dossiers')+"?ids=%s" % (",".join(selected)))
    
class DossierAdmin(WorkflowAdmin, VersionAdmin):
    inlines = (DossierCandidatInline, DiplomeInline, DossierOrigineInline, DossierAccueilInline, DossierMobiliteInline, )
    list_display = ('id', 'appel', '_region', 'etat', 'moyenne_votes', 'discipline', '_actions', )
    list_filter = ('etat', 'appel', 'discipline', )
    search_fields = ('appel__nom',
                     'candidat__nom', 'candidat__prenom',
                     'discipline__code', 'discipline__nom_court', 'discipline__nom_long',
    )
    fieldsets = (
        (None, {
            'fields': ('appel', ),
        }),
        ('État du dossier', {
            'fields': ('etat', ),
        }),
        ('Situation universitaire', {
            'classes': ('collapse',),
            'fields': ('candidat_statut', 'candidat_fonction', ),
        }),
        ('Lien avec l\'AUF', {
            'classes': ('collapse',),
            'fields': ('dernier_projet_description', 'dernier_projet_annee', 'derniere_bourse_categorie', 'derniere_bourse_annee',),
        }),
    )
    
    #actions = [affecter_dossiers_expert]

    def _actions(self, obj):
        return "<a href='%s'>Évaluer</a>" % reverse('evaluer', args=(obj.id, ))
    _actions.allow_tags = True

    def _region(self, obj):
        return obj.appel.region
    _region.short_description = "Région"


    def queryset(self, request):
        regions = [g.region for g in request.user.groupes_regionaux.all()]
        return super(DossierAdmin, self).queryset(request).filter(appel__region__in=regions)

    
class ExpertAdmin(admin.ModelAdmin):
    pass
    

class GroupeRegionalAdmin(admin.ModelAdmin):
    pass
    

    
#admin.site.add_action(affecter_dossiers_expert, 'Affecter experts')

admin.site.register(Appel, AppelAdmin)
admin.site.register(Dossier, DossierAdmin)
admin.site.register(Expert, ExpertAdmin)
admin.site.register(GroupeRegional, GroupeRegionalAdmin)
