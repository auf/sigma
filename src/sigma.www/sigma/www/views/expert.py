# -=- encoding: utf-8 -=-
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.core import serializers
from django.db import transaction

from sigma.www.models import Expert, Candidature, ExpertCandidature
from sigma.www.workflow import exporter
from sigma.www.utils import render_to_response, getSubjectList
from sigma.www.forms.expert import ExpertAjoutForm, ExpertEditForm
from sigma.www.views.candidature import statut_list_can

import hashlib

"""
Vues utilises afin de manipuler et de consulter les candidatures
"""

def liste(request):
    """Affichage de la liste complete des experts du systeme

    @param request
    """
    expert_list = Expert.objects.all()
    region_list_exp = {}
    for expert in expert_list:
        if expert.etablissement.region not in region_list_exp:
            region_list_exp[expert.etablissement.region] = []
        region_list_exp[expert.etablissement.region].append(expert)
    return render_to_response(request,
                              "sigma.www/expert_list.html", 
                              { 'region_list_exp': region_list_exp,
                                'type': "experts"})


def detail(request, object_id):
    """Affichage des details des informations sur un expert

    @param request
    @param object_id
    """
    p = get_object_or_404(Expert, pk=object_id)
    exp = p
    user = request.user

    # obtention de la liste des sujets
    subject_list = getSubjectList(p)

    # obtention de la liste des candidatures associees a cet expert
    t = ExpertCandidature.objects.filter(expert=p)
    t_id = [expcan.candidature.id for expcan in t]
    candidature_list = Candidature.objects.filter(id__in=t_id)

    candidature_list = statut_list_can(user, candidature_list=candidature_list)

    return render_to_response(request,
                              "sigma.www/expert_detail.html", 
                              {'expert': p,
                               'statut_list_can' : candidature_list,
                               'subject_list' : subject_list})

@login_required
@transaction.commit_on_success
def edit(request, object_id):
    """Interaction avec l'utilisateur afin de modifier un expert existant

    @param request
    @param object_id
    """
    expert = get_object_or_404(Expert, pk=object_id)

    form = ExpertEditForm(instance=expert)

    if request.method == "POST":
        form = ExpertEditForm(request.POST, instance=expert)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/experts/detail/%s/' % form.instance.id)
    return render_to_response(request,
                              'sigma.www/expert_edit.html',
                              {'form' : form,
                               'exper_id' : object_id,
                               })

@login_required
@transaction.commit_on_success
def add(request):
    """Interaction avec l'utilisateur afin d'ajouter un nouvel expert

    @param request
    """
    form = ExpertAjoutForm()

    if request.method == "POST":
        form = ExpertAjoutForm(request.POST, instance=None)

        if form.is_valid():
            form.save()
            password = form.instance.motdepasse
            form.instance.motdepasse = hashlib.md5(password).hexdigest()
            form.instance.save()
            return HttpResponseRedirect('/experts/detail/%s/' % form.instance.id)
    return render_to_response(request,
                              "sigma.www/expert_add.html",
                              {'form' : form })


def export(request, object_id):
    """Exportation d'un projet vers le format ods
    
    @param request
    @param object_id
    """
    expert = get_object_or_404(Expert, pk=object_id)
    user = request.user

    export = exporter.GenericODSExporter(expert, user)()

    response = HttpResponse(export, mimetype="application/vnd.oasis.opendocument.spreadsheet")
    response['Content-Disposition'] = 'attachment; filename=%s.ods' \
        % str(expert).replace(" ","_")
    return response


def json(request, region_id, discipline_id):
    """Recherche d'un expert selon sa region et des disciplines

    @param request
    @param id_region
    @param id_discipline
    """
    expert_list = Expert.objects.all()
    if int(region_id) > 0:
        expert_list = expert_list.filter(etablissement__region=int(region_id))
    if int(discipline_id) > 0:
        expert_list = expert_list.filter(discipline=int(discipline_id))
    json = serializers.serialize('json', expert_list, 
                                 fields=Expert.serialisable_fields)
    return HttpResponse(json)
        
