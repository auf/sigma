# -*- encoding: utf-8 -*-

from project.wcs.forms import *
from project.sigma import models as sigma

MAPPING = {

    # Identification
    'sigma_civilite': ('Candidat', 'civilite'),
    'sigma_prenom': ('Candidat', 'prenom'),
    'sigma_nom': ('Candidat', 'nom'),
    'sigma_nom_jeune_fille': ('Candidat', 'nom_jeune_fille'),
    'sigma_nationalite': ('Candidat', 'nationalite'),
    'sigma_date_naissance': ('Candidat', 'naissance_date'),

    # Coordonnées
    'sigma_adresse_complement': ('Candidat', 'adresse_complement'),
    'sigma_ville': ('Candidat', 'ville'),
    'sigma_code_postal': ('Candidat', 'code_postal'),
    'sigma_region': ('Candidat', 'region'),
    'sigma_pays': ('Candidat', 'pays'),
    'sigma_telephone_fixe': ('Candidat', 'telephone'),
    'sigma_telephone_portable': ('Candidat', 'telephone_portable'),
    'sigma_courriel': ('Candidat', 'courriel'),
    
    # Situation universitaire
    'sigma_statut_candidat': ('Dossier', 'candidat_statut'),
    'sigma_fonction': ('Dossier', 'candidat_fonction'),

    # Diplôme
    'sigma_diplome': ('Diplome', 'nom'),
    'sigma_diplome_date': ('Diplome', 'date'),
    'sigma_diplome_niveau': ('Diplome', 'niveau'),
    'sigma_diplome_etablissement': ('Diplome', 'etablissement'),
    'sigma_diplome_autre_etablissement': ('Diplome', 'autre_etablissement_nom'),
    'sigma_diplome_autre_etablissement_pays': ('Diplome', 'autre_etablissement_pays'),

    # Origine
    'sigma_origine_etablissement': ('DossierOrigine', 'etablissement'),
    'sigma_origine_autre_etablissement_adresse': ('DossierOrigine', 'autre_etablissement_adresse'),
    'sigma_origine_autre_etablissement_ville': ('DossierOrigine', 'autre_etablissement_ville'),
    'sigma_origine_autre_etablissement_code_postal': ('DossierOrigine', 'autre_etablissement_code_postal'),
    'sigma_origine_autre_etablissement_region': ('DossierOrigine', 'autre_etablissement_region'),
    'sigma_origine_autre_etablissement_pays': ('DossierOrigine', 'autre_etablissement_pays'),

    # Origine - Responsable insitutionnel
    'sigma_origine_responsable_institutionnel_civilite': ('DossierOrigine', 'resp_inst_civilite'),
    'sigma_origine_responsable_institutionnel_prenom': ('DossierOrigine', 'resp_inst_prenom'),
    'sigma_origine_responsable_institutionnel_nom': ('DossierOrigine', 'resp_inst_nom'),
    'sigma_origine_responsable_institutionnel_courriel': ('DossierOrigine', 'resp_inst_courriel'),
    'sigma_origine_responsable_institutionnel_fonction': ('DossierOrigine', 'resp_inst_fonction'),
    'sigma_origine_responsable_institutionnel_telephone': ('DossierOrigine', 'resp_inst_telephone'),
    'sigma_origine_responsable_institutionnel_fax': ('DossierOrigine', 'resp_inst_fax'),

    # Origine - Responsable scientifique
    'sigma_origine_responsable_scientifique_civilite': ('DossierOrigine', 'resp_sc_civilite'),
    'sigma_origine_responsable_scientifique_prenom': ('DossierOrigine', 'resp_sc_prenom'),
    'sigma_origine_responsable_scientifique_nom': ('DossierOrigine', 'resp_sc_nom'),
    'sigma_origine_responsable_scientifique_courriel': ('DossierOrigine', 'resp_sc_courriel'),
    'sigma_origine_responsable_scientifique_fonction': ('DossierOrigine', 'resp_sc_fonction'),
    'sigma_origine_responsable_scientifique_telephone': ('DossierOrigine', 'resp_sc_telephone'),
    'sigma_origine_responsable_scientifique_fax': ('DossierOrigine', 'resp_sc_fax'),

    # Origine - faculté
    'sigma_origine_faculte': ('DossierOrigine', 'faculte_nom'),
    'sigma_origine_faculte_adresse': ('DossierOrigine', 'faculte_adresse'),
    'sigma_origine_faculte_ville': ('DossierOrigine', 'faculte_ville'),
    'sigma_origine_faculte_code_postal': ('DossierOrigine', 'faculte_code_postal'),

    # Directeur de thèse - Origine
    'sigma_directeur_origine_civilite': ('DossierOrigine', 'dir_civilite'),
    'sigma_directeur_origine_prenom': ('DossierOrigine', 'dir_prenom'),
    'sigma_directeur_origine_nom': ('DossierOrigine', 'dir_nom'),
    'sigma_directeur_origine_courriel': ('DossierOrigine', 'dir_courriel'),
    'sigma_directeur_origine_telephone': ('DossierOrigine', 'dir_telephone'),

    # Accueil
    'sigma_accueil_etablissement': ('DossierAccueil', 'etablissement'),
    'sigma_accueil_autre_etablissement_adresse': ('DossierAccueil', 'autre_etablissement_adresse'),
    'sigma_accueil_autre_etablissement_ville': ('DossierAccueil', 'autre_etablissement_ville'),
    'sigma_accueil_autre_etablissement_code_postal': ('DossierAccueil', 'autre_etablissement_code_postal'),
    'sigma_accueil_autre_etablissement_region': ('DossierAccueil', 'autre_etablissement_region'),
    'sigma_accueil_autre_etablissement_pays': ('DossierAccueil', 'autre_etablissement_pays'),

    # Accueil - responsable scientifique
    'sigma_accueil_responsable_scientifique_civilite': ('DossierAccueil', 'resp_sc_civilite'),
    'sigma_accueil_responsable_scientifique_prenom': ('DossierAccueil', 'resp_sc_prenom'),
    'sigma_accueil_responsable_scientifique_nom': ('DossierAccueil', 'resp_sc_nom'),
    'sigma_accueil_responsable_scientifique_courriel': ('DossierAccueil', 'resp_sc_courriel'),
    'sigma_accueil_responsable_scientifique_fonction': ('DossierAccueil', 'resp_sc_fonction'),
    'sigma_accueil_responsable_scientifique_telephone': ('DossierAccueil', 'resp_sc_telephone'),
    'sigma_accueil_responsable_scientifique_fax': ('DossierAccueil', 'resp_sc_fax'),

    # Accueil - faculté
    'sigma_accueil_faculte': ('DossierAccueil', 'faculte_nom'),
    'sigma_accueil_faculte_adresse': ('DossierAccueil', 'faculte_adresse'),
    'sigma_accueil_faculte_ville': ('DossierAccueil', 'faculte_ville'),
    'sigma_accueil_faculte_code_postal': ('DossierAccueil', 'faculte_code_postal'),

    # Directeur de thèse - Accueil
    'sigma_directeur_accueil_civilite': ('DossierAccueil', 'dir_civilite'),
    'sigma_directeur_accueil_prenom': ('DossierAccueil', 'dir_prenom'),
    'sigma_directeur_accueil_nom': ('DossierAccueil', 'dir_nom'),
    'sigma_directeur_accueil_courriel': ('DossierAccueil', 'dir_courriel'),
    'sigma_directeur_accueil_telephone': ('DossierAccueil', 'dir_telephone'),

    # Période de mobilité
    'sigma_date_debut': ('DossierMobilite', 'date_debut'),
    'sigma_date_fin': ('DossierMobilite', 'date_fin'),
    'sigma_duree': ('DossierMobilite', 'duree'),

    # Dossier scientifique
    'sigma_intitule_projet': ('DossierMobilite', 'intitule_projet'),
    'sigma_mots_clefs': ('DossierMobilite', 'mots_clefs'),

    # Formation en cours
    'sigma_formation_en_cours_diplome': ('DossierMobilite', 'formation_en_cours_diplome'),
    'sigma_formation_en_cours_niveau': ('DossierMobilite', 'formation_en_cours_niveau'),

    # Programme de mission
    'sigma_type_intervention': ('DossierMobilite', 'type_intervention'),
    'sigma_public_vise': ('DossierMobilite', 'public_vise'),
    'sigma_autres_publics': ('DossierMobilite', 'autres_publics'),

    # Disciplines
    'sigma_discipline': ('DossierMobilite', 'discipline'),
    'sigma_sous_discipline': ('DossierMobilite', 'sous_discipline'),

    # Alternance
    'sigma_nb_mois_origine': ('DossierMobilite', 'alternance_nb_mois_origine'),
    'sigma_nb_mois_accueil': ('DossierMobilite', 'alternance_nb_mois_accueil'),
    'sigma_debut_accueil': ('DossierMobilite', 'alternance_accueil_puis_origine'),
 
    # Diplôme demandé
    'sigma_diplome_demande': ('DossierMobilite', 'diplome_demande_nom'),
    'sigma_diplome_demande_niveau': ('DossierMobilite', 'diplome_demande_niveau'),

    # Thèse
    'sigma_these_date_inscription': ('DossierMobilite', 'these_date_inscription'),
    'sigma_these_pays_soutenance': ('DossierMobilite', 'these_soutenance_pays'),
    'sigma_these_date_soutenance': ('DossierMobilite', 'these_soutenance_date'),
    'sigma_these_type': ('DossierMobilite', 'these_type'),

    # Lien avec l'AUF
    'sigma_dernier_projet_description': ('Dossier', 'dernier_projet_description'),
    'sigma_dernier_projet_annee': ('Dossier', 'dernier_projet_annee'),
    # 'sigma_derniere_bourse_categorie': ('Dossier', 'derniere_bourse_categorie'),
    'sigma_derniere_bourse_annee': ('Dossier', 'derniere_bourse_annee'),

}

for type_piece in sigma.TypePiece.objects.all():
    k = "sigma_piece_%s" % (type_piece.nom)
    MAPPING[k] = ('Piece', type_piece.nom)
