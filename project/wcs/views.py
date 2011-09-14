# -*- encoding: utf-8 -*-

from django.contrib import messages
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from project.sigma import models as sigma
from wrappers import WCSAppel
from tools import Appel as AppelImporteur
from models import Spool

@login_required
def importer_dossiers(request, appel_wcs):
    appel = sigma.Appel.objects.get(formulaire_wcs=appel_wcs)


    derniere_preparation = None
    started = False
    for spool in  appel.spools.all().order_by('-id'):
        if spool.requesting:
            started = True
        if derniere_preparation is None and \
             spool.date_requesting_debut is not None and \
             spool.date_requesting_fin is not None:
             derniere_preparation = spool

    # Lancer la récupération des données distantes et tester l'import
    if request.GET.get('action', '') == 'preparer':
        if started:
            messages.add_message(request, messages.INFO, 'Une préparation est déjà en cours.')
        else:
            messages.add_message(request, messages.INFO, 'La préparation a bien été demandée.')
            
            Spool(appel=appel).preparer()
        return redirect('importer_dossiers', appel_wcs)
     
    # Lancer la récupération des données distantes et effectuer l'import
    if request.GET.get('action', '') == 'importer':
        if derniere_preparation is None:
            messages.add_message(request, messages.ERROR, "Aucune importation n'est préparée.")
        elif derniere_preparation.processing:
            messages.add_message(request, messages.INFO, "L'importation est en cours.")
        else:  
            messages.add_message(request, messages.INFO, "L'importation a bien été demandée.")
            derniere_preparation.demander()
        return redirect('importer_dossiers', appel_wcs)
       

    c = {
        'appel' : appel,
        'derniere_preparation' : derniere_preparation,
        'spools' : appel.spools.all(),
    }
    return render_to_response("admin/wcs/importer_dossiers.html", \
                               Context(c), \
                               context_instance = RequestContext(request))
