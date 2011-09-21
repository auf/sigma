# -*- encoding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save

from sigma.models import Dossier
from sigma.workflow import DOSSIER_ETAT_BOURSIER


class Boursier(models.Model):
    """La fiche de suivi d'un boursier."""
    dossier = models.OneToOneField(Dossier, verbose_name='Dossier de candidature', 
                                   related_name='boursier', primary_key=True,
                                   editable=False)
    code_operation = models.CharField(max_length=11, verbose_name="Code d'opération CODA",
                                      blank=True, default='')

    class Meta:
        verbose_name = 'boursier'
        verbose_name_plural = 'boursiers'

    def __unicode__(self):
        return self.nom_complet()

    @property
    def prenom(self):
        return self.dossier.candidat.prenom

    @property
    def nom(self):
        return self.dossier.candidat.nom

    def nom_complet(self):
        return self.prenom + ' ' + self.nom
    nom_complet.short_description = 'Nom'


def dossier_post_save(sender, instance=None, **kwargs):
    if instance and instance.etat == DOSSIER_ETAT_BOURSIER:
        Boursier.objects.get_or_create(dossier=instance)
post_save.connect(dossier_post_save, sender=Dossier)
