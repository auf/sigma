# -=- encoding: utf-8 -=-
from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.forms.models import BaseInlineFormSet

from sigma.www.forms import SigmaModelForm
from sigma.references import models as ref
from sigma.www.models import *

import unicodedata

class CandidatureBlocForm (forms.Form):
    """Formulaire de mise a jour des valeurs des blocs de champs d'une candidature"""

    def __init__(self, bloc, candidature, *args, **kwargs):
        """
        @param bloc Bloc de champs a remplir
        @param candidature Candidature concerne 
        @param *args Arguments par defaut du formulaire
        @param **kwargs Arguments par defaut du formulaire
        """
        super(CandidatureBlocForm, self).__init__(*args, **kwargs)
        # On recupere les champs
        champs_list = ChampsCategorie.objects.filter(bloc=bloc.id)
        for champs in champs_list:
            name = unicodedata.normalize("NFKD", champs.libelle).encode('ascii','ignore')
            # Permet de gerer deux champs ayant le meme nom
            if name in self.fields:
                name = name + str(len(self.fields))
            if champs.type == "Texte":
                self.fields[name] = forms.CharField(required=False, label=champs.libelle)
                # On sauvegarde l objet champs pour pouvoir utiliser son id lors de 
                # l'enregistrement de la valeur
                self.fields[name].champs = champs
            elif champs.type == "Booleen":
                self.fields[name] = forms.BooleanField(required=False, label=champs.libelle)
                # On sauvegarde l objet champs pour pouvoir utiliser son id lors de 
                # l'enregistrement de la valeur
                self.fields[name].champs = champs
            elif champs.type == "Nombre":
                self.fields[name] = forms.IntegerField(required=False, label=champs.libelle)
                # On sauvegarde l objet champs pour pouvoir utiliser son id lors de 
                # l'enregistrement de la valeur
                self.fields[name].champs = champs

            # Get saved value
            if candidature and name in self.fields:
                # On recupere la valeur de la reponse
                answer = Answer.objects.filter(candidature=candidature).filter(champscategorie=champs)
                # sil y a au moins un  résultat
                if answer:
                    answer = answer.get()
                # sil n y a pas de résultat
                else:
                    answer.value = None
                # On set la valeur deja enregistree de la reponse dans le champs
                if champs.type == "Booleen":
                    # Cas particulier pour les booleens
                    self.fields[name].initial = True if answer.value == '1' else False
                else:
                    self.fields[name].initial = answer.value
                # On sauvegarde l objet answer pour pouvoir utiliser son id lors de 
                # l'enregistrement de la valeur lors de l'edition
                self.fields[name].answer = answer
   

class CandidaturePieceJointeForm(forms.ModelForm):
    """Formulaire de configuration de la presence des pieces jointes des candidatures"""
    class Meta:
        model = PieceJointeCandidature
        exclude = ['piecejointe']

    def as_table(self):
        return mark_safe(u"<tr>") \
            + mark_safe(u"<td>%s</td>" % (self.instance.piecejointe.nom)) \
            + mark_safe(u"<td>%s</td>" % (self.instance.piecejointe.description)) \
            + self._html_output(u'<td>%(errors)s%(field)s%(help_text)s</td>', u'<td>%s</td>', '</td></tr>', u'<br />%s', False) \
            + mark_safe(u"</tr>") 


class CandidaturePieceJointeFormSet(BaseInlineFormSet):
    """Generateur de formulaires de configuration des pieces jointes des candidatures"""
    def __init__(self, *args, **kwargs):
        """ 
        @param *args
        @param **kwargs
        """
        self.extra = 0
        self.can_delete = False
        self.prefix = "piecejointe_"
        self.form = CandidaturePieceJointeForm
        super(CandidaturePieceJointeFormSet, self).__init__(*args, **kwargs)


class CandidatureCriteresForm(forms.ModelForm):
    """Formulaire de configuration de la presence des pieces jointes des candidatures"""
    class Meta:
        model = CritereSupplementaireCandidature
        exclude = ['critere']

    def as_table(self):
        return mark_safe(u"<tr>") \
            + mark_safe(u"<td>%s</td>" % (self.instance.critere.nom)) \
            + mark_safe(u"<td>%s</td>" % (self.instance.critere.description)) \
            + self._html_output(u'<td>%(errors)s%(field)s%(help_text)s</td>', u'<td>%s</td>', '</td></tr>', u'<br />%s', False) \
            + mark_safe(u"</tr>")


class CandidatureCriteresFormSet(BaseInlineFormSet):
    """Generateur de formulaires de configuration des pieces jointes des candidatures"""
    def __init__(self, *args, **kwargs):
        """ 
        @param *args
        @param **kwargs
        """
        self.extra = 0
        self.can_delete = False
        self.prefix = "piecejointe_"
        self.form = CandidatureCriteresForm
        super(CandidatureCriteresFormSet, self).__init__(*args, **kwargs)


class CandidatureEditForm(SigmaModelForm):
    """Formulaire de mise a jour et d'edition des informations d'une candidature"""
    class Meta:
        model = Candidature
        exclude = ['statut', 
                   'appel',
                   'diplome_date',
                   'etablissement',
                   'discipline',
                   'type',
                   'reception_bureau',
                   'date_reception',
                   'mobilite_debut',
                   'mobilite_fin',
                   'mobilite_debute_accueil',
                   'origine_etabl',
                   'origine_etabl_autre',
                   'origine_duree_mois',
                   'accueil_etabl',
                   'accueil_etabl_autre',
                   'piecesjointes',
                   'accueil_duree_mois',
                   'piecesjointes',
                   'criteres',
                   'notes',
                   'experts',
                   'actif']
    
    def get_title(self):
        return "%s %s (%s) / modifier" % \
            (self.instance.prenom, self.instance.nom, self.instance.id)

    def get_action_url(self):
        return "/candidatures/edit/%s/" % self.instance.id


