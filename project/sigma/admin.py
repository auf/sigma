# -*- encoding: utf-8 -*-

from django.contrib import admin
from auf.django.workflow.admin import WorkflowAdmin
from models import Appel

class AppelAdmin(WorkflowAdmin):
    fields = ('nom', 'etat', )

admin.site.register(Appel, AppelAdmin)
