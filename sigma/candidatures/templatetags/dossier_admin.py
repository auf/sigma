# -*- encoding: utf-8 -*-

from django import template
from django.utils.encoding import smart_unicode

from auf.django.references.models import Region, Pays

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

@register.inclusion_tag('admin/candidatures/dossier/submit_line.html', takes_context=True)
def dossier_submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    return {
        'onclick_attrib': (opts.get_ordered_objects() and change
                            and 'onclick="submitOrderForm();"' or ''),
        'show_delete_link': (not is_popup and context['has_delete_permission']
                              and (change or context['show_delete'])),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': context['has_add_permission'] and
                            not is_popup and (not save_as or context['add']),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True,
        'full_context': context,
    }

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
