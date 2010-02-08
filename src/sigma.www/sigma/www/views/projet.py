# -=- encoding: utf-8 -=-
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

from sigma.www.models import Appel, Candidature, ProjetPoste, Categorie, ChampsCategorie, BlocChamps
from sigma.www.utils import render_to_response
from sigma.www.workflow import exporter

def list(request, criteria='', value=''):
    """Obtention de la liste de tout les projetposte accessible a l'utilisateur"""
    user = request.user
    ppostes = ProjetPoste.all(user, criteria, value)

    return render_to_response(request,
                              "sigma.www/projet_list.html",
                              { 'object_list': ppostes,
                                'criteria' : criteria,
                                'value' : value,
                                "type" : "projets"})

def detail(request, object_id):
    """Obtention des details d'un projet poste"""
    p = get_object_or_404(ProjetPoste, pk=object_id)
    user = request.user

    return render_to_response(request,
                              "sigma.www/projet_detail.html",
                              {"projet":  p})
                               
                              
def export(request, object_id=None):
    """Exporation d'un projet vers le format ods"""
    user = request.user
    projet = None

    if object_id:
        projet = get_object_or_404(ProjetPoste, pk=object_id)
    else:
        projet = ProjetPoste.objects.all()

    export = exporter.GenericODSExporter(projet, user)
    
    response = HttpResponse(export(), mimetype="application/vnd.oasis.opendocument.spreadsheet")
    response['Content-Disposition'] = 'attachment; filename=%s' % export.getFilename()

    return response


def export_search(request, value):
    """Exportation d'un projet vers le format ods"""
    user = request.user
    projet = None

    projet = ProjetPoste.search(user, value)

    export = exporter.GenericODSExporter(projet, user)
    
    response = HttpResponse(export(), mimetype="application/vnd.oasis.opendocument.spreadsheet")
    response['Content-Disposition'] = 'attachment; filename=%s' % export.getFilename()

    return response


def categorie_json(request, object_id):
    projet_post = get_object_or_404(ProjetPoste, pk=object_id)
    categorie = get_object_or_404(Categorie, pk=projet_post.getCategorie().id)
    
    categorie_json = serializers.serialize('json', [categorie], 
                                           fields=Categorie.serialisable_fields)
    return HttpResponse(categorie_json)

