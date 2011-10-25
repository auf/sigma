# -*- encoding: utf-8 -*-

from django import forms
from django.forms.util import ErrorList
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.forms.formsets import TOTAL_FORM_COUNT, INITIAL_FORM_COUNT, MAX_NUM_FORM_COUNT

import sigma.models as sigma
import datamaster_modeles.models as ref


# Fields

class ChoiceLabelField(forms.Field):

    def __init__(self, choices):
        self.map = dict((label, code) for (code, label) in choices)

    def to_python(self, value):
        return self.map.get(value)


class DisciplineField(forms.Field):

    def to_python(self, value):
        try:
            return ref.Discipline.objects.get(nom=value)
        except ref.Discipline.DoesNotExist:
            return None


class PaysField(forms.Field):

    def to_python(self, value):
        try:
            return ref.Pays.objects.get(nom=value)
        except ref.Pays.DoesNotExist:
            return None


class NiveauEtudesField(forms.Field):

    def to_python(self, value):
        try:
            return sigma.NiveauEtude.objects.get(nom=value)
        except sigma.NiveauEtude.DoesNotExist:
            return None


class EtablissementField(forms.Field):

    def to_python(self, value):
        pays, sep, etablissement = value.partition(' - ')
        try:
            return ref.Etablissement.objects.get(pays__nom=pays, nom=etablissement)
        except Etablissement.DoesNotExist:
            return None


class InterventionField(forms.Field):

    def to_python(self, value):
        try:
            return sigma.Intervention.objects.get(nom=value)
        except simga.Intervention.DoesNotExist:
            return None


class PublicField(forms.Field):

    def to_python(self, value):
        try:
            return sigma.Public.objects.get(nom=value)
        except sigma.Public.DoesNotExist:
            return None


# Forms

class PieceForm(modelformset_factory(sigma.Piece, exclude=('dossier', ))):

    def __init__(self, *args, **kwargs):
        """
        Surcharge le formset pour manipuler les data afin de les formatter comme si
        elles avaient été postées.
        """
        _prefix = 'form-'
        data, files = args

        # request.POST (ne contient pas les clefs avec les fichiers)
        clean_data = {}

        # request.FILES
        clean_files = {}

        for idx, k in enumerate(data):
            f_k = "%s%d-nom" % (_prefix, idx)
            clean_data[f_k] = k

            f_fic = "%s%d-fichier" % (_prefix, idx)
            clean_files[f_fic] = data[k]
             
        # On ajoute manuellement les meta servant au formset
        metadata = {}
        metadata[_prefix + TOTAL_FORM_COUNT] = len(data)
        metadata[_prefix + INITIAL_FORM_COUNT] = 0
        metadata[_prefix + MAX_NUM_FORM_COUNT] = len(data)

        clean_data.update(metadata)
        new_args = (clean_data, clean_files)
        super(PieceForm, self).__init__(*new_args, **kwargs)

class DossierForm(CleanFormMixin):
    
    class Meta:
        model = sigma.Dossier
        exclude = ('etat', 'appel', 'candidat', )


    def prepare_discipline(self, value):
        return str2discipline(value)

    def prepare_derniere_bourse_annee(self, value):
        return value

    def prepare_opportunite_regionale(self, value):
        return value

    def prepare_dernier_projet_description(self, value):
        return value

    def prepare_bureau_rattachement(self, value):
        return value

    def prepare_dernier_projet_annee(self, value):
        return value

    def prepare_derniere_bourse_categorie(self, value):
        return value

    def prepare_candidat_statut(self, value):
        return value

    def prepare_moyenne_academique(self, value):
        return value

    def prepare_candidat_fonction(self, value):
        return value



class CandidatForm(CleanFormMixin):
 
    class Meta:
        model = sigma.Candidat
        exclude = ('dossier', )


    def prepare_telephone_pro(self, value):
        return value

    def prepare_naissance_date(self, value):
        return value

    def prepare_telephone_perso(self, value):
        return value

    def prepare_pays(self, value):
        return str2pays(value)

    def prepare_region(self, value):
        return value

    def prepare_courriel_perso(self, value):
        return value

    def prepare_adresse(self, value):
        return value

    def prepare_naissance_ville(self, value):
        return value

    def prepare_nom_jeune_fille(self, value):
        return value

    def prepare_prenom(self, value):
        return value

    def prepare_code_postal(self, value):
        return value

    def prepare_nom(self, value):
        return value

    def prepare_civilite(self, value):
        return value

    def prepare_ville(self, value):
        return value

    def prepare_nationalite(self, value):
        return value


