# -*- encoding: utf-8 -*-

from project.wcs.forms import *

MAPPING = {

    # Module : Dossier
    'sigma|Dossier|moyenne_votes' : ('Dossier', 'moyenne_votes') ,
    'sigma|Dossier|id' : ('Dossier', 'id') ,
    'sigma|Dossier|discipline' : ('Dossier', 'discipline') ,
    'sigma|Dossier|derniere_bourse_annee' : ('Dossier', 'derniere_bourse_annee') ,
    'sigma|Dossier|opportunite_regionale' : ('Dossier', 'opportunite_regionale') ,
    'sigma|Dossier|etat' : ('Dossier', 'etat') ,
    'sigma|Dossier|dernier_projet_description' : ('Dossier', 'dernier_projet_description') ,
    'sigma|Dossier|appel' : ('Dossier', 'appel') ,
    'sigma|Dossier|bureau_rattachement' : ('Dossier', 'bureau_rattachement') ,
    'sigma|Dossier|dernier_projet_annee' : ('Dossier', 'dernier_projet_annee') ,
    'sigma|Dossier|derniere_bourse_categorie' : ('Dossier', 'derniere_bourse_categorie') ,
    'sigma|Dossier|candidat_statut' : ('Dossier', 'candidat_statut') ,
    'sigma|Dossier|moyenne_academique' : ('Dossier', 'moyenne_academique') ,
    'sigma|Dossier|candidat_fonction' : ('Dossier', 'candidat_fonction') ,
    

    # Module : DossierAccueil
    'sigma|DossierAccueil|autre_etablissement_adresse' : ('DossierAccueil', 'autre_etablissement_adresse') ,
    'sigma|DossierAccueil|resp_inst_telephone' : ('DossierAccueil', 'resp_inst_telephone') ,
    'sigma|DossierAccueil|autre_etablissement_code_postal' : ('DossierAccueil', 'autre_etablissement_code_postal') ,
    'sigma|DossierAccueil|autre_etablissement_nom' : ('DossierAccueil', 'autre_etablissement_nom') ,
    'sigma|DossierAccueil|etablissement' : ('DossierAccueil', 'etablissement') ,
    'sigma|DossierAccueil|faculte_telephone' : ('DossierAccueil', 'faculte_telephone') ,
    'sigma|DossierAccueil|resp_sc_fonction' : ('DossierAccueil', 'resp_sc_fonction') ,
    'sigma|DossierAccueil|autre_etablissement_erreur' : ('DossierAccueil', 'autre_etablissement_erreur') ,
    'sigma|DossierAccueil|resp_sc_nom' : ('DossierAccueil', 'resp_sc_nom') ,
    'sigma|DossierAccueil|faculte_url' : ('DossierAccueil', 'faculte_url') ,
    'sigma|DossierAccueil|resp_sc_civilite' : ('DossierAccueil', 'resp_sc_civilite') ,
    'sigma|DossierAccueil|resp_sc_telephone' : ('DossierAccueil', 'resp_sc_telephone') ,
    'sigma|DossierAccueil|faculte_adresse' : ('DossierAccueil', 'faculte_adresse') ,
    'sigma|DossierAccueil|resp_inst_fax' : ('DossierAccueil', 'resp_inst_fax') ,
    'sigma|DossierAccueil|dossier' : ('DossierAccueil', 'dossier') ,
    'sigma|DossierAccueil|faculte_fax' : ('DossierAccueil', 'faculte_fax') ,
    'sigma|DossierAccueil|resp_inst_fonction' : ('DossierAccueil', 'resp_inst_fonction') ,
    'sigma|DossierAccueil|faculte_code_postal' : ('DossierAccueil', 'faculte_code_postal') ,
    'sigma|DossierAccueil|resp_inst_nom' : ('DossierAccueil', 'resp_inst_nom') ,
    'sigma|DossierAccueil|resp_inst_prenom' : ('DossierAccueil', 'resp_inst_prenom') ,
    'sigma|DossierAccueil|faculte_nom' : ('DossierAccueil', 'faculte_nom') ,
    'sigma|DossierAccueil|resp_inst_civilite' : ('DossierAccueil', 'resp_inst_civilite') ,
    'sigma|DossierAccueil|autre_etablissement_pays' : ('DossierAccueil', 'autre_etablissement_pays') ,
    'sigma|DossierAccueil|resp_sc_fax' : ('DossierAccueil', 'resp_sc_fax') ,
    'sigma|DossierAccueil|id' : ('DossierAccueil', 'id') ,
    'sigma|DossierAccueil|faculte_courriel' : ('DossierAccueil', 'faculte_courriel') ,
    'sigma|DossierAccueil|resp_inst_courriel' : ('DossierAccueil', 'resp_inst_courriel') ,
    'sigma|DossierAccueil|resp_sc_prenom' : ('DossierAccueil', 'resp_sc_prenom') ,
    'sigma|DossierAccueil|resp_sc_courriel' : ('DossierAccueil', 'resp_sc_courriel') ,
    'sigma|DossierAccueil|autre_etablissement_ville' : ('DossierAccueil', 'autre_etablissement_ville') ,
    'sigma|DossierAccueil|autre_etablissement_valide' : ('DossierAccueil', 'autre_etablissement_valide') ,
    'sigma|DossierAccueil|autre_etablissement_region' : ('DossierAccueil', 'autre_etablissement_region') ,
    'sigma|DossierAccueil|faculte_ville' : ('DossierAccueil', 'faculte_ville') ,
    

    # Module : DossierOrigine
    'sigma|DossierOrigine|autre_etablissement_ville' : ('DossierOrigine', 'autre_etablissement_ville') ,
    'sigma|DossierOrigine|id' : ('DossierOrigine', 'id') ,
    'sigma|DossierOrigine|autre_etablissement_code_postal' : ('DossierOrigine', 'autre_etablissement_code_postal') ,
    'sigma|DossierOrigine|resp_inst_civilite' : ('DossierOrigine', 'resp_inst_civilite') ,
    'sigma|DossierOrigine|faculte_courriel' : ('DossierOrigine', 'faculte_courriel') ,
    'sigma|DossierOrigine|resp_sc_telephone' : ('DossierOrigine', 'resp_sc_telephone') ,
    'sigma|DossierOrigine|autre_etablissement_pays' : ('DossierOrigine', 'autre_etablissement_pays') ,
    'sigma|DossierOrigine|resp_sc_fonction' : ('DossierOrigine', 'resp_sc_fonction') ,
    'sigma|DossierOrigine|resp_inst_prenom' : ('DossierOrigine', 'resp_inst_prenom') ,
    'sigma|DossierOrigine|resp_sc_fax' : ('DossierOrigine', 'resp_sc_fax') ,
    'sigma|DossierOrigine|autre_etablissement_adresse' : ('DossierOrigine', 'autre_etablissement_adresse') ,
    'sigma|DossierOrigine|resp_inst_telephone' : ('DossierOrigine', 'resp_inst_telephone') ,
    'sigma|DossierOrigine|dossier' : ('DossierOrigine', 'dossier') ,
    'sigma|DossierOrigine|faculte_nom' : ('DossierOrigine', 'faculte_nom') ,
    'sigma|DossierOrigine|resp_sc_prenom' : ('DossierOrigine', 'resp_sc_prenom') ,
    'sigma|DossierOrigine|resp_sc_civilite' : ('DossierOrigine', 'resp_sc_civilite') ,
    'sigma|DossierOrigine|resp_inst_fonction' : ('DossierOrigine', 'resp_inst_fonction') ,
    'sigma|DossierOrigine|etablissement' : ('DossierOrigine', 'etablissement') ,
    'sigma|DossierOrigine|autre_etablissement_erreur' : ('DossierOrigine', 'autre_etablissement_erreur') ,
    'sigma|DossierOrigine|resp_inst_courriel' : ('DossierOrigine', 'resp_inst_courriel') ,
    'sigma|DossierOrigine|autre_etablissement_nom' : ('DossierOrigine', 'autre_etablissement_nom') ,
    'sigma|DossierOrigine|autre_etablissement_region' : ('DossierOrigine', 'autre_etablissement_region') ,
    'sigma|DossierOrigine|resp_sc_nom' : ('DossierOrigine', 'resp_sc_nom') ,
    'sigma|DossierOrigine|faculte_adresse' : ('DossierOrigine', 'faculte_adresse') ,
    'sigma|DossierOrigine|faculte_telephone' : ('DossierOrigine', 'faculte_telephone') ,
    'sigma|DossierOrigine|resp_inst_nom' : ('DossierOrigine', 'resp_inst_nom') ,
    'sigma|DossierOrigine|faculte_fax' : ('DossierOrigine', 'faculte_fax') ,
    'sigma|DossierOrigine|faculte_url' : ('DossierOrigine', 'faculte_url') ,
    'sigma|DossierOrigine|resp_sc_courriel' : ('DossierOrigine', 'resp_sc_courriel') ,
    'sigma|DossierOrigine|faculte_ville' : ('DossierOrigine', 'faculte_ville') ,
    'sigma|DossierOrigine|autre_etablissement_valide' : ('DossierOrigine', 'autre_etablissement_valide') ,
    'sigma|DossierOrigine|faculte_code_postal' : ('DossierOrigine', 'faculte_code_postal') ,
    'sigma|DossierOrigine|resp_inst_fax' : ('DossierOrigine', 'resp_inst_fax') ,
    

    # Module : DossierMobilite
    'sigma|DossierMobilite|these_date_inscription' : ('DossierMobilite', 'these_date_inscription') ,
    'sigma|DossierMobilite|these_type_autre' : ('DossierMobilite', 'these_type_autre') ,
    'sigma|DossierMobilite|alternance_nb_mois_origine' : ('DossierMobilite', 'alternance_nb_mois_origine') ,
    'sigma|DossierMobilite|diplome_demande_nom' : ('DossierMobilite', 'diplome_demande_nom') ,
    'sigma|DossierMobilite|id' : ('DossierMobilite', 'id') ,
    'sigma|DossierMobilite|formation_en_cours_niveau' : ('DossierMobilite', 'formation_en_cours_niveau') ,
    'sigma|DossierMobilite|autres_publics' : ('DossierMobilite', 'autres_publics') ,
    'sigma|DossierMobilite|diplome_demande_niveau' : ('DossierMobilite', 'diplome_demande_niveau') ,
    'sigma|DossierMobilite|these_date_obtention_prevue' : ('DossierMobilite', 'these_date_obtention_prevue') ,
    'sigma|DossierMobilite|dir_ori_civilite' : ('DossierMobilite', 'dir_ori_civilite') ,
    'sigma|DossierMobilite|these_type' : ('DossierMobilite', 'these_type') ,
    'sigma|DossierMobilite|date_debut' : ('DossierMobilite', 'date_debut') ,
    'sigma|DossierMobilite|public_vise' : ('DossierMobilite', 'public_vise') ,
    'sigma|DossierMobilite|formation_en_cours_diplome' : ('DossierMobilite', 'formation_en_cours_diplome') ,
    'sigma|DossierMobilite|alternance_accueil_puis_origine' : ('DossierMobilite', 'alternance_accueil_puis_origine') ,
    'sigma|DossierMobilite|alternance_nb_mois_accueil' : ('DossierMobilite', 'alternance_nb_mois_accueil') ,
    'sigma|DossierMobilite|duree' : ('DossierMobilite', 'duree') ,
    'sigma|DossierMobilite|date_fin' : ('DossierMobilite', 'date_fin') ,
    'sigma|DossierMobilite|intitule_projet' : ('DossierMobilite', 'intitule_projet') ,
    'sigma|DossierMobilite|type_intervention' : ('DossierMobilite', 'type_intervention') ,
    'sigma|DossierMobilite|these_soutenance_date' : ('DossierMobilite', 'these_soutenance_date') ,
    'sigma|DossierMobilite|dir_ori_prenom' : ('DossierMobilite', 'dir_ori_prenom') ,
    'sigma|DossierMobilite|dir_acc_prenom' : ('DossierMobilite', 'dir_acc_prenom') ,
    'sigma|DossierMobilite|dossier' : ('DossierMobilite', 'dossier') ,
    'sigma|DossierMobilite|mots_clefs' : ('DossierMobilite', 'mots_clefs') ,
    'sigma|DossierMobilite|dir_acc_civilite' : ('DossierMobilite', 'dir_acc_civilite') ,
    'sigma|DossierMobilite|dir_ori_nom' : ('DossierMobilite', 'dir_ori_nom') ,
    'sigma|DossierMobilite|dir_acc_nom' : ('DossierMobilite', 'dir_acc_nom') ,
    'sigma|DossierMobilite|discipline' : ('DossierMobilite', 'discipline') ,
    'sigma|DossierMobilite|these_soutenance_pays' : ('DossierMobilite', 'these_soutenance_pays') ,
    'sigma|DossierMobilite|sous_discipline' : ('DossierMobilite', 'sous_discipline') ,
    

}

