# -*- encoding: utf-8 -*-

from django.db import models
from workflow import AppelWorkflow

class Appel(AppelWorkflow, models.Model):
    """
    Un Appel est une proposition de l'AUF pour offrir une bourse de mobilité s'intégrant dans un projet.
    """
    nom = models.CharField(max_length=255, verbose_name="Nom")
    code_budgetaire = models.CharField(max_length=255, verbose_name="Code budgétaire", blank=True, null=True)
    formulaire_wcs = models.CharField(max_length=255, verbose_name="Nom du formulaire WCS", blank=True, null=True)
    date_debut = models.DateField(verbose_name="Date de début", blank=True, null=True)
    date_fin = models.DateField(verbose_name="Date de fin", blank=True, null=True)
    date_activation = models.DateField(verbose_name="Date d'activation", blank=True, null=True)
    date_desactivation = models.DateField(verbose_name="Date de désactivation", blank=True, null=True)

    def __unicode__(self):
        return self.nom
