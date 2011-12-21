# -*- encoding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from sendfile import sendfile

from auf.django.workflow.admin import WorkflowAdmin
from auf.django.export.admin import ExportAdmin
from datamaster_modeles.models import Region

from sigma.models import *
from sigma.forms import *
from sigma.workflow import DOSSIER_ETAT_BOURSIER
from sigma.customfilterspec import AppelRegionFilterSpec, RegionFilterSpec # Ne pas enlever!


class DossierConformiteAdmin(admin.TabularInline):
    """
    Admin pour spécifier spécifier si la conformité est passée ou non
    """
    form = ConformiteForm
    model = Conformite
    extra = 0
    max_num = 0
    can_delete = False


class TypeConformiteAdmin(admin.ModelAdmin):
    form = TypeConformiteForm


class AppelAdmin(WorkflowAdmin):
    list_display = ('nom', 'region', 'code_budgetaire', 'date_debut_appel', 'date_fin_appel', '_actions', )
    list_filter = ('region', )
    search_fields = ('nom', 'code_budgetaire')
    fieldsets = (
        (None, {
            'fields': (
                'nom',
                'region',
                'code_budgetaire',
                'formulaire_wcs',
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
                'types_piece',
                'etat',
            )
        }),
    )
    filter_horizontal = ['conformites', 'types_piece']

    class Media:
        js = ("js/appel.js",)

    def _actions(self, obj):
        dossiers_url = "<a href='%s?appel=%s'>Voir les dossiers</a>" % (reverse('admin:sigma_dossier_changelist'), obj.id)
        if hasattr(settings, 'WCS_SIGMA_URL') and obj.formulaire_wcs is not None:
            importer_url = "<a href='%s'>Importer</a>" % (reverse('importer_dossiers', args=(obj.formulaire_wcs, )))
            return " | ".join((dossiers_url, importer_url))
        else:
            return dossiers_url
    _actions.allow_tags = True

    def get_form(self, request, obj=None, **kwargs):
        form = super(AppelAdmin, self).get_form(request, obj, **kwargs)
        if form.declared_fields.has_key('region'):
            region_field = form.declared_fields['region']
        else:
            region_field = form.base_fields['region']

        region_ids = [g.region.id for g in request.user.groupes_regionaux.all()]
        region_field.queryset = Region.objects.filter(id__in=region_ids)
        return form

    def has_add_permission(self, request):
        if not request.user.groupes_regionaux.all():
            return False

        return super(AppelAdmin, self).has_add_permission(request)

    def queryset(self, request):
        return Appel.objects.region(request.user)


class BaseDossierFaculteInline(admin.StackedInline):
    max_num = 1
    template = "admin/sigma/edit_inline/single-stack.html"
    can_delete = False


