# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib import admin
from reversion.admin import VersionAdmin
from auf.django.workflow.admin import WorkflowAdmin
from models import Piece, Appel, DossierOrigine, DossierAccueil, DossierMobilite, Diplome, Candidat, Dossier, TypePiece

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

class DossierAdmin(WorkflowAdmin, VersionAdmin):
    #change_list_template = "admin/sigma/dossier/change_list.html"
    inlines = (DiplomeInline, DossierOrigineInline, DossierAccueilInline, DossierMobiliteInline, )
    list_display = ('id', 'appel', 'candidat', 'etat', 'moyenne_votes', 'discipline', '_actions', )
    list_filter = ('etat', 'appel', 'discipline', )
    search_fields = ('appel__nom',
                     'candidat__nom', 'candidat__prenom',
                     'discipline__code', 'discipline__nom_court', 'discipline__nom_long',
    )
    fieldsets = (
        (None, {
            'fields': ('candidat', 'appel', ),
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

    def _actions(self, obj):
        return "<a href='%s'>Évaluer</a>" % reverse('evaluer', args=(obj.id, ))
    _actions.allow_tags = True

admin.site.register(Appel, AppelAdmin)
admin.site.register(Candidat, CandidatAdmin)
admin.site.register(Dossier, DossierAdmin)
