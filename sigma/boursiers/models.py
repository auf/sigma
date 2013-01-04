# -*- encoding: utf-8 -*-

import datetime
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save
from django.db.models import Sum
from django.conf import settings
from django.core import exceptions

import auf.django.references.models as ref

from sigma.lib.models import (
    Individu,
    OrigineAbstract,
    AccueilAbstract,
    MobiliteAbstract,
    )
from sigma.candidatures.models import Dossier, Appel, DossierMobilite
from sigma.candidatures.workflow import DOSSIER_ETAT_RETENU

ENABLE_FILTERED_QUERYSETS = getattr(settings, 'ENABLE_FILTERED_QUERYSETS', True)


def copy_model(source, dest):
    fields = [x.attname for x in dest()._meta.fields
              if hasattr(source, x.attname)]
    data = dict([(x, getattr(source, x)) for x in fields])
    return dest(**data)



class Allocataire(Individu):
    """
    Représente un individu unique étant, ou ayant été, receveur d'une
    bourse.
    """

    # identification avancée
    nationalite = models.ForeignKey(
        ref.Pays,
        verbose_name=u"Nationalité",
        blank=True,
        null=True
        )

    # coordonnées
    # TODO: DRY... Expert.pays, Candidat.Pays.
    pays = models.ForeignKey(
        ref.Pays,
        related_name="allocataires",
        verbose_name=u"Pays de résidence",
        blank=True,
        null=True
        )

    @classmethod
    def from_dossier(cls, dossier, code_operation=None):
        if not dossier.est_allouable():
            raise ValueError(
                'Le dossier est incomplet, ou invalide. '
                'Impossible d\'allouer une bourse à ce candidat.')
        

        # Creer une copie du modele
        candidat = dossier.candidat
        allocataire = copy_model(candidat, Allocataire)

        # TODO: Changer lorsque qu'on change le champ de
        # candidat.region pour candidat.province.
        allocataire.province = candidat.province or candidat.region

        # Save
        allocataire.save()
        return allocataire

    @property
    def allocations_by_appel(self):
        allocations_dict = {}
        for alloc in self.allocations.all().order_by(
            'dossier__appel__id'):
            appel = alloc.dossier.appel
            nom = appel.nom
            if nom not in allocations_dict.keys():
                allocations_dict[nom] = {}
                allocations_dict[nom]['allocations'] = []
                allocations_dict[nom]['id'] = appel.id
            allocations_dict[nom]['allocations'].append(alloc);
            
        res = [(k, allocations_dict[k])
                for k in allocations_dict.keys()]
        return res


class AllocationManager(models.Manager):
    """Manager pour les allocations.

       Cache les fiches allocations dont le dossier de candidature n'indique
       pas qu'ils sont allocataires."""

    def get_query_set(self):
        base_qs = super(AllocationManager, self).get_query_set()
        if not ENABLE_FILTERED_QUERYSETS:
            return base_qs
        return base_qs.filter(dossier__etat=DOSSIER_ETAT_RETENU)


