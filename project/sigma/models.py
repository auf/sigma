# -*- encoding: utf-8 -*-

from django import forms
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from dynamo import dynamo_registry
from dynamo.models import *
from workflow import AppelWorkflow, DossierWorkflow
from datamaster_modeles.models import Pays, Bureau, Etablissement, Discipline, Region
from project.wcs.wrappers import WCSAppel
from smart_selects.db_fields import ChainedForeignKey

import auf.django.coda.models as coda_models

CIVILITE = (
    ('MR', "Monsieur"),
    ('MM', "Madame"),
    ('ME', "Mademoiselle"),
)

TYPE_THESE = (
    ('CT', "Co-tutelle"),
    ('CD', "Co-direction"),
    ('AU', "Autre"),
)

CANDIDAT_STATUT = (
    ('1', 'Etudiant'),
    ('2', 'Chercheur'),
    ('3', 'Enseignant'),
    ('4', 'Enseignant-chercheur'),
    ('5', 'Post-doc'),
)

REPONSE = (
    ('sr', "sr"),
    ('a', "a"),
    ('r', "r"),
)

PERIODE = (
    ('civile', "Année civile"),
    ('academique', "Année académique"),
)

BAREME = (
    ('mensuel', "Mensuel"),
    ('perdiem', "Perdiem"),
    ('allocation', "Allocation unique"),
)

NOTE_MIN = 1
NOTE_MAX = 100

class ExpertManager(models.Manager):

    def region(self, user):
        regions = [g.region for g in user.groupes_regionaux.all()]
        return self.get_query_set().filter(region__in=regions)

    def get_query_set(self):
        fkeys = ('region', )
        return super(ExpertManager, self).get_query_set().select_related(*fkeys).all()

class Expert(models.Model):

    objects = ExpertManager()

    nom = models.CharField(max_length=255, verbose_name=u"Nom")
    prenom = models.CharField(max_length=255, verbose_name=u"Prénom")
    courriel =  models.EmailField(max_length=75, null=True, blank=True)
    region = models.ForeignKey(Region, verbose_name=u"Région")
    region.region_filter_spec = True
    etablissement = models.ForeignKey(Etablissement,
                        verbose_name=u"Établissement",
                        blank=True, null=True)
    commentaire = models.TextField(null=True, blank=True)
    actif = models.BooleanField(default=True)
    disciplines = models.ManyToManyField(Discipline,
                        verbose_name=u"Disciplines",
                        blank=True, null=True)

    class Meta:
        ordering = ['nom', 'prenom']

    def __unicode__(self):
        return "%s %s" %(self.prenom, self.nom)

