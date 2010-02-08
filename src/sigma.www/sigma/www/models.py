# -=- encoding: utf-8 -=-
from sigma.references.models import ProjetPoste as ref_ProjetPoste
from sigma.references.models import Poste as ref_Poste
from sigma.references.models import Poste as ref_Region

from sigma.www.files import storage

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _

import django.contrib.auth.models 
import os
import datetime
import re

import sigma.references
import sigma.www.patch

class Categorie(models.Model):
    """Representation des types de bourses qui peuvent etre offertes 
    par l'AUF"""

    nom = models.CharField(
        max_length=100, 
        verbose_name=_("nom_categorie"))
    poste = models.ForeignKey(
        sigma.references.models.Poste, 
        verbose_name=_("poste"))

    # meta 
    actif = models.BooleanField(default=True)

    # traitement
    exception_possible = models.BooleanField(
        verbose_name=_("exception_possible"))
    renouvellement_possible = models.BooleanField(
        verbose_name=_("renouvellement_possible"))
    renouvellement_nb_max = models.PositiveIntegerField(
        verbose_name=_("renouvellement_nb_max"),
        blank=True, null=True)

    # criteres
    age_max = models.PositiveIntegerField(
        verbose_name=_("age_max"))
    statut_etudiant_obligatoire = models.BooleanField(
        verbose_name=_("statut_etudiant_obligatoire"))
    mobilite_duree_mois_min = models.PositiveIntegerField(
        verbose_name=_("mobilite_duree_mois_min"))
    mobilite_duree_mois_max = models.PositiveIntegerField(
        verbose_name=_("mobilite_duree_mois_max"))
    origine_etabl_membre_obligatoire = models.BooleanField(
        verbose_name=_("origine_etabl_membre_obligatoire"))
    accueil_etabl_membre_obligatoire = models.BooleanField(
        verbose_name=_("accueil_etabl_membre_obligatoire"))
    diplome_duree_validite_obligatoire = models.BooleanField(
        verbose_name=_("diplome_duree_validite_obligatoire"))
    diplome_duree_validite_min = models.PositiveIntegerField(
        verbose_name=_("diplome_duree_validite_min"),
        blank=True, null=True)
    alternance_obligatoire = models.BooleanField(
        verbose_name=_("alternance_obligatoire"))
    alternance_duree_min_mois = models.PositiveIntegerField(
        verbose_name=_("alternance_duree_min_mois"), 
        blank=True, null=True)
    niveau_etude = models.ForeignKey(
        to='NiveauEtude',
        blank = True, null = True,
        verbose_name=_("niveau_etude"))

    serialisable_fields = ('exception_possible',
                           'renouvellement_possible',
                           'renouvellement_nb_max',
                           'age_max',
                           'statut_etudiant_obligatoire',
                           'mobilite_duree_mois_min',
                           'mobilite_duree_mois_max',
                           'origine_etabl_membre_obligatoire',
                           'accueil_etabl_membre_obligatoire',
                           'diplome_duree_validite_obligatoire',
                           'diplome_duree_validite_min',
                           'alternance_obligatoire',
                           'alternance_duree_min_mois',
                           'niveau_etude')

    def __unicode__(self):
        return "%s - %s" % (self.poste.code, self.nom)

    def get_absolute_url(self):
        return "/categories/detail/%s" % self.id

    @staticmethod
    def search(user, value):
        if not value:
            return Categorie.objects.all()
        if value.isdigit():
            return Categorie.objects.filter(id=int(value))
        conds = models.Q(nom__contains=value)
        return Categorie.objects.filter(conds)


class WorkflowObject(models.Model):
    """Objets suivit par un workflow doivent
    tous etre de type workflow afin de pouvoir logger leurs evenements
    """

