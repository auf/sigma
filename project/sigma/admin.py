# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import admin
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
    list_display = ('id', 'name', 'field_type',  )
    form = TypeConformiteForm

class ProxyAppelConformite(Appel.conformites.through):
    """
    Ce proxy sert uniquement dans l'admin à disposer d'un libellé
    plus ergonomique.
    """

    class Meta:
        proxy=True
        verbose_name = u"Type de conformité"
        verbose_name_plural = u"Conformités demandées pour cet appel"

    def __unicode__(self,):
        return u"code conformité #%s" % self.id

class TypeConformiteInline(admin.TabularInline):
    """
    Association des types de conformité à un appel.
    """
    fields = ('typeconformite', )
    model = ProxyAppelConformite
    extra = 0
    verbose_name = u"Type de conformités"
    verbose_name_plural = u"Conformités demandées pour cet appel"

class TypePieceInline(admin.TabularInline):
    """
    Association des types de pièce à un appel.
    """
    model = Appel.types_piece.through
    extra = 0
    verbose_name = u"Type de pièce"
    verbose_name_plural = u"Type de pièce demandées pour cet appel"

class AppelAdmin(WorkflowAdmin):
    inlines = (TypeConformiteInline, TypePieceInline)
    list_display = ('nom', 'region', 'code_budgetaire', 'date_debut_appel', 'date_fin_appel', 'etat', '_actions', )
    list_filter = ('region', 'etat')
    search_fields = ('nom', 'code_budgetaire')
    fieldsets = (
        (None, {'fields': ('nom',
        'region',
        'code_budgetaire',
        'formulaire_wcs',
        ('date_debut_appel', 'date_fin_appel'),
        ('date_debut_mobilite', 'date_fin_mobilite'),
        'periode',
        'bareme',
        ('montant_mensuel_origine_sud', 'montant_mensuel_origine_nord'),
        ('montant_mensuel_accueil_sud', 'montant_mensuel_accueil_nord'),
        'montant_prime_installation',
        ('montant_perdiem_sud', 'montant_perdiem_nord'),
        'montant_allocation_unique',
        'appel_en_ligne',
        'etat',
        )}),)

    def _actions(self, obj):
        dossiers_url = "<a href='%s?appel__id__exact=%s'>Voir les dossiers</a>" % (reverse('admin:sigma_dossier_changelist'), obj.id)
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
    template = "admin/sigma/edit_inline/stacked.html"
    fieldsets = (
        (None, {'fields': ('pays', 'etablissement',)}),
        ('Autre établissement', {
            'classes': ['collapse'],
            'fields': (('autre_etablissement_nom', 'autre_etablissement_adresse'),
                       ('autre_etablissement_ville', 'autre_etablissement_code_postal'),
                       ('autre_etablissement_region', 'autre_etablissement_pays'))
        }),
        ('Responsable institutionnel', {
            'fields': (('resp_inst_civilite', 'resp_inst_nom', 'resp_inst_prenom'),
                       ('resp_inst_courriel', 'resp_inst_fonction'),
                       ('resp_inst_telephone', 'resp_inst_fax'))
        }),
        ('Responsable scientifique', {
            'fields': (('resp_sc_civilite', 'resp_sc_nom', 'resp_sc_prenom'),
                       ('resp_sc_courriel', 'resp_sc_fonction'),
                       ('resp_sc_telephone', 'resp_sc_fax'))
        }),
        ('Faculté', {
            'fields': ('faculte_nom',
                       ('faculte_url', 'faculte_courriel'),
                       ('faculte_adresse', 'faculte_ville', 'faculte_code_postal'),
                       ('faculte_telephone', 'faculte_fax'))
        }),
    )


class DossierOrigineInline(BaseDossierFaculteInline):
    model = DossierOrigine
    verbose_name = verbose_name_plural = "Origine"


class DossierAccueilInline(BaseDossierFaculteInline):
    model = DossierAccueil
    verbose_name = verbose_name_plural = "Accueil"


