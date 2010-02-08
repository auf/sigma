from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template import defaulttags, VariableDoesNotExist, Variable

from sigma.www import workflow
from sigma.www.models import Appel

register = template.Library()

def is_mandatory(field):
    """
    @param field
    """
    return not(field.blank) or not(field.null)
register.filter('is_mandatory', is_mandatory)

def getattr(obj, arg):
    """ Try to get an attribute from an object.

    @param obj
    @param arg
    """
    try:
        return arg.rel.to.objects.get(id=arg.value_from_object(obj))
    except AttributeError:
        if arg.get_internal_type() == "BooleanField":
             if obj.__getattribute__(arg.name) == 0:
                 return 'False'
             return 'True'
        return obj.__getattribute__(arg.name)
    except ObjectDoesNotExist:
        return ""

register.filter('getattr', getattr)

def status_is(ob, status):
    """Check if the current status of an object is 
    the one we expect

    @param ob
    @param status
    """
    return ob.statut == status
register.filter('status_is', status_is)