class Appel(WorkflowObject):
    """Un appel d'offre est une instance de distribution de bourses pour un 
    projet-poste particulier
    """
    field_dependencies = {
        'alternance_obligatoire': 'alternance_duree_min_mois',
        'renouvellement_possible' : 'renouvellement_nb_max',
        'diplome_duree_validite_obligatoire': 'diplome_duree_validite_min',}

    serialisable_fields = ( 'renouvellement_possible',
                            'renouvellement_nb_max',
                            'age_max',
                            'statut_etudiant_obligatoire',
                            'mobilite_duree_mois_min',
                            'mobilite_duree_mois_max',
                            'origine_etabl_membre_obligatoire',
                            'accueil_etabl_membre_obligatoire',
                            'diplome_duree_validite_obligatoire',
                            'diplome_duree_validite_min',
                            'alternance_obligatoire',
                            'alternance_duree_min_mois',
                            'niveau_etude')

    STATUT_CHOICES = (
        ('Nouveau', _("Nouveau_appel")),
        ('Supprime', _("Supprime_appel")),
        ('Diffuse', _("Diffuse_appel")),
        ('Analyse', _("Analyse_appel")), 
        ('Evalue', _("Evalue_appel")),
        ('Selectionne', _("Selectionne_appel")),
        ('Notifie', _("Notifie_appel")),
        ('Suivie', _("Suivie_appel")), 
        ('Ferme', _("Ferme_appel")),
        )

    # meta
    actif = models.BooleanField()

    # Information generales
    nom = models.CharField(
        max_length=200, 
        verbose_name=_("nom_appel"))
    projetposte = models.ForeignKey(
        'ProjetPoste', 
        verbose_name=_("projetposte"))

    # traitement
    statut = models.CharField(
        max_length=32, 
        choices=STATUT_CHOICES, 
        default='Nouveau', 
        verbose_name=("statut"))

    renouvellement_possible = models.BooleanField(
        verbose_name=_("renouvellement_possible"), 
        subject=_("Parametres generaux"))
    renouvellement_nb_max = models.PositiveIntegerField( 
        verbose_name=_("renouvellement_nb_max"), 
        subject=_("Parametres generaux"),
        blank=False, null=True)
    inscription_date_debut = models.DateField(
        verbose_name=_("inscription_date_debut"), 
        subject=_("Parametres generaux"))
    inscription_date_fin = models.DateField(
        verbose_name=_("inscription_date_fin"), 
        subject=_("Parametres generaux"))
    mobilite_date_debut = models.DateField(
        verbose_name=_("mobilite_date_debut"), 
        subject=_("Parametres generaux"))
    mobilite_date_fin = models.DateField(
        verbose_name=_("mobilite_date_fin"), 
        subject=_("Parametres generaux"))
    piecesjointes = models.ManyToManyField(
        "PieceJointeType",
        verbose_name=_("Pieces jointes"),
        subject=_("Pieces"),
        blank=True, null=True)
    criteres = models.ManyToManyField(
        "CritereSupplementaire",
        verbose_name=_("Criteres supplementaires"),
        subject=_("Criteres supplementaires"),
        blank=True, null=True)

    # criteres
    age_max = models.IntegerField(
        verbose_name=_("age_max"), 
        subject=_("Criteres de selection"))
    statut_etudiant_obligatoire = models.BooleanField(
        verbose_name=_("statut_etudiant_obligatoire"), 
        subject=_("Criteres de selection"))
    niveau_etude = models.ForeignKey(
        to='NiveauEtude',
        blank = True, null=True,
        verbose_name=_("Niveau d'etude"),
        subject=_("Criteres de selection"))
    mobilite_duree_mois_min = models.PositiveIntegerField(
        verbose_name=_("mobilite_duree_mois_min"), 
        subject=_("Criteres de selection"))
    mobilite_duree_mois_max = models.PositiveIntegerField(
        verbose_name=_("mobilite_duree_mois_max"), 
        subject=_("Criteres de selection"))
    origine_etabl_membre_obligatoire = models.BooleanField(
        verbose_name=_("origine_etabl_membre_obligatoire"), 
        subject=_("Criteres de selection"))
    accueil_etabl_membre_obligatoire = models.BooleanField(
        verbose_name=_("accueil_etabl_membre_obligatoire"), 
        subject=_("Criteres de selection"))
    diplome_duree_validite_obligatoire = models.BooleanField(
        verbose_name=_("diplome_duree_validite_obligatoire"), 
        subject=_("Criteres de selection"))
    diplome_duree_validite_min = models.PositiveIntegerField(
        verbose_name=_("diplome_duree_validite_min"), 
        subject=_("Criteres de selection"),
        blank=True, null=True)
    alternance_obligatoire = models.BooleanField(
        verbose_name=_("alternance_obligatoire"), 
        subject=_("Criteres de selection"))
    alternance_duree_min_mois = models.PositiveIntegerField(
        verbose_name=_("alternance_duree_min_mois"), 
        subject=_("Criteres de selection"),
        blank=True, null=True)

    def __unicode__(self):
        return self.nom
   
    def get_absolute_url(self):
        return "/appels/detail/%s" % self.id

    def candidatures(self):
        """Obtention des candidatures de l'appel d'offre"""
        return Candidature.objects.filter(appel=self)    
        
    def nb_candidatures(self):
        """Obtention du nombre de candidature de l'appel d'offre"""
        return len(self.candidatures())
        
    @staticmethod
    def search(user, value):
        """Recherche d'un appel d'offre en utilisant les criteres predefinis
        
        @param user Utilisateur courant
        @param value Valeur recherchee
        """
        if not value:
            return Appel.objects.all()
        elif value.isdigit():
            conds = models.Q(id=int(value))
            return Appel.objects.filter(conds)
        else:
            conds = models.Q(nom__contains=value)
            return Appel.objects.filter(conds)
        