class UserProfile(models.Model):
    user = models.ForeignKey("auth.User", unique=True)
    disciplines = models.ManyToManyField(Discipline,
                        verbose_name=u"Disciplines",
                        blank=True, null=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class AppelManager(models.Manager):

    def region(self, user):
        regions = [g.region for g in user.groupes_regionaux.all()]
        return self.get_query_set().filter(region__in=regions)

    def get_query_set(self):
        fkeys = ('region', )
        return super(AppelManager, self).get_query_set().select_related(*fkeys).all()

if hasattr(settings, 'WCS_SIGMA_URL'):
    wcs = WCSAppel()
    APPEL_WCS_CHOICES = [(appel, appel) for appel in wcs.liste()]
else:
    APPEL_WCS_CHOICES = None


class Appel(AppelWorkflow, MetaModel, models.Model):
    """
    Un Appel est une proposition de l'AUF pour offrir une bourse de mobilité
    s'intégrant dans un projet.
    """

    objects = AppelManager()

    nom = models.CharField(max_length=255, verbose_name=u"Nom")
    region = models.ForeignKey(Region)
    region.region_filter_spec = True
    code_budgetaire = models.ForeignKey(
        coda_models.Element, verbose_name=u"Code budgétaire",
        limit_choices_to=({'niveau': 3, 'code__regex': r'^[^9]......$'})
    )
    formulaire_wcs = models.CharField(max_length=255, choices=APPEL_WCS_CHOICES,
                        verbose_name=u"Nom du formulaire WCS",
                        blank=True, null=True)
    date_debut_appel = models.DateField(verbose_name=u"Début de l'appel",
                        help_text=settings.HELP_TEXT_DATE,
                        blank=True, null=True)
    date_fin_appel = models.DateField(verbose_name=u"Fin de l'appel",
                        help_text=settings.HELP_TEXT_DATE,
                        blank=True, null=True)
    date_debut_mobilite = models.DateField(verbose_name=u"Début de la mobilité",
                        help_text=settings.HELP_TEXT_DATE,
                        blank=True, null=True)
    date_fin_mobilite = models.DateField(verbose_name=u"Fin de la mobilité",
                        help_text=settings.HELP_TEXT_DATE,
                        blank=True, null=True)
    appel_en_ligne = models.BooleanField(verbose_name=u"Appel d’offres en ligne")
    periode = models.CharField(max_length=32, verbose_name=u"Période de mobilité",
                        choices=PERIODE, blank=True, null=True)
    bareme = models.CharField(max_length=32, verbose_name=u"Barème",
                        choices=BAREME, blank=True, null=True)
    montant_mensuel_origine_sud = models.IntegerField(
                        verbose_name=u"Montant mensuel pays origine Sud",
                        blank=True, null=True)
    montant_mensuel_origine_nord = models.IntegerField(
                        verbose_name=u"Montant mensuel pays origine Nord",
                        blank=True, null=True)
    montant_mensuel_accueil_sud = models.IntegerField(
                        verbose_name=u"Montant mensuel pays accueil Sud",
                        blank=True, null=True)
    montant_mensuel_accueil_nord = models.IntegerField(
                        verbose_name=u"Montant mensuel pays accueil Nord",
                        blank=True, null=True)
    prime_installation_sud = models.IntegerField(
        verbose_name=u"Prime d'installation (pays du Sud)",
        blank=True, null=True
    )
    prime_installation_nord = models.IntegerField(
        verbose_name=u"Prime d'installation (pays du Nord)",
        blank=True, null=True
    )
    montant_perdiem_sud = models.IntegerField(
                        verbose_name=u"Montant jour (perdiem) pays Sud ",
                        blank=True, null=True)
    montant_perdiem_nord = models.IntegerField(
                        verbose_name=u"Montant jour (perdiem) pays Nord",
                        blank=True, null=True)
    montant_allocation_unique = models.IntegerField(
                        verbose_name=u"Montant allocation unique",
                        blank=True, null=True)
    conformites = models.ManyToManyField("TypeConformite", verbose_name=u"Conformités à demander",
                                         blank=True, null=True)
    types_piece = models.ManyToManyField("TypePiece", verbose_name=u"Types de pièces à demander",
                                          blank=True, null=True)

    class Meta:
        ordering = ['nom']

    def __unicode__(self):
        return self.nom

class Candidat(models.Model):
    """
    Personne qui répond à un appel d'offre.
    """
    dossier = models.OneToOneField('Dossier', verbose_name=u"Dossier", related_name="candidat")
    # meta
    date_creation = models.DateField(auto_now_add=True,
                        help_text=settings.HELP_TEXT_DATE,
                        verbose_name=u"Date de création")
    date_modification = models.DateField(auto_now=True,
                        help_text=settings.HELP_TEXT_DATE,
                        verbose_name=u"Date de modification")

    # identification personne
    civilite = models.CharField(max_length=2, verbose_name=u"Civilité",
                        choices=CIVILITE,
                        blank=True, null=True)
    nom = models.CharField(max_length=255, verbose_name=u"Nom")
    prenom = models.CharField(max_length=255, verbose_name=u"Prénom")
    nom_jeune_fille = models.CharField(max_length=255,
                        verbose_name=u"Nom de jeune fille",
                        blank=True, null=True)

    # identification avancée personne
    nationalite = models.ForeignKey(Pays, verbose_name=u"Nationalité",
                        blank=True, null=True)
    naissance_date = models.DateField(max_length=255,
                        verbose_name=u"Date de naissance",
                        help_text=settings.HELP_TEXT_DATE,
                        blank=True, null=True)

    # coordonnées
    pays = models.ForeignKey(Pays, related_name="pays",
                        verbose_name=u"Pays de résidence",
                        blank=True, null=True)
    adresse = models.CharField(max_length=255, verbose_name=u"Adresse",
                        blank=True, null=True)
    adresse_complement = models.CharField(max_length=255, verbose_name=u"Complément d'adresse",
                        blank=True, null=True)
    ville = models.CharField(max_length=255, verbose_name=u"Ville",
                        blank=True, null=True)
    region = models.CharField(max_length=255, verbose_name=u"Région",
                        blank=True, null=True)
    code_postal = models.CharField(max_length=255, verbose_name=u"Code postal",
                        blank=True, null=True)
    telephone = models.CharField(max_length=255,
                        verbose_name=u"Téléphone fixe",
                        blank=True, null=True, help_text=u"(+ code régional)")
    telephone_portable = models.CharField(max_length=255,
                        verbose_name=u"Téléphone portable",
                        blank=True, null=True, help_text=u"(+ code régional)")
    courriel = models.EmailField(max_length=255,
                        verbose_name=u"Adresse électronique",
                        blank=True, null=True)

    def __unicode__(self):
        return u"%s %s" % (self.nom.upper(), self.prenom)

class CategorieBourse(models.Model):
    """
    Catégorie de bourse : couche d'abstraction permettant aux utilisateurs de
    spécifier de nouveaux types de bourses.
    Cette catégorie doit être liée à un code budgétaire.
    """
    pass

class NiveauEtude(models.Model):
    """
    Nombre d'années universitaires.
    """
    nom = models.CharField(max_length=255, verbose_name=u"nom",)
    annees = models.CharField(max_length=2,
                        verbose_name=u"Nombre d'années universitaires", )

    class Meta:
        verbose_name = "niveau d'études"
        verbose_name_plural = "niveaux d'études"
        ordering = ['nom']

    def __unicode__(self):
        return self.nom

class Note(models.Model):
    """
    Une personne attribue une note à un dossier de candidature.
    """
    dossier = models.ForeignKey("Dossier", related_name="notes")
    expert = models.ForeignKey(Expert)
    date = models.DateField(auto_now_add=True)
    note = models.IntegerField(blank=True, null=True)

class Commentaire(models.Model):
    """
    Une personne peut ajouter un commentaire à un dossier de candidature.
    """
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)
    texte = models.TextField(verbose_name=u"Texte")

