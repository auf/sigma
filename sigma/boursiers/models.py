# -*- encoding: utf-8 -*-

import datetime
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save
from django.db.models import Sum
from django.conf import settings

import auf.django.references.models as ref

from sigma.candidatures.models import Dossier, DossierMobilite
from sigma.candidatures.workflow import DOSSIER_ETAT_RETENU

ENABLE_FILTERED_QUERYSETS = getattr(settings, 'ENABLE_FILTERED_QUERYSETS', True)


class BoursierManager(models.Manager):
    """Manager pour les boursiers.

       Cache les fiches boursier dont le dossier de candidature n'indique
       pas qu'ils sont boursiers."""

    def get_query_set(self):
        base_qs = super(BoursierManager, self).get_query_set()
        if not ENABLE_FILTERED_QUERYSETS:
            return base_qs
        return base_qs.filter(dossier__etat=DOSSIER_ETAT_RETENU)


class BoursierInactifManager(models.Manager):
    """Manager pour les boursiers inactifs."""

    def get_query_set(self):
        base_qs = super(BoursierInactifManager, self).get_query_set()
        if not ENABLE_FILTERED_QUERYSETS:
            return base_qs
        return base_qs.exclude(dossier__etat=DOSSIER_ETAT_RETENU)


class Boursier(models.Model):
    """La fiche de suivi d'un boursier."""
    dossier = models.OneToOneField(
        Dossier, verbose_name='Candidature',
        related_name='boursier', primary_key=True, editable=False
    )
    code_operation = models.CharField(
        max_length=11, verbose_name="Code d'opération CODA", blank=True,
        db_index=True
    )
    numero_police_assurance = models.CharField(
        max_length=100, verbose_name="Numéro de police d'assurance",
        blank=True, default=''
    )

    date_debut = models.DateField(
        verbose_name="Date de début",
        blank=True,
        null=True,
        )
    date_fin = models.DateField(
        verbose_name="Date de fin",
        blank=True,
        null=True,
        )

    # Managers
    objects = BoursierManager()
    inactifs = BoursierInactifManager()

    class Meta:
        verbose_name = 'Allocataire'
        verbose_name_plural = 'Allocataires'

    def __unicode__(self):
        return self.nom_complet()

    def pays_origine(self):
        origine = self.dossier.origine
        if origine:
            return origine.pays
    pays_origine.short_description = 'Pays d\'origine'
    pays_origine.admin_order_field = 'dossier__origine__pays__nom'
            
    def code_bureau(self):
        pays = self.pays_origine()
        if pays:
            return pays.code_bureau.code
    code_bureau.short_description = 'Code d\'implantation d\'origine'
    code_bureau.admin_order_field = 'dossier__origine__pays__code_bureau__nom'

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

    def responsable_budgetaire(self):
        return '%s %s' % (
            self.appel().responsable_budgetaire.prenom,
            self.appel().responsable_budgetaire.nom,
            )
    responsable_budgetaire.short_description = 'Responsable Budgétaire'
    responsable_budgetaire.admin_order_field = 'dossier__appel__responsable_budgetaire__nom'

    def appel(self):
        return self.dossier.appel
    appel.short_description = 'Appel'
    appel.admin_order_field = 'dossier__appel__nom'

    def debut_mobilite(self):
        try:
            if (self.dossier.mobilite.date_debut_origine and
                self.dossier.mobilite.date_debut_accueil):
                return min(
                    self.dossier.mobilite.date_debut_origine,
                    self.dossier.mobilite.date_debut_accueil,
                    )
            else:
                return (self.dossier.mobilite.date_debut_accueil or
                        self.dossier.mobilite.date_debut_origine or
                        None)
        except DossierMobilite.DoesNotExist:
            return None
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
        dossier_lieu = getattr(self.dossier, lieu)
        pays = getattr(dossier_lieu, 'pays', None)

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

    def _abonnement(self, qs):
        return (
            qs.aggregate(total=Sum('montant_eur'))['total']
            or Decimal('0')
            )

    @property
    def abonnement_total(self):
        return self._abonnement(self.depenses_previsionnelles.all())

    @property
    def abonnement_total_origine(self):
        return self._abonnement(
            self.depenses_previsionnelles.filter(implantation='O'))

    @property
    def abonnement_total_accueil(self):
        return self._abonnement(
            self.depenses_previsionnelles.filter(implantation='A'))

    @property
    def prime_installation(self):
        pays = self.dossier.accueil.pays
        if pays is None:
            return Decimal('0')
        nord_sud = pays.nord_sud.lower()
        return Decimal(str(getattr(
                self.dossier.appel, 'prime_installation_%s' %
                nord_sud
                )))

    def depenses_totales(self):
        return self.abonnement_total + self.prime_installation
    depenses_totales.short_description = (
        'Total des dépenses prévues')

    def depenses_reelles_totales(self):
        return (self.get_depenses_reelles()
                .filter(etat_paiement='P')
                .aggregate(total=Sum('montant')))['total']
    depenses_reelles_totales.short_description = (
        'Total des dépenses CODA payées')

    def get_depenses_reelles(self):
        return EcritureCODA.objects \
            .filter(boursier_id=self.code_operation) \
            .order_by('numero_pcg', 'nom_pcg', '-date_document')

    def nom_complet(self):
        return self.prenom() + ' ' + self.nom()
    nom_complet.short_description = 'Nom'

    def creer_depenses_previsionelles(self):
        duree_accueil = self.dossier.mobilite.duree_accueil
        duree_origine = self.dossier.mobilite.duree_origine
        if self.bareme() == 'mensuel':
            for m in duree_accueil:
                DepensePrevisionnelle.objects.create(
                    boursier=self,
                    description='Abonnement mensuel (Accueil)',
                    date=m,
                    montant_eur=self.montant('accueil') or Decimal('0'),
                    implantation='A'
                    )
            for m in duree_origine:
                DepensePrevisionnelle.objects.create(
                    boursier=self,
                    description='Abonnement mensuel (Origine)',
                    date=m,
                    montant_eur=self.montant('origine') or Decimal('0'),
                    implantation='O'
                    )
        elif self.bareme() == 'perdiem':
            for m in duree_accueil.days_iterator:
                DepensePrevisionnelle.objects.create(
                    boursier=self,
                    description='Abonnement perdiem (Accueil)',
                    date=m,
                    montant_eur=self.montant('accueil') or Decimal('0'),
                    implantation='A'
                    )
            for m in duree_origine.days_iterator:
                DepensePrevisionnelle.objects.create(
                    boursier=self,
                    description='Abonnement perdiem (Origine)',
                    date=m,
                    montant_eur=self.montant('origine') or Decimal('0'),
                    implantation='O'
                    )
        elif self.bareme() == 'allocation':
            DepensePrevisionnelle.objects.create(
                boursier=self,
                description='Allocation unique (Acueil)',
                date=self.dossier.mobilite.date_debut_accueil,
                montant_eur=self.montant('accueil') or Decimal('0'),
                implantation='A'
                )

    def creer_vues_ensemble(self):
        for t in VueEnsemble.TYPE_CHOICES:
            VueEnsemble.objects.create(
                vue_type=t[0],
                code_document=VueEnsemble.CODE_DOCUMENT_DEFAULTS[t[0]],
                boursier=self,
                )

    def save(self, *args, **kwargs):
        # Assurons-nous que les codes opération sont uniques
        Boursier.inactifs \
                .filter(code_operation=self.code_operation) \
                .update(code_operation='')
        super(Boursier, self).save(*args, **kwargs)


