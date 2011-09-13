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
    'attestation_d_accord_du_directeur_de_these_justifiant_le_stage_de_recherche' : ('Piece', 'attestation') ,
    #'adresse_electronique_du_responsable_2' : ('', '') ,
    #'cocher_la_case_ci_dessous_obligatoire' : ('', '') ,
    #'pays' : ('', '') ,
    #'curriculum_vitae' : ('', '') ,
    #'num_dossier' : ('', '') ,
    #'wcs_status' : ('', '') ,
    #'telephone_personnel' : ('', '') ,
    #'date_de_fin' : ('', '') ,
    #'prenom_2' : ('', '') ,
    #'municipalite_ville_2' : ('', '') ,
    #'municipalite_ville_3' : ('', '') ,
    #'fonction' : ('', '') ,
    #'wcs_workflow_status' : ('', '') ,
    'discipline' : ('Dossier', 'discipline') ,
    #'civilite' : ('', '') ,
    #'faculte_departement_ou_laboratoire' : ('', '') ,
    #'calendrier_du_stage' : ('', '') ,
    #'formation_de_3e_cycle_ou_pos_graduacao_pour_les_etudiants_du_bresil' : ('', '') ,
    #'fonction_2' : ('', '') ,
    #'faculte_departement_ou_laboratoire_2' : ('', '') ,
    #'prenom_du_responsable' : ('', '') ,
    #'wcs_user_display_name' : ('', '') ,
    'nom' : ('Candidat', 'nom') ,
    #'civilite_du_responsable' : ('', '') ,
    #'municipalite_ville' : ('', '') ,
    #'copie_de_l_attestation_d_inscription' : ('', '') ,
    #'etablissement_d_accueil_membre_de_l_auf_en_amerique_du_nord_ou_du_grupo_coimbra_de_universidades_brasileiras_pour_le_bresil' : ('', '') ,
    #'date_de_debut' : ('', '') ,
    #'attestation_d_accueil_du_responsable' : ('', '') ,
    #'nom_de_jeune_fille_si_different' : ('', '') ,
    #'adresse_postale' : ('', '') ,
    #'nom_du_responsable_2' : ('', '') ,
    #'region_province_etat' : ('', '') ,
    #'telephone_professionnel' : ('', '') ,
    #'civilite_du_responsable_2' : ('', '') ,
    #'prenom_du_responsable_2' : ('', '') ,
    #'code_postal' : ('', '') ,
    'prenom' : ('Candidat', 'prenom') ,
    #'date_de_naissance' : ('', '') ,
    #'nom_du_responsable' : ('', '') ,
    #'adresse_electronique_du_responsable' : ('', '') ,
    #'wcs_comments' : ('', '') ,
    #'formation_en_cours' : ('', '') ,
    #'etablissement_d_origine_membre_de_l_auf_en_amerique_du_nord_ou_du_grupo_coimbra_de_universidades_brasileiras_pour_le_bresil' : ('', '') ,
    #'date_d_obtention_prevue' : ('', '') ,
    #'adresse_courriel' : ('', '') ,
    #'nom_du_candidat' : ('', '') ,
    #'pays_de_nationalite' : ('', '') ,
    #'telephone' : ('', '') ,
    #'nombre_total_de_mois' : ('', '') ,
    'descriptif_detaille_du_sujet_de_these' : ('Piece', 'these') ,
    #'wcs_user_email' : ('', '') ,
    

    # Module : surcharge defaut
    

})
