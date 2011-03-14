# -*- encoding: utf-8 -*-

from django.db import models
from workflow import AppelWorkflow
from datamaster_modeles.models import Pays, Bureau, Etablissement, Discipline

CIVILITE = (
    ('MR', "Monsieur"),
    ('MM', "Madame"),
    ('ME', "Mademoiselle"),
)

TYPE_THESE = (
    ('CT', "Co-Tutelle"),
    ('CD', "Co-Direction"),
    ('AU', "Autre"),
)
    
CANDIDAT_STATUT = (
    ('1', 'Etudiant'),
    ('2', 'Chercheur'),
    ('3', 'Enseignant'),
    ('4', 'Enseignant-chercheur'),
    ('5', 'Post-Doc'),
)

REPONSE = (
    ('sr', "sr"),
    ('a', "a"),
    ('r', "r"),
)



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


class CategorieBourse(models.Model):
    """
    Catégorie de bourse : couche d'abstraction permettant aux utilisateurs de spécifier de nouveaux types de bourses.
    Cette catégorie doit être liée à un code budgétaire.
    """
    pass

class NiveauEtude(models.Model):
    """
    Nombre d'années universitaires.
    """
    annees = models.CharField(max_length=2, verbose_name="Nombre d'années universitaires", )
    nom = models.CharField(max_length=255, verbose_name="nom",)

class Diplome(models.Model):
    """
    """
    nom = models.CharField(max_length=255, verbose_name="Nom", blank=True, null=True)
    date = models.DateField(max_length=255, verbose_name="Date", blank=True, null=True)
    niveau = models.ForeignKey(NiveauEtude, related_name="niveau", verbose_name="Niveau d'étude", blank=True, null=True)
    etablissement_nom = models.CharField(max_length=255, verbose_name="Nom de l'établissement", blank=True, null=True)
    etablissement_pays = models.ForeignKey(Pays, related_name="etablissement_pays", verbose_name="Pays de l'établissement", blank=True, null=True)
    
class Dossier(models.Model):
    """
    Informations générales du dossier de candidature.
    """
    appel = models.ForeignKey(Appel, verbose_name="Appel", related_name="appel")
    candidat = models.ForeignKey(Candidat, verbose_name="Candidat", related_name="candidat")

    candidat_statut = models.CharField(max_length=255, verbose_name="Statut du candidat", choices=CANDIDAT_STATUT, blank=True, null=True)
    candidat_fonction = models.CharField(max_length=255, verbose_name="Statut du candidat", blank=True, null=True)

    # ?? je ne trouve pas dans le UI... mais il y a des data??
    bureau_rattachement = models.ForeignKey(Bureau, blank=True, null=True)

    # Dernier diplôme obtenu
    diplomes = models.ManyToManyField(Diplome, blank=True, null=True)

    # Tentative pour récupérer de l'information passée
    dernier_projet_description = models.TextField(verbose_name="Description du dernier projet ou programme", blank=True, null=True)
    dernier_projet_annee = models.CharField(max_length=4, verbose_name="Année du dernier projet ou programme", blank=True, null=True)
    derniere_bourse_categorie = models.ForeignKey(CategorieBourse, related_name="bourse_categorie", verbose_name="Catégorie de la dernière bourse", blank=True, null=True)
    derniere_bourse_annee = models.CharField(max_length=4, verbose_name="Année de la dernière bourse", blank=True, null=True)

    ## ???? probablement le chose irrecevable, rapproché, recevable (devrait etre géré par WF état auf.django.workflow)
    #statut = models.IntegerField(db_column='F_STATUT', default=1)   # foreign

    ## ????
    # etat = models.BooleanField(db_column='I_ETAT', default=False)

    
    # Évaluation
    moyenne_academique = models.FloatField(verbose_name="Moyenne académique", blank=True, null=True)
    opportunite_regionale = models.CharField(max_length=255, verbose_name="Opportunité régionale", blank=True, null=True)

    # traitement ????
    #########################################################################################################

    #classement_1 = models.IntegerField(null=True, db_column='N_CLASSEMENT_1', blank=True)
    #classement_2 = models.IntegerField(null=True, db_column='N_CLASSEMENT_2', blank=True)
    #classement_3 = models.IntegerField(null=True, db_column='N_CLASSEMENT_3', blank=True)

    #coche_selection = models.BooleanField(db_column='I_COCHE_SELECTION', default=False)
    #reponse_notification = models.CharField(max_length=6, db_column='Y_REPONSE_NOTIFICATION', choices=REPONSE, default='sr')
    #commentaire_notification = models.CharField(max_length=255, db_column='L_COMMENTAIRE_NOTIFICATION')
    #autres_criteres = models.CharField(max_length=255, db_column='L_AUTRES_CRITERES')
    #erreurs_recevabilite = models.TextField(db_column='L_ERREURS_RECEVABILITE')
    #repechage = models.BooleanField(db_column='I_REPECHAGE', default=False)
    #rendu_irrecevable = models.BooleanField(db_column='I_RENDU_IRRECEVABLE', default=False)

    # Toutes les données n'ont aucune date de spécifiée???
    #########################################################################################################
    # dd_activation = models.CharField(max_length=10, db_column='DD_ACTIVATION', default='0000-00-00')
    # df_activation = models.CharField(max_length=10, db_column='DF_ACTIVATION', default='0000-00-00')
    


