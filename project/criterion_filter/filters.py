# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.admin.filterspecs import FilterSpec, ChoicesFilterSpec
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class RangeValuesFilterSpec(FilterSpec):
    """
    Adds filtering by ranges of values in the admin filter sidebar.
    Set range split points in the model field attribute 'list_filter_range'.
    
    my_model_field.list_filter_range = [100, 200, 300]
    
    Will define the ranges:
      my_model_field < 100
      my_model_field >= 100 AND my_model_field < 200
      my_model_field >= 200 AND my_model_field < 300
      my_model_field >= 300    
    """

    def __init__(self, f, request, params, model, model_admin):
        super(RangeValuesFilterSpec, self).__init__(f, request, params, model, model_admin)
        self.field_generic = '%s__' % self.field.name
        self.parsed_params = dict([(k, v) for k, v in params.items() if k.startswith(self.field_generic)])

        self.links = [(_('All'), {})]
        
        last_value = None
        for max_value in sorted(f.list_filter_range):
            max_value = str(max_value)
            if last_value == None:
                label = '&lt; ' + max_value
                range = {'%s__lt' % f.name: max_value}
            else:
                label = last_value + ' - ' + max_value
                range = {'%s__gte' % self.field.name: last_value, '%s__lt' % f.name: max_value}
            self.links.append((_(mark_safe(label)), range))
            last_value = max_value
        self.links.append((_(mark_safe('&ge; ' + max_value)), {'%s__gte' % f.name: max_value}))

    def choices(self, cl):
        for title, param_dict in self.links:
            yield {'selected': self.parsed_params == param_dict,
                   'query_string': cl.get_query_string(param_dict, [self.field_generic]),
                   'display': title}

FilterSpec.filter_specs.insert(0, (lambda f: hasattr(f, 'list_filter_range'), RangeValuesFilterSpec))
