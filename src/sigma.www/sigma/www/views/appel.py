# -=- encoding: utf-8 -=-
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core import serializers
from django.contrib.auth.decorators import user_passes_test
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from sigma.www.utils import render_to_response, getSubjectList
from sigma.www.views.candidature import statut_list_can
from sigma.www.workflow.logger import WorkflowLogger
from sigma.www.forms.appel import *
from sigma.www import workflow
from sigma.www.models import *


def statut_list_app(user, only_nontraite=False, categorie=None, appel_list = None):
    """Creation de la liste des appels par statut ou pseudo-statut

    @param user L'utilisateur courant
    @param only_nontraite Est-ce qu'on doit afficher seulement les 
                          appels d'offres consideres comme non-traites
    """
    statut_list = {}
    statut_list[u"nontraite"] = []

    if appel_list is None:
        appel_list = Appel.objects.all().order_by('-id')

    if categorie is not None:
        appel_list = appel_list.filter(projetposte__id__in=ProjetPoste.objects.filter(code_poste__id=categorie.poste.id))

    for appel in appel_list:
        if not appel.statut in statut_list:
            statut_list[appel.statut] = []

        handler = workflow.Manager().get_handler(appel, user)
        
        can_list = statut_list_can(user, appel)

        if handler.is_executable(appel):
            statut_list[u"nontraite"].append(appel)
        elif not only_nontraite:
            if "incomplet" in can_list and len(can_list["incomplet"]) > 0:
                statut_list[u"nontraite"].append(appel)
            else:
                statut_list[appel.statut].append(appel)

    # on supprime les listes vides
    for statut, appel_list in statut_list.items():
        if not appel_list:
            del statut_list[statut]
    return statut_list


def liste(request):
    """Obtention de liste de tout les appels d'offre accessible a l'utilisateur

    @param request Requete http
    """
    user = request.user
    statut_list = statut_list_app(user)

    return render_to_response(request,
                              "sigma.www/appel_list.html", 
                              { 'statut_list_app': statut_list,
                                "type": "appels"})


def detail(request, object_id):
    """Obtention des details d'un appel d'offre
    
    @param request
    @param object_id
    """
    p = get_object_or_404(Appel, pk=object_id)
    user = request.user

    label1=_("elimine")
    label2=_("nontraite")

    candidatures = statut_list_can(user, p)

    bloc_list = {}
    blocs = BlocChamps.objects.filter(categorie=p.projetposte.getCategorie())
    for bloc in blocs:
        bloc_list[bloc] = ChampsCategorie.objects.filter(bloc=bloc)
    
    infos = workflow.Manager().get_logs(p, user, WorkflowLogger.INFO)
    erreurs = workflow.Manager().get_logs(p, user, WorkflowLogger.ERROR)

    # obtention de la liste des sujets
    subject_list = getSubjectList(p)

    return render_to_response(request,
                              "sigma.www/appel_detail.html", 
                              {"appel": p,
                               "statut_list_can": candidatures,
                               "bloc_list" : bloc_list,
                               "infos" : infos,
                               "erreurs": erreurs,
                               "subject_list" : subject_list,
                               })


@login_required
def edit_statut(request, object_id):
    """Modification du statut d'un appel d'offre afin de passer au statut suivant

    @param request
    @param object_id
    """
    p = get_object_or_404(Appel, pk=object_id)
    if request.method == "POST":
        form = AppelStatutForm(request.POST, instance=p)
        action = request.POST["action"]
        user = request.user
        workflow.Manager().execute(p, user, action)
        return HttpResponseRedirect('/appels/detail/%s/' % p.id)
    else:
        form = AppelStatutForm(instance=p)
    return render_to_response(request, 'sigma.www/appel_statut_edit.html',  { 'form': form } )


