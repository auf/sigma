from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from sigma.www import workflow
from sigma.www.models import Appel, Candidature

register = template.Library()

def can_export_candidatures_appel(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return len(Candidature.objects.filter(appel=appel)) != 0
register.filter('can_export_candidatures_appel', can_export_candidatures_appel)

def can_export_appel(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return True
register.filter('can_export_appel', can_export_appel)

def can_add_appel(user):
    if not isinstance(user, User):
        return False
    return workflow.Manager().can_add(Appel, user)
register.filter('can_add_appel', can_add_appel)

def can_edit_appel(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return workflow.Manager().can_edit(appel, user)
register.filter('can_edit_appel', can_edit_appel)

def can_ouvre(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return workflow.Manager().is_reacheable(appel, user, "Ouvrir")
register.filter('can_ouvre', can_ouvre)

def can_supprime(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return workflow.Manager().is_reacheable(appel, user, "Supprimer")
register.filter('can_supprime', can_supprime)
    
def can_analyse(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return workflow.Manager().is_reacheable(appel, user, "Analyser")
register.filter('can_analyse', can_analyse)

def can_evalue(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return workflow.Manager().is_reacheable(appel, user, "Evaluer")
register.filter('can_evalue', can_evalue)

def can_selectionne(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return workflow.Manager().is_reacheable(appel, user, "Selectionner")
register.filter('can_selectionne', can_selectionne)

def can_notifie(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return workflow.Manager().is_reacheable(appel, user, "Notifier")
register.filter('can_notifie', can_notifie)

def can_suit(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return workflow.Manager().is_reacheable(appel, user, "Suivre")
register.filter('can_suit', can_suit)

def can_ferme(user, appel):
    if not isinstance(user, User):
        return False
    if not isinstance(appel, Appel):
        return False
    return workflow.Manager().is_reacheable(appel, user, "Fermer")
register.filter('can_ferme', can_ferme)
