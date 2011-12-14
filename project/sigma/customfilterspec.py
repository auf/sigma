# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, RelatedFilterSpec
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

class RegionFilterSpec(RelatedFilterSpec):
    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(RegionFilterSpec, self).__init__(f, request, params, model,
                                               model_admin,
                                               field_path=field_path)
        self.lookup_choices = [(g.region.id, g.region) for g in request.user.groupes_regionaux.all()]

class AppelRegionFilterSpec(RelatedFilterSpec):
    def __init__(self, f, request, params, model, model_admin, field_path=None):
        super(AppelRegionFilterSpec, self).__init__(f, request, params,
                                                    model, model_admin,
                                                    field_path=field_path)
        qs = f.rel.to._default_manager.all()
        region_ids = [g.region.id for g in request.user.groupes_regionaux.all()]
        objs = f.rel.to._default_manager.filter(region__in=region_ids)
        self.lookup_choices = [(o.pk, o) for o in objs]

FilterSpec.filter_specs.insert(0, (lambda f: bool(f.rel and hasattr(f, 'region_filter_spec')),
                                   RegionFilterSpec))
FilterSpec.filter_specs.insert(0, (lambda f: bool(f.rel and hasattr(f, 'appelregion_filter_spec')),
                                   AppelRegionFilterSpec))