class Allocation(models.Model):
    """
    Représente l'allocation d'une bourse (unique, ou durant une année universitaire).
    """

    # Managers
    # objects = AllocationManager()

    # Dossier 
    dossier = models.ForeignKey(
        Dossier,
        verbose_name='Candidature',
        related_name='allocations',
        )

    # Allocataire.
    allocataire = models.ForeignKey(
        Allocataire,
        related_name='allocations',
        )

    # Si c'est un renouvellement, référer l'allocation originale.
    allocation_originale = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        help_text=('Si c\'est un renouvellement, choisissez '
                   ' l\'allocation originale'),
        )

    # Utilisé pour effectuer les recherches d'écritures CODA.
    code_operation = models.CharField(
        max_length=11,
        verbose_name="Code d'opération CODA",
        blank=True,
        db_index=True,
        )

    # Numéro de police d'assurance pour la période.
    numero_police_assurance = models.CharField(
        max_length=100, verbose_name="Numéro de police d'assurance",
        blank=True, default=''
        )

    # Plus ancienne des date de debut, incluant origine et accueil.
    date_debut = models.DateField(
        verbose_name="Date de début",
        blank=True,
        null=True,
        )

    # Plus récente des date de fin, incluant origine et accueil.
    date_fin = models.DateField(
        verbose_name="Date de fin",
        blank=True,
        null=True,
        )

    def create_vues_ensemble(self):
        for t in VueEnsemble.TYPE_CHOICES:
            VueEnsemble.objects.create(
                vue_type=t[0],
                code_document=VueEnsemble.CODE_DOCUMENT_DEFAULTS[t[0]],
                allocation=self,
                )

    def create_mobilite(self):
        # Créé les details de mobilite pour une allocation.
        
        # Quelques verifications.
        origine, accueil, mobilite = (
            self.dossier.origine,
            self.dossier.accueil,
            self.dossier.mobilite,
            )

        if origine:
            origine = copy_model(
                self.dossier.origine, AllocationOrigine)
            origine.allocation = self
            origine.save()

        if accueil:
            accueil = copy_model(
                self.dossier.origine, AllocationAccueil)
            accueil.allocation = self
            accueil.save()

        if mobilite:
            mobilite = copy_model(
                self.dossier.mobilite, AllocationMobilite)
            mobilite.allocation = self
            mobilite.save()


    def create_depenses_previsionelles(self, force_create=False):
        # Creer les depenses previsionelles prevues.
        # Le parametre force_create va creer des depenses
        # previsionelles meme si aucunes existe dans la base de
        # donnees.
        if not force_create:
            if self.depenses_previsionnelles.count() > 0:
                return


        duree_accueil = self.mobilite.duree_accueil
        duree_origine = self.mobilite.duree_origine
        montant_accueil = self.montant('accueil') or Decimal('0')
        montant_origine = self.montant('origine') or Decimal('0')
        bareme = self.dossier.appel.bareme
        
        if bareme == 'mensuel':
            accueil_iterator = duree_accueil
            origine_iterator = duree_origine
            accueil_desc = 'Abonnement mensuel (Accueil)'
            origine_desc = 'Abonnement mensuel (Origine)'
        elif bareme == 'perdiem':
            accueil_iterator = duree_accueil.days_iterator
            origine_iterator = duree_origine.days_iterator
            accueil_desc = 'Abonnement perdiem (Accueil)'
            origine_desc = 'Abonnement perdiem (Origine)'
        elif bareme == 'allocation':
            DepensePrevisionnelle.objects.create(
                allocation=self,
                description='Allocation unique (Acueil)',
                date=self.mobilite.date_debut_accueil,
                montant_eur=montant_accueil,
                implantation='A'
                )
            return
        else:
            # Si aucun match, ne fait rien. Ca ne devrait pas arriver.
            return
        
        # Si c'est mensuel ou perdiem, creer les depenses
        # previsionnelles:
        for mois in accueil_iterator:
            DepensePrevisionnelle.objects.create(
                allocation=self,
                description='Abonnement mensuel (Accueil)',
                date=mois,
                montant_eur=montant_accueil,
                implantation='A'
                )
        for mois in origine_iterator:
            DepensePrevisionnelle.objects.create(
                allocation=self,
                description='Abonnement mensuel (Origine)',
                date=mois,
                montant_eur=montant_origine,
                implantation='O'
                )

    def nom_complet(self):
        return self.prenom() + ' ' + self.nom()
    nom_complet.short_description = 'Nom'

    def pays_origine(self):
        origine = self.origine
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
        return self.allocataire.prenom
    prenom.short_description = 'Prénom'
    prenom.admin_order_field = 'allocataire__prenom'

    def nom(self):
        return self.allocataire.nom
    nom.short_description = 'Nom'
    nom.admin_order_field = 'allocataire__nom'

    def naissance_date(self):
        return self.allocataire.naissance_date
    naissance_date.short_description = 'Date de naissance'
    naissance_date.admin_order_field = 'allocataire__naissance_date'

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
            if (self.mobilite.date_debut_origine and
                self.mobilite.date_debut_accueil):
                return min(
                    self.mobilite.date_debut_origine,
                    self.mobilite.date_debut_accueil,
                    )
            else:
                return (self.mobilite.date_debut_accueil or
                        self.mobilite.date_debut_origine or
                        None)
        except AllocationMobilite.DoesNotExist:
            return None
    debut_mobilite.short_description = 'Début de la mobilité'
    # XXX: Trouver comment ordonner par la plus petite des date de début
    debut_mobilite.admin_order_field = 'dossier__mobilite__date_debut_origine'

    def bareme(self):
        return self.dossier.appel.bareme

    def implantation(self, lieu):
        etablissement = getattr(self, lieu).etablissement
        if etablissement:
            try:
                return etablissement.implantation
            except ref.Implantation.DoesNotExist:
                return None
        else:
            return None

    def montant(self, lieu):
        orig_acc = getattr(self, lieu)
        pays = getattr(orig_acc, 'pays', None)

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
        pays = self.accueil.pays
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

    def __unicode__(self):
        return 'Allocataire <%s> pour <%s>' % (
            self.allocataire.nom_complet(), self.dossier.appel.nom)

    # def validate_unique(self, *a, **kw):
    #     super(Allocation, self).validate_unique(*a, **kw)
    #     if (self.code_operation not in ('', None) and
    #         Allocation.tous.filter(code_operation=self.code_operation).count()
    #         > 0):
    #         raise exceptions.ValidationError('code_operation is not unique!')


class AllocationOrigine(OrigineAbstract):
    """
    Informations sur le contexte d'origine de l'allocataire.
    """
    allocation = models.OneToOneField(
        Allocation,
        verbose_name=u"Allocation",
        related_name="origine",
        )


class AllocationAccueil(AccueilAbstract):
    """
    Informations sur le contexte d'accueil de l'allocataire.
    """
    allocation = models.OneToOneField(
        Allocation,
        verbose_name=u"Allocation",
        related_name="accueil",
        )


class AllocationMobilite(MobiliteAbstract):
    """
    Informations sur la mobilité demandée par le candidat.
    """
    allocation = models.OneToOneField(
        Allocation,
        verbose_name=u"Allocation",
        related_name="mobilite",
        )


class FicheFinanciere(Allocation):
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
    allocation = models.ForeignKey(
        'Allocation',
        related_name='vue_ensemble',
        )

    class Meta:
        verbose_name ='Engagement d\'allocations'
        verbose_name_plural ='Engagements d\'allocations'

    @property
    def montant(self):
        if self.vue_type == 'EA':
            return self.allocation.abonnement_total
        elif self.vue_type == 'AO':
            return self.allocation.abonnement_total_origine
        elif self.vue_type == 'AA':
            return self.allocation.abonnement_total_accueil
        elif self.vue_type == 'II':
            return self.allocation.prime_installation


class DepensePrevisionnelle(models.Model):
    IMPLANTATION_CHOICES = (
        ('O', 'Origine'),
        ('A', 'Accueil'),
    )

    allocation = models.ForeignKey(
        Allocation,
        related_name='depenses_previsionnelles',
        null=True,
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
