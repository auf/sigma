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
        super(ChoiceLabelField, self).__init__(required=False)
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
        if value is None:
            return None
        pays, sep, etablissement = value.partition(' - ')
        try:
            return ref.Etablissement.objects.get(pays__nom=pays, nom=etablissement)
        except ref.Etablissement.DoesNotExist:
            return None


class InterventionField(forms.Field):

    def to_python(self, value):
        try:
            return sigma.Intervention.objects.get(nom=value)
        except sigma.Intervention.DoesNotExist:
            return None


class PublicField(forms.Field):

    def to_python(self, value):
        try:
            return sigma.Public.objects.get(nom=value)
        except sigma.Public.DoesNotExist:
            return None


# Forms

class DossierForm(forms.ModelForm):
    candidat_statut = ChoiceLabelField(choices=sigma.CANDIDAT_STATUT)
    discipline = DisciplineField(required=False)
    
    class Meta:
        model = sigma.Dossier
        exclude = ('etat', 'appel', 'candidat', )


class CandidatForm(forms.ModelForm):
    civilite = ChoiceLabelField(choices=sigma.CIVILITE)
    nationalite = PaysField(required=False)
    pays = PaysField(required=False)
 
    class Meta:
        model = sigma.Candidat
        exclude = ('dossier', )


class DiplomeForm(forms.ModelForm):
    niveau = NiveauEtudesField(required=False)
    etablissement = EtablissementField(required=False)
    autre_etablissement_pays = PaysField(required=False)

    class Meta:
        model = sigma.Diplome
        exclude = ('dossier',)


class DossierOrigineForm(forms.ModelForm):
    etablissement = EtablissementField(required=False)
    autre_etablissement_pays = PaysField(required=False)
    resp_inst_civilite = ChoiceLabelField(sigma.CIVILITE)
    resp_sc_civilite = ChoiceLabelField(sigma.CIVILITE)
 
    class Meta:
        model = sigma.DossierOrigine
        exclude = ('dossier', )


class DossierAccueilForm(forms.ModelForm):
    etablissement = EtablissementField(required=False)
    autre_etablissement_pays = PaysField(required=False)
    resp_inst_civilite = ChoiceLabelField(sigma.CIVILITE)
    resp_sc_civilite = ChoiceLabelField(sigma.CIVILITE)
 
    class Meta:
        model = sigma.DossierAccueil
        exclude = ('dossier', )


class DossierMobiliteForm(forms.ModelForm):
    formation_en_cours_niveau = NiveauEtudesField(required=False)
    type_intervention = InterventionField(required=False)
    public_vise = PublicField(required=False)
    discipline = DisciplineField(required=False)
    diplome_demande_niveau = NiveauEtudesField(required=False)
    these_soutenance_pays = PaysField(required=False)
    these_type = ChoiceLabelField(sigma.TYPE_THESE)
    dir_ori_civilite = ChoiceLabelField(sigma.CIVILITE)
    dir_acc_civilite = ChoiceLabelField(sigma.CIVILITE)
 
    class Meta:
        model = sigma.DossierMobilite
        exclude = ('dossier', )


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
            if data[k]:
                f_k = "%s%d-nom" % (_prefix, idx)
                clean_data[f_k] = k

                f_fic = "%s%d-fichier" % (_prefix, idx)
                clean_files[f_fic] = data[k]
             
        # On ajoute manuellement les meta servant au formset
        metadata = {}
        metadata[_prefix + TOTAL_FORM_COUNT] = len(clean_data)
        metadata[_prefix + INITIAL_FORM_COUNT] = 0
        metadata[_prefix + MAX_NUM_FORM_COUNT] = len(clean_data)

        clean_data.update(metadata)
        new_args = (clean_data, clean_files)
        super(PieceForm, self).__init__(*new_args, **kwargs)
