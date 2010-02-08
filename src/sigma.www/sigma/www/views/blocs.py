from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required

from sigma.www.models import Appel, Candidature, ProjetPoste, Categorie, ChampsCategorie, BlocChamps

@login_required
def blocs_json(request, projet_id):
    projet_post = get_object_or_404(ProjetPoste, pk=projet_id)

    blocs = BlocChamps.objects.filter(categorie=projet_post.getCategorie())
        

    blocs_json = serializers.serialize('json', blocs)

    return HttpResponse(blocs_json)


