# -*- encoding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save

import auf.django.references.models as ref

from sigma.candidatures.models import Dossier
from sigma.candidatures.workflow import DOSSIER_ETAT_RETENU


class BoursierManager(models.Manager):
    """Manager pour les boursiers.

       Cache les fiches boursier dont le dossier de candidature n'indique
       pas qu'ils sont boursiers."""

    def get_query_set(self):
        qs = super(BoursierManager, self).get_query_set()
        return qs.filter(dossier__etat=DOSSIER_ETAT_RETENU)


class BoursierInactifManager(models.Manager):
    """Manager pour les boursiers inactifs."""

    def get_query_set(self):
        qs = super(BoursierInactifManager, self).get_query_set()
        return qs.exclude(dossier__etat=DOSSIER_ETAT_RETENU)


class Boursier(models.Model):
    """La fiche de suivi d'un boursier."""
    dossier = models.OneToOneField(
        Dossier, verbose_name='dossier de candidature',
        related_name='boursier', primary_key=True, editable=False
    )
    code_operation = models.CharField(
        max_length=11, verbose_name="code d'opération CODA", blank=True,
        db_index=True
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
        verbose_name = 'Boursier'
        verbose_name_plural = 'Boursiers'

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
        return min(self.dossier.mobilite.date_debut_origine,
                   self.dossier.mobilite.date_debut_accueil)
    debut_mobilite.short_description = 'Début de la mobilité'
    # XXX: Trouver comment ordonner par la plus petite des date de début
    debut_mobilite.admin_order_field = 'dossier__mobilite__date_debut_origine'

    def bareme(self):
        return self.dossier.appel.bareme

    def implantation(self, lieu):
        etablissement = getattr(self.dossier, lieu).etablissement
        if etablissement:
            try:
                return etablissement.implantation
            except ref.Implantation.DoesNotExist:
                return None
        else:
            return None

    def montant(self, lieu):
        pays = getattr(self.dossier, lieu).pays
        if pays is None:
            return None
        nord_sud = pays.nord_sud.lower()

        appel = self.dossier.appel
        bareme = appel.bareme
        if bareme == 'mensuel':
            return getattr(appel, 'montant_mensuel_%s_%s' % (lieu, nord_sud))
        elif bareme == 'perdiem':
            return getattr(appel, 'montant_perdiem_%s' % nord_sud)
        elif bareme == 'allocation':
            return appel.montant_allocation_unique
        else:
            return None

    def prime_installation(self):
        pays = self.dossier.accueil.pays
        if pays is None:
            return None
        nord_sud = pays.nord_sud.lower()
        return getattr(self.dossier.appel, 'prime_installation_%s' % nord_sud)

    def nom_complet(self):
        return self.prenom() + ' ' + self.nom()
    nom_complet.short_description = 'Nom'

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


class EcritureCODA(models.Model):
    DEBIT_CREDIT_CHOICES = (
        ('D', u'Débit'),
        ('C', u'Crédit'),
    )
    ETAT_PAIEMENT_CHOICES = (
        ('D', 'Disponible'),
        ('A', 'Attente'),
        ('X', 'Fermé (non-lettrable)'),
        ('P', 'Payé'),
        ('O', 'Proposé'),
        ('F', 'Effet en cours'),
        ('Y', 'Effet payé'),
        ('J', 'Effet en attente'),
    )

    boursier_id = models.CharField(
        max_length=11, verbose_name="ID du boursier", db_index=True
    )
    code_document = models.CharField(u"code de document", max_length=12)
    numero_document = models.CharField(u"numéro de document", max_length=12)
    periode = models.CharField(u"exercice/période", max_length=7)
    date_document = models.DateField(u"date du document")
    description = models.CharField(max_length=36)
    numero_pcg = models.CharField(u"numéro de compte PCG", max_length=5)
    nom_pcg = models.CharField(u"nom de compte PCG", max_length=36)
    montant = models.DecimalField(
        u"montant (EUR)", max_digits=17, decimal_places=2
    )
    implantation_payeuse = models.CharField(
        u"implantation payeuse", max_length=32
    )
    salarie = models.CharField(max_length=32)
    debit_credit = models.CharField(
        u"débit/crédit", max_length=1, choices=DEBIT_CREDIT_CHOICES
    )
    etat_paiement = models.CharField(
        u"état de paiement", max_length=1, choices=ETAT_PAIEMENT_CHOICES
    )
    date_maj = models.DateField(
        u"dernière mise à jour", db_index=True
    )


def dossier_post_save(sender, instance=None, **kwargs):
    if instance and instance.etat == DOSSIER_ETAT_RETENU:
        Boursier.objects.get_or_create(dossier=instance)
post_save.connect(dossier_post_save, sender=Dossier)