class Candidature(WorkflowObject):
    """Une candidature est une reponse d'un individu a un appel d'offre"""

    class Meta:
        permissions = (
            ("can_select_candidature", 
             "Peut rejetter ou approuver des candidatures"),
            ("can_classe_candidature", 
             "Peut dire si une candidature est complète ou non"),)

    TYPE_CHOICES = (
        ('Professeur', _('Professeur')),
        ('Chercheur', _('Chercheur')),
        ('Etudiant', _('Etudiant')),)

    STATUT_CHOICES = (
        ('Nouveau', _('Nouveau')),
        ('Supprime', _('Supprime')),
        ('PreIrrecevable', _('PreIrrecevable')),
        ('PreRecevable', _('PreRecevable')),
        ('Recevable', _('Recevable')),
        ('Irrecevable', _('Irrecevable')),
        ('Classe', _('Classe')),
        ('Non-Classe', _('Non-Classe')),
        ('Selectionne', _('Selectione')),
        ('Attente', _('Attente')),
        ('Desiste', _('Desiste')),
        ('Boursie', _('Boursie')),
        ('Complet', _('Complet')),)

    GENRE_CHOICES = (
        ('M', _('Masculin')),
        ('F', _('Feminin')),)

    CIVILITE_CHOICES = (
        ('M.', _('Monsieur')),
        ('Mme', _('Madame')),
        ('Mlle', _('Mademoiselle')),)


    field_dependencies = {'origine_etabl':'origine_etabl_autre',
                          'accueil_etabl':'accueil_etabl_autre'}

    serialisable_fields = (
        'id', 
        'nom', 
        'prenom', 
        'statut', 
        'discipline', 
        'appel', 
        'origine_etabl')

    # Meta
    actif = models.BooleanField(default=True)

    # Informations essentielles
    nom = models.CharField(
        max_length=40, 
        verbose_name=_("nom"))
    prenom = models.CharField(
        max_length=40, 
        verbose_name=_("prenom"))

    # Informations generales
    nationalite = models.ForeignKey(
        sigma.references.models.Pays, 
        related_name='nationalite', 
        verbose_name=_('nationalite'), 
        blank=False, 
        null=True)
    genre = models.CharField(
        max_length=32, 
        choices=GENRE_CHOICES, 
        verbose_name=_("genre"), 
        blank=False, 
        null=True)
    nom_jeune_fille = models.CharField(
        max_length=40, 
        verbose_name=_("nom_jeune_fille"), 
        blank=True, 
        null=True)
    civilite = models.CharField(
        max_length=32, 
        choices=CIVILITE_CHOICES, 
        verbose_name=_("civilite"), 
        blank=False, 
        null=True)
    date_naissance = models.DateField(
        verbose_name=_("date_naissance"), 
        blank=False, 
        null=True)
    pays_naissance = models.ForeignKey(
        sigma.references.models.Pays, 
        related_name='pays_naissance', 
        verbose_name=_("pays_naissance"), 
        blank=True, 
        null=True)
    ville_naissance = models.CharField(
        max_length=40, 
        verbose_name=_("ville_naissance"), 
        blank=True, 
        null=True)

    # coordonnées
    adresse = models.CharField(
        max_length=100, 
        verbose_name=_("adresse"), 
        subject=_("Coordonnees"), 
        blank=False, 
        null=True)
    ville = models.CharField(
        max_length=40, 
        verbose_name=_("ville"), 
        subject=_("Coordonnees"), 
        blank=False, 
        null=True)
    province = models.CharField(
        max_length=40, 
        verbose_name=_("province"), 
        subject=_("Coordonnees"), 
        blank=False, 
        null=True)
    pays = models.ForeignKey(
        sigma.references.models.Pays, 
        related_name='pays', 
        verbose_name=_("pays"), 
        subject=_("Coordonnees"), 
        blank=False, 
        null=True)
    code_postal = models.CharField(
        max_length=20, 
        verbose_name=_("code_postal"), 
        subject=_("Coordonnees"), 
        blank=False, 
        null=True)
    tel = models.CharField(
        max_length=30, 
        verbose_name=_("tel"), 
        subject=_("Coordonnees"), 
        blank=False, 
        null=True)
    fax = models.CharField(
        max_length=30, 
        verbose_name=_("fax"), 
        subject=_("Coordonnees"), 
        blank=True, 
        null=True)
    tel_professionnel = models.CharField(
        max_length=30, 
        verbose_name=_("tel_professionnel"), 
        subject=_("Coordonnees"), 
        blank=True, 
        null=True)
    fax_professionnel = models.CharField(
        max_length=30, 
        verbose_name=_("fax_professionnel"), 
        subject=_("Coordonnees"), 
        blank=True, 
        null=True)
    courriel = models.EmailField(
        max_length=50, 
        verbose_name=_("courriel"), 
        subject=_("Coordonnees"), 
        blank=True, 
        null=True)

    # profil
    fonction = models.CharField(
        max_length=40, 
        verbose_name=_("fonction"), 
        blank=True,
        null=True)
    niveau_etude = models.ForeignKey(
        to='NiveauEtude',
        blank=True,
        null=True)
    diplome_intitule = models.CharField(
        max_length=40, 
        verbose_name=_("diplome_intitule"), 
        blank=True,
        null=True)
    diplome_date = models.DateField(
        verbose_name=_("diplome_date"), 
        blank=False,
        null=True)
    etablissement = models.ForeignKey(
        sigma.references.models.Etablissement, 
        verbose_name=_("etablissement"), 
        blank=True,
        null=True)
    discipline = models.ForeignKey(
        sigma.references.models.Discipline, 
        verbose_name=_("discipline"), 
        blank=False,
        null=True)

    # traitement
    statut = models.CharField(
        max_length=32, 
        choices=STATUT_CHOICES, 
        default='Nouveau', 
        verbose_name=_("statut"))
    type = models.CharField(
        max_length=32, 
        choices=TYPE_CHOICES, 
        verbose_name=_("type"), 
        blank=True,
        null=True)
    reception_bureau = models.ForeignKey(
        sigma.references.models.Bureau, 
        verbose_name=_("reception_bureau"), 
        blank=False,
        null=True)
    date_reception = models.DateField(
        verbose_name=_("date_reception"), 
        blank=True,
        null=True)
    appel = models.ForeignKey(
        'Appel', 
        verbose_name=_("appel"), 
        blank=False,
        null=True)
    piecesjointes = models.ManyToManyField(
        "PieceJointeType", 
        through='PieceJointeCandidature',
        verbose_name=_("Pieces jointes"), 
        subject=_("Pieces"),
        blank=True, 
        null=True)
    criteres = models.ManyToManyField(
        "CritereSupplementaire", 
        through='CritereSupplementaireCandidature',
        verbose_name=_("Criteres supplementaires"),
        subject=_("Criteres supp."),
        blank=True, 
        null=True)
    experts = models.ManyToManyField(
        "Expert", 
        through='ExpertCandidature',
        verbose_name=_("Experts"), 
        subject=_("Experts"),
        blank=True, 
        null=True)

    # mobilite
    mobilite_debut = models.DateField(
        verbose_name=_("mobilite_debut"), 
        blank=False,
        null=True)
    mobilite_fin = models.DateField(
        verbose_name=_("mobilite_fin"), 
        blank=False,
        null=True)
    mobilite_debute_accueil = models.BooleanField(
        verbose_name=_("mobilite_debute_accueil"), 
        blank=True,
        default=False,
        null=False)

    # origine
    origine_pays = models.ForeignKey(
        sigma.references.models.Pays, 
        related_name='origine_pays', 
        verbose_name=_("origine_pays"), 
        subject=_("Origine"),
        blank=False,
        null=True)
    origine_etabl = models.ForeignKey(
        sigma.references.models.Etablissement, 
        related_name='origine_etabl', 
        verbose_name=_("origine_etabl"), 
        subject=_("Origine"),
        blank=False,
        null=True)
    origine_etabl_autre = models.CharField(
        max_length=100, 
        verbose_name=_("origine_etabl_autre"), 
        subject=_("Origine"),
        blank=False,
        null=True)
    origine_duree_mois = models.PositiveIntegerField(
        verbose_name=_("origine_duree_mois"), 
        subject=_("Origine"),
        blank=True,
        null=True)
    origine_resp_institutionnel_civilite = models.CharField(
        max_length=32, 
        choices=CIVILITE_CHOICES, 
        verbose_name=_("origine_resp_institutionnel_civilite"), 
        subject=_("Origine"),
        blank=True,
        null=True)
    origine_resp_institutionnel_nom = models.CharField(
        max_length=40,
        verbose_name=_("origine_resp_institutionnel_nom"), 
        subject=_("Origine"),
        blank=True,
        null=True)
    origine_resp_institutionnel_prenom = models.CharField(
        max_length=40, 
        verbose_name=_("origine_resp_institutionnel_prenom"), 
        subject=_("Origine"),
        blank=True,
        null=True)
    origine_resp_institutionnel_fonction = models.CharField(
        max_length=40,
        verbose_name=_("origine_resp_institutionnel_fonction"), 
        subject=_("Origine"),
        blank=True,
        null=True)
    origine_resp_scientifique_civilite = models.CharField(
        max_length=32, 
        choices=CIVILITE_CHOICES,
        verbose_name=_("origine_resp_scientifique_civilite"), 
        subject=_("Origine"),
        blank=True,
        null=True)
    origine_resp_scientifique_nom = models.CharField(
        max_length=40,
        verbose_name=_("origine_resp_scientifique_nom"), 
        subject=_("Origine"),
        blank=True,
        null=True)
    origine_resp_scientifique_prenom = models.CharField(
        max_length=40,
        verbose_name=_("origine_resp_scientifique_prenom"), 
        subject=_("Origine"),
        blank=True,
        null=True)
    origine_resp_scientifique_fonction = models.CharField(
        max_length=40,
        verbose_name=_("origine_resp_scientifique_fonction"), 
        subject=_("Origine"),
        blank=True,
        null=True)

    # accueil
    accueil_pays = models.ForeignKey(
        sigma.references.models.Pays, 
        related_name='accueil_pays', 
        verbose_name=_("accueil_pays"), 
        subject=_("Accueil"),
        blank=False,
        null=True)
    accueil_etabl = models.ForeignKey(
        sigma.references.models.Etablissement, 
        related_name='accueil_etabl',
        verbose_name=_("accueil_etabl"), 
        subject=_("Accueil"),
        blank=False,
        null=True)
    accueil_etabl_autre = models.CharField(
        max_length=100, 
        verbose_name=_("accueil_etabl_autre"), 
        subject=_("Accueil"),
        blank=False,
        null=True,)
    accueil_duree_mois = models.PositiveIntegerField(
        verbose_name=_("accueil_duree_mois"), 
        subject=_("Accueil"),
        blank=True,
        null=True)
    accueil_resp_institutionnel_civilite = models.CharField(
        max_length=32, 
        choices=CIVILITE_CHOICES, 
        verbose_name=_("accueil_resp_institutionnel_civilite"), 
        subject=_("Accueil"),
        blank=True,
        null=True)
    accueil_resp_institutionnel_nom = models.CharField(
        max_length=40, 
        verbose_name=_("accueil_resp_institutionnel_nom"), 
        subject=_("Accueil"),
        blank=True,
        null=True)
    accueil_resp_institutionnel_prenom = models.CharField(
        max_length=40, 
        verbose_name=_("accueil_resp_institutionnel_prenom"), 
        subject=_("Accueil"),
        blank=True,
        null=True)
    accueil_resp_institutionnel_fonction = models.CharField(
        max_length=40, 
        verbose_name=_("accueil_resp_institutionnel_fonction"), 
        subject=_("Accueil"),
        blank=True,
        null=True)
    accueil_resp_scientifique_civilite = models.CharField(
        max_length=32, 
        choices=CIVILITE_CHOICES, 
        verbose_name=_("accueil_resp_scientifique_civilite"), 
        subject=_("Accueil"),
        blank=True,
        null=True)
    accueil_resp_scientifique_nom = models.CharField(
        max_length=40,
        verbose_name=_("accueil_resp_scientifique_nom"), 
        subject=_("Accueil"),
        blank=True,
        null=True)
    accueil_resp_scientifique_prenom = models.CharField(
        max_length=40,
        verbose_name=_("accueil_resp_scientifique_prenom"), 
        subject=_("Accueil"),
        blank=True,
        null=True)
    accueil_resp_scientifique_fonction = models.CharField(
        max_length=40,
        verbose_name=_("accueil_resp_scientifique_fonction"), 
        subject=_("Accueil"),
        blank=True,
        null=True)

    def __unicode__(self):
        return "%s - %s, %s" % (self.id, self.nom, self.prenom)

    def get_absolute_url(self):
        return "/candidatures/detail/%s" % self.id

    def is_valid(self):
        """Verification que la candidature a tout ses champs obligatoire 
        remplis"""
        for field in self._meta.fields:
            if not field.blank:
                if not getattr(self, field.name):
                    return False
        return True
            

    def get_moyenne(self):
        """Calcul de la moyenne des notes d'un candidat"""
        moyenne = 0
        candidature_expert_list = ExpertCandidature.objects.filter(candidature=self, is_note=True)
        if len(candidature_expert_list):
            for candidature_expert in candidature_expert_list:
                moyenne += candidature_expert.note
            return moyenne/len(candidature_expert_list)
        return "--"


    @staticmethod
    def search(user, value, by_appel=True):
        """Recherche des candidatures correspondant a differents criteres de 
        recherche et etant accessible a l'utilisateur en question

        @param user
        @param value
        """
        candidature_par_appel = {}
        candidatures = []

        if by_appel:
            for appel in Appel.objects.all():
                # nous recherchons toutes les candidatures
                if not value:
                    candidatures = Candidature.objects.filter(appel=appel)
                # nous recherchons par id
                elif value.isdigit():
                    candidatures = Candidature.objects.filter(appel=appel, id=int(value))
                # nous recherchons par nos criteres pre-definis
                else:
                    conds = models.Q(appel=appel) \
                        & models.Q(nom__contains=value) \
                        | models.Q(prenom__contains=value) \
                        | models.Q(nom_jeune_fille__contains=value)
                    candidatures = Candidature.objects.filter(conds)
                # classement des candidatures par appel d'offre
                for candidature in candidatures:
                    if candidature.appel not in candidature_par_appel:
                        candidature_par_appel[candidature.appel] = []
                    candidature_par_appel[candidature.appel].append(candidature)
            return candidature_par_appel
        else:
            # nous recherchons toutes les candidatures
            if not value:
                return Candidature.objects.all()
            # nous recherchons par id
            elif value.isdigit():
                candidatures = Candidature.objects.filter(id=int(value))
                # nous recherchons par nos criteres pre-definis
            else:
                conds = models.Q(nom__contains=value) \
                    | models.Q(prenom__contains=value) \
                    | models.Q(nom_jeune_fille__contains=value)
                return Candidature.objects.filter(conds)