class FicheFinanciere(Boursier):

    class Meta:
        proxy = True


class VueEnsemble(models.Model):
    CODE_DOCUMENT_DEFAULTS = {
        'EA': 'F-BOURSE-ENG',
        'AO': 'F-BOURSE-ABT',
        'AA': 'F-BOURSE-ABT',
        'II': 'F-FAC',
        }

    TYPE_CHOICES = (
        ('EA', 'Engagement de l\'allocation'),
        ('AO', 'Abonnement - Origine'),
        ('AA', 'Abonnement - Accueil'),
        ('II', 'Indemnité d\'installation'),
        )

    vue_type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        )
    code_document = models.CharField(
        max_length=32,
        )
    code_sigma = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        )
    boursier = models.ForeignKey(
        'Boursier',
        related_name='vue_ensemble',
        )

    class Meta:
        verbose_name ='Engagement d\'allocations'
        verbose_name_plural ='Engagements d\'allocations'

    @property
    def montant(self):
        if self.vue_type == 'EA':
            return self.boursier.abonnement_total
        elif self.vue_type == 'AO':
            return self.boursier.abonnement_total_origine
        elif self.vue_type == 'AA':
            return self.boursier.abonnement_total_accueil
        elif self.vue_type == 'II':
            return self.boursier.prime_installation


class DepensePrevisionnelle(models.Model):
    IMPLANTATION_CHOICES = (
        ('O', 'Origine'),
        ('A', 'Accueil'),
    )

    boursier = models.ForeignKey(
        Boursier, related_name="depenses_previsionnelles"
    )
    numero = models.IntegerField(null=True, blank=True, verbose_name='Numéro')
    description = models.CharField(max_length=36)
    commentaires = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
        )

    # Si perdiem, ajouter une date.
    date = models.DateField(
        null=True,
        blank=True,
        )

    montant_eur = models.DecimalField(
        max_digits=17,
        decimal_places=2,
        verbose_name='Montant (EUR)',
        )
    implantation = models.CharField(
        max_length=1,
        choices=IMPLANTATION_CHOICES,
        null=True,
        blank=True,
        )

    class Meta:
        verbose_name = "Dépense prévisionnelle"
        verbose_name_plural = "Dépenses prévisionnelles"

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
        # Creer boursier
        b, created = Boursier.objects.get_or_create(dossier=instance)
        if created:
            # Creer vues d'ensemble et depenses previsionnelles
            mobilite = instance.get_mobilite()
            if mobilite:
                b.date_debut = instance.mobilite.duree_totale.debut
                b.date_fin = instance.mobilite.duree_totale.fin
                
            b.creer_vues_ensemble()
            b.creer_depenses_previsionelles()

post_save.connect(dossier_post_save, sender=Dossier)
