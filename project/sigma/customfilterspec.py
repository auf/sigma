# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.admin.filterspecs import FilterSpec
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _

class RegionFilterSpec(FilterSpec):
    def __init__(self, f, request, params, model, model_admin):
        super(RegionFilterSpec, self).__init__(f, request, params, model, model_admin)
        self.lookup_val = request.GET.get(f.name, None)
        if isinstance(f, models.ManyToManyField):
            self.lookup_title = f.rel.to._meta.verbose_name
        else:
            self.lookup_title = f.verbose_name

        # Queryset
        qs = f.rel.to._default_manager.all()

        region_ids = [g.region.id for g in request.user.groupes_regionaux.all()]
        qs = qs.filter(id__in=region_ids)

        self.lookup_choices = qs.all()

    def title(self):
        return self.lookup_title

    def choices(self, cl):
        if self.lookup_choices.count() > 1:
            yield {'selected': self.lookup_val is None,
                   'query_string': cl.get_query_string({}, [self.field.name]),
                   'display': _('All')}
        for inst in self.lookup_choices:
            val = smart_unicode(inst.pk)
            yield {'selected': self.lookup_val == val,
                   'query_string': cl.get_query_string({self.field.name: val}),
                   'display': smart_unicode(inst)}

FilterSpec.filter_specs.insert(0, (lambda f: bool(f.rel and hasattr(f, 'region_filter_spec')), RegionFilterSpec))