class DossierFaculte(models.Model):
    dossier = models.ForeignKey(Dossier, verbose_name="Dossier",)

    # Etablissement connu de l'AUF
    etablissement = models.ForeignKey(Etablissement, related_name="etablissement", verbose_name="Établissement", blank=True, null=True)

    # Autre établissement
    autre_etablissement_nom = models.CharField(max_length=255, verbose_name="Autre établissement", blank=True, null=True)
    autre_etablissement_pays = models.ForeignKey(Pays, related_name="autre_etablissement_pays", verbose_name="Pays", blank=True, null=True)
    autre_etablissement_adresse = models.CharField(max_length=255, verbose_name="Adresse", blank=True, null=True)
    autre_etablissement_code_postal = models.CharField(max_length=255, verbose_name="Adresse", blank=True, null=True)
    autre_etablissement_ville = models.CharField(max_length=255, verbose_name="Ville", blank=True, null=True)
    autre_etablissement_region = models.CharField(max_length=255, verbose_name="Region", blank=True, null=True)
    autre_etablissement_valide = models.NullBooleanField(verbose_name="Erreur recevabilité établissement", blank=True, null=True)
    autre_etablissement_erreur = models.CharField(max_length=255, verbose_name="Commentaire sur la recevabilité", blank=True, null=True)

    # responsable institutionnel (Directeur de thèse)
    resp_inst_civilite = models.CharField(max_length=2, verbose_name="Civilité responsable institutionnel", choices=CIVILITE, blank=True, null=True)
    resp_inst_nom = models.CharField(max_length=255, verbose_name="Nom du responsable institutionnel", blank=True, null=True)
    resp_inst_prenom = models.CharField(max_length=255, verbose_name="Prénom du responsable institutionnel", blank=True, null=True)
    resp_inst_fonction = models.CharField(max_length=255, verbose_name="Nom du responsable institutionnel", blank=True, null=True)
    resp_inst_courriel = models.CharField(max_length=255, verbose_name="Courriel du responsable institutionnel", blank=True, null=True)
    resp_inst_telephone = models.CharField(max_length=255, verbose_name="Téléphone du responsable institutionnel", blank=True, null=True)
    resp_inst_fax = models.CharField(max_length=255, verbose_name="FAX du responsable institutionnel", blank=True, null=True)

    # responsable scientifique (Accord scientifique)
    resp_sc_civilite = models.CharField(max_length=2, verbose_name="Civilité responsable scientifique", choices=CIVILITE, blank=True, null=True)
    resp_sc_nom = models.CharField(max_length=255, verbose_name="Nom du responsable scientifique", blank=True, null=True)
    resp_sc_prenom = models.CharField(max_length=255, verbose_name="Prénom du responsable scientifique", blank=True, null=True)
    resp_sc_fonction = models.CharField(max_length=255, verbose_name="Nom du responsable scientifique", blank=True, null=True)
    resp_sc_courriel = models.CharField(max_length=255, verbose_name="Courriel du responsable scientifique", blank=True, null=True)
    resp_sc_telephone = models.CharField(max_length=255, verbose_name="Téléphone du responsable scientifique", blank=True, null=True)
    resp_sc_fax = models.CharField(max_length=255, verbose_name="FAX du responsable scientifique", blank=True, null=True)

    # faculté, département ou labo (Accord scientifique)
    faculte_url = models.CharField(max_length=255, verbose_name="URL de la faculté", blank=True, null=True)
    faculte_nom = models.CharField(max_length=255, verbose_name="Nom de la faculté", blank=True, null=True)
    faculte_adresse = models.CharField(max_length=255, verbose_name="Adresse de la faculté", blank=True, null=True)
    faculte_code_postal = models.CharField(max_length=255, verbose_name="Code postal de la faculté", blank=True, null=True)
    faculte_ville = models.CharField(max_length=255, verbose_name="Ville de la faculté", blank=True, null=True)
    faculte_courriel = models.CharField(max_length=255, verbose_name="Courriel de la faculté", blank=True, null=True)
    faculte_telephone = models.CharField(max_length=255, verbose_name="Téléphone de la faculté", blank=True, null=True)
    faculte_fax = models.CharField(max_length=255, verbose_name="FAX de la faculté", blank=True, null=True)
    

