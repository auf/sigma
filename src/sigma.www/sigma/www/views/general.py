# -=- encoding: utf-8 -=-
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import Context, RequestContext, loader
from django.conf import settings

from sigma.www.views.candidature import statut_list_can
from sigma.www.authentification import SettingsBackend
from sigma.www.views.appel import statut_list_app
from sigma.www.utils import render_to_response
from sigma.www.forms.general import SearchForm
from sigma.www.forms.user import UserEditForm
from sigma.www import workflow
from sigma.www.models import *

def handler500(request, template_name="sigma.www/500.html"):
    t = loader.get_template("sigma.www/500.html") # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({'request_path': request.path,
                                                     'MEDIA_URL': settings.MEDIA_URL})))

def index(request):
    """Affichage de la page principale de Sigma"""
    user = request.user
    if request.method == "POST":
        if form.is_valid():
            form.save()
    return render_to_response(request, 
                              'sigma.www/index.html', 
                              {'user': user} )

@login_required
def profile(request):
    """Page d'accueil du site"""
    # droits d'acces
    user = request.user
    (permissions, bureaux) = SettingsBackend().get_rights(user)

    # template par defaut
    template = 'sigma.www/profile.html'

    # structures de contenu
    candidature_par_appel = {}
    candidature_list = []
    appels_par_statut = {}

    # Dans le cas d'un expert
    if user.is_expert():
        template = 'sigma.www/profile_expert.html'
        candidature_list = [ec.candidature.id for ec in ExpertCandidature.objects.filter(expert=user.expert, is_note=False)]
        candidature_list = Candidature.objects.filter(id__in=candidature_list)        
    
    appels_par_statut = statut_list_app(user, only_nontraite=True)

    # Gestion de la liste des candidature
    for appel in Appel.objects.all().order_by('-id'):
        if user.is_expert():
            candidatures = statut_list_can(user = user, 
                                           only_nontraite = False,
                                           for_expert = True,
                                           appel = appel, 
                                           candidature_list = candidature_list)
        else:
            candidatures = statut_list_can(user = user, 
                                           appel = appel,
                                           only_nontraite = True)
        if candidatures:
            candidature_par_appel[appel] = candidatures

    return render_to_response(request, 
                              template, 
                              {'permissions': permissions,
                               'bureaux': bureaux,
                               'statut_list_app' : appels_par_statut,
                               'candidature_par_appel': candidature_par_appel,
                               } )

def search(request, value=None):
    """Recherche d'objets du modeles correspondant a une valeur voulue

    @param request
    @param value
    """
    user = request.user
    form = SearchForm()
    if request.method == "POST":
        form = SearchForm(request.POST)
    elif request.method == "GET":
        form = SearchForm(request.GET)

    value = form.data['value']

    appel_list = Appel.search(request.user, value)
    candidature_list = Candidature.search(request.user, value, by_appel=False)
    categorie_list = Categorie.search(request.user, value)
    projet_list = ProjetPoste.search(request.user, value)
    expert_list = Expert.search(request.user, value)

    length = len(categorie_list) + len(projet_list) + len(expert_list) + len(appel_list) + len(candidature_list)

    appel_total_len = len(Appel.objects.all())
    candidature_total_len = len(Candidature.objects.all())
    categorie_total_len = len(Categorie.objects.all())
    projet_total_len = len(ProjetPoste.objects.all())
    expert_total_len = len(Expert.objects.all())
    
    return render_to_response(request,
                              'sigma.www/resultats.html',
                              {'value' : value,
                               'length' : length,
                               'statut' : '',
                               'appel_list' : appel_list,
                               'candidature_list' : candidature_list,
                               'projet_list' : projet_list,
                               'expert_list' : expert_list,
                               'categorie_list' : categorie_list,
                               'appel_total_len': appel_total_len,
                               'candidature_total_len': candidature_total_len,
                               'categorie_total_len': categorie_total_len,
                               'projet_total_len': projet_total_len,
                               'expert_total_len': expert_total_len})
                               