@login_required
def add(request):
    """Ajout d'un appel d'offre

    @param request
    """
    user = request.user
    form = AppelAjoutForm()
    if request.method == "POST":
        form = AppelAjoutForm(request.POST, instance=None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/appels/detail/%s/' % form.instance.id)
    else:
        projets_id = [projet.id for projet in ProjetPoste.all(user)]
        form.fields['projetposte'].queryset = ProjetPoste.objects.filter(id__in=projets_id)

    return render_to_response(request,
                              'sigma.www/appel_add.html',
                              {'form' : form })
                                   

@login_required
def edit(request, object_id):
    """Edition d'un appel d'offre

    @param request
    @param object_id
    """
    appel = get_object_or_404(Appel, pk=object_id)
    
    form = AppelEditForm(instance=appel)

    if request.method == "POST":
        form = AppelEditForm(request.POST, instance=appel)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/appels/detail/%s/' % form.instance.id)
    else:
        form = AppelEditForm(instance=appel)
        return render_to_response(request, 
                                  'sigma.www/appel_edit.html',
                                  {'form': form,
                                   'object_id' : object_id, 
                                   })

@login_required
def delete(request, object_id):
    """Suppression de l'appel d'offre
    
    @param request
    @param object_id
    """
    appel = get_object_or_404(Appel, pk=object_id)
    user = request.user

    workflow.Manager().execute(appel, user, "Supprimer")

    return HttpResponseRedirect('/appels/')


@login_required
def json(request, object_id=None):
    """Obtention de la valeur d'un appel complet en json

    @param request
    @param object_id
    """
    appel = None
    if object_id is not None:
        appel = get_object_or_404(Appel, pk=object_id)
    else:
        appel = Appel()

    json = serializers.serialize('json', [appel], 
                                 fields=Appel.serialisable_fields)
    return HttpResponse(json)


@login_required
def json_field_dependencies(request):
    """Obtention des champs qui ont des dependances, 
    notons que nous ne supportons que les dependances simples

    @param request
    """
    serialisable = []
    app = Appel()
    for field in Appel.field_dependencies:
        serialisable.append(field)
        setattr(app, field, Appel.field_dependencies[field])
    json = serializers.serialize('json', [app],
                                 fields=serialisable)
    return HttpResponse(json)


def export(request, object_id=None, statut=None):
    """Exportation des appels d'offre d'un certains statut ou un seul en particulier

    @param request
    @param object_id
    @param statut
    """
    user = request.user
    appels = None
    filename = ""
    
    if object_id is not None:
        appels = get_object_or_404(Appel, pk=object_id)
    elif statut is not None:
        appel_list = statut_list_app(user)[statut]
        try:
            appels = [appel for appel, len_app in appel_list]
        except TypeError:
            appels = appel_list
    else:
        appels = Appel.objects.all()

    export = workflow.exporter.GenericODSExporter(appels, user)

    response = HttpResponse(export(), mimetype="application/vnd.oasis.opendocument.spreadsheet")
    response['Content-Disposition'] = 'attachment; filename=%s' % export.getFilename()
    return response


def export_can(request, object_id, statut=None):
    """
    @param request
    @param object_id
    @param statut
    """
    appel = get_object_or_404(Appel, pk=object_id)
    user = request.user
    candidatures = statut_list_can(user, appel)
    filename = ""

    if candidatures.items():
        if statut is not None:
            candidatures = candidatures[statut]
            filename = '%s-candidatures-%s.ods' % (unicode(appel).replace(" ","_"), statut)
        else:
            candidatures = list(reduce(set.union,map(set,candidatures.values())))
            filename = '%s-candidatures.ods' % (
                unicode(appel).replace(" ","_"))

        export = workflow.Manager().export(candidatures, user, workflow.exporter.ODSType)
        
        response = HttpResponse(export, mimetype="application/vnd.oasis.opendocument.spreadsheet")
        response['Content-Disposition'] = 'attachment; filename=%s' % (filename)
        return response
    raise Http404

def export_lettres(request, object_id, statut=None):
    """Exportation d'une serie de lettres types en format odt

    @param request
    @param object_id
    @param statut
    """
    appel = get_object_or_404(Appel, pk=object_id)
    user = request.user
    candidatures = statut_list_can(user, appel)

    if statut is not None:
        candidatures = candidatures[statut]
    else:
        candidatures = list(reduce(set.union,map(set,candidatures.values())))

    export = workflow.Manager().export(candidatures, user, workflow.exporter.MultiODFType)

    response = HttpResponse(export, mimetype="application/zip")
    response['Content-Disposition'] = 'attachment; filename=%s-lettre_type_candidatures-%s.zip' \
        % (unicode(appel).replace(" ","_"), statut)
    return response


def criteria(request):
    """Gestion de l'ajout d'un nouveau critere supplementaire
    a un appel d'offre

    @param request
    """
    form = AppelCriteriaAjout()

    if request.method == "POST":
        form = AppelCriteriaAjout(request.POST, instance=None)
        if form.is_valid():
            form.save()
            return render_to_response(request,
                              'sigma.www/appel_criteria_save.html',
                              {'form' : form })

    return render_to_response(request,
                              'sigma.www/appel_criteria_add.html',
                              {'form' : form })
    
