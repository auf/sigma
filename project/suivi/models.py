# -*- encoding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save

from auf.django.coda.models import LigneEcriture
from sigma.models import Dossier
from sigma.workflow import DOSSIER_ETAT_BOURSIER


class BoursierManager(models.Manager):
    """Manager pour les boursiers.

       Cache les fiches boursier dont le dossier de candidature n'indique
       pas qu'ils sont boursiers."""

    def get_query_set(self):
        qs = super(BoursierManager, self).get_query_set()
        return qs.filter(dossier__etat=DOSSIER_ETAT_BOURSIER)


class BoursierInactifManager(models.Manager):
    """Manager pour les boursiers inactifs."""

    def get_query_set(self):
        qs = super(BoursierInactifManager, self).get_query_set()
        return qs.exclude(dossier__etat=DOSSIER_ETAT_BOURSIER)


class Boursier(models.Model):
    """La fiche de suivi d'un boursier."""
    dossier = models.OneToOneField(Dossier, verbose_name='dossier de candidature',
                                   related_name='boursier', primary_key=True,
                                   editable=False)
    code_operation = models.CharField(max_length=11, verbose_name="code d'opération CODA",
                                      blank=True, default='', db_index=True)
    numero_police_assurance = models.CharField(max_length=100, verbose_name="numéro de police d'assurance",
                                               blank=True, default='')
    responsable_budgetaire = models.CharField(max_length=100, verbose_name="responsable budgétaire",
                                              blank=True, default='')

    # Managers
    objects = BoursierManager()
    inactifs = BoursierInactifManager()

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

    def lignes_ecritures_coda(self):
        return LigneEcriture.objects.filter(tiers_operation__code=self.code_operation)

    def save(self, *args, **kwargs):
        # Assurons-nous que les codes opération sont uniques
        Boursier.inactifs.filter(code_operation=self.code_operation).update(code_operation='')
        super(Boursier, self).save(*args, **kwargs)


def dossier_post_save(sender, instance=None, **kwargs):
    if instance and instance.etat == DOSSIER_ETAT_BOURSIER:
        Boursier.objects.get_or_create(dossier=instance)
post_save.connect(dossier_post_save, sender=Dossier)


class DepensePrevisionnelle(models.Model):
    IMPLANTATION_CHOICES = (
        ('O', 'Origine'),
        ('A', 'Accueil'),
    )

    boursier = models.ForeignKey(Boursier, related_name="depensesprevisionnelles")
    numero = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    description = models.CharField(max_length=36)
    montant_eur = models.DecimalField(max_digits=17, decimal_places=2)
    implantation = models.CharField(max_length=1, choices=IMPLANTATION_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name= "Dépense prévisionnelle"
        verbose_name_plural = "Dépenses prévisionnelles"

    def __unicode__(self):
        return self.description
