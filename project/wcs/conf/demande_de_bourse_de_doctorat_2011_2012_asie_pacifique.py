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
    #'pays_de_soutenance_prevu' : ('', '') ,
    #'nom_de_l_etablissement_d_obtention' : ('', '') ,
    #'cocher_la_case_ci_dessous_obligatoire' : ('', '') ,
    #'civilite_du_responsable_2' : ('', '') ,
    #'si_oui_precisez_le_type_de_bourse_obtenue' : ('', '') ,
    #'avez_vous_deja_beneficie_d_une_bourse_de_l_auf' : ('', '') ,
    #'discipline' : ('', '') ,
    #'pays_de_l_etablissement' : ('', '') ,
    #'faculte_departement_ou_laboratoire_2' : ('', '') ,
    #'civilite_du_directeur_de_these_accueil' : ('', '') ,
    #'etablissement_d_origine_membre_de_l_auf' : ('', '') ,
    #'nom' : ('', '') ,
    #'nombre_de_mois_a_l_accueil' : ('', '') ,
    #'ville_de_naissance' : ('', '') ,
    #'attestation_d_accord_du_directeur_de_these_a_l_origine' : ('', '') ,
    #'region_province_etat' : ('', '') ,
    #'adresse_electronique' : ('', '') ,
    #'date_de_1ere_inscription_en_these' : ('', '') ,
    #'code_postal' : ('', '') ,
    #'telephone_professionnel' : ('', '') ,
    #'titre_et_fonction_actuels' : ('', '') ,
    'nom_du_candidat' : ('Candidat', 'nom') ,
    #'curriculum_vitae' : ('', '') ,
    #'intitule_du_diplome_actuellement_prepare_ou_poste_occupe' : ('', '') ,
    #'nom_du_directeur_de_these_origine' : ('', '') ,
    #'niveau_d_etudes_en_nombre_d_annees_universitaires' : ('', '') ,
    #'type_de_these' : ('', '') ,
    #'intitule_du_dernier_diplome_obtenu' : ('', '') ,
    #'fonction' : ('', '') ,
    #'situation_universitaire' : ('', '') ,
    #'fonction_2' : ('', '') ,
    #'intitule_du_sujet_de_these' : ('', '') ,
    #'si_autre_diplome_ou_titre_du_poste_occupe_precisez' : ('', '') ,
    #'prenom_du_directeur_de_these_2' : ('', '') ,
    #'adresse_de_correspondance_adresse_postale' : ('', '') ,
    #'adresse_electronique_du_responsable_2' : ('', '') ,
    #'civilite_du_responsable' : ('', '') ,
    #'date_d_obtention' : ('', '') ,
    #'date_de_fin_2' : ('', '') ,
    #'prenom' : ('', '') ,
    'nom_du_responsable' : ('Candidat', 'prenom') ,
    #'descriptif_detaille_du_sujet_de_these' : ('', '') ,
    #'nom_de_jeune_fille' : ('', '') ,
    'pays' : ('Candidat', 'pays') ,
    #'prenom_du_directeur_de_these' : ('', '') ,
    #'niveau_d_etudes_nombre_d_annees_universitaires' : ('', '') ,
    #'telephone_personnel' : ('', '') ,
    #'date_de_fin' : ('', '') ,
    #'prenom_2' : ('', '') ,
    #'precisez_l_annee_2' : ('', '') ,
    #'avez_vous_deja_participe_a_un_programme_de_l_auf' : ('', '') ,
    #'wcs_workflow_status' : ('', '') ,
    #'mot_cle_3' : ('', '') ,
    #'mot_cle_2' : ('', '') ,
    #'mot_cle_1' : ('', '') ,
    #'date_de_debut_2' : ('', '') ,
    #'prenom_du_responsable' : ('', '') ,
    #'telephone' : ('', '') ,
    #'date_de_debut' : ('', '') ,
    #'civilite_du_directeur_de_these_origine' : ('', '') ,
    #'prenom_du_responsable_2' : ('', '') ,
    #'date_de_naissance' : ('', '') ,
    #'wcs_comments' : ('', '') ,
    #'precisez_l_annee' : ('', '') ,
    #'civilite' : ('', '') ,
    #'etablissement_d_accueil_membre_de_l_auf' : ('', '') ,
    #'nom_du_responsable_2' : ('', '') ,
    #'protocole_de_recherche' : ('', '') ,
    #'date_de_soutenance_prevue' : ('', '') ,
    #'num_dossier' : ('', '') ,
    #'attestation_d_accord_du_directeur_de_these_a_l_accueil' : ('', '') ,
    #'wcs_status' : ('', '') ,
    #'municipalite_ville_2' : ('', '') ,
    #'municipalite_ville_3' : ('', '') ,
    #'pays_de_naissance' : ('', '') ,
    #'faculte_departement_ou_laboratoire' : ('', '') ,
    #'nom_du_directeur_de_these_accueil' : ('', '') ,
    #'wcs_user_display_name' : ('', '') ,
    #'municipalite_ville' : ('', '') ,
    #'si_oui_precisez_le_dernier_auquel_vous_avez_participe' : ('', '') ,
    #'adresse_electronique_du_directeur_de_these_accueil' : ('', '') ,
    #'adresse_electronique_du_directeur_de_these_origine' : ('', '') ,
    #'nombre_de_mois_a_l_origine' : ('', '') ,
    #'pays_de_nationalite' : ('', '') ,
    #'adresse_electronique_du_responsable' : ('', '') ,
    #'wcs_user_email' : ('', '') ,
    

    # Module : surcharge defaut
    

})
