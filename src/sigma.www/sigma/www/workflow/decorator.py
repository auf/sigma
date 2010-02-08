# -=- encoding: utf-8 -=-
from django.http import Http404
from django.utils.translation import ugettext as _

from sigma.www import workflow
from sigma.www.models import Candidature, Appel

def userCanEdit(objtype):
    """Décorateur qui teste que l'utilisateur courant peut editer un objet"""
    def decorator(func):
        def inner(request, *args, **kwargs):
            user = request.user
            try:
                object_id = int(kwargs['object_id'])
                ob = objtype.objects.get(id=object_id)
                if not workflow.Manager().can_edit(ob, user):
                    raise Http404(_("Impossible d'editer cet objet"))
            except KeyError:
                pass
            return func(request, *args, **kwargs)
        return inner
    return decorator


def userCanNote(objtype):
    """Décorateur qui teste que l'utilisateur courant peut noter un objet"""
    def decorator(func):
        def inner(request, *args, **kwargs):
            user = request.user
            try:
                if objtype != Candidature:
                    raise Http404(_("Impossible de noter ce type d'objet"))
                object_id = int(kwargs['object_id'])
                ob = objtype.objects.get(id=object_id)
                handler = workflow.Manager().get_handler(ob, user)
                if not handler.can_note(ob):
                    raise Http404(_("Impossible d'editer cet objet"))
            except KeyError:
                pass
            return func(request, *args, **kwargs)
        return inner
    return decorator