class DossierQuerySet(models.query.QuerySet):
    def filter(self, *args, **kwargs):
        pays = kwargs.pop('pays', None)
        region_accueil = kwargs.pop('regionaccueil', None)
        region_origine = kwargs.pop('regionorigine', None)
        qs = self
        if pays is not None:
            qs = qs.filter(candidat__pays__code=pays)
        if region_accueil is not None:
            qs = qs.filter(accueil__etablissement__region=region_accueil)
        if region_origine is not None:
            qs = qs.filter(origine__etablissement__region=region_origine)
        return super(DossierQuerySet, qs).filter(*args, **kwargs)

class DossierManager(models.Manager):

    def region(self, user):
        regions = [g.region for g in user.groupes_regionaux.all()]
        return self.get_query_set().filter(appel__region__in=regions)

    def get_query_set(self):
        fkeys = ('appel', 'origine', 'accueil', )
        return DossierQuerySet(Dossier).select_related(*fkeys).all()

class Dossier(DossierWorkflow, InstanceModel, models.Model):
    """
    Informations générales du dossier de candidature.
    """

    objects = DossierManager()

    appel = models.ForeignKey(Appel, related_name="appel", verbose_name=u"Appel")
    appel.admin_filter_select = True
    appel.appelregion_filter_spec = True

    candidat_statut = models.CharField(max_length=255,
                        verbose_name=u"Statut du candidat",
                        choices=CANDIDAT_STATUT, blank=True, null=True)
    candidat_fonction = models.CharField(max_length=255,
                        verbose_name=u"Fonction", blank=True, null=True)

    # Utilisé lors des appels internationaux pour définir le bureau (région) de traitement
    # Cette valeur était dérivée de dossier.etablissement (normalement équivalent de dossier.origine.etablissement)
    # Maintenant, on spécifie la valeur avec la région où est fait l'appel
    bureau_rattachement = models.ForeignKey(Bureau,
                        verbose_name=u"Bureau de rattachement",
                        blank=True, null=True)

    # Tentative pour récupérer de l'information passée
    dernier_projet_description = models.TextField(
                        verbose_name=u"Description du dernier projet \
                            ou programme",
                        blank=True, null=True)
    dernier_projet_annee = models.CharField(max_length=4,
                        verbose_name=u"Année du dernier projet ou programme",
                        blank=True, null=True)
    derniere_bourse_categorie = models.ForeignKey(CategorieBourse,
                        related_name="bourse_categorie",
                        verbose_name=u"Catégorie de la dernière bourse",
                        blank=True, null=True)
    derniere_bourse_annee = models.CharField(max_length=4,
                        verbose_name=u"Année de la dernière bourse",
                        blank=True, null=True)

    # Évaluations (à terminer // expert classements)
    annotations = models.ManyToManyField(Commentaire,
                        verbose_name=u"Commentaires", blank=True, null=True)
    moyenne_votes = models.FloatField(verbose_name=u"Moyenne des évaluateurs",
                        blank=True, null=True)
    moyenne_academique = models.FloatField(verbose_name=u"Moyenne académique",
                        blank=True, null=True)
    opportunite_regionale = models.CharField(max_length=255,
                        verbose_name=u"Opportunité régionale",
                        blank=True, null=True)
    #classement_1 = models.IntegerField(null=True, db_column='N_CLASSEMENT_1', blank=True)
    #classement_2 = models.IntegerField(null=True, db_column='N_CLASSEMENT_2', blank=True)
    #classement_3 = models.IntegerField(null=True, db_column='N_CLASSEMENT_3', blank=True)
    #coche_selection = models.BooleanField(db_column='I_COCHE_SELECTION', default=False)

    # Recevabilité (à faire)
    #autres_criteres = models.CharField(max_length=255, db_column='L_AUTRES_CRITERES')
    #erreurs_recevabilite = models.TextField(db_column='L_ERREURS_RECEVABILITE')
    #repechage = models.BooleanField(db_column='I_REPECHAGE', default=False)
    #rendu_irrecevable = models.BooleanField(db_column='I_RENDU_IRRECEVABLE', default=False)

    # Notifications (à faire)
    #reponse_notification = models.CharField(max_length=6, db_column='Y_REPONSE_NOTIFICATION', choices=REPONSE, default='sr')
    #commentaire_notification = models.CharField(max_length=255, db_column='L_COMMENTAIRE_NOTIFICATION')

    # ce champs est système, il est saisi dans la partie mobilité mais il est copié ici pour pouvoir être filtré
    discipline = models.ForeignKey(Discipline, verbose_name=u"Discipline", blank=True, null=True)
    experts = models.ManyToManyField(Expert, verbose_name=u'Experts',
                                     related_name="dossiers", blank=True)

    class Meta:
        ordering = ['appel__nom', 'candidat__nom', 'candidat__prenom']

    def __unicode__(self, ):
        try:
            candidat = u"%s pour l'" % self.candidat
        except:
            candidat = u""
        return u"dossier #%s (%sappel %s)" % (self.id, candidat, self.appel)

    def calculer_moyenne(self,):
        if self.id:
            notes = [note.note for note in self.notes.all() if note.note is not None]
            if len(notes) > 0:
                self.moyenne_votes = float(sum(notes)) / len(notes)
            else:
                self.moyenne_votes = 0

    def __init__(self, *args, **kwargs):
        """
        A l'instanciation, on synchronise les meta pour optimisation
        """
        super(Dossier, self).__init__(*args, **kwargs)

        try:
            if self.discipline != self.mobilite.discipline:
                self.discipline = self.mobilite.discipline
                self.save()
        except:
            pass

        # Prépouplation des objets notes selon les experts sélectionnés
        if self.id is not None:

            experts_presents = []

            for n in self.notes.all():
                try:
                    experts_presents.append(n.expert)
                except:
                    # l'expert a été supprimé
                    pass

            for expert in self.experts.all():
               if expert not in experts_presents:
                 note = Note()
                 note.dossier = self
                 note.expert = expert
                 note.save()


    def save(self, *args, **kwargs):
        self.calculer_moyenne()

        super(Dossier, self).save(*args, **kwargs)

    def nom(self):
        return self.candidat.nom.upper()
    nom.short_description = "Nom"
    nom.admin_order_field = 'candidat__nom'

    def prenom(self):
        return self.candidat.prenom
    prenom.short_description = "Prénom"
    prenom.admin_order_field = 'candidat__prenom'

    def naissance_date(self):
        return self.candidat.naissance_date
    naissance_date.short_description = "Date de naissance"
    naissance_date.admin_order_field = 'candidat__naissance_date'

