# -*- encoding: utf-8 -*-

from django import forms
from default_mapping import *
from project.sigma import models as sigma
from project.wcs import forms as wcs

#class Dossier(wcs.DossierForm):
#    pass   
#
#class Candidat(wcs.CandidatForm):
#    pass

MAPPING.update({

    # Module : wcs specifique
    'telephone_2' : ('Dossier', 'telephone') ,
    #'nom_de_jeune_fille' : ('', '') ,
    #'pays_de_soutenance_prevu' : ('', '') ,
    #'si_oui_precisez_le_type_de_bourse_obtenue' : ('', '') ,
    #'nom_de_l_etablissement_d_obtention' : ('', '') ,
    #'adresse_electronique_du_responsable_2' : ('', '') ,
    #'cocher_la_case_ci_dessous_obligatoire' : ('', '') ,
    #'pays' : ('', '') ,
    #'date_de_soutenance_prevue' : ('', '') ,
    #'num_dossier' : ('', '') ,
    #'wcs_status' : ('', '') ,
    #'prenom_du_directeur_de_these' : ('', '') ,
    #'niveau_d_etudes_nombre_d_annees_universitaires' : ('', '') ,
    #'niveau_d_etudes_en_nombre_d_annees_universitaires' : ('', '') ,
    #'telephone_personnel' : ('', '') ,
    #'date_de_fin' : ('', '') ,
    #'prenom_2' : ('Candidat', 'prenom') ,
    #'municipalite_ville_2' : ('', '') ,
    #'intitule_du_diplome_actuellement_prepare' : ('', '') ,
    #'intitule_du_dernier_diplome_obtenu' : ('', '') ,
    #'pays_de_naissance' : ('', '') ,
    #'wcs_workflow_status' : ('', '') ,
    #'discipline' : ('', '') ,
    #'mot_cle_2' : ('', '') ,
    #'mot_cle_1' : ('', '') ,
    #'municipalite_ville_3' : ('', '') ,
    #'situation_universitaire' : ('', '') ,
    #'si_autre_diplome_precisez' : ('', '') ,
    #'nom_du_directeur_de_these_accueil' : ('', '') ,
    #'civilite' : ('', '') ,
    #'fonction_2' : ('', '') ,
    #'faculte_departement_ou_laboratoire_2' : ('', '') ,
    #'civilite_du_directeur_de_these_accueil' : ('', '') ,
    #'prenom_du_responsable' : ('', '') ,
    #'wcs_user_display_name' : ('', '') ,
    #'intitule_du_sujet_de_these' : ('', '') ,
    #'prenom_du_directeur_de_these_2' : ('', '') ,
    #'adresse_de_correspondance_adresse_postale' : ('', '') ,
    #'etablissement_d_origine_membre_de_l_auf' : ('', '') ,
    'nom' : ('Candidat', 'nom') ,
    #'curriculum_vitae' : ('Piece', 'cv') ,
    #'type_de_these' : ('', '') ,
    #'civilite_du_responsable' : ('', '') ,
    #'nombre_de_mois_a_l_accueil' : ('', '') ,
    #'date_d_obtention' : ('', '') ,
    #'municipalite_ville' : ('', '') ,
    #'date_de_1ere_inscription_en_these' : ('', '') ,
    #'fonction' : ('', '') ,
    #'nom_du_directeur_de_these_origine' : ('', '') ,
    #'date_de_debut' : ('', '') ,
    #'precisez_l_annee' : ('', '') ,
    #'ville_de_naissance' : ('', '') ,
    #'si_oui_precisez_le_dernier_auquel_vous_avez_participe' : ('', '') ,
    #'adresse_electronique_du_directeur_de_these_accueil' : ('', '') ,
    #'pays_de_l_etablissement' : ('', '') ,
    #'faculte_departement_ou_laboratoire' : ('', '') ,
    #'region_province_etat' : ('', '') ,
    #'civilite_du_directeur_de_these_origine' : ('', '') ,
    #'adresse_electronique' : ('', '') ,
    #'civilite_du_responsable_2' : ('', '') ,
    #'prenom_du_responsable_2' : ('', '') ,
    #'code_postal' : ('', '') ,
    'prenom' : ('Candidat', 'prenom') ,
    #'precisez_l_annee_2' : ('', '') ,
    #'date_de_naissance' : ('', '') ,
    #'telephone_professionnel' : ('', '') ,
    #'nom_du_responsable' : ('', '') ,
    #'adresse_electronique_du_responsable' : ('', '') ,
    #'wcs_comments' : ('', '') ,
    #'mot_cle_3' : ('', '') ,
    #'titre_et_fonction_actuels' : ('', '') ,
    #'adresse_electronique_du_directeur_de_these_origine' : ('', '') ,
    #'avez_vous_deja_participe_a_un_programme_de_l_auf' : ('', '') ,
    #'etablissement_d_accueil' : ('', '') ,
    #'nom_du_candidat' : ('', '') ,
    #'pays_de_nationalite' : ('', '') ,
    #'telephone' : ('', '') ,
    #'nom_du_responsable_2' : ('', '') ,
    'descriptif_detaille_du_sujet_de_these' : ('Piece', 'these') ,
    #'avez_vous_deja_beneficie_d_une_bourse_de_l_auf' : ('', '') ,
    #'protocole_de_recherche' : ('', '') ,
    #'wcs_user_email' : ('', '') ,
    

    # Module : surcharge defaut
    

})
