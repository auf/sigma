# encoding: utf-8

from project.wcs.forms import *

MAPPING = {

    # Identification

    'civilite': ('Candidat', 'civilite'),
    'nom': ('Candidat', 'nom'),
    'prenom': ('Candidat', 'prenom'),
    'pays_de_nationalite': ('Candidat', 'nationalite'),
    'date_de_naissance': ('Candidat', 'naissance_date'),

    # Adresse de correspondance

    'adresse_de_correspondance_adresse_postale': ('Candidat', 'adresse'),
    'municipalite_ville': ('Candidat', 'ville'),
    'departement': ('Candidat', 'region'),
    'code_postal': ('Candidat', 'code_postal'),
    'pays': ('Candidat', 'pays'),
    'telephone_personnel_fixe_ou_gsm': ('Candidat', 'telephone'),
    'adresse_electronique': ('Candidat', 'courriel'),

    # Établissement d'origine

    'etablissement_d_origine_membre_de_l_auf': (
        'DossierOrigine', 'etablissement'
    ),
    'faculte': ('DossierOrigine', 'faculte_nom'),
    # 'departement_ou_laboratoire'
    'annee_d_etudes_en_cours': (
        'DossierMobilite', 'formation_en_cours_niveau'
    ),
    'diplome_en_cours_d_obtention': (
        'DossierMobilite', 'formation_en_cours_diplome'
    ),
    'discipline': ('DossierMobilite', 'discipline'),

    # Lien avec l'AUF ou autres

    # 'avez_vous_deja_beneficie_d_une_bourse_de_l_auf'
    'si_oui_precisez_le_type_de_bourse_obtenue': (
        'Dossier', 'derniere_bourse_categorie'
    ),
    'precisez_l_annee': ('Dossier', 'derniere_bourse_annee'),
    # 'etes_vous_actuellement_boursier_ou_avez_vous_deja_obtenu_une_bourse...'
    # 'si_oui_precisez_l_annee'
    # 'et_l_organisme'

    # Identification de la structure d'accueil

    'nom_2': ('DossierAccueil', 'autre_etablissement_nom'),
    'adresse_adresse_postale': (
        'DossierAccueil', 'autre_etablissement_adresse'
    ),
    'municipalite_ville_2': ('DossierAccueil', 'autre_etablissement_ville'),
    'region_province_etat': ('DossierAccueil', 'autre_etablissement_region'),
    'code_postal_2': ('DossierAccueil', 'autre_etablissement_code_postal'),
    'pays_2': ('DossierAccueil', 'autre_etablissement_pays'),
    # 'telephone'
    # 'urldu_site_de_la_structure_d_accueil'

    # Identification du responsable du stagiaire dans la structure d'accueil

    'civilite_du_responsable': ('DossierAccueil', 'resp_sc_civilite'),
    'nom_du_responsable': ('DossierAccueil', 'resp_sc_nom'),
    'prenom_du_responsable': ('DossierAccueil', 'resp_sc_prenom'),
    'fonction': ('DossierAccueil', 'resp_sc_fonction'),
    'unite_administrative': ('DossierAccueil', 'faculte_nom'),
    'adresse': ('DossierAccueil', 'faculte_adresse'),
    'municipalite_ville_3': ('DossierAccueil', 'faculte_ville'),
    'code_postal_3': ('DossierAccueil', 'faculte_code_postal'),
    # 'pays_3'
    'telephone_2': ('DossierAccueil', 'resp_sc_telephone'),
    'adresse_eletronique_du_responsable': (
        'DossierAccueil', 'resp_sc_courriel'
    ),

    # Durée du stage

    'date_de_debut': ('DossierMobilite', 'date_debut_accueil'),
    'date_de_fin': ('DossierMobilite', 'date_fin_accueil'),
    # 'nombre_de_mois_souhaite'

    # Pièces

    'lettre_de_motivation': ('Piece', 'Lettre de motivation'),
    'curriculum_vitae': ('Piece', 'Curriculum vitae'),
    'descriptif_detaille_du_projet_professionnel_integre_dans'
    '_l_activite_les_projets_de_la_structure_d_accueil': (
        'Piece', 'Descriptif du projet professionnel'
    ),
    'copie_du_dossier_de_scolarite_universitaire': (
        'Piece', 'Copie du dossier de scolarité universitaire'
    ),
    'attestation_d_inscription_a_l_universite_pour_l_annee_en_cours': (
        'Piece', "Attestation d'inscription à l'université"
    ),
    'attestation_d_accord_motive_de_l_etablissement_d_origine'
    '_delivree_signee_et_cachetee_par_le_responsable_scientifique_direct'
    '_et_par_le_doyen': (
        'Piece', "Attestation d'accord"
    ),
    'attestation_d_accueil_du_responsable_du_projet_de_stage'
    '_dans_l_etablissement_d_accueil': (
        'Piece', "Attestation d'accueil"
    ),
    'le_document_faisant_preuve_de_competence_linguistique'
    '_en_francais_le_cas_echeant': (
        'Piece', "Preve de compétence linguistique"
    ),

}
