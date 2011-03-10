# -*- encoding: utf-8 -*-

from django.contrib import admin
from auf.django.workflow.admin import WorkflowAdmin
from models import Appel

class AppelAdmin(WorkflowAdmin):
    fields = ('nom',
        'code_budgetaire',
        #'formulaire_wcs',
        'date_debut',
        'date_fin',
        'date_activation',
        'date_desactivation',
        'etat', )

admin.site.register(Appel, AppelAdmin)
