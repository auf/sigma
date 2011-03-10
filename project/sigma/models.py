# -*- encoding: utf-8 -*-

from django.db import models
from workflow import AppelWorkflow

class Appel(AppelWorkflow, models.Model):
    """
    """
    nom = models.CharField(max_length=200, verbose_name="Nom")

#    field_dependencies = {
#        'alternance_obligatoire': 'alternance_duree_min_mois',
#        'renouvellement_possible' : 'renouvellement_nb_max',
#        'diplome_duree_validite_obligatoire': 'diplome_duree_validite_min',}
#
#    serialisable_fields = ( 'renouvellement_possible',
#                            'renouvellement_nb_max',
#                            'age_max',
#                            'statut_etudiant_obligatoire',
#                            'mobilite_duree_mois_min',
#                            'mobilite_duree_mois_max',
#                            'origine_etabl_membre_obligatoire',
#                            'accueil_etabl_membre_obligatoire',
#                            'diplome_duree_validite_obligatoire',
#                            'diplome_duree_validite_min',
#                            'alternance_obligatoire',
#                            'alternance_duree_min_mois',
#                            'niveau_etude')
#
#    STATUT_CHOICES = (
#        ('Nouveau', _("Nouveau_appel")),
#        ('Supprime', _("Supprime_appel")),
#        ('Diffuse', _("Diffuse_appel")),
#        ('Analyse', _("Analyse_appel")), 
#        ('Evalue', _("Evalue_appel")),
#        ('Selectionne', _("Selectionne_appel")),
#        ('Notifie', _("Notifie_appel")),
#        ('Suivie', _("Suivie_appel")), 
#        ('Ferme', _("Ferme_appel")),
#        )
#
#    # meta
#    actif = models.BooleanField()
#
#    # Information generales
#    nom = models.CharField(
#        max_length=200, 
#        verbose_name=_("nom_appel"))
#    projetposte = models.ForeignKey(
#        'ProjetPoste', 
#        verbose_name=_("projetposte"))
#
#    # traitement
#    statut = models.CharField(
#        max_length=32, 
#        choices=STATUT_CHOICES, 
#        default='Nouveau', 
#        verbose_name=("statut"))
#
#    renouvellement_possible = models.BooleanField(
#        verbose_name=_("renouvellement_possible"), 
#        subject=_("Parametres generaux"))
#    renouvellement_nb_max = models.PositiveIntegerField( 
#        verbose_name=_("renouvellement_nb_max"), 
#        subject=_("Parametres generaux"),
#        blank=False, null=True)
#    inscription_date_debut = models.DateField(
#        verbose_name=_("inscription_date_debut"), 
#        subject=_("Parametres generaux"))
#    inscription_date_fin = models.DateField(
#        verbose_name=_("inscription_date_fin"), 
#        subject=_("Parametres generaux"))
#    mobilite_date_debut = models.DateField(
#        verbose_name=_("mobilite_date_debut"), 
#        subject=_("Parametres generaux"))
#    mobilite_date_fin = models.DateField(
#        verbose_name=_("mobilite_date_fin"), 
#        subject=_("Parametres generaux"))
#    piecesjointes = models.ManyToManyField(
#        "PieceJointeType",
#        verbose_name=_("Pieces jointes"),
#        subject=_("Pieces"),
#        blank=True, null=True)
#    criteres = models.ManyToManyField(
#        "CritereSupplementaire",
#        verbose_name=_("Criteres supplementaires"),
#        subject=_("Criteres supplementaires"),
#        blank=True, null=True)
#
#    # criteres
#    age_max = models.IntegerField(
#        verbose_name=_("age_max"), 
#        subject=_("Criteres de selection"))
#    statut_etudiant_obligatoire = models.BooleanField(
#        verbose_name=_("statut_etudiant_obligatoire"), 
#        subject=_("Criteres de selection"))
#    niveau_etude = models.ForeignKey(
#        to='NiveauEtude',
#        blank = True, null=True,
#        verbose_name=_("Niveau d'etude"),
#        subject=_("Criteres de selection"))
#    mobilite_duree_mois_min = models.PositiveIntegerField(
#        verbose_name=_("mobilite_duree_mois_min"), 
#        subject=_("Criteres de selection"))
#    mobilite_duree_mois_max = models.PositiveIntegerField(
#        verbose_name=_("mobilite_duree_mois_max"), 
#        subject=_("Criteres de selection"))
#    origine_etabl_membre_obligatoire = models.BooleanField(
#        verbose_name=_("origine_etabl_membre_obligatoire"), 
#        subject=_("Criteres de selection"))
#    accueil_etabl_membre_obligatoire = models.BooleanField(
#        verbose_name=_("accueil_etabl_membre_obligatoire"), 
#        subject=_("Criteres de selection"))
#    diplome_duree_validite_obligatoire = models.BooleanField(
#        verbose_name=_("diplome_duree_validite_obligatoire"), 
#        subject=_("Criteres de selection"))
#    diplome_duree_validite_min = models.PositiveIntegerField(
#        verbose_name=_("diplome_duree_validite_min"), 
#        subject=_("Criteres de selection"),
#        blank=True, null=True)
#    alternance_obligatoire = models.BooleanField(
#        verbose_name=_("alternance_obligatoire"), 
#        subject=_("Criteres de selection"))
#    alternance_duree_min_mois = models.PositiveIntegerField(
#        verbose_name=_("alternance_duree_min_mois"), 
#        subject=_("Criteres de selection"),
#        blank=True, null=True)
#
#    def __unicode__(self):
#        return self.nom