class DossierFaculteForm(CleanFormMixin):

    def prepare_autre_etablissement_ville(self, value):
        return value
    
    def prepare_autre_etablissement_code_postal(self, value):
        return value

    def prepare_resp_inst_civilite(self, value):
        return value

    def prepare_faculte_courriel(self, value):
        return value

    def prepare_resp_sc_telephone(self, value):
        return value
    
    def prepare_autre_etablissement_pays(self, value):
        return value

    def prepare_resp_sc_fonction(self, value):
        return value

    def prepare_resp_inst_prenom(self, value):
        return value

    def prepare_resp_sc_fax(self,value):
        return value

    def prepare_autre_etablissement_adresse(self, value):
        return value

    def prepare_resp_inst_telephone(self, value):
        return value

    def prepare_faculte_nom(self, value):
        return value

    def prepare_resp_sc_prenom(self, value):
        return value

    def prepare_resp_sc_civilite(self, value):
        return value

    def prepare_resp_inst_fonction(self, value):
        return value

    def prepare_etablissement(self, value):
        return value

    def prepare_autre_etablissement_erreur(self, value):
        return value

    def prepare_resp_inst_courriel(self, value):
        return value

    def prepare_autre_etablissement_nom(self, value):
        return value

    def prepare_resp_sc_nom(self, value):
        return value

    def prepare_faculte_adresse(self, value):
        return value

    def prepare_faculte_telephone(self, value):
        return value

    def prepare_resp_inst_nom(self, value):
        return value

    def prepare_faculte_fax(self, value):
        return value

    def prepare_faculte_url(self, value):
        return value

    def prepare_resp_sc_courriel(self, value):
        return value

    def prepare_faculte_ville(self, value):
        return value

    def prepare_autre_etablissement_valide(self, value):
        return value

    def prepare_faculte_code_postal(self, value):
        return value

    def prepare_resp_inst_fax(self, value):
        return value


class DossierOrigineForm(DossierFaculteForm):
 
    class Meta:
        model = sigma.DossierOrigine
        exclude = ('dossier', )



class DossierAccueilForm(DossierFaculteForm):
 
    class Meta:
        model = sigma.DossierAccueil
        exclude = ('dossier', )


class DossierMobiliteForm(CleanFormMixin):
 
    class Meta:
        model = sigma.DossierMobilite
        exclude = ('dossier', )


    def prepare_(self, value):
        return value

    def prepare_these_date_inscription(self, value):
        return value

    def prepare_these_type_autre(self, value):
        return value

    def prepare_alternance_nb_mois_origine(self, value):
        return value

    def prepare_diplome_demande_nom(self, value):
        return value

    def prepare_formation_en_cours_niveau(self, value):
        return value

    def prepare_autres_publics(self, value):
        return value

    def prepare_diplome_demande_niveau(self, value):
        return value

    def prepare_these_date_obtention_prevue(self, value):
        return value

    def prepare_dir_ori_civilite(self, value):
        return value

    def prepare_these_type(self, value):
        return value

    def prepare_date_debut(self, value):
        return value

    def prepare_public_vise(self, value):
        return value

    def prepare_formation_en_cours_diplome(self, value):
        return value

    def prepare_alternance_accueil_puis_origine(self, value):
        return value

    def prepare_alternance_nb_mois_accueil(self, value):
        return value

    def prepare_duree(self, value):
        return value

    def prepare_date_fin(self, value):
        return value

    def prepare_intitule_projet(self, value):
        return value

    def prepare_type_intervention(self, value):
        return value

    def prepare_these_soutenance_date(self, value):
        return value

    def prepare_dir_ori_prenom(self, value):
        return value

    def prepare_dir_acc_prenom(self, value):
        return value

    def prepare_mots_clefs(self, value):
        return value

    def prepare_dir_acc_civilite(self, value):
        return value

    def prepare_dir_ori_nom(self, value):
        return value

    def prepare_dir_acc_nom(self, value):
        return value

    def prepare_discipline(self, value):
        return value

    def prepare_these_soutenance_pays(self, value):
        return value

    def prepare_sous_discipline(self, value):
        return value
