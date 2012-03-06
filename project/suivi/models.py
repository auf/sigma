# -*- encoding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save

import auf.django.references.models as ref
from auf.django.coda import models as coda

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
    dossier = models.OneToOneField(
        Dossier, verbose_name='dossier de candidature',
        related_name='boursier', primary_key=True, editable=False
    )
    code_operation = models.CharField(
        max_length=11, verbose_name="code d'opération CODA", blank=True,
        default='', db_index=True
    )
    numero_police_assurance = models.CharField(
        max_length=100, verbose_name="numéro de police d'assurance",
        blank=True, default=''
    )
    responsable_budgetaire = models.ForeignKey(ref.Employe,
        verbose_name="responsable budgétaire",
        blank=True, null=True
    )
    date_debut = models.DateField(
        verbose_name="date de début", blank=True, null=True
    )
    date_fin = models.DateField(
        verbose_name="date de fin", blank=True, null=True
    )

    # Managers
    objects = BoursierManager()
    inactifs = BoursierInactifManager()

    class Meta:
        verbose_name = 'boursier'
        verbose_name_plural = 'boursiers'

    def __unicode__(self):
        return self.nom_complet()

    def prenom(self):
        return self.dossier.candidat.prenom
    prenom.short_description = 'Prénom'
    prenom.admin_order_field = 'dossier__candidat__prenom'

    def nom(self):
        return self.dossier.candidat.nom
    nom.short_description = 'Nom'
    nom.admin_order_field = 'dossier__candidat__nom'

    def naissance_date(self):
        return self.dossier.candidat.naissance_date
    naissance_date.short_description = 'Date de naissance'
    naissance_date.admin_order_field = 'dossier__candidat__naissance_date'

    def appel(self):
        return self.dossier.appel
    appel.short_description = 'Appel'
    appel.admin_order_field = 'dossier__appel__nom'

    def debut_mobilite(self):
        return self.dossier.mobilite.date_debut
    debut_mobilite.short_description = 'Début de la mobilité'
    debut_mobilite.admin_order_field = 'dossier__mobilite__date_debut'

    @property
    def implantation_origine(self):
        etablissement = self.dossier.origine.etablissement
        if etablissement:
            try:
                return etablissement.implantation
            except ref.Implantation.DoesNotExist:
                return None
        else:
            return None

    @property
    def implantation_accueil(self):
        etablissement = self.dossier.accueil.etablissement
        if etablissement:
            try:
                return etablissement.implantation
            except ref.Implantation.DoesNotExist:
                return None
        else:
            return None

    @property
    def debut_accueil(self):
        return self.dossier.mobilite.alternance_accueil_puis_origine

    @property
    def implantation_debut(self):
        if self.debut_accueil:
            return self.implantation_accueil
        else:
            return self.implantation_origine

    @property
    def implantation_fin(self):
        if self.debut_accueil:
            return self.implantation_origine
        else:
            return self.implantation_accueil

    @property
    def mois_debut(self):
        if self.debut_accueil:
            return self.dossier.mobilite.alternance_nb_mois_accueil
        else:
            return self.dossier.mobilite.alternance_nb_mois_origine

    @property
    def mois_fin(self):
        if self.debut_accueil:
            return self.dossier.mobilite.alternance_nb_mois_origine
        else:
            return self.dossier.mobilite.alternance_nb_mois_accueil

    @property
    def bareme(self):
        return self.dossier.appel.bareme

    @property
    def montant_origine(self):
        pays = self.dossier.origine.pays
        if pays is None:
            return None

        appel = self.dossier.appel
        bareme = appel.bareme
        if bareme == 'mensuel':
            if pays.nord_sud == 'Nord':
                return appel.montant_mensuel_origine_nord
            else:
                return appel.montant_mensuel_origine_sud
        elif bareme == 'perdiem':
            if pays.nord_sud == 'Nord':
                return appel.montant_perdiem_nord
            else:
                return appel.montant_perdiem_sud
        elif bareme == 'allocation':
            return appel.montant_allocation_unique
        else:
            return None

    @property
    def montant_accueil(self):
        pays = self.dossier.accueil.pays
        if pays is None:
            return None

        appel = self.dossier.appel
        bareme = appel.bareme
        if bareme == 'mensuel':
            if pays.nord_sud == 'Nord':
                return appel.montant_mensuel_accueil_nord
            else:
                return appel.montant_mensuel_accueil_sud
        elif bareme == 'perdiem':
            if pays.nord_sud == 'Nord':
                return appel.montant_perdiem_nord
            else:
                return appel.montant_perdiem_sud
        else:
            return None

    @property
    def montant_debut(self):
        if self.debut_accueil:
            return self.montant_accueil
        else:
            return self.montant_origine

    @property
    def montant_fin(self):
        if self.debut_accueil:
            return self.montant_origine
        else:
            return self.montant_accueil

    @property
    def prime_installation(self):
        pays = self.dossier.accueil.pays
        if pays is None:
            return None
        elif pays.nord_sud == 'Nord':
            return self.dossier.appel.prime_installation_nord
        else:
            return self.dossier.appel.prime_installation_sud

    def nom_complet(self):
        return self.prenom() + ' ' + self.nom()
    nom_complet.short_description = 'Nom'

    def lignes_ecritures_coda(self):
        return coda.Ligne.objects.filter(
            tiers_operation__code=self.code_operation
        )

    def save(self, *args, **kwargs):
        # Assurons-nous que les codes opération sont uniques
        Boursier.inactifs \
                .filter(code_operation=self.code_operation) \
                .update(code_operation='')
        super(Boursier, self).save(*args, **kwargs)


class DepensePrevisionnelle(models.Model):
    IMPLANTATION_CHOICES = (
        ('O', 'Origine'),
        ('A', 'Accueil'),
    )

    boursier = models.ForeignKey(
        Boursier, related_name="depenses_previsionnelles"
    )
    numero = models.IntegerField(null=True, blank=True, verbose_name='numéro')
    date = models.DateField()
    description = models.CharField(max_length=36)
    montant_eur = models.DecimalField(max_digits=17, decimal_places=2,
                                      verbose_name='montant (EUR)')
    implantation = models.CharField(max_length=1,
                                    choices=IMPLANTATION_CHOICES, null=True,
                                    blank=True)

    class Meta:
        verbose_name = "dépense prévisionnelle"
        verbose_name_plural = "dépenses prévisionnelles"

    def __unicode__(self):
        return self.description


def dossier_post_save(sender, instance=None, **kwargs):
    if instance and instance.etat == DOSSIER_ETAT_BOURSIER:
        Boursier.objects.get_or_create(dossier=instance)
post_save.connect(dossier_post_save, sender=Dossier)
