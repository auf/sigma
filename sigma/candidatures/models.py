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
from sigma.lib.models import (
    Individu,
    OrigineAbstract,
    AccueilAbstract,
    MobiliteAbstract,
    CIVILITE,
    BOOLEAN_RADIO_OPTIONS,
    )
from sigma.dynamo import dynamo_registry
from sigma.dynamo.models import \
        MetaModel, InstanceModel, TypeProperty, ValueProperty
from sigma.candidatures.workflow import DossierWorkflow, DOSSIER_ETAT_RETENU

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
NOTE_MAX = 20


# Sql query to find experts and match discipline

EXP_TPL = """SELECT
* FROM (
  SELECT
    *,
    SUM(DMATCH) AS DMATCH_S
  FROM (
    SELECT
      candidatures_expert_disciplines.discipline_id as ced_did,
      candidatures_expert_disciplines.expert_id as ced_eid,
      candidatures_expert.id,
      candidatures_expert.prenom,
      candidatures_expert.nom,
      candidatures_expert.courriel,
      candidatures_expert.region_id,
      candidatures_expert.etablissement_id,
      candidatures_expert.commentaire,
      candidatures_expert.actif, (
      CASE WHEN
        candidatures_expert_disciplines.discipline_id IN (
          -- Dossiers for which you're looking for experts.
          SELECT
            discipline_id
          FROM
            candidatures_dossiermobilite
          WHERE dossier_id IN (%(dossiers)s)
        )
      THEN 1
      ELSE 0
      END
    ) as DMATCH
    FROM
      candidatures_expert
    JOIN candidatures_expert_disciplines ON
      candidatures_expert.id =
      candidatures_expert_disciplines.expert_id
    JOIN ref_discipline rf ON
      rf.id =
      candidatures_expert_disciplines.discipline_id
    %(subset_cond)s
    ) AS GROUPED_EXPERTS
  GROUP BY id) AS SUPER_EXPERTS
  ORDER BY -DMATCH_S;"""

# Used if we are working on a subset of experts.
EXP_SUBSET_TPL = """    -- IDs gotten from get_rules() in forms.py
    WHERE candidatures_expert.id IN (%(experts)s)"""


class ExpertManager(models.Manager):

    def get_discipline_match(self, dossiers, qs=None):
        """
        Chaque expert retournée par cette méthode a un attribut
        "DMATCH_S" qui indique le nombre de disciplines
        correspondantes au(x) DossierMobilite relié au(x) dossiers
        passés commen argument.

        Les experts sont triés par correspondance de discipline.

        At least we're not doing 1 query with joins per Expert :P
        This may require optimization.
        """

        # If no qs is supplied, get default QS and don't get expert
        # subset. Else, pass a where .. in clause to get the subset.
        if qs != None and qs.count() == 0:
            return qs
        elif not qs:
            qs = self.get_query_set()
            subset_cond = ''
        else:
            e_ids = [str(x[0]) for x in qs.values_list('id')]
            e_ids = ','.join(e_ids)
            subset_cond = EXP_SUBSET_TPL % {
                'experts': e_ids
                }
        # Get dossier IDs, from either queryset or iterable.
        try:
            d_ids = [str(x[0]) for x in dossiers.values_list('id')]
        except AttributeError:
            d_ids = [str(x.id) for x in dossiers]
        d_ids = ','.join(d_ids)

        # Build query.
        query = EXP_TPL % {
            'dossiers': d_ids,
            'subset_cond': subset_cond,
            }

        # Add a dumb all method
        raw = self.raw(query)
        raw.all = lambda: raw

        # Add a filter method (Makes a new query because we can't
        # .filter on a raw query)
        def _outer_filter(raw_q):
            def _filter(*a, **kw):
                return Expert.objects.filter(
                    id__in=[x.id for x in raw_q]).filter(*a, **kw)
            return _filter

        raw.filter = _outer_filter(raw)

        # Return query.
        return raw

    def get_query_set(self):
        fkeys = ('region', )
        return super(ExpertManager, self).get_query_set() \
                .select_related(*fkeys).all()


