# -*- encoding: utf-8 -*-

from django.contrib import admin
from auf.django.workflow.admin import WorkflowAdmin
from models import Appel, Candidat

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

admin.site.register(Appel, AppelAdmin)
admin.site.register(Candidat, CandidatAdmin)
