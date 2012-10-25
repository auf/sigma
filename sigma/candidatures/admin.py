# -*- encoding: utf-8 -*-
import os

from auf.django.export.admin import ExportAdmin
from auf.django.permissions import get_rules
from auf.django.permissions.forms import make_global_permissions_form
from auf.django.references import models as ref
from auf.django.workflow.admin import WorkflowAdmin
from django import forms
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.contrib.auth.admin import \
        UserAdmin as DjangoUserAdmin, GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserForm
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext, defaultfilters
from sendfile import sendfile

from sigma.candidatures.models import \
        Conformite, Appel, DossierOrigine, DossierAccueil, DossierMobilite, \
        Candidat, Dossier, Expert, Piece, TypePiece, AttributWCS, Diplome, \
        TypeConformite
from sigma.candidatures.forms import \
        ConformiteForm, TypeConformiteForm, RequiredInlineFormSet, PieceForm
from sigma.candidatures.workflow import DOSSIER_ETAT_BOURSIER
from sigma.custom_admin import ModelAdmin, GuardedModelAdmin

# Filtres

class RegionFilter(admin.SimpleListFilter):
    title = 'région'
    parameter_name = 'region'

    def lookups(self, request, model_admin):
        return [
            (unicode(a), b)
            for (a, b) in get_rules().filter_queryset(
                request.user, 'manage', ref.Region.objects.all()
            ).values_list('id', 'nom')
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(region=self.value())
        else:
            return queryset


class AppelFilter(admin.SimpleListFilter):
    title = 'appel'
    parameter_name = 'appel'

    def lookups(self, request, model_admin):
        region_ids = get_rules().filter_queryset(
            request.user, 'manage', ref.Region.objects.all()
        ).values_list('id', flat=True)
        return [
            (unicode(a), b)
            for (a, b) in Appel.objects.filter(region__in=region_ids)
            .values_list('id', 'nom')
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(appel=self.value())
        else:
            return queryset


class RegionOrigineFilter(admin.SimpleListFilter):
    title = "région d'origine"
    parameter_name = 'region_origine'

    def lookups(self, request, model_admin):
        return [
            (unicode(a), b)
            for (a, b) in ref.Region.objects.values_list('id', 'nom')
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                Q(
                    origine__etablissement__isnull=False,
                    origine__etablissement__region=self.value()
                ) |
                Q(
                    origine__etablissement__isnull=True,
                    origine__etablissement__pays__region=self.value()
                )
            )
        else:
            return queryset


class RegionAccueilFilter(admin.SimpleListFilter):
    title = "région d'accueil"
    parameter_name = 'region_accueil'

    def lookups(self, request, model_admin):
        return [
            (unicode(a), b)
            for (a, b) in ref.Region.objects.values_list('id', 'nom')
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                Q(
                    accueil__etablissement__isnull=False,
                    accueil__etablissement__region=self.value()
                ) |
                Q(
                    accueil__etablissement__isnull=True,
                    accueil__etablissement__pays__region=self.value()
                )
            )
        else:
            return queryset


# Forms

class DossierMobiliteForm(forms.ModelForm):

    class Meta:
        model = DossierMobilite

    def clean_date_fin_origine(self):
        date_debut = self.cleaned_data.get('date_debut_origine')
        date_fin = self.cleaned_data.get('date_fin_origine')

        if date_debut and date_fin and date_fin < date_debut:
            raise forms.ValidationError(
                "La date de fin précède la date de début"
            )

        return date_fin

    def clean_date_fin_accueil(self):
        debut_accueil = self.cleaned_data.get('date_debut_accueil')
        fin_accueil = self.cleaned_data.get('date_fin_accueil')
        debut_origine = self.cleaned_data.get('date_debut_origine')
        fin_origine = self.cleaned_data.get('date_fin_origine')
        if debut_accueil and fin_accueil and fin_accueil < debut_accueil:
            raise forms.ValidationError(
                "La date de fin précède la date de début"
            )

        if debut_accueil and fin_accueil and \
           debut_origine and fin_origine and \
           not (fin_origine <= debut_accueil or fin_accueil <= debut_origine):
            raise forms.ValidationError(
                "Les périodes de mobilité se chevauchent"
            )
        return fin_accueil

    def clean_mots_clefs(self):
        mots_clefs = self.cleaned_data['mots_clefs']

        if mots_clefs.count(',') > 2:
            raise forms.ValidationError(
                "Vous avez droit qu'à trois mots clefs séparés avec virgules"
            )

        return mots_clefs


# Inlines

class TypePieceInline(admin.TabularInline):
    model = TypePiece
    prepopulated_fields = {'identifiant': ('nom',)}
    verbose_name = u'pièce à demander'
    verbose_name_plural = u'pièces à demander'


class BaseDossierFaculteInline(admin.StackedInline):
    max_num = 1
    template = "admin/candidatures/edit_inline/single-stack.html"
    can_delete = False


class DossierOrigineInline(BaseDossierFaculteInline):
    model = DossierOrigine
    verbose_name = verbose_name_plural = "Origine " \
            "(établissement d'inscription ou d'activité " \
            "à la date de la candidature)"

    fieldsets = (
        (None, {'fields': ('etablissement',)}),
        ('Autre établissement si non membre de l\'AUF', {
            'fields': (
                ('autre_etablissement_nom', 'autre_etablissement_adresse'),
                ('autre_etablissement_ville',
                 'autre_etablissement_code_postal'),
                ('autre_etablissement_region', 'autre_etablissement_pays')
            )
        }),
        ('Responsable institutionnel à l\'origine', {
            'fields': (
                ('resp_inst_civilite', 'resp_inst_nom', 'resp_inst_prenom'),
                ('resp_inst_fonction', 'resp_inst_courriel'),
                ('resp_inst_telephone', 'resp_inst_fax')
            )
        }),
        ('Responsable scientifique à l\'origine', {
            'fields': (('resp_sc_civilite', 'resp_sc_nom', 'resp_sc_prenom'),
                       ('resp_sc_fonction', 'resp_sc_courriel'),
                       ('resp_sc_telephone', 'resp_sc_fax'),
                       ('faculte_nom', 'faculte_adresse'),
                       ('faculte_ville', 'faculte_code_postal'))
        }),
        ("Directeur de thèse à l'origine", {
            'fields': ('dir_civilite',
                       ('dir_nom', 'dir_prenom'),
                       ('dir_courriel', 'dir_telephone'))
        }),
    )


class DossierAccueilInline(BaseDossierFaculteInline):
    model = DossierAccueil
    verbose_name = verbose_name_plural = "Accueil " \
            "(établissement de destination de la mobilité)"

    fieldsets = (
        (None, {'fields': ('etablissement',)}),
        ('Autre établissement si non membre de l\'AUF', {
            'fields': (
                ('autre_etablissement_nom', 'autre_etablissement_adresse'),
                ('autre_etablissement_ville',
                 'autre_etablissement_code_postal'),
                ('autre_etablissement_region', 'autre_etablissement_pays')
            )
        }),
        ('Responsable scientifique à l\'accueil', {
            'fields': (('resp_sc_civilite', 'resp_sc_nom', 'resp_sc_prenom'),
                       ('resp_sc_fonction', 'resp_sc_courriel'),
                       ('resp_sc_telephone', 'resp_sc_fax'),
                       ('faculte_nom', 'faculte_adresse'),
                       ('faculte_ville', 'faculte_code_postal'))
        }),
        ("Directeur de thèse à l'accueil", {
            'fields': ('dir_civilite',
                       ('dir_nom', 'dir_prenom'),
                       ('dir_courriel', 'dir_telephone'))
        }),
    )


class DossierConformiteAdmin(admin.TabularInline):
    """
    Admin pour spécifier spécifier si la conformité est passée ou non
    """
    form = ConformiteForm
    model = Conformite
    extra = 0
    max_num = 0
    can_delete = False


class DossierMobiliteInline(admin.StackedInline):
    form = DossierMobiliteForm
    model = DossierMobilite
    max_num = 1
    template = "admin/candidatures/edit_inline/single-stack.html"
    can_delete = False
    verbose_name = verbose_name_plural = "Mobilité"

    fieldsets = (
        ("Période de mobilité à l'origine", {
            'fields': (('date_debut_origine', 'date_fin_origine'),)
        }),
        ("Période de mobilité à l'accueil", {
            'fields': (('date_debut_accueil', 'date_fin_accueil'),)
        }),
        ('Dossier scientifique', {
            'fields': ('intitule_projet', 'mots_clefs')
        }),
        ('Disciplines', {
            'fields': (('discipline', 'sous_discipline'),)
        }),
        ('Formation en cours', {
            'fields': (
                ('formation_en_cours_diplome', 'formation_en_cours_niveau'),
            )
        }),
        ('Diplôme demandé', {
            'fields': (('diplome_demande_nom', 'diplome_demande_niveau'),)
        }),
        ('Thèse', {
            'fields': ('these_date_inscription',
                       'these_soutenance_pays',
                       'these_soutenance_date',
                       'these_type')
        }),
        ('Programme de mission', {
            'fields': ('type_intervention', 'public_vise', 'autres_publics')
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'intitule_projet':
            kwargs['widget'] = forms.TextInput(attrs={'size': 80})
        return super(DossierMobiliteInline, self) \
                .formfield_for_dbfield(db_field, **kwargs)


class DossierCandidatInline(admin.StackedInline):
    formset = RequiredInlineFormSet
    model = Candidat

    max_num = 1
    verbose_name = verbose_name_plural = "Identification"
    can_delete = False
    template = "admin/candidatures/edit_inline/single-stack.html"

    fieldsets = (
        (None, {
            'fields': ('civilite', ('nom', 'prenom'), 'nom_jeune_fille',
                       'nationalite', 'naissance_date',)
        }),
        ('Coordonnées', {
            'fields': (
                'adresse',
                'adresse_complement',
                ('ville', 'code_postal'),
                'region',
                'pays',
                ('telephone', 'telephone_portable'),
                'courriel')
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in ('adresse', 'adresse_complement'):
            kwargs['widget'] = forms.TextInput(attrs={'size': 80})
        elif db_field.name == 'naissance_date':
            kwargs['widget'] = forms.DateInput(format='%d/%m/%Y')
        return super(DossierCandidatInline, self) \
                .formfield_for_dbfield(db_field, **kwargs)


class DiplomeInline(admin.StackedInline):
    model = Diplome
    max_num = 1
    template = "admin/candidatures/edit_inline/single-stack.html"
    verbose_name = verbose_name_plural = "Dernier diplôme obtenu"
    can_delete = False

    fieldsets = (
        (None, {
            'fields': ('nom', 'date', 'niveau', 'etablissement')
        }),
        ('Autre établissement d\'obtention, si non membre de l\'AUF', {
            'fields': ('autre_etablissement_nom', 'autre_etablissement_pays')
        }),

    )


# Model admins

class TypeConformiteAdmin(ModelAdmin):
    form = TypeConformiteForm


class AppelAdmin(GuardedModelAdmin):
    list_display = (
        'nom', 'region_code', 'code_budgetaire', 'date_debut_appel',
        'date_fin_appel', '_actions',
    )
    list_filter = (RegionFilter,)
    search_fields = ('nom', 'code_budgetaire')
    fieldsets = ((None, {
        'fields': (
            'type_bourse',
            'nom',
            'region',
            'annee',
            'code_budgetaire',
            ('date_debut_appel', 'date_fin_appel'),
            ('date_debut_mobilite', 'date_fin_mobilite'),
            'periode',
            'bareme',
            ('montant_mensuel_origine_sud', 'montant_mensuel_origine_nord'),
            ('montant_mensuel_accueil_sud', 'montant_mensuel_accueil_nord'),
            ('montant_perdiem_sud', 'montant_perdiem_nord'),
            'montant_allocation_unique',
            ('prime_installation_sud', 'prime_installation_nord'),
            'appel_en_ligne',
            'conformites',
        )
    }),)
    filter_horizontal = ['conformites']
    inlines = [TypePieceInline]

    class Media:
        js = ("candidatures/appel.js",)

    def _actions(self, obj):
        return "<a href='%s?appel__id__exact=%s'>Voir les dossiers</a>" % \
                (reverse('admin:candidatures_dossier_changelist'), obj.id)
    _actions.allow_tags = True
    _actions.short_description = u''

    def region_code(self, obj):
        return obj.region.code
    region_code.short_description = u'région'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'region':
            kwargs['queryset'] = get_rules().filter_queryset(
                request.user, 'manage', ref.Region.objects.all()
            )
        return super(AppelAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


def affecter_dossiers_expert(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    return HttpResponseRedirect(
        reverse('affecter_experts_dossiers') + \
        "?ids=%s" % (",".join(selected))
    )
affecter_dossiers_expert.short_description = \
        'Assigner expert(s) au(x) dossier(s)'


class DossierAdmin(GuardedModelAdmin, WorkflowAdmin, ExportAdmin):
    inlines = (DossierCandidatInline, DiplomeInline, DossierOrigineInline,
               DossierAccueilInline, DossierMobiliteInline,
               DossierConformiteAdmin)
    list_display = (
        'nom', 'prenom', 'naissance_date', 'etat', 'moyenne_votes',
        'action_column'
    )
    list_display_links = ('nom', 'prenom')
    list_filter = (
        AppelFilter, 'etat', 'discipline', 'bureau_rattachement',
        'candidat__pays', RegionOrigineFilter, RegionAccueilFilter
    )
    search_fields = ('appel__nom', 'candidat__nom', 'candidat__prenom',
                     'candidat__nom_jeune_fille', 'discipline__code',
                     'discipline__nom_court', 'discipline__nom_long',
                     'origine__resp_inst_nom', 'origine__resp_inst_prenom',
                     'origine__resp_inst_courriel', 'origine__resp_sc_nom',
                     'origine__resp_sc_prenom', 'origine__resp_sc_courriel',
                     'origine__faculte_nom',
                     'origine__dir_nom', 'origine__dir_prenom',
                     'accueil__resp_sc_nom', 'accueil__resp_sc_prenom',
                     'accueil__resp_sc_courriel',
                     'accueil__faculte_nom',
                     'accueil__dir_nom', 'accueil__dir_prenom',
                     'mobilite__intitule_projet', 'mobilite__mots_clefs',
                     'mobilite__diplome_demande_nom',
    )
    fieldsets = (
        ('État du dossier', {
            'fields': ('etat', 'experts'),
        }),
        ('Situation universitaire', {
            'fields': ('candidat_statut', 'candidat_fonction', ),
        }),
        ('Lien avec l\'AUF', {
            'fields': ('dernier_projet_description', 'dernier_projet_annee',
                       'derniere_bourse_categorie',
                       'derniere_bourse_annee',),
        }),
    )
    actions = [affecter_dossiers_expert]
    filter_horizontal = ['experts']

    class Media:
        js = ('candidatures/dossier.js',)

    def _naissance_date(self, obj):
        return obj.candidat.naissance_date
    _naissance_date.short_description = "Date de naissance"

    def _nationalite(self, obj):
        return obj.candidat.nationalite
    _nationalite.short_description = "Nationalité"

    def action_column(self, obj):
        actions = []
        actions.append(
            "<a href='%s'>Évaluer</a>" % reverse('evaluer', args=(obj.id, ))
        )
        if obj.etat == DOSSIER_ETAT_BOURSIER:
            actions.append(
                "<nobr><a href='%s'>Fiche boursier</a></nobr>" %
                reverse('admin:boursiers_boursier_change', args=(obj.id,))
            )
        return '<br />\n'.join(actions)
    action_column.allow_tags = True
    action_column.short_description = ''

    def _region(self, obj):
        return obj.appel.region
    _region.short_description = "Région"

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'experts':
            kwargs['queryset'] = get_rules().filter_queryset(
                request.user, 'assign', Expert.objects.all()
            )
        return super(DossierAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )

    def get_urls(self):
        admin_urls = super(DossierAdmin, self).get_urls()
        additional_urls = patterns(
            '',
            url(r'^(\d+)/pieces/$',
                self.admin_site.admin_view(self.view_pieces),
                name='candidatures_dossier_pieces'),
            url(r'^(\d+)/pieces/add/$',
                self.admin_site.admin_view(self.view_pieces_add),
                name='candidatures_dossier_pieces_add'),
            url(r'^pieces/(\d+)/$',
                self.admin_site.admin_view(self.view_pieces_change),
                name='candidatures_dossier_pieces_change'),
            url(r'^pieces/(\d+)/delete/$',
                self.admin_site.admin_view(self.view_pieces_delete),
                name='candidatures_dossier_pieces_delete'),
            url(r'^pieces/(\d+)/download/$',
                self.admin_site.admin_view(self.view_pieces_download),
                name='candidatures_dossier_pieces_download'),
        )
        return additional_urls + admin_urls

    def view_pieces(self, request, id):
        dossier = Dossier.objects.get(pk=id)
        pieces_attendues = dict(
            (p.identifiant, {'pieces': [], 'nom': p.nom})
            for p in dossier.appel.pieces_attendues.all()
        )
        pieces_supplementaires = []
        for piece in dossier.pieces.all():
            if piece.identifiant in pieces_attendues:
                pieces_attendues[piece.identifiant]['pieces'].append(piece)
            else:
                pieces_supplementaires.append(piece)
        return render_to_response('admin/candidatures/dossier/pieces.html', {
            'dossier': dossier,
            'pieces_attendues': sorted(pieces_attendues.items()),
            'pieces_supplementaires': pieces_supplementaires,
        }, context_instance=RequestContext(request))

    def view_pieces_add(self, request, dossier_id):
        dossier = get_object_or_404(Dossier, pk=dossier_id)
        if request.method == 'POST':
            form = PieceForm(request.POST, request.FILES,
                             instance=Piece(dossier_id=dossier_id))
            if form.is_valid():
                form.save()
                return redirect(
                    'admin:candidatures_dossier_pieces', dossier_id
                )
        else:
            form = PieceForm(initial={
                'identifiant': request.GET.get('piece', '')
            })
        return render_to_response(
            'admin/candidatures/dossier/piece_form.html',
            {
                'dossier': dossier,
                'form': form
            },
            context_instance=RequestContext(request)
        )

    def view_pieces_change(self, request, piece_id):
        piece = get_object_or_404(Piece, pk=piece_id)
        if request.method == 'POST':
            form = PieceForm(request.POST, request.FILES, instance=piece)
            if form.is_valid():
                form.save()
                return redirect(
                    'admin:candidatures_dossier_pieces', piece.dossier.pk
                )
        else:
            form = PieceForm(instance=piece)
        return render_to_response('admin/sigma/dossier/piece_form.html', {
                'dossier': piece.dossier,
                'form': form
            }, context_instance=RequestContext(request))

    def view_pieces_delete(self, request, piece_id):
        piece = get_object_or_404(Piece, pk=piece_id)
        dossier = piece.dossier
        piece.delete()
        return redirect('admin:candidatures_dossier_pieces', dossier.pk)

    def view_pieces_download(self, request, piece_id):
        piece = get_object_or_404(Piece, pk=piece_id)
        if piece.fichier:
            return sendfile(
                request,
                os.path.join(settings.UPLOADS_ROOT, piece.fichier.name),
                attachment=True,
                attachment_filename=defaultfilters.slugify(piece.fichier.name),
            )
        else:
            raise Http404

    def response_add(self, request, obj, *args, **kwargs):
        """
        Retourne à la liste des dossiers pour l'appel en cours.
        """
        response = super(DossierAdmin, self).response_add(
            request, obj, *args, **kwargs
        )
        if response.status_code == 302 and \
           response['Location'].endswith('../'):
            response['Location'] += '?appel__id__exact=%d' % obj.appel.id
        return response

    def response_change(self, request, obj, *args, **kwargs):
        """
        Retourne à la liste des dossiers pour l'appel en cours.
        """
        response = super(DossierAdmin, self).response_change(
            request, obj, *args, **kwargs
        )
        if response.status_code == 302 and \
           response['Location'].endswith('../'):
            response['Location'] += '?appel__id__exact=%d' % obj.appel.id
        return response


class ExpertAdmin(GuardedModelAdmin):
    list_display = ('nom', 'prenom', '_region', '_disciplines')
    list_display_links = ('nom', 'prenom')
    list_filter = (RegionFilter, 'disciplines')
    search_fields = ('nom', 'prenom', 'courriel')
    fieldsets = (
        (None, {
            'fields': (
                ('prenom', 'nom'),
                'courriel',
                'region',
                'etablissement',
                'disciplines',
                'commentaire',
            )
        }),
    )
    filter_horizontal = ['disciplines']

    def _region(self, obj):
        return obj.region
    _region.short_description = "Région"

    def _disciplines(self, obj):
        return ', '.join([d.nom for d in obj.disciplines.all()])
    _disciplines.short_description = "Disciplines"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'region':
            kwargs['queryset'] = get_rules().filter_queryset(
                request.user, 'manage', ref.Region.objects.all()
            )
        return super(ExpertAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class AttributWCSAdmin(ModelAdmin):
    search_fields = ('dossier__id', )
    list_display = ('_dossier', 'attribut', 'valeur', )

    def _dossier(self, obj):
        return obj.dossier.id


# Admin pour le système d'authentification

GLOBAL_PERMISSIONS = (
    ('gerer_appels', u"Peut gérer les appels d'offres"),
    ('gerer_dossiers', u"Peut gérer les dossiers de candidature"),
    ('gerer_boursiers', u"Peut gérer les boursiers"),
    ('gerer_experts', u"Peut gérer les experts"),
    ('configurer_sigma', u"Peut configurer SIGMA"),
)


class UserForm(DjangoUserForm):
    regions = forms.ModelMultipleChoiceField(
        label=u'Régions',
        queryset=ref.Region.objects.all(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            profile = kwargs['instance'].get_profile()
            profile_data = {'regions': profile.regions.all()}
            initial = kwargs.get('initial')
            if initial:
                profile_data.update(initial)
            kwargs['initial'] = profile_data
        super(UserForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=commit)
        old_save_m2m = getattr(self, 'save_m2m', None)

        def save_m2m():
            if old_save_m2m:
                old_save_m2m()
            profile = user.get_profile()
            profile.regions = self.cleaned_data['regions']
            profile.save()

        if commit:
            save_m2m()
        else:
            self.save_m2m = save_m2m
        return user


class UserAdmin(DjangoUserAdmin):
    form = make_global_permissions_form(UserForm, GLOBAL_PERMISSIONS)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
            ) + tuple(x[0] for x in GLOBAL_PERMISSIONS)
        }),
        ('Groupes', {'fields': ('groups', 'regions')}),
    )
    list_filter = DjangoUserAdmin.list_filter + ('groups', 'profile__regions')


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group


class GroupAdmin(DjangoGroupAdmin):
    form = make_global_permissions_form(GroupForm, GLOBAL_PERMISSIONS)
    fieldsets = (
        (None, {
            'fields': (
                'name',
            ) + tuple(x[0] for x in GLOBAL_PERMISSIONS)
        }),
    )


admin.site.register(AttributWCS, AttributWCSAdmin)
admin.site.register(Appel, AppelAdmin)
admin.site.register(Dossier, DossierAdmin)
admin.site.register(Expert, ExpertAdmin)
admin.site.register(TypeConformite, TypeConformiteAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
