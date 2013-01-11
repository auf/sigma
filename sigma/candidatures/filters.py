# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import Q

from dateutil.relativedelta import relativedelta
import datetime

from auf.django.references import models as ref
# TODO: PERMSS
# from auf.django.permissions import get_rules

from sigma.candidatures.models import Appel, DossierOrigine, DossierAccueil

NULL = u'null'
NOT_NULL = u'not_null'

# Filtres

class EtablissementOrigineFilter(admin.SimpleListFilter):
    title = 'Établissement d\'origine'
    parameter_name = 'etablissement_origine'

    def lookups(self, request, model_admin):
        # TODO: PERMSS
        region_ids = ref.Region.objects.all().values_list('id', flat=True)
        # region_ids = get_rules().filter_queryset(
        #     request.user, 'manage', ref.Region.objects.all()
        # ).values_list('id', flat=True)
        return [
            ('etab_%s' % x[0], x[1]) for x in
            (ref.Etablissement.objects.filter(region__in=region_ids)
             .values_list('id', 'nom'))]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                origine__etablissement=self.value().split('etab_')[1],
                )
        return queryset


class AgeFilter(admin.SimpleListFilter):
    title = 'âge'
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        return [(str('age_%s' % x), str(x)) for x in range(10,110)]

    def queryset(self, request, queryset):
        if self.value():
            today = datetime.date.today()

            # If using integer, field won't auto select after
            # filtering.
            value = int(self.value().split('age_')[1])
            return queryset.filter(
                candidat__naissance_date__gt=(
                    today -
                    relativedelta(years=value + 1)),
                candidat__naissance_date__lte=(
                    today -
                    relativedelta(years=value)
                    ),
                )
            return queryset.filter(appel=self.value())
        else:
            return queryset


class RegionFilter(admin.SimpleListFilter):
    title = 'région'
    parameter_name = 'region'

    def lookups(self, request, model_admin):
        return [
            (unicode(a), b)
            # TODO: PERMSS
            for (a, b) in ref.Region.objects.all().order_by('nom').values_list('id', 'nom')
            # for (a, b) in get_rules().filter_queryset(
            #     request.user,
            #     'manage',
            #     ref.Region.objects.all().order_by('nom')
            # ).values_list('id', 'nom')
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
        # TODO: PERMSS
        region_ids = ref.Region.objects.all().values_list('id', flat=True)
        # region_ids = get_rules().filter_queryset(
        #     request.user, 'manage', ref.Region.objects.all()
        # ).values_list('id', flat=True)
        return [(unicode(a.id), unicode(a)) for a in \
                Appel.objects.filter(region__in=region_ids) ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(appel=self.value())
        else:
            return queryset


class _NullFKFilter(admin.SimpleListFilter):

    def queryset(self, request, queryset):
        v = self.value()
        if v:
            if v == NULL:
                return queryset.filter(Q(**{"%s__isnull" % self.parameter_name:
                    True}))
            else:
                return queryset.filter(Q(**{self.parameter_name: v}))
        else:
            return queryset



class _RegionFilter(_NullFKFilter):
    model = None

    def lookups(self, request, model_admin):
        entries = self.model.objects.\
                select_related('etablissement', 'etablissement__region').\
                filter(etablissement__isnull=False)
        
        regions_existantes = set([d.etablissement.region.code for d in entries])
        regions = ref.Region.objects.\
                filter(code__in=regions_existantes).\
                order_by('nom')
        return [(NULL, u"Sans région spécifiée"), ] + [
            (unicode(a), b)
            for (a, b) in regions.values_list('code', 'nom')
        ]

    def queryset(self, request, queryset):
        etablissement_key = self.parameter_name.split('__region__code')[0]
        v = self.value()
        if v:
            if v == NULL:
                return queryset.filter(Q(**{"%s__isnull" % self.parameter_name:
                    True}) | Q(**{"%s__isnull" % etablissement_key: True}))
            else:
                return queryset.filter(Q(**{self.parameter_name: v}))
        else:
            return queryset


class RegionOrigineFilter(_RegionFilter):
    title = "région d'origine"
    parameter_name = 'origine__etablissement__region__code'
    model = DossierOrigine


class RegionAccueilFilter(_RegionFilter):
    title = "région d'accueil"
    parameter_name = 'accueil__etablissement__region__code'
    model = DossierAccueil


class _PaysFilter(_NullFKFilter):
    model = None

    def queryset(self, request, queryset, implantation=None):
        pcode = request.GET.get('pays_%s' % implantation, None)
        if pcode:
            if pcode == NULL:
                return queryset.filter(
                    Q(**{'%s__etablissement__pays__isnull' %
                         implantation: True}) and
                    Q(**{'%s__autre_etablissement_pays__isnull' %
                         implantation: True})
                    )
            elif pcode == NOT_NULL:
                return queryset.exclude(
                    Q(**{'%s__etablissement__pays__isnull' %
                         implantation: True}) or
                    Q(**{'%s__autre_etablissement_pays__isnull' %
                         implantation: True})
                    )
            return queryset.filter(
                Q(**{'%s__etablissement__pays' %
                     implantation: pcode}) or
                Q(**{'%s__autre_etablissement_pays' %
                     implantation: pcode}))

    def lookups(self, request, model_admin):
        pays_existants = set(
            [x[0] for x in
             self.model.objects.values_list('etablissement__pays')
             if x[0]
             ]).union(
            set([x[0] for x in
                 self.model.objects.values_list('autre_etablissement_pays')
                 if x[0]
                 ]))

        pays = ref.Pays.objects.filter(code__in=pays_existants)
        return [
            (NULL, u"Sans pays spécifié"),
            (NOT_NULL, u"Avec pays spécifié"),
            ] + [
            (unicode(a), b)
            for (a, b) in pays.values_list('code', 'nom')
        ]


class PaysOrigineFilter(_PaysFilter):
    title = "pays d'origine"
    parameter_name = 'pays_origine'
    model = DossierOrigine

    def queryset(self, request, queryset):
        return super(PaysOrigineFilter, self).queryset(
            request, queryset, 'origine')


class PaysAccueilFilter(_PaysFilter):
    title = "pays d'accueil"
    parameter_name = 'pays_accueil'
    model = DossierAccueil

    def queryset(self, request, queryset):
        return super(PaysAccueilFilter, self).queryset(
            request, queryset, 'accueil')


