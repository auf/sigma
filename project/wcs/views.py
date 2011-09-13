# -*- encoding: utf-8 -*-

#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
#from django.contrib import messages
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from project.sigma import models as sigma
from wrappers import WCSAppel
from tools import Appel as AppelImporteur

@login_required
def importer_dossiers(request, appel_wcs):
    appel = sigma.Appel.objects.get(formulaire_wcs=appel_wcs)
    importeur = AppelImporteur()
    appel_nom = importeur.wcs.appel_id2txt(appel_wcs)
    module_name =  importeur._safe_module_name(appel_nom)
    mapping = importeur.get_mapping_module(module_name)

    wcs = WCSAppel()
    statut, data = wcs.test(appel_wcs)

    importeur.importer(appel_wcs)

    if statut:
        errors = ()
        champs_traites = [f for f in mapping.MAPPING.keys() if f in data]
        champs_non_traites = [f for f in data if f not in mapping.MAPPING.keys()]
        messages = importeur.messages
    else:
        errors = data

    c = {
        'appel' : appel,
        'statut' : statut,
        'errors' : errors,
        'champs_traites' : champs_traites,
        'champs_non_traites' : champs_non_traites,
        'output' : messages,
    }
    return render_to_response("admin/wcs/importer_dossiers.html", \
                               Context(c), \
                               context_instance = RequestContext(request))
