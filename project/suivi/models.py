# -*- encoding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save

from sigma.models import Dossier
from sigma.workflow import DOSSIER_ETAT_BOURSIER


class Boursier(models.Model):
    """La fiche de suivi d'un boursier."""
    dossier = models.OneToOneField(Dossier, verbose_name='dossier de candidature',
                                   related_name='boursier', primary_key=True,
                                   editable=False)
    code_operation = models.CharField(max_length=11, verbose_name="code d'opération CODA",
                                      blank=True, unique=True, null=True, db_index=True)

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


class EcritureBoursier(models.Model):
    """Une écriture CODA relative à un boursier."""
    boursier = models.ForeignKey(Boursier, db_column='code',
                                 verbose_name='boursier',
                                 related_name='ecritures_coda',
                                 to_field='code_operation')
    pcg = models.CharField(max_length=72)
    nom_pcg = models.CharField(max_length=36)
    code = models.CharField(max_length=12, db_column='doccode')
    numero = models.CharField(max_length=12, db_column='docnum')
    annee = models.IntegerField(db_column='yr')
    periode = models.IntegerField(db_column='period')
    date = models.DateTimeField(db_column='date_doc')
    description = models.CharField(max_length=36, db_column='descr_ligne')
    montant_eur = models.DecimalField(max_digits=12, decimal_places=2, db_column='montanteur')
    debit_credit = models.CharField(max_length=6, db_column='dc')
    implantation = models.CharField(max_length=32, db_column='imp_payeur')
    employe = models.CharField(max_length=36, db_column='salarie')
    paiement = models.CharField(max_length=23, db_column='statut_paiement')

    class Meta:
        db_table = 'coda_ecriture_boursier'
        managed = False
        ordering = ['date']
        verbose_name = 'écriture CODA'
        verbose_name_plural = 'écritures CODA'