class RegionalGroup(django.contrib.auth.models.Group):
    """
    Nouveau type de groupes utilises dans Django. 
    Nous y ajoutons la notions de bureau qui permet d'associer chaque groupe
    a l'un d'eux et ainsi de pouvoir classer les utilisateur par bureau
    de leurs groupes

    Note
    ====
    Cet objet est automatiquement ajoute au panneau d'administration 
    et nous ne devons pas ajouter le support pour dans un fichier 
    admin.py puisque le c'est une surcharge de la classe groupe qui elle, 
    est deja supportee.
    """
    bureau = models.ForeignKey(sigma.references.models.Bureau)
# on remplace ici la classe Group par notre propre classe
# supportant les bureaux
django.contrib.auth.models.Group = RegionalGroup


class AufUser(django.contrib.auth.models.User):
    """ Nouveau type d'utilisateur qui remplace l'utilisateur Django
    classique en permettant de faire le lien entre les objets de
    type employe et experts qui peuvent eux aussi se connecter au
    systeme afin de realiser certaines actions    
    """
    expert = models.ForeignKey(
        'Expert',
        unique = True,
        null = True,
        blank = True)
    employe = models.ForeignKey(
        sigma.references.models.Employe,
        unique = True,
        null = True,
        blank = True)

    def is_employe(self):
        return self.employe is not None

    def is_expert(self):
        return self.expert is not None

    def get_regions(self):
        return [group.region for group in RegionalGroup.objects.filter(id__in=self.groups.all())]

    def get_bureaux(self):
        return [group.bureau for group in RegionalGroup.objects.filter(id__in=self.groups.all())]
