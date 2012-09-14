# -*- coding: utf-8 -*-

from auf.django.permissions import get_rules
from auf.django.references import models as ref
from django.contrib.admin.filterspecs import FilterSpec, RelatedFilterSpec


class RegionFilterSpec(RelatedFilterSpec):
    def __init__(self, f, request, params, model, model_admin,
                 field_path=None):
        super(RegionFilterSpec, self).__init__(f, request, params, model,
                                               model_admin,
                                               field_path=field_path)
        self.lookup_choices = [(r.id, r) for r in get_rules().filter_queryset(
            request.user, 'manage', ref.Region.objects.all()
        )]


class AppelRegionFilterSpec(RelatedFilterSpec):
    def __init__(self, f, request, params, model, model_admin,
                 field_path=None):
        super(AppelRegionFilterSpec, self).__init__(
            f, request, params, model, model_admin, field_path=field_path
        )
        region_ids = [r.id for r in get_rules().filter_queryset(
            request.user, 'manage', ref.Region.objects.all()
        )]
        objs = f.rel.to._default_manager.filter(region__in=region_ids)
        self.lookup_choices = [(o.pk, o) for o in objs]

FilterSpec.filter_specs.insert(
    0,
    (lambda f: bool(f.rel and hasattr(f, 'region_filter_spec')),
     RegionFilterSpec)
)
FilterSpec.filter_specs.insert(
    0,
    (lambda f: bool(f.rel and hasattr(f, 'appelregion_filter_spec')),
     AppelRegionFilterSpec)
)
