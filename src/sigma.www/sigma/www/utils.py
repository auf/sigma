# -=- encoding: utf-8 -=-
from django.template import loader, Context
from django.shortcuts import render_to_response
from django.utils.timesince import timesince
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from sigma.www.forms.general import SearchForm
from sigma.www.templatetags import general_extra

from datetime import date

import re
import unicodedata

def is_displaying_login(request, template):
    """Est-ce qu'on doit afficher la boite de connexion ?

    @param request La requete actuelle
    @param template Le template a charger
    """
    return not(template == "sigma.www/login.html" \
               or request.user.is_authenticated())
    

def render_to_response(request, template, params):
    """Nouveau renderer de reponses qui ajoute les parametres de recherche
   
    @param request
    @param template
    @param params
    """
    t = loader.get_template(template)
    params.update({
        'app'        : 'Sigma',
        'user'       : request.user,
        'ip_address' : request.META['REMOTE_ADDR'],
        'search_form': SearchForm(),
        'request'    : request,
        'displaying_login' : is_displaying_login(request, template),
        })
    c = Context(params)
    return HttpResponse(t.render(c))
    

def calculateAge(born, seed=date.today(), months=False):
    """Calculate the age of a user.

    @param born Start date
    @param seed End date (default is today)
    @param months if yes calculate the age in months and if not in years
    """
    age_since = timesince(born, seed)

    years = re.compile("([\d]*) year").search(age_since)

    if months:
        age = 0
        months = re.compile("([\d]*) month").search(age_since)
        if years is not None:
           age += int(years.groups(0)[0])*12
        if months is not None:
            age += int(months.groups(0)[0])
        return age
    else:
        try:
            return int(years.groups(0)[0])
        except AttributeError:
            return 0


def remove_accents(chaine):
    """Enleves les accents des chaines de caracteres

    @param chaine La chaine a nettoyer
    """
    nkfd_form = unicodedata.normalize('NFKD', unicode(chaine))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


def getSubjectList(p):
    """Obtention des differents sujets et des fields associes a chacun
    pour les objets du model

    @param p L'objet du model duquel on veut extraire les 
             informations sur le sujet
    """
    obj = p
    subject_list = {}
    for field in p._meta.fields:
        if field.subject not in subject_list:
            subject_id = mark_safe(remove_accents(field.subject.replace(" ", "_").replace("'", "_").replace(".", "")))
            subject_list[field.subject] = [subject_id, field.subject, [], False]
        if field.name not in ['id', 'workflowobject_ptr', 'actif', 'statut']:
            subject_list[field.subject][2].append(field)
        if general_extra.getattr(p, field):
            subject_list[field.subject][3] = True
    return subject_list
