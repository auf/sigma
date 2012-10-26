# -*- encoding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from form_utils.forms import BetterModelForm
from django.forms import ModelForm
from auf.django.references.models import Discipline

from sigma.candidatures.models import \
        UserProfile, Piece, Note, Dossier, Commentaire, Expert, Conformite, \
        TypeConformite, NOTE_MIN, NOTE_MAX
from sigma.dynamo.forms import PropertyForm
from sigma.dynamo.fields import TEXT


class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


# PROFIL - DISCIPLINES

class DisciplineForm(BetterModelForm):
    """
    """
    disciplines = forms.ModelMultipleChoiceField(
        queryset=Discipline.objects.all(),
        label="Disciplines",
        widget=admin.widgets.FilteredSelectMultiple("disciplines", False),
        required=False,
        )

    class Meta:
        exclude = ('user', )
        model = UserProfile


# DOSSIER - PIÈCES JOINTES

class PieceForm(ModelForm):

    class Meta:
        model = Piece
        fields = ('identifiant', 'fichier', 'conforme')


# DOSSIER - EVALUATION

class NoteForm(BetterModelForm):
    class Meta:
        exclude = ('expert', 'dossier', )
        model = Note

    def clean_note(self):
        note = self.cleaned_data['note']

        if note < NOTE_MIN or note > NOTE_MAX:
            raise forms.ValidationError(
                "Vous devez spécifier une note entre %s et %s" %
                (NOTE_MIN, NOTE_MAX)
            )

        return note


class CommentaireForm(BetterModelForm):
    class Meta:
        exclude = ('user', )
        model = Commentaire


class EvaluationForm(BetterModelForm):
    class Meta:
        fields = ('moyenne_academique', 'opportunite_regionale', )
        model = Dossier


class ExpertChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        disciplines = ', '.join([d.code for d in obj.disciplines.all()])
        return "%s, %s (%s)" % (obj.nom, obj.prenom, disciplines)


class ExpertForm(forms.Form):
    experts = ExpertChoiceField(
        queryset=Expert.objects.all(),
        help_text="Maintenez appuyé « Ctrl », ou " \
        "« Commande (touche pomme) » sur un Mac, pour en sélectionner " \
        "plusieurs."
    )

    def __init__(self, *args, **kwargs):
        self.dossiers = kwargs.pop('dossiers')
        super(ExpertForm, self).__init__(*args, **kwargs)

    def save(self):
        for d in self.dossiers:
            d.experts = self.cleaned_data.get('experts', [])
            d.save()


# Dynamo - ADMIN

class ConformiteForm(PropertyForm):
    """
    Dans l'admin inline, on préserve le type défini par l'appel.
    """

    class Meta:
        exclude = ('type', 'value', )
        model = Conformite


class TypeConformiteForm(BetterModelForm):
    """
    Il n'y a qu'un type possible de pièces dans ce cas : boolean.
    """
    class Meta:
        exclude = ('field_type',)
        model = TypeConformite

    def save(self, commit=True):
        instance = super(TypeConformiteForm, self).save(commit)
        instance.field_type = TEXT
        return instance
