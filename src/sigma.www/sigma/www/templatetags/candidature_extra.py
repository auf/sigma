# -=- encoding: utf-8 -=-
from django import template
from django.contrib.auth.models import User

from sigma.www import workflow
from sigma.www.models import Candidature, Appel

register = template.Library()

def is_valid(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_valid(candidature, user)
register.filter('is_valid', is_valid)

def is_invalid(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return not is_valid(user, candidature)
register.filter('is_invalid', is_invalid)

def can_note_candidature(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    handler = workflow.Manager().get_handler(candidature, user)
    return handler.can_note(candidature)
register.filter('can_note_candidature', can_note_candidature)

def can_edit_candidature(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().can_edit(candidature, user)
register.filter('can_edit_candidature', can_edit_candidature)

def can_delete_candidature(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    if candidature == 'Supprime':
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Supprimer')
register.filter('can_delete_candidature', can_delete_candidature)

def can_add_candidature(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return workflow.Manager().can_add(Candidature, user, appel)
register.filter('can_add_candidature', can_add_candidature)

def can_rejete(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Rejeter')
register.filter('can_rejete', can_rejete)

def can_accepte(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Accepter')
register.filter('can_accepte', can_accepte)

def can_classe(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Classer')
register.filter('can_classe', can_classe)

def can_declasse(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Declasser')
register.filter('can_declasse', can_declasse)

def can_select(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Selectionner')
register.filter('can_select', can_select)

def can_attend(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Attendre')
register.filter('can_attend', can_attend)

def can_reveille(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Reveiller')
register.filter('can_reveille', can_reveille)

def can_desiste(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Desister')
register.filter('can_desiste', can_desiste)

def can_bourse(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Boursier')
register.filter('can_bourse', can_bourse)

def can_complete(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_reacheable(candidature, user, 'Completer')
register.filter('can_complete', can_complete)

def can_revert(user, candidature):
    if not isinstance(user, User):
        return False
    if not isinstance(candidature, Candidature):
        return False
    return workflow.Manager().is_undoable(candidature, user)
register.filter('can_revert', can_revert)
