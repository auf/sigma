# -*- encoding: utf-8 -*-

from django import forms
from django.db import models
from django.contrib.auth.models import User
from workflow import AppelWorkflow, DossierWorkflow
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

NOTE_MIN = 1
NOTE_RANGE = 1
NOTE_MAX = 5
NOTES = [(i, i) for i in range(NOTE_MIN, NOTE_MAX, NOTE_RANGE)]


class Expert(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom")
    prenom = models.CharField(max_length=255, verbose_name="Prénom")
    courriel =  models.EmailField(max_length=75, null=True, blank=True)
    region = models.CharField(max_length=255, verbose_name="Région", 
                        blank=True, null=True)
    etablissement = models.ForeignKey(Etablissement, 
                        verbose_name="Établissement", 
                        blank=True, null=True)
    commentaire = models.TextField(null=True, blank=True)
    actif = models.BooleanField()
    disciplines = models.ManyToManyField(Discipline, 
                        verbose_name="Disciplines", 
                        blank=True, null=True)
    dossiers = models.ManyToManyField('Dossier',
                                      verbose_name='Dossiers', 
                                      through='ExpertDossier',
                                      blank=True, null=True)
    
    def __unicode__(self):
        return "%s, %s (%d)" %(self.nom, self.prenom, self.id)

class ExpertDossier(models.Model):
    expert = models.ForeignKey('Expert')
    dossier = models.ForeignKey('Dossier')
    note = models.IntegerField(null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)


class UserProfile(models.Model):
    user = models.ForeignKey("auth.User", unique=True)
    disciplines = models.ManyToManyField(Discipline, 
                        verbose_name="Disciplines", 
                        blank=True, null=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Appel(AppelWorkflow, models.Model):
    """
    Un Appel est une proposition de l'AUF pour offrir une bourse de mobilité 
    s'intégrant dans un projet.
    """
    nom = models.CharField(max_length=255, verbose_name="Nom")
    code_budgetaire = models.CharField(max_length=255, 
                        verbose_name="Code budgétaire", 
                        blank=True, null=True)
    formulaire_wcs = models.CharField(max_length=255, 
                        verbose_name="Nom du formulaire WCS", 
                        blank=True, null=True)
    date_debut = models.DateField(verbose_name="Date de début", 
                        blank=True, null=True)
    date_fin = models.DateField(verbose_name="Date de fin", 
                        blank=True, null=True)
    date_activation = models.DateField(verbose_name="Date d'activation", 
                        blank=True, null=True)
    date_desactivation = models.DateField(verbose_name="Date de désactivation", 
                        blank=True, null=True)

    def __unicode__(self):
        return "#%s : %s" %(self.id, self.nom)

class Candidat(models.Model):
    """
    Personne qui répond à un appel d'offre.
    """
    # meta
    date_creation = models.DateField(auto_now_add=True, 
                        verbose_name="Date de création")
    date_modification = models.DateField(auto_now=True, 
                        verbose_name="Date de modification")

    # identification personne
    nom = models.CharField(max_length=255, verbose_name="Nom de famille")
    prenom = models.CharField(max_length=255, verbose_name="Prénom")
    nom_jeune_fille = models.CharField(max_length=255, 
                        verbose_name="Nom de jeune fille", 
                        blank=True, null=True)

    # identification avancée personne
    nationalite = models.ForeignKey(Pays, verbose_name="Nationalité", 
                        blank=True, null=True)
    naissance_ville = models.CharField(max_length=255, 
                        verbose_name="Ville de naissance", 
                        blank=True, null=True)
    naissance_date = models.DateField(max_length=255, 
                        verbose_name="Date de naissance", 
                        blank=True, null=True)
    naissance_pays = models.ForeignKey(Pays, related_name="naissance_pays", 
                        verbose_name="Pays de naissance", 
                        blank=True, null=True)

    # coordonnées
    pays = models.ForeignKey(Pays, related_name="pays", 
                        verbose_name="Pays de résidence", 
                        blank=True, null=True)
    adresse = models.CharField(max_length=255, verbose_name="Adresse", 
                        blank=True, null=True)
    code_postal = models.CharField(max_length=255, verbose_name="Code postal", 
                        blank=True, null=True)
    ville = models.CharField(max_length=255, verbose_name="Ville", 
                        blank=True, null=True)
    region = models.CharField(max_length=255, verbose_name="Région", 
                        blank=True, null=True)
    telephone_perso = models.CharField(max_length=255, 
                        verbose_name="Téléphone personnel", 
                        blank=True, null=True)
    fax_perso = models.CharField(max_length=255, verbose_name="FAX personnel", 
                        blank=True, null=True)
    courriel_perso = models.CharField(max_length=255, 
                        verbose_name="Courriel personnel", 
                        blank=True, null=True)
    telephone_pro = models.CharField(max_length=255, 
                        verbose_name="Téléphone professionnel", 
                        blank=True, null=True)
    fax_pro = models.CharField(max_length=255, 
                        verbose_name="FAX professionnel", 
                        blank=True, null=True)
    courriel_pro = models.CharField(max_length=255, 
                        verbose_name="Courriel professionnel", 
                        blank=True, null=True)

    # renseignements divers
    sexe = models.CharField(max_length=1, verbose_name="Genre", 
                        blank=True, null=True)
    civilite = models.CharField(max_length=2, verbose_name="Civilité", 
                        choices=CIVILITE,
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
    annees = models.CharField(max_length=2, 
                        verbose_name="Nombre d'années universitaires", )
    nom = models.CharField(max_length=255, verbose_name="nom",)

class Note(models.Model):
    """
    Une personne attribue une note à un dossier de candidature.
    """
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)
    note = models.IntegerField(choices=NOTES)

class Commentaire(models.Model):
    """
    Une personne peut ajouter un commentaire à un dossier de candidature.
    """
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)
    texte = models.TextField(verbose_name="Texte")

class Dossier(DossierWorkflow, models.Model):
    """
    Informations générales du dossier de candidature.
    """
    appel = models.ForeignKey(Appel, related_name="appel",
                        verbose_name="Appel")
    candidat = models.ForeignKey(Candidat, related_name="candidat", 
                        verbose_name="Candidat")
    candidat_statut = models.CharField(max_length=255,
                        verbose_name="Statut du candidat",  
                        choices=CANDIDAT_STATUT, blank=True, null=True)
    candidat_fonction = models.CharField(max_length=255, 
                        verbose_name="Fonction", blank=True, null=True)

    # Utilisé lors des appels internationaux pour définir le bureau (région) de traitement
    # Cette valeur était dérivée de dossier.etablissement (normalement équivalent de dossier.origine.etablissement)
    # Maintenant, on spécifie la valeur avec la région où est fait l'appel
    bureau_rattachement = models.ForeignKey(Bureau, 
                        verbose_name="Bureau de rattachement", 
                        blank=True, null=True)

    # Tentative pour récupérer de l'information passée
    dernier_projet_description = models.TextField(
                        verbose_name="Description du dernier projet \
                            ou programme", 
                        blank=True, null=True)
    dernier_projet_annee = models.CharField(max_length=4, 
                        verbose_name="Année du dernier projet ou programme", 
                        blank=True, null=True)
    derniere_bourse_categorie = models.ForeignKey(CategorieBourse, 
                        related_name="bourse_categorie", 
                        verbose_name="Catégorie de la dernière bourse", 
                        blank=True, null=True)
    derniere_bourse_annee = models.CharField(max_length=4, 
                        verbose_name="Année de la dernière bourse", 
                        blank=True, null=True)

    # Évaluations (à terminer // expert classements)
    notes = models.ManyToManyField(Note, verbose_name="Notes", 
                        blank=True, null=True)
    annotations = models.ManyToManyField(Commentaire, 
                        verbose_name="Commentaires", blank=True, null=True)
    moyenne_votes = models.FloatField(verbose_name="Moyenne des évaluateurs", 
                        blank=True, null=True)
    moyenne_academique = models.FloatField(verbose_name="Moyenne académique", 
                        blank=True, null=True)
    opportunite_regionale = models.CharField(max_length=255, 
                        verbose_name="Opportunité régionale", 
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
    
    def __unicode__(self, ):
        return u"dossier #%s (%s pour l'appel %s)" % (self.id, 
                            self.candidat, self.appel)

    def calculer_moyenne(self,):
        if self.id:
            notes = [note.note for note in self.notes.all()]
            if len(notes) > 0:
                self.moyenne_votes = float(sum(notes)) / len(notes)
            else:
                self.moyenne_votes = 0

    def save(self, *args, **kwargs):
        self.calculer_moyenne()
        super(Dossier, self).save(*args, **kwargs)

class DossierFaculte(models.Model):
    dossier = models.ForeignKey(Dossier, verbose_name="Dossier",)

    # Etablissement connu de l'AUF
    etablissement = models.ForeignKey(Etablissement, 
                        verbose_name="Établissement", 
                        blank=True, null=True)

    # Autre établissement
    autre_etablissement_nom = models.CharField(max_length=255, 
                        verbose_name="Autre établissement", 
                        blank=True, null=True)
    autre_etablissement_pays = models.ForeignKey(Pays, 
                        verbose_name="Pays", blank=True, null=True)
    autre_etablissement_adresse = models.CharField(max_length=255, 
                        verbose_name="Adresse", blank=True, null=True)
    autre_etablissement_code_postal = models.CharField(max_length=255, 
                        verbose_name="Code poste", blank=True, null=True)
    autre_etablissement_ville = models.CharField(max_length=255, 
                        verbose_name="Ville", blank=True, null=True)
    autre_etablissement_region = models.CharField(max_length=255, 
                        verbose_name="Région", blank=True, null=True)
    autre_etablissement_valide = models.NullBooleanField(
                        verbose_name="Erreur recevabilité établissement", 
                        blank=True, null=True)
    autre_etablissement_erreur = models.CharField(max_length=255, 
                        verbose_name="Commentaire sur la recevabilité", 
                        blank=True, null=True)

    # responsable institutionnel (Directeur de thèse)
    resp_inst_civilite = models.CharField(max_length=2, 
                        verbose_name="Civilité responsable institutionnel", 
                        choices=CIVILITE, blank=True, null=True)
    resp_inst_nom = models.CharField(max_length=255, 
                        verbose_name="Nom du responsable institutionnel", 
                        blank=True, null=True)
    resp_inst_prenom = models.CharField(max_length=255, 
                        verbose_name="Prénom du responsable institutionnel", 
                        blank=True, null=True)
    resp_inst_fonction = models.CharField(max_length=255, 
                        verbose_name="Fonction du responsable institutionnel", 
                        blank=True, null=True)
    resp_inst_courriel = models.CharField(max_length=255, 
                        verbose_name="Courriel du responsable institutionnel", 
                        blank=True, null=True)
    resp_inst_telephone = models.CharField(max_length=255, 
                        verbose_name="Téléphone du responsable institutionnel", 
                        blank=True, null=True)
    resp_inst_fax = models.CharField(max_length=255, 
                        verbose_name="FAX du responsable institutionnel", 
                        blank=True, null=True)

    # responsable scientifique (Accord scientifique)
    resp_sc_civilite = models.CharField(max_length=2, 
                        verbose_name="Civilité responsable scientifique", 
                        choices=CIVILITE, blank=True, null=True)
    resp_sc_nom = models.CharField(max_length=255, 
                        verbose_name="Nom du responsable scientifique", 
                        blank=True, null=True)
    resp_sc_prenom = models.CharField(max_length=255, 
                        verbose_name="Prénom du responsable scientifique", 
                        blank=True, null=True)
    resp_sc_fonction = models.CharField(max_length=255, 
                        verbose_name="Fonction du responsable scientifique", 
                        blank=True, null=True)
    resp_sc_courriel = models.CharField(max_length=255, 
                        verbose_name="Courriel du responsable scientifique", 
                        blank=True, null=True)
    resp_sc_telephone = models.CharField(max_length=255, 
                        verbose_name="Téléphone du responsable scientifique", 
                        blank=True, null=True)
    resp_sc_fax = models.CharField(max_length=255, 
                        verbose_name="FAX du responsable scientifique", 
                        blank=True, null=True)

    # faculté, département ou labo (Accord scientifique)
    faculte_url = models.CharField(max_length=255, 
                        verbose_name="URL de la faculté", 
                        blank=True, null=True)
    faculte_nom = models.CharField(max_length=255, 
                        verbose_name="Nom de la faculté", 
                        blank=True, null=True)
    faculte_adresse = models.CharField(max_length=255, 
                        verbose_name="Adresse de la faculté", 
                        blank=True, null=True)
    faculte_code_postal = models.CharField(max_length=255, 
                        verbose_name="Code postal de la faculté", 
                        blank=True, null=True)
    faculte_ville = models.CharField(max_length=255, 
                        verbose_name="Ville de la faculté", 
                        blank=True, null=True)
    faculte_courriel = models.CharField(max_length=255, 
                        verbose_name="Courriel de la faculté", 
                        blank=True, null=True)
    faculte_telephone = models.CharField(max_length=255, 
                        verbose_name="Téléphone de la faculté", 
                        blank=True, null=True)
    faculte_fax = models.CharField(max_length=255, 
                        verbose_name="FAX de la faculté", 
                        blank=True, null=True)
    
    class Meta:
        abstract = True

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


class Public(models.Model):
    """
    """
    nom = models.CharField(max_length=255, verbose_name="Nom")

class Intervention(models.Model):
    """
    """
    nom = models.CharField(max_length=255, verbose_name="Nom")

class DossierMobilite(models.Model):
    """Informations sur la mobilité demandée par le candidat.
    """
    dossier = models.OneToOneField(Dossier, verbose_name="Dossier", related_name="mobilite")

    # Période de mobilité
    date_debut = models.DateField(verbose_name="Date de début souhaitée", 
                        blank=True, null=True)
    date_fin = models.DateField(verbose_name="Date de fin souhaitée", 
                        blank=True, null=True)
    duree = models.CharField(max_length=255, 
                        verbose_name="Durée totale mobilité souhaitée (mois)", 
                        blank=True, null=True)

    # Dossier scientifique
    intitule_projet = models.CharField(max_length=255, 
                        verbose_name="Intitulé du projet", 
                        blank=True, null=True)
    mots_clefs = models.CharField(max_length=255, 
                        verbose_name="Mots clefs", blank=True, null=True)

    # Formation en cours
    formation_en_cours_diplome = models.CharField(max_length=255, 
                        verbose_name="Intitulé du diplôme", 
                        blank=True, null=True)
    formation_en_cours_niveau = models.ForeignKey(NiveauEtude, 
                        related_name="formation_en_cours_niveau", 
                        verbose_name="Niveau d'étude", blank=True, null=True)

    # Programme de mission
    type_intervention = models.ForeignKey(Intervention, 
                        verbose_name="Type d'intervention", 
                        blank=True, null=True)
    public_vise = models.ForeignKey(Public, verbose_name="Public visé", 
                        blank=True, null=True)
    autres_publics = models.CharField(max_length=255, 
                        verbose_name="Autres publics", blank=True, null=True)

    # Disciplines
    discipline = models.ForeignKey(Discipline, verbose_name="Discipline", 
                        blank=True, null=True)
    sous_discipline = models.CharField(max_length=255, blank=True, null=True)

    # Alternance
    alternance_nb_mois_origine = models.IntegerField(
                        verbose_name="Nombre de mois à l'origine", 
                        blank=True, null=True)
    alternance_nb_mois_accueil = models.IntegerField(
                        verbose_name="Nombre de mois à l'accueil", 
                        blank=True, null=True)
    alternance_accueil_puis_origine = models.NullBooleanField(
                        verbose_name="Mobilité commençée à l'accueil?", 
                        blank=True, null=True)

    # Diplôme demandé
    diplome_demande_nom = models.CharField(max_length=255, 
                        verbose_name="Diplôme demandé", blank=True, null=True)
    diplome_demande_niveau = models.ForeignKey(NiveauEtude, 
                        related_name="diplome_demande_niveau", 
                        verbose_name="Niveau d'étude", blank=True, null=True)
    
    # Thèse
    these_date_inscription = models.DateField(
                        verbose_name="Date d'inscription", 
                        blank=True, null=True)
    these_date_obtention_prevue = models.DateField(
                        verbose_name="Date d'obtention prévue", 
                        blank=True, null=True)
    these_soutenance_pays = models.ForeignKey(Pays, 
                        related_name="soutenance_pays", 
                        verbose_name="Pays de soutenance", 
                        blank=True, null=True)
    these_soutenance_date = models.DateField(
                        verbose_name="Date de soutenance", 
                        blank=True, null=True)
    these_type = models.CharField(max_length=2, 
                        verbose_name="Type de thèse", 
                        choices=TYPE_THESE, blank=True, null=True)
    these_type_autre = models.CharField(max_length=255, 
                        verbose_name="Autre type de thèse", 
                        blank=True, null=True)

    # directeur thèse accueil
    dir_acc_civilite = models.CharField(max_length=2, 
                        verbose_name="Civilité", choices=CIVILITE, 
                        blank=True, null=True)
    dir_acc_nom = models.CharField(max_length=255, 
                        verbose_name="Nom", blank=True, null=True)
    dir_acc_prenom = models.CharField(max_length=255, 
                        verbose_name="Prénom", blank=True, null=True)

    # directeur thèse origine
    dir_ori_civilite = models.CharField(max_length=2, verbose_name="Civilité", 
                        choices=CIVILITE, blank=True, null=True)
    dir_ori_nom = models.CharField(max_length=255, verbose_name="Nom", 
                        blank=True, null=True)
    dir_ori_prenom = models.CharField(max_length=255, verbose_name="Prénom", 
                        blank=True, null=True)

class Diplome(models.Model):
    """
    """
    dossier = models.ForeignKey(Dossier)
    nom = models.CharField(max_length=255, verbose_name="Nom", 
                        blank=True, null=True)
    date = models.DateField(max_length=255, verbose_name="Date", 
                        blank=True, null=True)
    niveau = models.ForeignKey(NiveauEtude, related_name="niveau", 
                        verbose_name="Niveau d'étude", 
                        blank=True, null=True)
    etablissement_nom = models.CharField(max_length=255, 
                        verbose_name="Nom de l'établissement", 
                        blank=True, null=True)
    etablissement_pays = models.ForeignKey(Pays, 
                        related_name="etablissement_pays", 
                        verbose_name="Pays de l'établissement", 
                        blank=True, null=True)


class TypePiece(models.Model):
    pass

    class Meta:
        verbose_name = "Type de pièce"


class Piece(models.Model):
    dossier = models.ForeignKey(Dossier)
    type = models.ForeignKey(TypePiece)
    conforme = models.NullBooleanField(verbose_name="Conforme?", 
                        blank=True, null=True)

    class Meta:
        verbose_name = "Pièce"
