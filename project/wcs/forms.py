# -*- encoding: utf-8 -*-

from django import forms
from project.sigma import models as sigma
from formats import *

class CleanFormMixin(forms.ModelForm):
    """
    Mixin form pour cabler une fonction de preparation des données
    """
    def _clean_fields(self):
        for name, field in self.fields.items():
            value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            if hasattr(self, 'prepare_%s' % name):
                    value = getattr(self, 'prepare_%s' % name)(value)
                    self.data[name] = value

        return super(CleanFormMixin, self)._clean_fields()


class DossierForm(CleanFormMixin):
    
    class Meta:
        model = sigma.Dossier
        exclude = ('etat', 'appel', 'candidat', )


    def prepare_discipline(self, value):
        return value

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