class DossierMobiliteForm(forms.ModelForm):
    class Meta:
        model = DossierMobilite

    def clean_date_fin(self):
        date_debut = self.cleaned_data['date_debut']
        date_fin = self.cleaned_data['date_fin']

        if date_fin < date_debut:
            raise forms.ValidationError("La date de fin doit être après la date de début")

        return date_fin


class DossierMobiliteInline(admin.StackedInline):
    form = DossierMobiliteForm
    model = DossierMobilite
    max_num = 1
    template = "admin/sigma/edit_inline/stacked.html"
    verbose_name = verbose_name_plural = "Mobilité"

    fieldsets = (
        ('Période de mobilité', {
            'fields': (('date_debut', 'date_fin'),
                       'duree')
        }),
        ('Dossier scientifique', {
            'fields': ('intitule_projet', 'mots_clefs')
        }),
        ('Formation en cours', {
            'fields': (('formation_en_cours_diplome', 'formation_en_cours_niveau'),)
        }),
        ('Programme de mission', {
            'fields': ('type_intervention', 'public_vise', 'autres_publics')
        }),
        ('Disciplines', {
            'fields': (('discipline', 'sous_discipline'),)
        }),
        ('Alternance', {
            'fields': (('alternance_nb_mois_origine',
                       'alternance_nb_mois_accueil',
                       'alternance_accueil_puis_origine'),)
        }),
        ('Diplôme demandé', {
            'fields': ('diplome_demande_nom', 'diplome_demande_niveau')
        }),
        ('Thèse', {
            'fields': ('these_date_inscription',
                       'these_date_obtention_prevue',
                       'these_soutenance_pays',
                       'these_soutenance_date',
                       'these_type',
                       'these_type_autre')
        }),
        ('Directeur thèse accueil', {
            'fields': (('dir_acc_civilite', 'dir_acc_nom', 'dir_acc_prenom'),)
        }),
        ('Directeur thèse origin', {
            'fields': (('dir_ori_civilite', 'dir_ori_nom', 'dir_ori_prenom'),)
        })
    )


class DossierCandidatInline(admin.StackedInline):
    formset = RequiredInlineFormSet
    model = Candidat
    max_num = 1
    verbose_name = verbose_name_plural = "Identification"

    fieldsets = (
        (None, {
            'fields': (('civilite', 'nom', 'prenom'), 'nom_jeune_fille',
                       'nationalite', 'naissance_ville', 'naissance_date',)
        }),
        ('Coordonnées', {
            'fields': (
                'adresse',
                ('ville', 'code_postal'),
                ('region', 'pays'),
                ('telephone_perso', 'courriel_perso'),
                ('telephone_pro', 'courriel_pro'))
        }),
    )

class DiplomeInline(admin.StackedInline):
    model = Diplome
    max_num = 1
    template = "admin/sigma/edit_inline/stacked.html"
    verbose_name = verbose_name_plural = "Diplômes"

    fieldsets = (
        (None, {
            'fields': ('nom', 'date', 'niveau', 'etablissement')
        }),
        ('Autre établissement', {
            'classes': ['collapse'],
            'fields': ('autre_etablissement_nom', 'autre_etablissement_pays')
        }),

    )
    
class PieceInline(admin.TabularInline):
    model = Piece
    extra = 0
    verbose_name = u"Pièce jointe"
    verbose_name_plural = u"Pièces jointes"
    
class ProxyExpert(Expert.dossiers.through):
    """
    Ce proxy sert uniquement dans l'admin à disposer d'un libellé
    plus ergonomique.
    """

    class Meta:
        proxy=True
        verbose_name = u"Expert"
        verbose_name_plural = u"Experts"

    def __unicode__(self):
        return u""

class ExpertInline(admin.TabularInline):
    model = ProxyExpert
    extra = 0
    max_num = 0
    verbose_name = u"Expert"
    verbose_name_plural = u"Experts"