class CandidatureStatutForm(forms.ModelForm):
    """Formulaire de mise a jour du statut d'une candidature"""
    class Meta:
        model = Candidature
        fields = ['statut']


class CandidatureAjoutForm(SigmaModelForm):
    """Formulaire d'ajout d'une candidature,

    Notons que le statut et l'appel d'offre sont des champs automatiquement remplis 
    puisque le statut prends toujours la valeur de depart par defaut et l'appel 
    d'offre doit etre passe en parametre
    """
    class Meta:
        model = Candidature
        exclude = ['statut', 
                   'appel', 
                   'piecesjointes', 
                   'criteres',
                   'notes',
                   'experts',
                   'actif']

    def __init__(self, validate=True, *args, **kwargs):
        self.check_for_blank = validate
        
        super(CandidatureAjoutForm, self).__init__(*args, **kwargs)

    def get_title(self):
        return "Ajouter une candidature"

    def get_action_url(self):
        return "/candidatures/add/%s/" % self.instance.appel.id

    def save(self, *args, **kwargs):
        """ Sauvegarde de la nouvelle instance de candidature avec une gestion 
        des pieces jointes mais ne s'assure par que les champs blank=False
        sont remplis

        @param *args
        @param  **kwargs
        """
        self.check_for_blank = False
        SigmaModelForm.save(self, *args, **kwargs)

        if len(PieceJointeCandidature.objects.filter(candidature=self.instance)) == 0:
            for piece in self.instance.appel.piecesjointes.iterator():
                cpiece = PieceJointeCandidature()
                cpiece.candidature=self.instance
                cpiece.piecejointe=piece
                cpiece.presente=False
                cpiece.conforme=False
                cpiece.save()

        if len(CritereSupplementaireCandidature.objects.filter(candidature=self.instance)) == 0:
            for criteria in self.instance.appel.criteres.iterator():
                ccriteria = CritereSupplementaireCandidature()
                ccriteria.candidature=self.instance
                ccriteria.critere = criteria
                ccriteria.valide = criteria.valide_par_default
                ccriteria.save()


    def validate(self, *args, **kwargs):
        """ Sauvegarde de la nouvelle instance de candidature avec une gestion 
        des pieces jointes mais s'asssure que les champs blank=False sont remplis

        @param *args
        @param  **kwargs
        """
        self.check_for_blank = True
        SigmaModelForm.save(self, *args, **kwargs)

        if len(PieceJointeCandidature.objects.filter(candidature=self.instance)) == 0:
            for piece in self.instance.appel.piecesjointes.iterator():
                cpiece = PieceJointeCandidature()
                cpiece.candidature=self.instance
                cpiece.piecejointe=piece
                cpiece.presente=False
                cpiece.conforme=False
                cpiece.save()

        if len(CritereSupplementaireCandidature.objects.filter(candidature=self.instance)) == 0:
            for criteria in self.instance.appel.criteres.iterator():
                ccriteria = CritereSupplementaireCandidature()
                ccriteria.candidature=self.instance
                ccriteria.critere = criteria
                ccriteria.valide = criteria.valide_par_default
                ccriteria.save()


    def clean(self):
        """Gere la validation des donnees afin de dispenser de validations
        les champs conditionel
        """
        # Gestion des champs dependant entre eux
        for dependency in Candidature.field_dependencies:
            if Candidature.field_dependencies[dependency] in self._errors:

                can_dep = getattr(Candidature, dependency)
                internal_type = can_dep.field.get_internal_type()

                if internal_type == 'ForeignKey':
                        if dependency in self.cleaned_data and \
                                not self.cleaned_data[dependency] == '':
                            del self._errors[Candidature.field_dependencies[dependency]]
                else:
                    if dependency in self.cleaned_data and \
                            not self.cleaned_data[dependency]:
                        del self._errors[Candidature.field_dependencies[dependency]]
            if dependency in self._errors:
                if Candidature.field_dependencies[dependency] in self.cleaned_data \
                        and not self.cleaned_data[Candidature.field_dependencies[dependency]] == '':
                    del self._errors[dependency]
        # Gestion des champs blank
        if not self.check_for_blank:
            for field in self.instance._meta.fields:
                if not field.blank and field.null and field.name in self._errors:
                    if self._errors[field.name] == [u'Ce champ est obligatoire.']:
                        del self._errors[field.name]
                        self.cleaned_data[field.name] = field.get_default()
        return self.cleaned_data


class CandidatureExpertAjout(forms.Form):
    """Formulaire d'ajout d'un critere de checklit par un appel d'offre"""
    bureau = forms.ModelChoiceField(required=False,
                                    queryset=ref.Bureau.objects.all())
    discipline = forms.ModelChoiceField(required=False,
                                        queryset=ref.Discipline.objects.all())
    expert = forms.ModelChoiceField(queryset=Expert.objects.all())


class CandidatureExpertNoter(forms.ModelForm):
    """Formulaire pour noter une candidature selon un expert"""
    class Meta:
        model = ExpertCandidature
        exclude = ['candidature', 'expert', 'is_note']
        
