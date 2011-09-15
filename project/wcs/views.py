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
    requesting = False
    processing = False
    diff_champs = None

    spools = appel.spools.all().order_by('-id')

    if len(spools) > 0:
        spool = spools[0]
        if spool.requesting:
            requesting = True
        if spool.processing:
            processing = True
        if spool.date_requesting_debut is not None and \
             spool.date_requesting_fin is not None:
             derniere_preparation = spool
             diff_champs = spool.diff_champs()

    # Lancer la récupération des données distantes et tester l'import
    if request.GET.get('action', '') == 'preparer':
        if requesting:
            messages.add_message(request, messages.INFO, 'Une préparation est déjà en cours.')
        else:
            messages.add_message(request, messages.INFO, 'La préparation a bien été demandée.')
            
            Spool(appel=appel).preparer()
        return redirect('importer_dossiers', appel_wcs)
     
    # Lancer la récupération des données distantes et effectuer l'import
    if request.GET.get('action', '') == 'importer':
        if derniere_preparation is None or derniere_preparation.date_requesting_fin is None:
            messages.add_message(request, messages.ERROR, "Aucune importation n'est préparée.")
        if derniere_preparation is not None and derniere_preparation.processing:
            messages.add_message(request, messages.INFO, "L'importation est en cours.")
        if derniere_preparation is not None and derniere_preparation.date_requesting_fin is not None:
            messages.add_message(request, messages.INFO, "L'importation a bien été demandée.")
            derniere_preparation.demander()

        return redirect('importer_dossiers', appel_wcs)
       

    c = {
        'appel' : appel,
        'requesting' : requesting,
        'processing' : processing,
        'derniere_preparation' : derniere_preparation,
        'spools' : spools,
        'diff_champs' : diff_champs,
    }
    return render_to_response("admin/wcs/importer_dossiers.html", \
                               Context(c), \
                               context_instance = RequestContext(request))