django.contrib.auth.models.User = AufUser

class Expert(models.Model):
    """Un expert dans le système qui à même de donner des notes"""

    serialisable_fields = ('nom', 'prenom', 'etablissement')

    nom = models.CharField(
        max_length=40, 
        verbose_name=_("Nom"))
    prenom = models.CharField(
        max_length=40, 
        verbose_name=_("Prenom"))
    courriel = models.CharField(
        max_length=255,
        verbose_name=_("Courriel"))
    motdepasse = models.CharField(
        max_length=255,
        verbose_name=_("Mot de passe"))
    etablissement = models.ForeignKey(
        sigma.references.models.Etablissement, 
        verbose_name=_("etablissement"), 
        blank=False,
        null=True)
    discipline = models.ManyToManyField(
        sigma.references.models.Discipline, 
        verbose_name=_("discipline"), 
        subject=_("Discipline"))
    actif = models.BooleanField()

    def __unicode__(self):
        return "%s %s" % (self.prenom, self.nom)

    def get_absolute_url(self):
        return "/experts/detail/%s" % self.id

    @staticmethod
    def search(user, value):
        """Recherche d'un expert dans le systeme
        
        Les champs recherche sont:
         - nom
         - prenom

        @param user Utilisateur courant
        @param value Valeur recherche dans les champs
        """
        if not value:
            resultats = Expert.objects.all()
        if value.isdigit():
            resultats = Expert.objects.filter(id=int(value))
        else:
            cond_nom = models.Q(nom__contains=value)
            cond_prenom = models.Q(prenom__contains=value)
            resultats = Expert.objects.filter(cond_nom|cond_prenom)
        return resultats


