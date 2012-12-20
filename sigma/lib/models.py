# -*- encoding: utf-8 -*-

import datetime

from django.db import models
from django.conf import settings
from auf.django.references import models as ref
from sigma.lib.temps import Periode


CIVILITE = (
    ('MR', "Monsieur"),
    ('MM', "Madame"),
    ('ME', "Mademoiselle"),
    )

BOOLEAN_RADIO_OPTIONS = (
    (True, 'Oui'),
    (False, 'Non')
)


class Individu(models.Model):
    """
    Model de base pour tout modèle représentant une personne.
    """

    # Info générales
    nom = models.CharField(
        max_length=255,
        verbose_name=u"Nom",
        )
    prenom = models.CharField(
        max_length=255,
        verbose_name=u"Prénom",
        )
    civilite = models.CharField(
        max_length=2,
        verbose_name=u"Civilité",
        choices=CIVILITE,
        blank=True,
        null=True,
        )
    naissance_date = models.DateField(
        max_length=255,
        verbose_name=u"Date de naissance",
        help_text=settings.HELP_TEXT_DATE,
        blank=True,
        null=True,
        )
    telephone = models.CharField(
        max_length=255,
        verbose_name=u"Téléphone fixe",
        help_text=u"(+ code régional)",
        blank=True,
        null=True,
        )
    telephone_portable = models.CharField(
        max_length=255,
        verbose_name=u"Téléphone portable",
        help_text=u"(+ code régional)",
        blank=True,
        null=True,
        )
    courriel = models.EmailField(
        max_length=255,
        verbose_name=u"Adresse électronique",
        blank=True,
        null=True,
        )

    # Infos location
    province = models.CharField(
        max_length=255,
        verbose_name=u"Région / Province / État",
        blank=True,
        null=True,
        )
    ville = models.CharField(
        max_length=255,
        verbose_name=u"Ville",
        blank=True,
        null=True,
        )
    adresse = models.TextField(
        u'Adresse',
        blank=True,
        null=True,
        )
    adresse_complement = models.TextField(
        u"complément d'adresse",
        blank=True,
        null=True,
        )
    code_postal = models.CharField(
        max_length=255,
        verbose_name=u"Code postal",
        blank=True,
        null=True,
        )

    def __unicode__(self):
        return self.nom_complet()

    def nom_complet(self):
        return ' '.join((self.prenom, self.nom))
    nom_complet.short_description = 'Nom complet'

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

    class Meta:
        abstract = True


class FaculteAbstract(models.Model):
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
        max_length=255, verbose_name=u"Adresse électronique", blank=True
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
        max_length=255, verbose_name=u"Adresse électronique", blank=True
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


class OrigineAbstract(FaculteAbstract):
    """
    Informations sur le contexte d'origine du candidat.
    """

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
        max_length=255, verbose_name=u"Adresse électronique", blank=True
    )
    resp_inst_telephone = models.CharField(
        max_length=255, verbose_name=u"Téléphone", blank=True
    )
    resp_inst_fax = models.CharField(
        max_length=255, verbose_name=u"Télécopieur", blank=True
    )

    class Meta:
        abstract = True



class AccueilAbstract(FaculteAbstract):
    """
    Informations sur le contexte d'accueil du candidat.
    """
    class Meta:
        abstract = True


class MobiliteAbstract(models.Model):
    """Informations sur la mobilité demandée par le candidat.
    """

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
        help_text="Séparés par des virgules, 3 maximum."
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
        ref.Pays,
        verbose_name=u"Pays de soutenance",
        blank=True,
        null=True,
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
        null=True,
        help_text=u"En euro (EUR)."
        )

    def save(self, *args, **kwargs):

        # Mots clefs en majuscule
        self.mots_clefs = self.mots_clefs.upper()

        super(MobiliteAbstract, self).save(*args, **kwargs)

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
        return Periode(
            self.date_debut_origine,
            self.date_fin_origine,
            )

    @property
    def duree_accueil(self):
        return Periode(
            self.date_debut_accueil,
            self.date_fin_accueil,
            )

    @property
    def duree_totale(self):
        return self.duree_origine + self.duree_accueil

    class Meta:
        abstract = True