class Expert(Individu):
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

    pays = models.ForeignKey(
        ref.Pays,
        related_name="experts",
        verbose_name=u"Pays de résidence",
        blank=True,
        null=True
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
        ref.Region, verbose_name=u"Régions", blank=True, null=True
    )
    disciplines = models.ManyToManyField(
        ref.Discipline, verbose_name=u"Disciplines", blank=True, null=True
    ) # TODO potentially obsolete, Davin says this is probably for Expert


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
            help_text=u"À défaut d'un type de bourse qui convienne, expliquez la nature de votre appel.")
    type_bourse = models.ForeignKey(TypeBourse,
            verbose_name=u"Type de bourse",
            blank=True, null=True)
    region = models.ForeignKey(ref.Region, verbose_name=u"Région")
    annee = models.IntegerField(u"année", validators=[validateur_annee, ])

    code_budgetaire = models.CharField(
        u"Code budgétaire", max_length=72,
        help_text=u"Le code budgétaire est composé de 5 chiffres + 2 lettres.",
        validators=[validateur_code_budgetaire, ]
    )
    responsable_budgetaire = models.ForeignKey(
        ref.Employe,
        verbose_name="Responsable budgétaire",
        blank=True,
        null=True,
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
        help_text=u"En euro (EUR). Indiquer 0 dans les champs non-pertinents",
    )
    montant_mensuel_origine_nord = models.IntegerField(
        u"Montant mensuel pays origine Nord", 
        blank=True, null=True,
        help_text=u"En euro (EUR). Indiquer 0 dans les champs non-pertinents",
    )
    montant_mensuel_accueil_sud = models.IntegerField(
        u"Montant mensuel pays accueil Sud", 
        blank=True, null=True,
        help_text=u"En euro (EUR). Indiquer 0 dans les champs non-pertinents",
    )
    montant_mensuel_accueil_nord = models.IntegerField(
        u"Montant mensuel pays accueil Nord", 
        blank=True, null=True,
        help_text=u"En euro (EUR). Indiquer 0 dans les champs non-pertinents",
    )
    prime_installation_sud = models.IntegerField(
        u"Prime d'installation (pays du Sud)", 
        blank=True, null=True,
        help_text=u"En euro (EUR). Indiquer 0 dans les champs non-pertinents",
    )
    prime_installation_nord = models.IntegerField(
        u"Prime d'installation (pays du Nord)", 
        blank=True, null=True,
        help_text=u"En euro (EUR). Indiquer 0 dans les champs non-pertinents",
    )
    montant_perdiem_sud = models.IntegerField(
        u"Montant jour (perdiem) pays Sud ", 
        blank=True, null=True,
        help_text=u"En euro (EUR). Indiquer 0 dans les champs non-pertinents",
    )
    montant_perdiem_nord = models.IntegerField(
        u"Montant jour (perdiem) pays Nord", 
        blank=True, null=True,
        help_text=u"En euro (EUR). Indiquer 0 dans les champs non-pertinents",
    )
    montant_allocation_unique = models.IntegerField(
        u"Montant allocation unique", 
        blank=True, null=True,
        help_text=u"En euro (EUR). Indiquer 0 dans les champs non-pertinents",
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

class Candidat(Individu):
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
    nom_jeune_fille = models.CharField(
        max_length=255,
        verbose_name=u"Nom de jeune fille",
        blank=True,
        )

    # identification avancée
    nationalite = models.ForeignKey(
        ref.Pays, verbose_name=u"Nationalité", blank=True, null=True
        )

    # coordonnées
    # TODO: DRY... Expert.pays, Candidat.Pays.
    pays = models.ForeignKey(
        ref.Pays,
        related_name="candidats",
        verbose_name=u"Pays de résidence",
        blank=True,
        null=True
        )

    # TODO: Migrer le data et utiliser Individu.province.
    region = models.CharField(
        max_length=255, verbose_name=u"Région / Province / État", blank=True
        )

    def __unicode__(self):
        return u"%s %s" % (self.nom.upper(), self.prenom)


class Note(models.Model):
    """
    Une personne attribue une note à un dossier de candidature.
    """
    dossier = models.ForeignKey("Dossier", related_name="notes")
    expert = models.ForeignKey(Expert, blank=True, null=True)
    commentaire = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        )
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
        Appel, related_name="dossier", verbose_name=u"Appel"
    )
    appel.admin_filter_select = True

    candidat_statut = models.CharField(
        max_length=255, verbose_name=u"Statut du candidat",
        choices=CANDIDAT_STATUT_CHOICES, blank=True
    )
    candidat_fonction = models.CharField(
        max_length=255, verbose_name=u"Fonction", blank=True,
        help_text="À ignorer si candidat est étudiant."
    )

    # Utilisé lors des appels internationaux pour définir le bureau (région)
    # de traitement Cette valeur était dérivée de dossier.etablissement
    # (normalement équivalent de dossier.origine.etablissement) Maintenant,
    # on spécifie la valeur avec la région où est fait l'appel
    bureau_rattachement = models.ForeignKey(
        ref.Bureau, verbose_name=u"Bureau de rattachement", blank=True,
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
    moyenne_academique = models.FloatField(
        verbose_name=u"Moyenne académique", blank=True, null=True
    )
    opportunite_regionale = models.CharField(
        max_length=255, verbose_name=u"Opportunité régionale", blank=True
    )

    # ce champs est système, il est saisi dans la partie mobilité mais il
    # est copié ici pour pouvoir être filtré
    discipline = models.ForeignKey(
        ref.Discipline, verbose_name=u"Discipline", blank=True, null=True
    )
    experts = models.ManyToManyField(
        Expert, verbose_name=u'Experts', related_name="dossiers",
        blank=True
    )

    objects = DossierManager()

    class Meta:
        ordering = ['appel__nom', 'candidat__nom', 'candidat__prenom']
        verbose_name = u"Candidature"
        verbose_name_plural = u"Candidatures"

    def __unicode__(self, ):
        try:
            candidat = u"%s pour l'" % self.candidat
        except:
            candidat = u""
        return u"%s #%s (%sappel %s)" % (self._meta.verbose_name,
                self.id, candidat, self.appel,)

    def moyenne_notes(self):
        return (self.notes.filter(expert__in=self.experts.all()).
                aggregate(avg=models.Avg('note'))['avg'])
    moyenne_notes.short_description = 'Moyenne des notes'

    def is_retainable(self):
        return self.etat == DOSSIER_ETAT_RETENU

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

    def get_mobilite(self):
        try:
            return self.mobilite
        except DossierMobilite.DoesNotExist:
            return None

    def est_allouable(self):
        """
        Retourne True si le dossier est complet et si l'appel et le
        dossier sont dans les etats necessaire pour pouvoir allouer
        une bourse au candidat.
        """
        # TODO: Produce validation here.
        return True

# on fait ca au change du m2m des experts dans le dossier
def experts_changed(sender, **kwargs):
    dossier = kwargs['instance']
    dossier.prepopuler_notes()
m2m_changed.connect(experts_changed, sender=Dossier.experts.through)


class DossierOrigine(OrigineAbstract):
    """
    Informations sur le contexte d'origine du candidat.
    """
    dossier = models.OneToOneField(
        Dossier,
        verbose_name=u"Dossier",
        related_name="origine",
        )

class DossierAccueil(AccueilAbstract):
    """
    Informations sur le contexte d'accueil du candidat.
    """
    dossier = models.OneToOneField(
        Dossier,
        verbose_name=u"Dossier",
        related_name="accueil",
        )


class DossierMobilite(MobiliteAbstract):
    """Informations sur la mobilité demandée par le candidat.
    """
    dossier = models.OneToOneField(
        Dossier,
        verbose_name=u"Dossier",
        related_name="mobilite",
        )


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
        verbose_name = 'Type de pièce'
        verbose_name_plural = 'Types de pièces'
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
        verbose_name = u"Type de conformité"
        verbose_name_plural = u"Types de conformités"


class Conformite(ValueProperty, models.Model):
    """
    Lié au dossier
    """
    dossier = models.ForeignKey(Dossier)
    type = models.ForeignKey("TypeConformite")
    conforme = models.NullBooleanField(verbose_name=u"Conforme?",
                        choices=BOOLEAN_RADIO_OPTIONS,
                        blank=True, null=True)
    commentaire = models.CharField(blank=True, null=True,
        max_length=255)

    class Meta:
        verbose_name = u"Conformité"

# on relie tous les modèles ensembles pour générer les admin
dynamo_registry.register(Appel, TypeConformite, Dossier, Conformite)