class DossierFaculte(models.Model):
    # Etablissement connu de l'AUF
    etablissement = ChainedForeignKey(Etablissement,
                        chained_field="pays",
                        chained_model_field="pays",
                        show_all=False,
                        auto_choose=True,
                        verbose_name=u"Établissement, si membre de l'AUF",
                        blank=True, null=True)

    # Autre établissement
    autre_etablissement_nom = models.CharField(max_length=255,
                        verbose_name=u"Autre établissement",
                        blank=True, null=True)
    autre_etablissement_pays = models.ForeignKey(Pays,
                        verbose_name=u"Pays", blank=True, null=True)
    autre_etablissement_adresse = models.CharField(max_length=255,
                        verbose_name=u"Adresse", blank=True, null=True)
    autre_etablissement_code_postal = models.CharField(max_length=255,
                        verbose_name=u"Code postal", blank=True, null=True)
    autre_etablissement_ville = models.CharField(max_length=255,
                        verbose_name=u"Ville", blank=True, null=True)
    autre_etablissement_region = models.CharField(max_length=255,
                        verbose_name=u"Région", blank=True, null=True)

    # responsable scientifique (Accord scientifique)
    resp_sc_civilite = models.CharField(max_length=2,
                        verbose_name=u"Civilité",
                        choices=CIVILITE, blank=True, null=True)
    resp_sc_nom = models.CharField(max_length=255,
                        verbose_name=u"Nom",
                        blank=True, null=True)
    resp_sc_prenom = models.CharField(max_length=255,
                        verbose_name=u"Prénom",
                        blank=True, null=True)
    resp_sc_fonction = models.CharField(max_length=255,
                        verbose_name=u"Fonction",
                        blank=True, null=True)
    resp_sc_courriel = models.CharField(max_length=255,
                        verbose_name=u"Courriel",
                        blank=True, null=True)
    resp_sc_telephone = models.CharField(max_length=255,
                        verbose_name=u"Téléphone",
                        blank=True, null=True)
    resp_sc_fax = models.CharField(max_length=255,
                        verbose_name=u"Télécopieur",
                        blank=True, null=True)

    # faculté, département ou labo (Accord scientifique)
    faculte_nom = models.CharField(max_length=255,
                        verbose_name=u"Faculté / Centre / Département",
                        blank=True, null=True)
    faculte_adresse = models.CharField(max_length=255,
                        verbose_name=u"Adresse",
                        blank=True, null=True)
    faculte_ville = models.CharField(max_length=255,
                        verbose_name=u"Ville",
                        blank=True, null=True)
    faculte_code_postal = models.CharField(max_length=255,
                        verbose_name=u"Code postal",
                        blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def pays(self):
        return self.etablissement.pays if self.etablissement else self.autre_etablissement_pays

class DossierOrigine(DossierFaculte):
    """
    Informations sur le contexte d'origine du candidat.
    """
    dossier = models.OneToOneField(Dossier, verbose_name=u"Dossier", related_name="origine")

    # Pour le champ de sélection Etablissement
    pays = models.ForeignKey(Pays, to_field="code", related_name="origine_pays",
                        verbose_name=u"Pays", blank=True, null=True)

    # responsable institutionnel à l'origine
    resp_inst_civilite = models.CharField(max_length=2,
                        verbose_name=u"Civilité",
                        choices=CIVILITE, blank=True, null=True)
    resp_inst_nom = models.CharField(max_length=255,
                        verbose_name=u"Nom",
                        blank=True, null=True)
    resp_inst_prenom = models.CharField(max_length=255,
                        verbose_name=u"Prénom",
                        blank=True, null=True)
    resp_inst_fonction = models.CharField(max_length=255,
                        verbose_name=u"Fonction",
                        blank=True, null=True)
    resp_inst_courriel = models.CharField(max_length=255,
                        verbose_name=u"Courriel",
                        blank=True, null=True)
    resp_inst_telephone = models.CharField(max_length=255,
                        verbose_name=u"Téléphone",
                        blank=True, null=True)
    resp_inst_fax = models.CharField(max_length=255,
                        verbose_name=u"Télécopieur",
                        blank=True, null=True)

class DossierAccueil(DossierFaculte):
    """
    Informations sur le contexte d'accueil du candidat.
    """
    dossier = models.OneToOneField(Dossier, verbose_name=u"Dossier", related_name="accueil")

    # Pour le champ de sélection Etablissement
    pays = models.ForeignKey(Pays, to_field="code", related_name="accueil_pays",
                        verbose_name=u"Pays", blank=True, null=True)


class Public(models.Model):
    """
    """
    nom = models.CharField(max_length=255, verbose_name=u"Nom")

    class Meta:
        verbose_name = "public visé"
        verbose_name_plural = "publics visés"
        ordering = ['nom']

    def __unicode__(self):
        return self.nom


class Intervention(models.Model):
    """
    """
    nom = models.CharField(max_length=255, verbose_name=u"Nom")

    class Meta:
        verbose_name = "intervention"
        verbose_name_plural = "interventions"
        ordering = ['nom']

    def __unicode__(self):
        return self.nom


class DossierMobilite(models.Model):
    """Informations sur la mobilité demandée par le candidat.
    """
    dossier = models.OneToOneField(Dossier, verbose_name=u"Dossier", related_name="mobilite")

    # Période de mobilité
    date_debut = models.DateField(verbose_name=u"Date de début souhaitée",
                        help_text=settings.HELP_TEXT_DATE,
                        blank=True, null=True)
    date_fin = models.DateField(verbose_name=u"Date de fin souhaitée",
                        help_text=settings.HELP_TEXT_DATE,
                        blank=True, null=True)
    duree = models.CharField(max_length=255,
                        verbose_name=u"Durée totale mobilité souhaitée (mois)",
                        blank=True, null=True)

    # Dossier scientifique
    intitule_projet = models.CharField(max_length=255,
                        verbose_name=u"Intitulé du projet",
                        blank=True, null=True)
    mots_clefs = models.CharField(max_length=255,
                        verbose_name=u"Mots clefs", blank=True, null=True)

    # Disciplines
    discipline = models.ForeignKey(Discipline, verbose_name=u"Discipline",
                        blank=True, null=True)
    sous_discipline = models.CharField(max_length=255, blank=True, null=True)

    # Formation en cours
    formation_en_cours_diplome = models.CharField(max_length=255,
                        verbose_name=u"Intitulé du diplôme",
                        blank=True, null=True)
    formation_en_cours_niveau = models.ForeignKey(NiveauEtude,
                        related_name="formation_en_cours_niveau",
                        verbose_name=u"Niveau d'études", blank=True, null=True)

    # Diplôme demandé
    diplome_demande_nom = models.CharField(max_length=255,
                        verbose_name=u"Diplôme demandé", blank=True, null=True)
    diplome_demande_niveau = models.ForeignKey(NiveauEtude,
                        related_name="diplome_demande_niveau",
                        verbose_name=u"Niveau d'études", blank=True, null=True)

    # Alternance
    alternance_nb_mois_origine = models.IntegerField(
                        verbose_name=u"Nombre de mois à l'origine",
                        blank=True, null=True)
    alternance_nb_mois_accueil = models.IntegerField(
                        verbose_name=u"Nombre de mois à l'accueil",
                        blank=True, null=True)
    alternance_accueil_puis_origine = models.NullBooleanField(
                        verbose_name=u"Mobilité commençée à l'accueil?",
                        blank=True, null=True)

    # Thèse
    these_date_inscription = models.DateField(
                        help_text=settings.HELP_TEXT_DATE,
                        verbose_name=u"Date de première inscription en thèse",
                        blank=True, null=True)
    these_date_obtention_prevue = models.DateField(
                        help_text=settings.HELP_TEXT_DATE,
                        verbose_name=u"Date d'obtention prévue",
                        blank=True, null=True)
    these_soutenance_pays = models.ForeignKey(Pays,
                        related_name="soutenance_pays",
                        verbose_name=u"Pays de soutenance",
                        blank=True, null=True)
    these_soutenance_date = models.DateField(
                        help_text=settings.HELP_TEXT_DATE,
                        verbose_name=u"Date de soutenance",
                        blank=True, null=True)
    these_type = models.CharField(max_length=2,
                        verbose_name=u"Type de thèse",
                        choices=TYPE_THESE, blank=True, null=True)

    # directeur thèse accueil
    dir_acc_civilite = models.CharField(max_length=2,
                        verbose_name=u"Civilité", choices=CIVILITE,
                        blank=True, null=True)
    dir_acc_nom = models.CharField(max_length=255,
                        verbose_name=u"Nom", blank=True, null=True)
    dir_acc_prenom = models.CharField(max_length=255,
                        verbose_name=u"Prénom", blank=True, null=True)
    dir_acc_courriel = models.CharField(max_length=255,
                        verbose_name=u"adresse électronique",
                        blank=True, null=True)
    dir_acc_telephone = models.CharField(max_length=255,
                        verbose_name=u"Téléphone",
                        blank=True, null=True)

    # directeur thèse origine
    dir_ori_civilite = models.CharField(max_length=2, verbose_name=u"Civilité",
                        choices=CIVILITE, blank=True, null=True)
    dir_ori_nom = models.CharField(max_length=255, verbose_name=u"Nom",
                        blank=True, null=True)
    dir_ori_prenom = models.CharField(max_length=255, verbose_name=u"Prénom",
                        blank=True, null=True)
    dir_ori_courriel = models.CharField(max_length=255,
                        verbose_name=u"adresse électronique",
                        blank=True, null=True)
    dir_ori_telephone = models.CharField(max_length=255,
                        verbose_name=u"Téléphone",
                        blank=True, null=True)

    # Programme de mission
    type_intervention = models.ForeignKey(Intervention,
                        verbose_name=u"Type d'intervention",
                        blank=True, null=True)
    public_vise = models.ForeignKey(Public, verbose_name=u"Public visé",
                        blank=True, null=True)
    autres_publics = models.CharField(max_length=255,
                        verbose_name=u"Autres publics", blank=True, null=True)


class Diplome(models.Model):
    """
    """
    dossier = models.ForeignKey(Dossier)
    nom = models.CharField(max_length=255, verbose_name=u"Intitulé",
                        blank=True, null=True)
    date = models.DateField(max_length=255, verbose_name=u"Date d'obtention",
                        help_text=settings.HELP_TEXT_DATE,
                        blank=True, null=True)
    niveau = models.ForeignKey(NiveauEtude, related_name="niveau",
                        verbose_name=u"Niveau d'études",
                        blank=True, null=True)

    # Etablissement connu de l'AUF
    etablissement = models.ForeignKey(Etablissement,
                        verbose_name=u"Établissement d'obtention si membre de l'AUF",
                        blank=True, null=True)

    # Autre établissement
    autre_etablissement_nom = models.CharField(max_length=255,
                        verbose_name=u"Autre établissement",
                        blank=True, null=True)
    autre_etablissement_pays = models.ForeignKey(Pays,
                        related_name="etablissement_pays",
                        verbose_name=u"Pays de l'établissement",
                        blank=True, null=True)


class TypePiece(models.Model):
    """
    """
    nom = models.CharField(max_length=255, verbose_name=u"Nom système")

    def __unicode__(self):
        return unicode(self.nom)

    class Meta:
        verbose_name = 'type de pièce'
        verbose_name_plural = 'types de pièces'
        ordering = ['nom']

class Piece(models.Model):
    """
    """
    dossier = models.ForeignKey(Dossier, related_name="pieces")
    nom = models.CharField(max_length=255, verbose_name=u"Nom", blank=True, null=True)
    fichier = models.FileField(verbose_name=u"Fichier", upload_to="pieces",
                               storage=FileSystemStorage(location=settings.UPLOADS_ROOT),
                               blank=True, null=True)
    conforme = models.NullBooleanField(verbose_name=u"Pièce conforme")

    def __unicode__(self):
        return unicode(self.nom)

class AttributWCS(models.Model):
    """
    """
    dossier = models.ForeignKey(Dossier, related_name="attributs_wcs")
    attribut = models.CharField(max_length=255, verbose_name=u"Attribut", blank=True, null=True)
    valeur = models.TextField(verbose_name=u"Valeur", blank=True, null=True)

    class Meta:
        verbose_name = u"Attribut WCS"
        verbose_name_plural = u"Attributs WCS"

    def __unicode__(self):
        return u"%s" % self.attribut

class GroupeRegional(models.Model):
    region = models.ForeignKey(Region, verbose_name="région")
    users = models.ManyToManyField('auth.User', related_name="groupes_regionaux", verbose_name=u"membres", blank=True, null=True)

    class Meta:
        verbose_name = u"groupe régional"
        verbose_name_plural = "groupes régionaux"
        ordering = ['region__nom']

    def __unicode__(self):
        return self.region.nom

################################################################################
# Dynamo
################################################################################
class TypeConformite(TypeProperty, models.Model):
    """
    Lié à l'appel
    """
    class Meta:
        verbose_name = u"type de conformité"
        verbose_name_plural = u"types de conformités"

class Conformite(ValueProperty, models.Model):
    """
    Lié au dossier
    """
    dossier = models.ForeignKey(Dossier)
    type = models.ForeignKey("TypeConformite")
    conforme = models.NullBooleanField(verbose_name=u"Conforme?",
                        blank=True, null=True)

    class Meta:
        verbose_name = u"Conformité"

# on relie tous les modèles ensembles pour générer les admin
dynamo_registry.register(Appel, TypeConformite, Dossier, Conformite)


