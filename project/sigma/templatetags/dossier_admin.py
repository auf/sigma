# -*- encoding: utf-8 -*-

from django import template
from django.utils.encoding import smart_unicode

from datamaster_modeles.models import Region, Pays

register = template.Library()


@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_region_origine(context):
    return {'title': u"région d'origine",
            'choices': prepare_choices(Region.objects.values_list('id', 'nom'), 'regionorigine', context, remove=['pays'])}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_region_accueil(context):
    return {'title': u"région d'accueil",
            'choices': prepare_choices(Region.objects.values_list('id', 'nom'), 'regionaccueil', context, remove=['pays'])}

@register.inclusion_tag('admin/filter.html', takes_context=True)
def filter_pays(context):
    return {'title': u"pays",
            'choices': prepare_choices(Pays.objects.values_list('code', 'nom'), 'pays', context)}

def prepare_choices(choices, query_param, context, remove=[]):
    request = context['request']
    cl = context['cl']
    query_val = request.GET.get(query_param)
    result = [{'selected': query_val is None,
               'query_string': cl.get_query_string({}, [query_param] + remove),
               'display': 'Tout'}]
    for k, v in choices:
        result.append({'selected': smart_unicode(k) == query_val,
                       'query_string': cl.get_query_string({query_param: k}, remove),
                       'display': v})
    return result