class ExpertCandidature(models.Model):
    """Classe d'association entre les candidatures et les experts"""
    candidature = models.ForeignKey(
        'Candidature', 
        verbose_name=_("candidature"))
    expert = models.ForeignKey(
        'Expert', 
        verbose_name=_("Expert"))
    note = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0)
    is_note = models.BooleanField(
        default=False)

    def __unicode__(self):
        return "%s: %s" % (self.candidature, self.expert)


class Note(models.Model):
    """Une note qui est donné à une candidature par un expert """
    candidature = models.ForeignKey(
        'Candidature', 
        verbose_name=_("candidature"))
    expert = models.ForeignKey(
        'Expert', 
        verbose_name=_("Expert"))
    note = models.DecimalField(
        max_digits=4, 
        decimal_places=0, 
        default=0)
    description = models.CharField(
        max_length=255, 
        verbose_name=_("description"))

    def __unicode__(self):
        return "%s: %s" % (self.description, self.note)


class ChampsCategorie(models.Model):
    """Les champs des blogs de champs d'une catégories"""
    TYPE_CHOICES = (
        ('Texte', _('Texte')),
        ('Booleen', _('Booleen')),
        ('Nombre', _('Nombre')),)

    libelle = models.CharField(
        max_length=30, 
        verbose_name=_("libelle"))
    type = models.CharField(
        max_length=32, 
        choices=TYPE_CHOICES, 
        default='Texte', 
        verbose_name=_("type"))
    bloc = models.ManyToManyField(
        'BlocChamps', 
        verbose_name=_("bloc"))

    serialisable_fields = ('libelle', 'type')

    def __unicode__(self):
        return self.libelle


