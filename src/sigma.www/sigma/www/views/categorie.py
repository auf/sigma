from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

from sigma.www.models import Appel, Candidature, ProjetPoste, Categorie, BlocChamps
from sigma.www.views.appel import statut_list_app
from sigma.www.utils import render_to_response
from sigma.www.workflow import exporter

def liste(request, criteria='', value=''):
    """Obtention et affichage de liste des categories et leurs appels d'offres

    @param request
    @param criteria
    @param value
    """
    user = request.user
    categorie_list = Categorie.objects.all().order_by('-id')
    categories = {}

    for categorie in categorie_list:
        app_list_length = len(Appel.objects.filter(projetposte__code_poste__id=categorie.poste.id))
        categories[categorie] = app_list_length
    return render_to_response(request,
                              "sigma.www/categorie_list.html",                               
                              { 'categorie_list': categories,
                                "criteria": criteria,
                                "value" : value,
                                "type": "categories"})


def detail(request, object_id=None):
    """Affichage des details de la categorie et de ses parametres
    
    @param request 
    @param object_id
    """
    categorie = get_object_or_404(Categorie, pk=object_id)
    blocs_dict = {}
    blocs = BlocChamps.objects.filter(categorie=object_id)
    for bloc in blocs:
        blocs_dict[bloc] = ChampsCategorie.objects.filter(bloc=bloc.id)
    return  render_to_response(request,
                               'sigma.www/categorie_detail.html',
                               {"categorie" : categorie,
                                "blocs_list" : blocs_dict,
                                })


def export(request, object_id):
    """Exportation d'une categorie vers le format ods

    @param request
    @param object_id
    """
    categorie = get_object_or_404(Categorie, pk=object_id)
    user = request.user

    export = exporter.GenericODSExporter(categorie, user)()

    response = HttpResponse(export, mimetype="application/vnd.oasis.opendocument.spreadsheet")
    response['Content-Disposition'] = 'attachment; filename=%s.ods' \
        % str(categorie).replace(" ","_")
    return response


def json(request, object_id=None):
    """Expertation des donnees d'une categorie par json
    
    @param request
    @param object_id
    """
    categorie = None
    if object_id is not None:
        categorie = get_object_or_404(Categorie, pk=object_id)
    else:
        categorie = Categorie()

    json = serializers.serialize('json', [categorie],
                                 fields=Categorie.serialisable_fields)
    return HttpResponse(json)
