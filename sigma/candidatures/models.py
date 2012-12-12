# -*- encoding: utf-8 -*-

import re
import datetime
import calendar

from auf.django.references import models as ref
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from sigma.dynamo import dynamo_registry
from sigma.dynamo.models import \
        MetaModel, InstanceModel, TypeProperty, ValueProperty
from sigma.candidatures.workflow import DossierWorkflow

CIVILITE = (
    ('MR', "Monsieur"),
    ('MM', "Madame"),
    ('ME', "Mademoiselle"),
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

BOOLEAN_RADIO_OPTIONS = (
    (1, 'Oui'),
    (0, 'Non')
)

NOTE_MIN = 1
NOTE_MAX = 20


class ExpertManager(models.Manager):

    def get_query_set(self):
        fkeys = ('region', )
        return super(ExpertManager, self).get_query_set() \
                .select_related(*fkeys).all()


class Expert(models.Model):
    nom = models.CharField(max_length=255, verbose_name=u"Nom")
    prenom = models.CharField(max_length=255, verbose_name=u"Prénom")
    courriel = models.EmailField(max_length=75, blank=True)
    region = models.ForeignKey(ref.Region, verbose_name=u"Région")
    etablissement = models.ForeignKey(
        ref.Etablissement, verbose_name=u"Établissement", blank=True,
        null=True
    )
    commentaire = models.TextField(blank=True)
    actif = models.BooleanField(default=True)
    disciplines = models.ManyToManyField(
        ref.Discipline, verbose_name=u"Disciplines", blank=True, null=True
    )

    objects = ExpertManager()

    class Meta:
        ordering = ['nom', 'prenom']
        verbose_name = u"Expert"
        verbose_name_plural = u"Experts"

    def __unicode__(self):
        return "%s %s" % (self.prenom, self.nom)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', primary_key=True)
    regions = models.ManyToManyField(
        ref.Region, verbose_name=u"régions", blank=True, null=True
    )
    disciplines = models.ManyToManyField(
        ref.Discipline, verbose_name=u"disciplines", blank=True, null=True
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


class AppelManager(models.Manager):

    def get_query_set(self):
        fkeys = ('region', )
        return super(AppelManager, self).get_query_set() \
                .select_related(*fkeys).all()


class TypeBourse(models.Model):
    nom = models.CharField(u"nom", max_length=255)

    def __unicode__(self):
        return self.nom

def validateur_annee(value):
    string_value = unicode(value)
    if re.match(r"^\d{4}$", string_value) is None:
        raise ValidationError("Inscrivez l'année avec 4 chiffres")
    return value

def validateur_code_budgetaire(value):
    if re.match(r"^\d{5}\w{2}$", value) is None:
        raise ValidationError(u"Le code budgétaire est composé de 5 chiffres + 2 lettres")
    return value


class Appel(MetaModel, models.Model):
    """
    Un Appel est une proposition de l'AUF pour offrir une bourse de mobilité
    s'intégrant dans un projet.
    """

    objects = AppelManager()

    nom = models.CharField(u"nom", max_length=255, blank=True,
            help_text=u"À défaut d'un type de bourse qui convienne, expliquez la nature de votre appel")
    type_bourse = models.ForeignKey(TypeBourse,
            verbose_name=u"type de bourse",
            blank=True, null=True)
    region = models.ForeignKey(ref.Region, verbose_name=u"région")
    annee = models.IntegerField(u"année", validators=[validateur_annee, ])

    code_budgetaire = models.CharField(
        u"Code budgétaire", max_length=72,
        help_text=u"Le code budgétaire est composé de 5 chiffres + 2 lettres",
        validators=[validateur_code_budgetaire, ]
    )
    date_debut_appel = models.DateField(
        u"Début de l'appel", help_text=settings.HELP_TEXT_DATE,
        blank=True, null=True
    )
    date_fin_appel = models.DateField(
        u"Fin de l'appel", help_text=settings.HELP_TEXT_DATE,
        blank=True, null=True
    )
    date_debut_mobilite = models.DateField(
        u"Début de la mobilité",
        help_text=settings.HELP_TEXT_DATE, blank=True, null=True
    )
    date_fin_mobilite = models.DateField(
        u"Fin de la mobilité",
        help_text=settings.HELP_TEXT_DATE, blank=True, null=True
    )
    periode = models.CharField(
        u"Période de mobilité", max_length=32, choices=PERIODE, blank=True
    )
    bareme = models.CharField(
        u"Barème", max_length=32, choices=BAREME, blank=True
    )
    montant_mensuel_origine_sud = models.IntegerField(
        u"Montant mensuel pays origine Sud", 
        blank=True, null=True,
        help_text=u"Indiquer 0 dans les champs non-pertinents",
    )
    montant_mensuel_origine_nord = models.IntegerField(
        u"Montant mensuel pays origine Nord", 
        blank=True, null=True,
        help_text=u"Indiquer 0 dans les champs non-pertinents",
    )
    montant_mensuel_accueil_sud = models.IntegerField(
        u"Montant mensuel pays accueil Sud", 
        blank=True, null=True,
        help_text=u"Indiquer 0 dans les champs non-pertinents",
    )
    montant_mensuel_accueil_nord = models.IntegerField(
        u"Montant mensuel pays accueil Nord", 
        blank=True, null=True,
        help_text=u"Indiquer 0 dans les champs non-pertinents",
    )
    prime_installation_sud = models.IntegerField(
        u"Prime d'installation (pays du Sud)", 
        blank=True, null=True,
        help_text=u"Indiquer 0 dans les champs non-pertinents",
    )
    prime_installation_nord = models.IntegerField(
        u"Prime d'installation (pays du Nord)", 
        blank=True, null=True,
        help_text=u"Indiquer 0 dans les champs non-pertinents",
    )
    montant_perdiem_sud = models.IntegerField(
        u"Montant jour (perdiem) pays Sud ", 
        blank=True, null=True,
        help_text=u"Indiquer 0 dans les champs non-pertinents",
    )
    montant_perdiem_nord = models.IntegerField(
        u"Montant jour (perdiem) pays Nord", 
        blank=True, null=True,
        help_text=u"Indiquer 0 dans les champs non-pertinents",
    )
    montant_allocation_unique = models.IntegerField(
        u"Montant allocation unique", 
        blank=True, null=True,
        help_text=u"Indiquer 0 dans les champs non-pertinents",
    )
    conformites = models.ManyToManyField(
        "TypeConformite", verbose_name=u"Conformités à demander",
        blank=True, null=True
    )
    pieces_attendues = models.ManyToManyField(
        "TypePiece", verbose_name=u"Pièces à demander",
        blank=True, null=True
    )

    class Meta:
        ordering = ['nom']
        verbose_name = u"Appel"
        verbose_name_plural = u"Appels"

    def __unicode__(self):
        if self.nom != u"":
            return u"%s %s" % (self.nom, self.code_budgetaire)
        else:
            return u"%s %s %s %s" % (self.type_bourse, self.annee,
                    self.region.nom, self.code_budgetaire)

    def clean(self):
        if not self.nom and self.type_bourse is None:
            raise ValidationError(u"Choisissez un type de bourse ET/OU remplissez un nom")
        if self.date_debut_appel is not None and self.date_fin_appel is not None and \
                self.date_debut_appel > self.date_fin_appel:
            raise ValidationError(u"La date de fin d'appel précède la date de début d'appel")
        if self.date_debut_mobilite is not None and self.date_fin_mobilite is not None and \
                self.date_debut_mobilite > self.date_fin_mobilite:
            raise ValidationError(u"La date de fin de mobilité précède la date de début de mobilité")

class Candidat(models.Model):
    """
    Personne qui répond à un appel d'offre.
    """
    dossier = models.OneToOneField(
        'Dossier', verbose_name=u"Dossier", related_name="candidat"
    )

    # meta
    date_creation = models.DateField(auto_now_add=True,
                        help_text=settings.HELP_TEXT_DATE,
                        verbose_name=u"Date de création")
    date_modification = models.DateField(auto_now=True,
                        help_text=settings.HELP_TEXT_DATE,
                        verbose_name=u"Date de modification")

    # identification personne
    civilite = models.CharField(
        max_length=2, verbose_name=u"Civilité", choices=CIVILITE,
        blank=True
    )
    nom = models.CharField(max_length=255, verbose_name=u"Nom")
    prenom = models.CharField(max_length=255, verbose_name=u"Prénom")
    nom_jeune_fille = models.CharField(
        max_length=255, verbose_name=u"Nom de jeune fille", blank=True
    )

    # identification avancée personne
    nationalite = models.ForeignKey(
        ref.Pays, verbose_name=u"Nationalité", blank=True, null=True
    )
    naissance_date = models.DateField(
        max_length=255, verbose_name=u"Date de naissance",
        help_text=settings.HELP_TEXT_DATE, blank=True, null=True
    )

    # coordonnées
    pays = models.ForeignKey(
        ref.Pays, related_name="pays", verbose_name=u"Pays de résidence",
        blank=True, null=True
    )
    adresse = models.TextField(u'Adresse', blank=True)
    adresse_complement = models.TextField(
        u"complément d'adresse", blank=True
    )
    ville = models.CharField(
        max_length=255, verbose_name=u"Ville", blank=True
    )
    region = models.CharField(
        max_length=255, verbose_name=u"Région / Province / État", blank=True
    )
    code_postal = models.CharField(
        max_length=255, verbose_name=u"Code postal", blank=True
    )
    telephone = models.CharField(
        max_length=255, verbose_name=u"Téléphone fixe", blank=True,
        help_text=u"(+ code régional)"
    )
    telephone_portable = models.CharField(
        max_length=255, verbose_name=u"Téléphone portable", blank=True,
        help_text=u"(+ code régional)"
    )
    courriel = models.EmailField(
        max_length=255, verbose_name=u"Adresse électronique", blank=True
    )

    def age(self):
        if not self.naissance_date:
            return None
        today = datetime.date.today()
        try:
            birthday = self.naissance_date.replace(
                year=today.year)
        except ValueError:
            birthday = self.naissance_date.replace(
                year=today.year,
                day=self.naissance_date.day-1)
        if birthday > today:
            return today.year - self.naissance_date.year - 1
        else:
            return today.year - self.naissance_date.year

    def __unicode__(self):
        return u"%s %s" % (self.nom.upper(), self.prenom)


class Note(models.Model):
    """
    Une personne attribue une note à un dossier de candidature.
    """
    dossier = models.ForeignKey("Dossier", related_name="notes")
    expert = models.ForeignKey(Expert, blank=True, null=True)
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

    def get_query_set(self):
        fkeys = ('appel', 'origine', 'accueil', 'candidat', )
        return DossierQuerySet(Dossier).select_related(*fkeys).all()


class Dossier(DossierWorkflow, InstanceModel, models.Model):
    """
    Informations générales du dossier de candidature.
    """
    CANDIDAT_STATUT_CHOICES = (
        ('1', 'Etudiant'),
        ('2', 'Chercheur'),
        ('3', 'Enseignant'),
        ('4', 'Enseignant-chercheur'),
        ('5', 'Post-doc'),
    )

    DERNIERE_MOBILITE_TYPE = (
        ('stage_professionel', 'Stage professionnel (SP)'),
        ('mission', 'Mission d\'appui et d\'enseignement (ME)'),
        ('doctorat', 'Doctorat (Formation à la Recherche - FR)'),
        ('contribution', 'Contribution à manifestation scientifique (BX)'),
        ('master', 'Master/Maitrise (Formation Initiale - FX)'),
        ('perfectionnement_formation', 'Perfectionnement en formation (PF)'),
        ('perfectionnement_recherche', 'Perfectionnement en recherche (hors post-doc) (PR)'),
        ('post_doctorat', 'Post-doctorat (PP)'),
        ('stage_culturel', 'Stage culturel (SC)')
    )

    a_verifier = models.BooleanField(verbose_name=u"À vérifier", default=False)

    appel = models.ForeignKey(
        Appel, related_name="appel", verbose_name=u"appel"
    )
    appel.admin_filter_select = True

    candidat_statut = models.CharField(
        max_length=255, verbose_name=u"Statut du candidat",
        choices=CANDIDAT_STATUT_CHOICES, blank=True
    )
    candidat_fonction = models.CharField(
        max_length=255, verbose_name=u"Fonction", blank=True,
        help_text="ignorer si candidat est étudiant"
    )

    # Utilisé lors des appels internationaux pour définir le bureau (région)
    # de traitement Cette valeur était dérivée de dossier.etablissement
    # (normalement équivalent de dossier.origine.etablissement) Maintenant,
    # on spécifie la valeur avec la région où est fait l'appel
    bureau_rattachement = models.ForeignKey(
        ref.Bureau, verbose_name=u"bureau de rattachement", blank=True,
        null=True
    )

    # Tentative pour récupérer de l'information passée

    derniere_bourse_toggle = models.BooleanField(
        verbose_name=u"Avez-vous déjà bénéficié d'une mobilité de l'AUF ?",
        choices=BOOLEAN_RADIO_OPTIONS,
        default=0
    )
    derniere_bourse_categorie = models.CharField(
        max_length=100, verbose_name=u"Si oui, précisez le type",
        choices=DERNIERE_MOBILITE_TYPE,
        blank=True
    )
    derniere_bourse_annee = models.CharField(
        max_length=4, verbose_name=u"Précisez l'année",
        blank=True
    )

    dernier_projet_toggle = models.BooleanField(
        verbose_name=u"Avez-vous déjà bénéficié d'un autre programme de l'AUF ?",
        choices=BOOLEAN_RADIO_OPTIONS,
        default=0
    )
    dernier_projet_description = models.TextField(
        verbose_name=u"Si oui, précisez lequel",
        blank=True
    )
    dernier_projet_annee = models.CharField(
        max_length=4, verbose_name=u"Précisez l'année",
        blank=True
    )

    # Évaluations (à terminer // expert classements)
    annotations = models.ManyToManyField(
        Commentaire, verbose_name=u"Commentaires", blank=True, null=True
    )
    moyenne_votes = models.FloatField(
        verbose_name=u"Évaluation", blank=True, null=True
    )
    moyenne_academique = models.FloatField(
        verbose_name=u"Moyenne académique", blank=True, null=True
    )
    opportunite_regionale = models.CharField(
        max_length=255, verbose_name=u"Opportunité régionale", blank=True
    )

    # ce champs est système, il est saisi dans la partie mobilité mais il
    # est copié ici pour pouvoir être filtré
    discipline = models.ForeignKey(
        ref.Discipline, verbose_name=u"discipline", blank=True, null=True
    )
    experts = models.ManyToManyField(
        Expert, verbose_name=u'Experts', related_name="dossiers",
        blank=True
    )

    objects = DossierManager()

    class Meta:
        ordering = ['appel__nom', 'candidat__nom', 'candidat__prenom']
        verbose_name = u"Dossier de candidature"
        verbose_name_plural = u"Dossiers de candidature"

    def __unicode__(self, ):
        try:
            candidat = u"%s pour l'" % self.candidat
        except:
            candidat = u""
        return u"%s #%s (%sappel %s)" % (self._meta.verbose_name,
                self.id, candidat, self.appel,)

    def calculer_moyenne(self,):
        if self.id:
            notes = [note.note for note in self.notes.all()
                     if note.note is not None]
            if len(notes) > 0:
                self.moyenne_votes = float(sum(notes)) / len(notes)
            else:
                self.moyenne_votes = 0

    def prepopuler_notes(self, *args, **kwargs):
        """
        A l'instanciation, on synchronise les meta pour optimisation
        """
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

# on fait ca au change du m2m des experts dans le dossier
def experts_changed(sender, **kwargs):
    dossier = kwargs['instance']
    dossier.prepopuler_notes()
m2m_changed.connect(experts_changed, sender=Dossier.experts.through)

class DossierFaculte(models.Model):
    # Etablissement connu de l'AUF
    etablissement = models.ForeignKey(
        ref.Etablissement,
        verbose_name=u"Établissement, si membre de l'AUF",
        blank=True, null=True
    )

    # Autre établissement
    autre_etablissement_nom = models.CharField(
        max_length=255, verbose_name=u"Autre établissement", blank=True
    )
    autre_etablissement_pays = models.ForeignKey(
        ref.Pays, verbose_name=u"Pays", blank=True, null=True
    )
    autre_etablissement_adresse = models.CharField(
        max_length=255, verbose_name=u"Adresse", blank=True
    )
    autre_etablissement_code_postal = models.CharField(
        max_length=255, verbose_name=u"Code postal", blank=True
    )
    autre_etablissement_ville = models.CharField(
        max_length=255, verbose_name=u"Ville", blank=True
    )
    autre_etablissement_region = models.CharField(
        max_length=255, verbose_name=u"Région / Province / État", blank=True
    )

    # responsable scientifique (Accord scientifique)
    resp_sc_civilite = models.CharField(
        max_length=2, verbose_name=u"Civilité", choices=CIVILITE, blank=True
    )
    resp_sc_nom = models.CharField(
        max_length=255, verbose_name=u"Nom", blank=True
    )
    resp_sc_prenom = models.CharField(
        max_length=255, verbose_name=u"Prénom", blank=True
    )
    resp_sc_fonction = models.CharField(
        max_length=255, verbose_name=u"Fonction", blank=True
    )
    resp_sc_courriel = models.CharField(
        max_length=255, verbose_name=u"Courriel", blank=True
    )
    resp_sc_telephone = models.CharField(
        max_length=255, verbose_name=u"Téléphone", blank=True
    )
    resp_sc_fax = models.CharField(
        max_length=255, verbose_name=u"Télécopieur", blank=True
    )

    # faculté, département ou labo (Accord scientifique)
    faculte_nom = models.CharField(
        max_length=255, verbose_name=u"Faculté / Centre / Département",
        blank=True
    )
    faculte_adresse = models.CharField(
        max_length=255, verbose_name=u"Adresse", blank=True
    )
    faculte_ville = models.CharField(
        max_length=255, verbose_name=u"Ville", blank=True
    )
    faculte_code_postal = models.CharField(
        max_length=255, verbose_name=u"Code postal", blank=True
    )

    # directeur thèse
    dir_civilite = models.CharField(
        max_length=2, verbose_name=u"Civilité", choices=CIVILITE,
        blank=True
    )
    dir_nom = models.CharField(
        max_length=255, verbose_name=u"Nom", blank=True
    )
    dir_prenom = models.CharField(
        max_length=255, verbose_name=u"Prénom", blank=True
    )
    dir_courriel = models.CharField(
        max_length=255, verbose_name=u"adresse électronique", blank=True
    )
    dir_telephone = models.CharField(
        max_length=255, verbose_name=u"Téléphone", blank=True
    )

    class Meta:
        abstract = True

    @property
    def pays(self):
        if self.etablissement:
            return self.etablissement.pays
        else:
            return self.autre_etablissement_pays


class DossierOrigine(DossierFaculte):
    """
    Informations sur le contexte d'origine du candidat.
    """
    dossier = models.OneToOneField(
        Dossier, verbose_name=u"Dossier", related_name="origine"
    )

    # Pour le champ de sélection Etablissement
    pays = models.ForeignKey(
        ref.Pays, to_field="code", related_name="origine_pays",
        verbose_name=u"Pays", blank=True, null=True
    )

    # responsable institutionnel à l'origine
    resp_inst_civilite = models.CharField(
        max_length=2, verbose_name=u"Civilité", choices=CIVILITE,
        blank=True
    )
    resp_inst_nom = models.CharField(
        max_length=255, verbose_name=u"Nom", blank=True
    )
    resp_inst_prenom = models.CharField(
        max_length=255, verbose_name=u"Prénom", blank=True
    )
    resp_inst_fonction = models.CharField(
        max_length=255, verbose_name=u"Fonction", blank=True
    )
    resp_inst_courriel = models.CharField(
        max_length=255, verbose_name=u"Courriel", blank=True
    )
    resp_inst_telephone = models.CharField(
        max_length=255, verbose_name=u"Téléphone", blank=True
    )
    resp_inst_fax = models.CharField(
        max_length=255, verbose_name=u"Télécopieur", blank=True
    )


class DossierAccueil(DossierFaculte):
    """
    Informations sur le contexte d'accueil du candidat.
    """
    dossier = models.OneToOneField(
        Dossier, verbose_name=u"Dossier", related_name="accueil"
    )

    # Pour le champ de sélection Etablissement
    pays = models.ForeignKey(
        ref.Pays, to_field="code", related_name="accueil_pays",
        verbose_name=u"Pays", blank=True, null=True
    )


class DossierMobilite(models.Model):
    """Informations sur la mobilité demandée par le candidat.
    """
    class Periode(object):
        def __init__(self, debut, fin, mois=None):
            self.debut = debut
            self.fin = fin
            self.mois = mois or self.calc_mois()

        def days_in_month(self, date):
            # Retourne le nombre de jours dans un mois.
            return calendar.monthrange(
                date.year,
                date.month,
                )[1]

        def calc_mois(self):
            if not self.debut or not self.fin:
                return 0

            calc_debut = datetime.date(
                self.debut.year,
                self.debut.month,
                1,
                )

            calc_fin = datetime.date(
                self.fin.year,
                self.fin.month,
                1,
                )

            if self.debut.day > 20:
                calc_debut += datetime.timedelta(
                    days=self.days_in_month(calc_debut)
                    )

            if (self.fin.day < 20 and
                calc_fin - datetime.timedelta(1) >= calc_debut):
                calc_fin -= datetime.timedelta(1)

            # + 1 parce que inclusif
            return (((calc_fin.year - calc_debut.year) * 12)
                    + calc_fin.month
                    - (calc_debut.month)
                    + 1
                    )

        @property
        def jours(self):
            # +1 parce que c'est inclusif.
            if not self.fin or not self.debut:
                return 0
            return (self.fin - self.debut).days + 1

        def __add__(self, periode):
            return DossierMobilite.Periode(
                self.debut or periode.debut or None,
                (
                    self.fin + datetime.timedelta(days=periode.jours)
                    if self.debut else periode.fin or None
                 ),
                mois=self.mois + periode.mois,
                )

    TYPE_THESE_CHOICES = (
        ('CT', "Co-tutelle"),
        ('CD', "Co-direction"),
        ('AU', "Autre"),
    )
    NIVEAU_DETUDES_CHOICES = (
        ('licence', 'Licence'),
        ('master1', 'Master 1'),
        ('master2', 'Master 2'),
        ('doctorat', 'Doctorat')
    )

    dossier = models.OneToOneField(
        Dossier, verbose_name=u"Dossier", related_name="mobilite"
    )

    # Période de mobilité
    date_debut_origine = models.DateField(
        verbose_name=u"Date de début souhaitée",
        help_text=settings.HELP_TEXT_DATE, blank=True, null=True
    )
    date_fin_origine = models.DateField(
        verbose_name=u"Date de fin souhaitée",
        help_text=settings.HELP_TEXT_DATE, blank=True, null=True
    )
    date_debut_accueil = models.DateField(
        verbose_name=u"Date de début souhaitée",
        help_text=settings.HELP_TEXT_DATE, blank=True, null=True
    )
    date_fin_accueil = models.DateField(
        verbose_name=u"Date de fin souhaitée",
        help_text=settings.HELP_TEXT_DATE, blank=True, null=True
    )

    # Dossier scientifique
    intitule_projet = models.TextField(u"Intitulé du projet", blank=True)
    mots_clefs = models.CharField(
        max_length=255, verbose_name=u"Mots clefs", blank=True,
        help_text="séparés par des virgules, 3 maximum"
    )

    # Disciplines
    discipline = models.ForeignKey(
        ref.Discipline, verbose_name=u"Discipline", blank=True, null=True
    )
    sous_discipline = models.CharField(max_length=255, blank=True)

    # Formation en cours
    formation_en_cours_diplome = models.CharField(
        max_length=255, verbose_name=u"Intitulé du diplôme", blank=True
    )
    formation_en_cours_niveau = models.CharField(
        max_length=100, verbose_name=u"Niveau d'études", blank=True,
        choices=NIVEAU_DETUDES_CHOICES
    )

    # Diplôme demandé
    diplome_demande_nom = models.CharField(
        max_length=255, verbose_name=u"Diplôme demandé", blank=True
    )
    diplome_demande_niveau = models.CharField(
        max_length=100, verbose_name=u"Niveau d'études", blank=True,
        choices=NIVEAU_DETUDES_CHOICES
    )

    # Thèse
    these_date_inscription = models.DateField(
        help_text=settings.HELP_TEXT_DATE,
        verbose_name=u"Date de première inscription en thèse",
        blank=True, null=True
    )
    these_soutenance_pays = models.ForeignKey(
        ref.Pays, related_name="soutenance_pays",
        verbose_name=u"Pays de soutenance", blank=True, null=True
    )
    these_soutenance_date = models.DateField(
        help_text=settings.HELP_TEXT_DATE,
        verbose_name=u"Date de soutenance prévue",
        blank=True, null=True
    )
    these_type = models.CharField(
        max_length=2, verbose_name=u"Type de thèse",
        choices=TYPE_THESE_CHOICES, blank=True
    )

    # Programme de mission
    type_intervention = models.CharField(
        u"Type d'intervention", max_length=255, blank=True
    )
    public_vise = models.CharField(
        u"Public visé", max_length=255, blank=True
    )
    autres_publics = models.CharField(
        u"Autres publics", max_length=255, blank=True
    )

    # Co-financement

    cofinancement = models.BooleanField(
        verbose_name=u"Votre mobilité sera-t-elle partiellement financée par un autre organisme ?",
        choices=BOOLEAN_RADIO_OPTIONS,
        default=0
    )
    cofinancement_source = models.TextField(
        verbose_name=u"Source du cofinancement",
        blank=True,
        null=True
    )
    cofinancement_montant = models.DecimalField(
        max_digits=17, decimal_places=2,
        verbose_name=u"Montant du cofinancement",
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        # Mots clefs en majuscule
        self.mots_clefs = self.mots_clefs.upper()

        super(DossierMobilite, self).save(*args, **kwargs)

    def periodes_mobilite(self):
        """
        Retourne les périodes de mobilité sous forme d'une liste de tuples.

        Les tuples sont de la forme (lieu, date_debut, date_fin)
        """
        periodes = []
        if self.date_debut_origine and self.date_fin_origine:
            periodes.append(
                ('origine', self.date_debut_origine, self.date_fin_origine)
            )
        if self.date_debut_accueil and self.date_fin_accueil:
            periodes.append(
                ('accueil', self.date_debut_accueil, self.date_fin_accueil)
            )
        periodes.sort(key=lambda x: x[1])
        return periodes

    @property
    def duree_origine(self):
        return self.Periode(
            self.date_debut_origine,
            self.date_fin_origine,
            )

    @property
    def duree_accueil(self):
        return self.Periode(
            self.date_debut_accueil,
            self.date_fin_accueil,
            )

    @property
    def duree_totale(self):
        return self.duree_origine + self.duree_accueil


class Diplome(models.Model):
    dossier = models.ForeignKey(Dossier)
    nom = models.CharField(
        max_length=255, verbose_name=u"Intitulé", blank=True
    )
    date = models.DateField(
        max_length=255, verbose_name=u"Date d'obtention",
        help_text=settings.HELP_TEXT_DATE, blank=True, null=True
    )
    niveau = models.CharField(
        max_length=100, verbose_name=u"Niveau d'études", blank=True
    )

    # Etablissement connu de l'AUF
    etablissement = models.ForeignKey(
        ref.Etablissement,
        verbose_name=u"Établissement d'obtention si membre de l'AUF",
        blank=True, null=True
    )

    # Autre établissement
    autre_etablissement_nom = models.CharField(
        max_length=255, verbose_name=u"Autre établissement", blank=True
    )
    autre_etablissement_pays = models.ForeignKey(
        ref.Pays, related_name="etablissement_pays",
        verbose_name=u"Pays de l'établissement",
        blank=True, null=True
    )


class TypePiece(models.Model):
    nom = models.CharField(max_length=100)
    identifiant = models.SlugField(max_length=100)

    def __unicode__(self):
        return u"%s (%s)" % (self.nom, self.identifiant, )

    class Meta:
        verbose_name = 'type de pièce'
        verbose_name_plural = 'types de pièces'
        ordering = ['nom']


class Piece(models.Model):
    dossier = models.ForeignKey(Dossier, related_name="pieces")
    identifiant = models.CharField(max_length=100, blank=True)
    fichier = models.FileField(
        max_length=255,
        upload_to="pieces",
        storage=FileSystemStorage(location=settings.UPLOADS_ROOT),
        blank=True, null=True
    )
    conforme = models.NullBooleanField(verbose_name=u"Pièce conforme")

    def __unicode__(self):
        return self.identifiant


class AttributWCS(models.Model):
    dossier = models.ForeignKey(Dossier, related_name="attributs_wcs")
    attribut = models.CharField(
        max_length=255, verbose_name=u"Attribut", blank=True
    )
    valeur = models.TextField(verbose_name=u"Valeur", blank=True)

    class Meta:
        verbose_name = u"Attribut WCS"
        verbose_name_plural = u"Attributs WCS"

    def __unicode__(self):
        return u"%s" % self.attribut


# Dynamo

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