class BlocChamps(models.Model):
    """Les blocs de champs qui doivent être remplis par une candidature qui 
    répond à une appel d'offre
    """
    libelle = models.CharField(
        max_length=30, 
        verbose_name=_("libelle"))
    categorie = models.ManyToManyField(
        'Categorie', 
        verbose_name=_("categorie"))

    serialisable_fields = ('libelle', )

    def __unicode__(self):
        return self.libelle


class Answer(models.Model):
    """Réponse à un champs d'un bloc de champs d'une catégorie"""
    value = models.CharField(max_length=255) 
    champscategorie = models.ForeignKey('ChampsCategorie')
    candidature = models.ForeignKey('Candidature')

    serialisable_fields = ('value')


class ProjetPosteManager(models.Manager):
    """Gestionnaire des projets poste qui nous permet de ne seulement 
    obtenir que les projetpostes qui ont une categorie correspondante"""
    def get_query_set(self):
        postes_mob = ref_Poste.objects.filter(type='Mobilités')
        postes_cat = Categorie.objects.values_list('poste__id', flat=True)

        queryset = super(ProjetPosteManager, self).get_query_set()
        queryset = queryset.filter(actif=True)
        queryset = queryset.filter(code_poste__id__in=postes_mob)
        queryset = queryset.filter(code_poste__id__in=postes_cat)
        return queryset


