from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required

from sigma.www.models import Appel, Candidature, ProjetPoste, Categorie, ChampsCategorie, BlocChamps

@login_required
def champs_appel_json(request, bloc_id):
    champs_list = ChampsCategorie.objects.filter(bloc=bloc_id)
    
    champs_json = serializers.serialize('json', champs_list)

    ret = ''
    for champs in champs_list:
        ret += '<li>' + champs.libelle + '</li>'
    return HttpResponse(ret)

@login_required
def champs_json(request, bloc_id):
    champs_list = ChampsCategorie.objects.filter(groupe=bloc_id)
    
    champs_json = serializers.serialize('json', champs_list)

    ret = ''
    for champs in champs_list:
        if champs.type == "Booleen":
            ret += '<p><label for="id_' + champs.libelle + '">'+ champs.libelle + ': </label><input type="checkbox" name="' + champs.libelle + '" id="id_'+ champs.libelle +'"/>'+ '</p>'
        if champs.type == "Texte":
            ret += '<p><label for="id_' + champs.libelle + '">'+ champs.libelle + ': </label><input type="text" name="' + champs.libelle + '" id="id_'+ champs.libelle +'"/>'+ '</p>'
        elif champs.type == "Nombre":
            ret += '<p><label for="id_' + champs.libelle + '">'+ champs.libelle + ': </label><input type="text" name="' + champs.libelle + '" id="id_'+ champs.libelle +'"/>'+ '</p>'

    return HttpResponse(ret)