class DossierOrigineInline(BaseDossierFaculteInline):
    model = DossierOrigine
    verbose_name = verbose_name_plural = "Origine (établissement d'inscription ou d'activité à la date de la candidature)"

    fieldsets = (
        (None, {'fields': ('pays', 'etablissement',)}),
        ('Autre établissement si non membre de l\'AUF', {
            'classes': ['collapse'],
            'fields': (('autre_etablissement_nom', 'autre_etablissement_adresse'),
                       ('autre_etablissement_ville', 'autre_etablissement_code_postal'),
                       ('autre_etablissement_region', 'autre_etablissement_pays'))
        }),
        ('Responsable institutionnel à l\'origine', {
            'fields': (('resp_inst_civilite', 'resp_inst_nom', 'resp_inst_prenom'),
                       ('resp_inst_fonction', 'resp_inst_courriel'),
                       ('resp_inst_telephone', 'resp_inst_fax'))
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
    verbose_name = verbose_name_plural = "Accueil (établissement de destination de la mobilité)"

    fieldsets = (
        (None, {'fields': ('pays', 'etablissement',)}),
        ('Autre établissement si non membre de l\'AUF', {
            'classes': ['collapse'],
            'fields': (('autre_etablissement_nom', 'autre_etablissement_adresse'),
                       ('autre_etablissement_ville', 'autre_etablissement_code_postal'),
                       ('autre_etablissement_region', 'autre_etablissement_pays'))
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

class DossierMobiliteForm(forms.ModelForm):
    class Meta:
        model = DossierMobilite

    def clean_date_fin(self):
        date_debut = self.cleaned_data['date_debut']
        date_fin = self.cleaned_data['date_fin']

        if date_debut and date_fin and date_fin < date_debut:
            raise forms.ValidationError("La date de fin doit être après la date de début")

        return date_fin

    def clean_mots_clefs(self):
        mots_clefs = self.cleaned_data['mots_clefs']

        if mots_clefs.count(',') > 2:
            raise forms.ValidationError("Vous avez droit qu'à trois mots clefs séparés avec virgules")

        return mots_clefs


class DossierMobiliteInline(admin.StackedInline):
    form = DossierMobiliteForm
    model = DossierMobilite
    max_num = 1
    template = "admin/sigma/edit_inline/single-stack.html"
    can_delete = False
    verbose_name = verbose_name_plural = "Mobilité"

    fieldsets = (
        ('Période de mobilité', {
            'fields': (('date_debut', 'date_fin'),
                       'duree')
        }),
        ('Dossier scientifique', {
            'fields': ('intitule_projet', 'mots_clefs')
        }),
        ('Disciplines', {
            'fields': (('discipline', 'sous_discipline'),)
        }),
        ('Formation en cours', {
            'fields': (('formation_en_cours_diplome', 'formation_en_cours_niveau'),)
        }),
        ('Diplôme demandé', {
            'fields': ('diplome_demande_nom', 'diplome_demande_niveau')
        }),
        ('Alternance', {
            'fields': (('alternance_nb_mois_origine',
                       'alternance_nb_mois_accueil',
                       'alternance_accueil_puis_origine'),)
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


class DossierCandidatForm(forms.ModelForm):
    class Meta:
        model = Candidat

    def __init__(self, *args, **kwargs):
        super(DossierCandidatForm, self).__init__(*args, **kwargs)
        self.fields['naissance_date'].widget = admin.widgets.AdminTextInputWidget()


class DossierCandidatInline(admin.StackedInline):
    formset = RequiredInlineFormSet
    model = Candidat
    form = DossierCandidatForm

    max_num = 1
    verbose_name = verbose_name_plural = "Identification"
    can_delete = False
    template = "admin/sigma/edit_inline/single-stack.html"

    fieldsets = (
        (None, {
            'fields': ('civilite', ('nom', 'prenom'), 'nom_jeune_fille',
                       'nationalite', 'naissance_date',)
        }),
        ('Coordonnées', {
            'fields': (
                ('adresse', 'adresse_complement'),
                ('ville', 'code_postal'),
                ('region', 'pays'),
                ('telephone', 'telephone_portable'),
                'courriel')
        }),
    )


class DiplomeInline(admin.StackedInline):
    model = Diplome
    max_num = 1
    template = "admin/sigma/edit_inline/single-stack.html"
    verbose_name = verbose_name_plural = "Dernier diplôme obtenu"
    can_delete = False

    fieldsets = (
        (None, {
            'fields': ('nom', 'date', 'niveau', 'etablissement')
        }),
        ('Autre établissement d\'obtention, si non membre de l\'AUF', {
            'classes': ['collapse'],
            'fields': ('autre_etablissement_nom', 'autre_etablissement_pays')
        }),

    )


def affecter_dossiers_expert(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    return HttpResponseRedirect(reverse('affecter_experts_dossiers')+"?ids=%s" % (",".join(selected)))
affecter_dossiers_expert.short_description = 'Assigner expert(s) au(x) dossier(s)'

class DossierAdmin(WorkflowAdmin, ExportAdmin):
    change_list_template = "admin/sigma/dossier_change_list.html"
    inlines = (DossierCandidatInline, DiplomeInline, DossierOrigineInline,
               DossierAccueilInline, DossierMobiliteInline,
               DossierConformiteAdmin)
    list_display = ('appel', 'nom', 'prenom', 'naissance_date', 'etat', 'moyenne_votes', 'action_column')
    list_display_links = ('nom', 'prenom')
    list_filter = ('etat', 'appel', 'discipline', 'bureau_rattachement')
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
        (None, {
            'fields': ('appel', ),
        }),
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


    def _naissance_date(self, obj):
        return obj.candidat.naissance_date
    _naissance_date.short_description = "Date de naissance"

    def _nationalite(self, obj):
        return obj.candidat.nationalite
    _nationalite.short_description = "Nationalité"

    def action_column(self, obj):
        actions = []
        actions.append("<a href='%s'>Évaluer</a>" % reverse('evaluer', args=(obj.id, )))
        if obj.etat == DOSSIER_ETAT_BOURSIER:
            actions.append("<nobr><a href='%s'>Fiche boursier</a></nobr>" %
                           reverse('admin:suivi_boursier_change', args=(obj.id,)))
        return '<br />\n'.join(actions)
    action_column.allow_tags = True
    action_column.short_description = ''

    def _region(self, obj):
        return obj.appel.region
    _region.short_description = "Région"

    def queryset(self, request):
        return Dossier.objects.region(request.user).select_related('appel', 'mobilite', 'candidat')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'experts':
            kwargs['queryset'] = Expert.objects.region(request.user)
        return super(DossierAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(DossierAdmin, self).get_form(request, obj, **kwargs)
        if form.declared_fields.has_key('appel'):
            appel_field = form.declared_fields['appel']
        else:
            appel_field = form.base_fields['appel']

        appel_field.queryset = Appel.objects.region(request.user)
        return form

    def get_urls(self):
        admin_urls = super(DossierAdmin, self).get_urls()
        additional_urls = patterns(
            '',
            url(r'^(\d+)/pieces/$',
                self.admin_site.admin_view(self.view_pieces),
                name='sigma_dossier_pieces'),
            url(r'^(\d+)/pieces/add/$',
                self.admin_site.admin_view(self.view_pieces_add),
                name='sigma_dossier_pieces_add'),
            url(r'^pieces/(\d+)/$',
                self.admin_site.admin_view(self.view_pieces_change),
                name='sigma_dossier_pieces_change'),
            url(r'^pieces/(\d+)/delete/$',
                self.admin_site.admin_view(self.view_pieces_delete),
                name='sigma_dossier_pieces_delete'),
            url(r'^pieces/(\d+)/download/$',
                self.admin_site.admin_view(self.view_pieces_download),
                name='sigma_dossier_pieces_download'),
        )
        return additional_urls + admin_urls

    def view_pieces(self, request, id):
        dossier = Dossier.objects.get(pk=id)
        pieces_attendues = dict((x.nom, []) for x in dossier.appel.types_piece.all())
        pieces_supplementaires = []
        for piece in dossier.pieces.all():
            if piece.nom in pieces_attendues:
                pieces_attendues[piece.nom].append(piece)
            else:
                pieces_supplementaires.append(piece)
        return render_to_response('admin/sigma/dossier/pieces.html', {
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
                return redirect('admin:sigma_dossier_pieces', dossier_id)
        else:
            form = PieceForm(initial={'nom': request.GET.get('piece', '')})
        return render_to_response('admin/sigma/dossier/piece_form.html', {
            'dossier': dossier,
            'form': form
        }, context_instance=RequestContext(request))

    def view_pieces_change(self, request, piece_id):
        piece = get_object_or_404(Piece, pk=piece_id)
        if request.method == 'POST':
            form = PieceForm(request.POST, request.FILES, instance=piece)
            if form.is_valid():
                form.save()
                return redirect('admin:sigma_dossier_pieces', piece.dossier.pk)
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
        return redirect('admin:sigma_dossier_pieces', dossier.pk)

    def view_pieces_download(self, request, piece_id):
        piece = get_object_or_404(Piece, pk=piece_id)
        if piece.fichier:
            return sendfile(request,
                            os.path.join(settings.UPLOADS_ROOT, piece.fichier.name),
                            attachment=True)
        else:
            raise Http404


class ExpertAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', '_region', '_disciplines')
    list_display_links = ('nom', 'prenom')
    list_filter = ('region', 'disciplines')
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

    def queryset(self, request):
        return Expert.objects.region(request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ExpertAdmin, self).get_form(request, obj, **kwargs)
        if form.declared_fields.has_key('region'):
            region_field = form.declared_fields['region']
        else:
            region_field = form.base_fields['region']

        region_ids = [g.region.id for g in request.user.groupes_regionaux.all()]
        region_field.queryset = Region.objects.filter(id__in=region_ids)
        return form

    def _region(self, obj):
        return obj.region
    _region.short_description = "Région"

    def _disciplines(self, obj):
        return ', '.join([d.nom for d in obj.disciplines.all()])
    _disciplines.short_description = "Disciplines"


class GroupeRegionalAdmin(admin.ModelAdmin):
    form = GroupeRegionalAdminForm


class AttributWCSAdmin(admin.ModelAdmin):
    search_fields = ('dossier__id', )
    list_display = ('_dossier', 'attribut', 'valeur', )

    def _dossier(self, obj):
        return obj.dossier.id


admin.site.register(TypePiece)
admin.site.register(AttributWCS, AttributWCSAdmin)
admin.site.register(Appel, AppelAdmin)
admin.site.register(Dossier, DossierAdmin)
admin.site.register(Expert, ExpertAdmin)
admin.site.register(GroupeRegional, GroupeRegionalAdmin)
admin.site.register(TypeConformite, TypeConformiteAdmin)
admin.site.register(NiveauEtude)
admin.site.register(Intervention)
admin.site.register(Public)