class ProjetPoste(ref_ProjetPoste):
    """Un projet poste est une instance d'une categorie

    Chacun des projets poste se verra associe un certains nombre 
    d'appels d'offre
    """
    objects = ProjetPosteManager()

    class Meta:
        proxy = True

    serialisable_fields = ('code', 
                           'code_bureau', 
                           'code_programme', 
                           'actif')

    def get_absolute_url(self):
        return "/projets/detail/%s" % self.id

    def getCategorie(self):
        """Obtention de la categorie d'un projetposte en cherchant la categorie 
        correspondant a son poste"""
        for cat in Categorie.objects.filter(poste=self.code_poste):
            return cat

    def getRegion(self):
        """Obtention de la region d'un projet en allant chercher celle 
        associee a son bureau"""
        return self.code_bureau.region

    @staticmethod
    def search(user, value):
        """Recherche de projetposte pour une valeur quelquonque 
        et un utilisateur

        @param user Utilisateur courant
        @param value Valeur recherchee
        """
        resultats = []
        if not value:
            resultats = ProjetPoste.all(user)
        elif value.isdigit():
            resultats = ProjetPoste.all(user, criteria="id", value=int(value))
        else:
            conds = models.Q(code__contains=value)
            resultats = ProjetPoste.objects.filter(conds)
        return resultats
            

    @staticmethod
    def all(user, criteria='', value=''):
        """Obtention de tout les projetsposte correspondant a un critere 
        d'une valeur

        @param user Utilisateur courant
        @param criteria Critere de recherche
        @param value Valeur recherche
        """
        projets = []
        if user is not None:
            queryset = []
            if not(criteria == '' and value == ''):
                key = '%s__contains' % (criteria)
                queryset = ProjetPoste.objects.filter(**{str(key):value})
            else:
                queryset = ProjetPoste.objects.all()
            bureaux = user.get_bureaux()
            for pposte in queryset:
                try:
                    if user.is_staff \
                            or pposte.code_bureau in bureaux:
                        projets.append(pposte)
                except sigma.references.models.Bureau.DoesNotExist:
                    pass
        return projets


class WorkflowLog(models.Model):
    """Pour les objets du workflow, on log chaque action qui sont executes.

    Les logs sont gardes dans la base de donnees afin de pouvoir par la suite
    consulter l'historique d'evolution des objets
    """
    LEVEL_CHOICES = (
        (1, _("ERROR")), # Un critere de sélection n'est pas respecté
        (2, _("WARNING")), # Un facteur d'erreur non bloquant
        (3, _("INFO")), # Passage réussi d'un statut à un autre
        (4, _("SYS")),) # Événement système illégal
        
    objet = models.ForeignKey(WorkflowObject)
    from_state = models.CharField(
        max_length=32, 
        choices=Candidature.STATUT_CHOICES)
    to_state = models.CharField(
        max_length=32, 
        choices=Candidature.STATUT_CHOICES)
    description = models.CharField(
        max_length=80)
    user = models.ForeignKey(
        django.contrib.auth.models.User, 
        null=True)
    level = models.PositiveIntegerField(
        choices=LEVEL_CHOICES)
    timestamp = models.DateTimeField(
        auto_now=True)
    commentaires = models.CharField(
        max_length=200)

    class Meta:
        unique_together = (("objet", "from_state", "to_state", "description"),)

    def __init__(self, *args, **kwargs):
        """
        @param *args
        @param **kwargs
        """
        models.Model.__init__(self, *args, **kwargs)

    def __unicode__(self):
        return self.description


class PieceJointeType(models.Model):
    """Representation des types de pieces jointes possible"""
    nom = models.CharField(max_length=32)
    description = models.CharField(max_length=80)

    def __unicode__(self):
        return self.description

class PieceJointeCandidature(models.Model):
    """Lien entre un type de piece jointe et une candidature"""
    candidature = models.ForeignKey(Candidature)
    piecejointe = models.ForeignKey(PieceJointeType)
    presente = models.BooleanField(default=False)
    conforme = models.BooleanField(default=False)
    fichier = models.FileField(null=True, blank=True, 
                               upload_to=storage.get_upload_path_pjc)

    _re_search_filename = re.compile(r'pj_\d*_(\S*)')

    def __unicode__(self):
        return unicode(self.piecejointe)

    def getFilename(self):
        filename = ''
        try:
            basename = os.path.basename(self.fichier.url)
            filename = PieceJointeCandidature._re_search_filename.match(basename)
            filename = filename.groups()[0]
        except ValueError:
            pass
        return filename

class CritereSupplementaire(models.Model):
    """Un critere supplementaire a evaluer lors de l'analyse descandidatures"""
    nom = models.CharField(max_length=32)
    description = models.CharField(max_length=80)
    valide_par_default = models.BooleanField(default=True)

    def __unicode__(self):
        return self.description

class CritereSupplementaireCandidature(models.Model):
    """Lien entre une candidature et un critère supplémentaire disponible dans
    le système et ouvert à tous les appels d'offres"""
    candidature = models.ForeignKey(Candidature)
    critere = models.ForeignKey(CritereSupplementaire)
    valide = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.critere)


class NiveauEtude(models.Model):
    """Niveau d'etude d'un candidat"""
    nom = models.CharField(max_length=20)
    description = models.CharField(max_length=80)

    def __unicode__(self):
        return self.nom
