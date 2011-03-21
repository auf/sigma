# -*- encoding: utf-8 -*-

from django.contrib import admin
from auf.django.workflow.admin import WorkflowAdmin
from models import Appel, Candidat, Diplome, Dossier, DossierOrigine, DossierAccueil, DossierMobilite

class AppelAdmin(WorkflowAdmin):
    fields = ('nom',
        'code_budgetaire',
        #'formulaire_wcs',
        'date_debut',
        'date_fin',
        'date_activation',
        'date_desactivation',
        'etat',
        )

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

class DiplomeInline(admin.StackedInline):
    model = Diplome
    max_num = 1
    template = "admin/sigma/edit_inline/stacked.html"
    verbose_name = verbose_name_plural = "Diplômes"

class DossierAdmin(WorkflowAdmin):
    exclude = ('candidat', 'appel', )
    inlines = (DiplomeInline, DossierOrigineInline, DossierAccueilInline, DossierMobiliteInline, )
    fieldsets = (
        ('Situation universitaire', {
            'fields': ('candidat_statut', 'candidat_fonction', ),
        }),
        ('État du dossier', {
            'classes': ('collapse',),
            'fields': ('etat', ),
        }),
    )

admin.site.register(Appel, AppelAdmin)
admin.site.register(Candidat, CandidatAdmin)
admin.site.register(Dossier, DossierAdmin)
