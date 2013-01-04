# -*- encoding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.db.models.query import QuerySet
from django.db.models import Q
from form_utils.forms import BetterModelForm
from django.forms import ModelForm
from auf.django.permissions import get_rules
from auf.django.references.models import Discipline, Etablissement

from sigma.candidatures.models import \
        UserProfile, Piece, Note, Dossier, Commentaire, Expert, Conformite, \
        TypeConformite, NOTE_MIN, NOTE_MAX
from sigma.dynamo.forms import PropertyForm
from sigma.dynamo.fields import TEXT


class NoteInlineFormSet(BaseInlineFormSet):
    def __init__(self,
                 data=None,
                 files=None,
                 instance=None,
                 save_as_new=False,
                 prefix=None,
                 queryset=None,
                 **kwargs):
        if not queryset:
            queryset = Note.objects.filter(
                expert__in=instance.experts.all(),
                )
        super(NoteInlineFormSet, self).__init__(
            data,
            files,
            instance,
            save_as_new,
            prefix,
            queryset,
            **kwargs)


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

# Widgets:
class ExpertWidget(forms.widgets.Widget):

    def render(self, name, value, attrs=None):
        exp = Expert.objects.get(id=value)
        nom = '%s %s' % (exp.prenom, exp.nom)
        return mark_safe(
            u'<input readonly class="readonly_field" value="%(nom)s"'
            '/><input type="hidden" name="%(name)s" value="%(value)s"'
            '/>' % {
                'value': value,
                'name': name,
                'nom': nom,
                })

class NoteWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe(
            u'<input readonly class="readonly_field" value="%s"/>' %
            value)


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

    conforme = forms.NullBooleanField(widget=forms.RadioSelect(choices=((True, 'Oui'),
    (False, 'Non'))))

    class Meta:
        model = Piece
        fields = ('identifiant', 'fichier', 'conforme')

# DOSSIER - EVALUATION

class NoteForm(BetterModelForm):
    expert = forms.CharField(
        max_length=1024,
        widget=ExpertWidget,
        )

    def __init__(self, *a, **kw):
        super(NoteForm, self).__init__(*a, **kw)

    class Meta:
        exclude = ('dossier', )
        model = Note

    def clean_expert(self):
        # Make it readonly.
        if 'expert' in self.changed_data:
            raise forms.ValidationError(
                "Impossible de modifier l'expert"
                )
        return Expert.objects.get(id=self.cleaned_data['expert'])

    def clean_note(self):
        note = self.cleaned_data['note']
        if note is None:
            return note
        if note < NOTE_MIN or note > NOTE_MAX:
            raise forms.ValidationError(
                "Vous devez spécifier une note entre %s et %s" %
                (NOTE_MIN, NOTE_MAX)
                )
        return note

    def clean(self):
        if (self.instance.id == None and
            self.instance.dossier.notes.filter(
                expert=self.cleaned_data['expert']).count() > 0):
            raise forms.ValidationError(
                'Une seule note peut être inscrite par expert, par'
                ' dossier.'
            )
        return self.cleaned_data


NoteFormSet = inlineformset_factory(
    Dossier,
    Note,
    form=NoteForm,
    extra=0,
    formset=NoteInlineFormSet,
    can_delete=False,
    )


class CommentaireForm(BetterModelForm):
    class Meta:
        exclude = ('user', )
        model = Commentaire


class EvaluationForm(BetterModelForm):
    moyenne_notes = forms.CharField(
        label='Moyenne des notes',
        required=False,
        widget=NoteWidget,
        )

    def __init__(self, *a, **kw):
        super(EvaluationForm, self).__init__(*a, **kw)
        moyenne = float(0)
        if self.instance.id:
            moyenne = self.instance.moyenne_notes()
        self.initial['moyenne_notes'] = moyenne

    class Meta:
        fields = (
            'moyenne_academique',
            'moyenne_notes',
            'opportunite_regionale',
            )
        model = Dossier


class ExpertChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *a, **kw):
        self.dossiers = kw.pop('dossiers', None)
        super(ExpertChoiceField, self).__init__(*a, **kw)

    def label_from_instance(self, obj):
        match_str = ''
        if obj.DMATCH_S > 0:
            match_str = '*'
        disciplines = ', '.join([d.nom for d in obj.disciplines.all()])
        return "%s%s, %s (%s)" % (match_str, obj.nom, obj.prenom, disciplines)


class ExpertForm(forms.Form):
    filter_horizontal = ['experts']

    def __init__(self, *args, **kwargs):
        self.dossiers = kwargs.pop('dossiers')
        req = kwargs.pop('request', None)
        super(ExpertForm, self).__init__(*args, **kwargs)
        self.fields['experts'] = ExpertChoiceField(
            'Experts',
            dossiers=self.dossiers,
            required=False,
            help_text=(
                'Maintenez appuyé « Ctrl », ou « Commande (touche '
                'pomme) » sur un Mac, pour en sélectionner '
                'plusieurs. N-B: l\'astérisque (*) devant les saisies '
                'd\'experts signifie une correspondance de la '
                'discipline de l\'applicant avec celle de l\'expert.'
                )
            )
        if req:
            self.fields['experts'].queryset = (
                Expert.objects.get_discipline_match(
                    self.dossiers,
                    get_rules().filter_queryset(
                        req.user, 'assign', Expert.objects.all()
                        )))
            # import pdb; pdb.set_trace()
            self.fields['experts'].widget = (
                admin.widgets.RelatedFieldWidgetWrapper(
                    admin.widgets.FilteredSelectMultiple(
                            'Experts',
                            True,
                            choices=self.fields['experts'].choices,),
                    Dossier._meta._name_map['experts'][0].rel,
                    admin.site,
                    ))


    def clean_experts(self):
        etabs = Etablissement.objects.filter(
            dossierorigine__dossier__in=self.dossiers)

        ex_check = Expert.objects.filter(
            etablissement__in=etabs,
            id__in=self.cleaned_data.get('experts', []))
        if ex_check.count() > 0:

            ex_str = ', '.join([
                    ('%s %s' % (x.prenom, x.nom)).encode('utf8')
                 for x in ex_check])

            if isinstance(self.dossiers, QuerySet):
                d_str_qs = self.dossiers
            else:
                d_str_qs = Dossier.objects.filter(
                    id__in=[x.id for x in self.dossiers]
                    )
            d_str_qs = d_str_qs.filter(origine__etablissement__in=etabs)

            d_str = ', '.join([
                    str(x) for x in
                    d_str_qs
                    ])

            err = mark_safe(
                'Impossible d\'assigner un expert du même '
                'établissement que le l\'établissement '
                'd\'origine du candidat: Le ou les experts %s '
                'travaillent dans les établissements d\'origine des '
                'dossiers %s.' % (
                    ex_str,
                    d_str)
                )
            raise forms.ValidationError(mark_safe(err))
        return self.cleaned_data.get('experts')

    def save(self):
        for d in self.dossiers:
            d.experts = self.cleaned_data.get('experts', [])
            d.save()
            d.prepopuler_notes()


# Dynamo - ADMIN

class ConformiteForm(PropertyForm):
    """
    Dans l'admin inline, on préserve le type défini par l'appel.
    """
    conforme = forms.NullBooleanField(widget=forms.RadioSelect(choices=((True, 'Oui'),
    (False, 'Non'))))

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
