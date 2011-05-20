# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import admin
from reversion.admin import VersionAdmin
from auf.django.workflow.admin import WorkflowAdmin
from models import Piece, Appel, DossierOrigine, DossierAccueil, DossierMobilite, Diplome, Candidat, Dossier, TypePiece, Expert

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
    inlines = (DiplomeInline, DossierOrigineInline, DossierAccueilInline, DossierMobiliteInline, )
    list_display = ('id', 'appel', 'candidat', 'etat', )
    list_filter = ('etat', 'appel', )
    search_fields = ('appel__nom', 'candidat__nom', 'candidat__prenom', )
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

    
class ExpertAdmin(admin.ModelAdmin):
    pass
    

def affecter_dossiers_expert(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    return HttpResponseRedirect(reverse('affecter_experts_dossiers')+"?ids=%s" % (",".join(selected)))
    
admin.site.add_action(affecter_dossiers_expert, 'Affecter experts')

admin.site.register(Appel, AppelAdmin)
admin.site.register(Candidat, CandidatAdmin)
admin.site.register(Dossier, DossierAdmin)
admin.site.register(Expert, ExpertAdmin)
