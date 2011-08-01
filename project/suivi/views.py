# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from sigma.models import Dossier
from models import BoursierCoda, EcritureBoursier

@login_required
def suivi(request, dossier_id):
    dossier = Dossier.objects.get(id=dossier_id)
    elements2 = [e.element2 for e in dossier.elements2.all()]
    
    depenses = EcritureBoursier.objects.using('coda').filter(code__in=elements2).order_by('yr', 'period')
    
    c = {
        'elements2' : elements2,
        'depenses' : depenses,
        'dossier' : dossier,
    }
    return render_to_response("admin/suivi/suivi.html", \
                               Context(c), \
                               context_instance = RequestContext(request))
