# -*- encoding: utf-8 -*-

from django.db import models
from workflow import AppelWorkflow
from datamaster_modeles.models import Pays

class Appel(AppelWorkflow, models.Model):
    """
    Un Appel est une proposition de l'AUF pour offrir une bourse de mobilité s'intégrant dans un projet.
    """
    nom = models.CharField(max_length=255, verbose_name="Nom")
    code_budgetaire = models.CharField(max_length=255, verbose_name="Code budgétaire", blank=True, null=True)
    formulaire_wcs = models.CharField(max_length=255, verbose_name="Nom du formulaire WCS", blank=True, null=True)
    date_debut = models.DateField(verbose_name="Date de début", blank=True, null=True)
    date_fin = models.DateField(verbose_name="Date de fin", blank=True, null=True)
    date_activation = models.DateField(verbose_name="Date d'activation", blank=True, null=True)
    date_desactivation = models.DateField(verbose_name="Date de désactivation", blank=True, null=True)

    def __unicode__(self):
        return self.nom

CIVILITE = (
    ('MR', "Monsieur"),
    ('MM', "Madame"),
    ('ME', "Mademoiselle"),
)
class Candidat(models.Model):
    """
    Personne qui répond à un appel d'offre.
    """
    # meta
    date_creation = models.DateField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateField(auto_now=True, verbose_name="Date de modification")

    # identification personne
    nom = models.CharField(max_length=255, verbose_name="Nom de famille")
    prenom = models.CharField(max_length=255, verbose_name="Prénom")
    nom_jeune_fille = models.CharField(max_length=255, verbose_name="Nom de jeune fille", blank=True, null=True)

    # identification avancée personne
    nationalite = models.ForeignKey(Pays, verbose_name="Nationalité", blank=True, null=True)
    naissance_ville = models.CharField(max_length=255, verbose_name="Ville de naissance", blank=True, null=True)
    naissance_date = models.DateField(max_length=255, verbose_name="Date de naissance", blank=True, null=True)
    naissance_pays = models.ForeignKey(Pays, related_name="naissance_pays", verbose_name="Pays de naissance", blank=True, null=True)

    # coordonnées
    pays = models.ForeignKey(Pays, related_name="pays", verbose_name="Pays de résidence", blank=True, null=True)
    adresse = models.CharField(max_length=255, verbose_name="Adresse", blank=True, null=True)
    code_postal = models.CharField(max_length=255, verbose_name="Code postal", blank=True, null=True)
    ville = models.CharField(max_length=255, verbose_name="Ville", blank=True, null=True)
    region = models.CharField(max_length=255, verbose_name="Région", blank=True, null=True)
    telephone_perso = models.CharField(max_length=255, verbose_name="Téléphone personnel", blank=True, null=True)
    fax_perso = models.CharField(max_length=255, verbose_name="FAX personnel", blank=True, null=True)
    courriel_perso = models.CharField(max_length=255, verbose_name="Courriel personnel", blank=True, null=True)
    telephone_pro = models.CharField(max_length=255, verbose_name="Téléphone professionnel", blank=True, null=True)
    fax_pro = models.CharField(max_length=255, verbose_name="FAX professionnel", blank=True, null=True)
    courriel_pro = models.CharField(max_length=255, verbose_name="Courriel professionnel", blank=True, null=True)

    # renseignements divers
    sexe = models.CharField(max_length=1, verbose_name="Sexe", blank=True, null=True)
    civilite = models.CharField(max_length=2, verbose_name="Civilité", choices=CIVILITE, blank=True, null=True)

    

