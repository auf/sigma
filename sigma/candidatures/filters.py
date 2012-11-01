# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import Q

from auf.django.references import models as ref
from auf.django.permissions import get_rules

from sigma.candidatures.models import Appel, DossierOrigine, DossierAccueil

NULL = u'null'

# Filtres

class RegionFilter(admin.SimpleListFilter):
    title = 'région'
    parameter_name = 'region'

    def lookups(self, request, model_admin):
        return [
            (unicode(a), b)
            for (a, b) in get_rules().filter_queryset(
                request.user,
                'manage',
                ref.Region.objects.all().order_by('nom')
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

    def lookups(self, request, model_admin):
        pays_existants = set([dic['pays'] for dic in
                self.model.objects.values('pays')])
        pays = ref.Pays.objects.filter(code__in=pays_existants)
        return [(NULL, u"Sans pays spécifié"), ] + [
            (unicode(a), b)
            for (a, b) in pays.values_list('code', 'nom')
        ]

class PaysOrigineFilter(_PaysFilter):
    title = "pays d'origine"
    parameter_name = 'origine__pays'
    model = DossierOrigine


class PaysAccueilFilter(_PaysFilter):
    title = "pays d'accueil"
    parameter_name = 'accueil__pays'
    model = DossierAccueil