def affecter_dossiers_expert(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    return HttpResponseRedirect(reverse('affecter_experts_dossiers')+"?ids=%s" % (",".join(selected)))
affecter_dossiers_expert.short_description = 'Assigner expert(s) au(x) dossier(s)'
    
class DossierAdmin(WorkflowAdmin, ExportAdmin):
    change_list_template = "admin/sigma/dossier_change_list.html"
    inlines = (DossierCandidatInline, DiplomeInline, DossierOrigineInline, DossierAccueilInline, DossierMobiliteInline, DossierConformiteAdmin, PieceInline, ExpertInline)
    list_display = ('id', 'nom', 'prenom', '_naissance_date', '_nationalite', 'discipline', 'etat', 'appel', 'moyenne_votes', '_evaluer', '_fiche_boursier' )
    list_display_links = ('nom', 'prenom')
    list_filter = ('etat', 'appel', 'discipline', 'bureau_rattachement')
    search_fields = ('appel__nom',
                     'candidat__nom', 'candidat__prenom', 'candidat__nom_jeune_fille',
                     'discipline__code', 'discipline__nom_court', 'discipline__nom_long',
                     'origine__resp_inst_nom', 'origine__resp_inst_prenom', 'origine__resp_inst_courriel', 'origine__resp_sc_nom', 'origine__resp_sc_prenom', 'origine__resp_sc_courriel', 'origine__faculte_nom', 'origine__faculte_courriel',
                     'accueil__resp_inst_nom', 'accueil__resp_inst_prenom', 'accueil__resp_inst_courriel', 'accueil__resp_sc_nom', 'accueil__resp_sc_prenom', 'accueil__resp_sc_courriel', 'accueil__faculte_nom', 'accueil__faculte_courriel',
                     'mobilite__intitule_projet', 'mobilite__mots_clefs', 'mobilite__diplome_demande_nom', 'mobilite__dir_acc_nom', 'mobilite__dir_acc_prenom', 'mobilite__dir_ori_nom', 'mobilite__dir_ori_prenom',
    )
    fieldsets = (
        (None, {
            'fields': ('appel', ),
        }),
        ('État du dossier', {
            'fields': ('etat', ),
        }),
        ('Situation universitaire', {
            'classes': ('collapse',),
            'fields': ('candidat_statut', 'candidat_fonction', ),
        }),
        ('Lien avec l\'AUF', {
            'classes': ('collapse',),
            'fields': ('dernier_projet_description', 'dernier_projet_annee', 'derniere_bourse_categorie', 'derniere_bourse_annee',),
        }),
    )
    
    actions = [affecter_dossiers_expert]

    
    def _naissance_date(self, obj):
        return obj.candidat.naissance_date
    _naissance_date.short_description = "Date de naissance"
    
    def _nationalite(self, obj):
        return obj.candidat.nationalite
    _nationalite.short_description = "Nationalité"
    
    def _evaluer(self, obj):
        return "<a href='%s'>Évaluer</a>" % reverse('evaluer', args=(obj.id, ))
    _evaluer.allow_tags = True
    _evaluer.short_description = 'Évaluation'
    
    def _fiche_boursier(self, obj):
		if obj.etat == DOSSIER_ETAT_BOURSIER:
			return "<a href='%s'>Fiche boursier</a>" % reverse(
				'admin:suivi_boursier_change', args=(obj.id,)
			)
		else:
			return ''
    _fiche_boursier.allow_tags = True
    _fiche_boursier.short_description = ''

    def _region(self, obj):
        return obj.appel.region
    _region.short_description = "Région"

    def queryset(self, request):
        return Dossier.objects.region(request.user).select_related('appel', 'mobilite', 'candidat')

    def get_form(self, request, obj=None, **kwargs):
        form = super(DossierAdmin, self).get_form(request, obj, **kwargs)
        if form.declared_fields.has_key('appel'):
            appel_field = form.declared_fields['appel']
        else:
            appel_field = form.base_fields['appel']

        appel_field.queryset = Appel.objects.region(request.user)
        return form

class ExpertAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', '_region', '_disciplines')
    list_filter = ('region', 'disciplines')
    search_fields = ('nom', 'prenom', 'courriel')
    exclude = ('dossiers',)

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