class DossierOrigine(DossierFaculte):
    """
    Informations sur le contexte d'origine du candidat.
    """
    pass

class DossierAccueil(DossierFaculte):
    """
    Informations sur le contexte d'accueil du candidat.
    """
    pass


class DossierMobilite(models.Model):
    """Informations sur la mobilité demandée par le candidat.
    """
    dossier = models.ForeignKey(Dossier, verbose_name="Dossier",)

    # Période de mobilité
    date_debut = models.DateField(verbose_name="Date de début souhaitée", blank=True, null=True)
    date_fin = models.DateField(verbose_name="Date de fin souhaitée", blank=True, null=True)
    duree = models.CharField(max_length=255, verbose_name="Durée totale mobilité souhaitée (mois)", blank=True, null=True)

    # Dossier scientifique
    intitule_projet = models.CharField(max_length=255, verbose_name="Intitulé du projet", blank=True, null=True)
    mots_clefs = models.CharField(max_length=255, verbose_name="Mots clefs", blank=True, null=True)

    # Formation en cours
    formation_en_cours_diplome = models.CharField(max_length=255, verbose_name="Intitulé du diplôme", blank=True, null=True)
    formation_en_cours_niveau = models.ForeignKey(NiveauEtude, related_name="formation_en_cours_niveau", verbose_name="Niveau d'étude", blank=True, null=True)

    ## pas trouvé dans le UI...
    ############################################################################################################
    type_intervention = models.IntegerField(db_column='F_TYPE_INTERVENTION', default=0)  # foreign
    public_vise = models.IntegerField(db_column='F_PUBLIC_VISE', default=0)  # foreign
    autres_publics = models.CharField(max_length=255, verbose_name="Autres publics", blank=True, null=True)
    ############################################################################################################

    # Disciplines
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", blank=True, null=True)
    sous_discipline = models.CharField(max_length=255, blank=True, null=True)

    # Alternance
    alternance_nb_mois_origine = models.IntegerField(verbose_name="Nombre de mois à l'origine", blank=True, null=True)
    alternance_nb_mois_accueil = models.IntegerField(verbose_name="Nombre de mois à l'accueil", blank=True, null=True)
    alternance_accueil_puis_origine = models.NullBooleanField(verbose_name="Mobilité commençée à l'accueil?", blank=True, null=True)

    ## pas trouvé dans le UI...
    ############################################################################################################
    diplome_demande_nom = models.CharField(max_length=255, verbose_name="Diplôme demandé", blank=True, null=True)
    diplome_demande_niveau = models.ForeignKey(NiveauEtude, related_name="diplome_demande_niveau", verbose_name="Niveau d'étude", blank=True, null=True)
    ############################################################################################################
    
    # Thèse
    these_date_inscription = models.DateField(verbose_name="Date d'inscription", blank=True, null=True)
    these_date_obtention_prevue = models.DateField(verbose_name="Date d'obtention prévue", blank=True, null=True)
    these_soutenance_pays = models.ForeignKey(Pays, related_name="soutenance_pays", verbose_name="Pays de soutenance", blank=True, null=True)
    these_soutenance_date = models.DateField(verbose_name="Date de soutenance", blank=True, null=True)
    these_type = models.CharField(max_length=2, verbose_name="Type de thèse", choices=TYPE_THESE, blank=True, null=True)
    these_type_autre = models.CharField(max_length=255, verbose_name="Autre type de thèse", blank=True, null=True)

    # directeur thèse accueil
    dir_acc_civilite = models.CharField(max_length=2, verbose_name="Civilité", choices=CIVILITE, blank=True, null=True)
    dir_acc_nom = models.CharField(max_length=255, verbose_name="Nom", blank=True, null=True)
    dir_acc_prenom = models.CharField(max_length=255, verbose_name="Prénom", blank=True, null=True)

    # directeur thèse origine
    dir_ori_civilite = models.CharField(max_length=2, verbose_name="Civilité", choices=CIVILITE, blank=True, null=True)
    dir_ori_nom = models.CharField(max_length=255, verbose_name="Nom", blank=True, null=True)
    dir_ori_prenom = models.CharField(max_length=255, verbose_name="Prénom", blank=True, null=True)
