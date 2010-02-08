# -=- encoding: utf-8 -=-
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.db import transaction
from django.forms.models import inlineformset_factory

from sigma.www.models import Appel, Candidature, ProjetPoste, Categorie, \
    BlocChamps, Answer, Note, PieceJointeCandidature

from sigma.www.workflow.logger import WorkflowLogger
from sigma.www.workflow.decorator import *
from sigma.www.utils import render_to_response, getSubjectList
from sigma.www import DEFAULT_SUBJECT
from sigma.www.forms.candidature import *
from sigma.www.forms.note import *
from sigma.www import workflow

from StringIO import StringIO

import mimetypes

def statut_list_can(user, appel=None, only_nontraite=False, for_expert=False, candidature_list=None):
    """Creation de la liste des candidature par statut ou par categorie de statut
    
    @oaram user Utilisateur courant
    @param appel Appel d'offre
    @param only_nontraite Est-ce qu'on doit afficher seulement les 
                          candidatures considereess comme non-traitees
    @param candidature_list                         
    """
    statut_list_can = {}
    statut_list_can[u"elimine"] = []
    statut_list_can[u"nontraite"] = []
    statut_list_can[u"incomplet"] = []
    
    if appel is None and candidature_list is None:
        candidature_list = Candidature.objects.order_by('statut').all()
    else:
        if candidature_list is None:
            candidature_list = Candidature.objects.order_by('statut').filter(appel=appel)

    for candidature in candidature_list:
        # On initialise a liste si elle n existe pas encore
        if not candidature.statut in statut_list_can :
            statut_list_can[candidature.statut] = []

        # a traiter
        handler = workflow.Manager().get_handler(candidature, user)

        if for_expert:
            statut_list_can[u"nontraite"].append(candidature)
        else:
            if handler.is_executable(candidature):
                statut_list_can[u"nontraite"].append(candidature)
            elif not only_nontraite:
                if candidature.statut != 'Complet' \
                        and handler.is_completed(candidature) \
                        and not handler.is_undoable(candidature):
                    statut_list_can[u"elimine"].append(candidature)

                elif not handler.is_valid(candidature) and \
                        not handler.is_completed(candidature):
                    statut_list_can[u"incomplet"].append(candidature)
                else:
                    statut_list_can[candidature.statut].append(candidature)

    # on supprime les listes vides
    for statut, candidature_list in statut_list_can.items():
        if not candidature_list:
            del statut_list_can[statut]

    return statut_list_can


def generate_arianne(candidature, user):
    """Generation du fil d'arianne d'une candidature

    @param candidature
    @param user
    """
    ariannes = []
    handler = workflow.Manager().get_handler(candidature, user)
    if candidature.statut in handler.final_states:
        for (choice, choicelabel) in Candidature.STATUT_CHOICES:
            if choice == handler.init:
                ariannes.append((choice, choicelabel))
            else:
                log = handler.get_logs(candidature, WorkflowLogger.INFO, to_state=choice)
                if len(log) > 0:
                    ariannes.append((choice, choicelabel))
    else:
        for (choice, choicelabel) in Candidature.STATUT_CHOICES:
            if choice == "PreRecevable" or choice == "PreIrrecevable":
                log = handler.get_logs(candidature, WorkflowLogger.INFO, to_state=choice)
                if choice == "PreRecevable" and len(log) > 0:
                    ariannes.append((choice, choicelabel))
                elif choice == "PreIrrecevable" and len(log) > 0:
                    ariannes.append((choice, choicelabel))
            elif choice not in handler.final_states:
                ariannes.append((choice, choicelabel))
    return ariannes
                    

"""
Vues utilises afin de manipuler et de consulter les candidatures
"""

def liste(request):
    """Liste toutes les candidatures du systeme

    @param request La requete http
    """
    appels = []
    candidature_par_appel = {}
    user = request.user
    for appel in Appel.objects.all().order_by('-id'):
        appels.append(appel)
        if appel not in candidature_par_appel:
            candidatures = statut_list_can(user, appel)
            if candidatures:
                candidature_par_appel[appel] = candidatures
    return render_to_response(request,
                              'sigma.www/candidature_list.html',
                              { 'list_candidatures' : candidature_par_appel,
                                'type': 'candidatures',
                                'appels' : appels,
                                })

@login_required
@userCanEdit(Candidature)
@transaction.commit_on_success
def add(request, appel_id, object_id=None, validation=True):
    """
    Ajout d'une candidature dans le systeme, ou sauvegarde d'une candidature 
    partiellement validee.

    Nous entendons par partiellement validee, une candidature n'ayant pas
    necessairement ses champs marque comme "blank=False" remplis.

    @param request
    @param appel_id
    @param object_id
    @param validation
    """
    p = get_object_or_404(Appel, pk=appel_id)

    candidature = None

    if object_id is not None:
        candidature = get_object_or_404(Candidature, pk=object_id)

    form = CandidatureAjoutForm(instance=candidature)

    bloc_list = {}
    blocs = BlocChamps.objects.filter(categorie=p.projetposte.getCategorie())
    
    for bloc in blocs:
        bloc_list[bloc] = CandidatureBlocForm(bloc, None)

    if request.method == "POST":
        form = CandidatureAjoutForm(validation, request.POST, instance=candidature)
        form.instance.appel_id = request.POST['appel']

        for bloc in blocs:
            bloc_list[bloc] = CandidatureBlocForm(bloc, None, request.POST)

        if form.is_valid():
            # get bloc fields
            for bloc, champs_form in bloc_list.items():
                # On vérifie que le form courant est bon
                if not champs_form.is_valid():
                    return render_to_response(request,
                              'sigma.www/candidature_add.html',
                              {'form' : form,
                               'appel_id': appel_id,
                               "bloc_list" : bloc_list,
                               })

            form.save()

            for bloc, champs_form in bloc_list.items():
                # on sauvegarde tous les champs
                for champs, data in champs_form.cleaned_data.items():
                    answer = Answer()
                    # on set la valeur
                    answer.value = data
                    # on set le champs
                    answer.champscategorie = champs_form.fields[champs].champs 
                    # on set la candidature
                    answer.candidature = get_object_or_404(Candidature, pk=form.instance.id)
                    answer.save()

            return HttpResponseRedirect('/candidatures/detail/%s/' % form.instance.id)
    return render_to_response(request,
                              'sigma.www/candidature_add.html',
                              {'form' : form,
                               'appel_id': appel_id,
                               "bloc_list" : bloc_list,
                               })


@login_required
@userCanEdit(Candidature)
@transaction.commit_on_success
def save(request, appel_id, object_id=None):
    """Ajout d'une candidature en ne validant pas tout les champs
    marque comme blank

    @param request
    @param appel_id
    """
    return add(request, appel_id, object_id, validation=False)


@login_required
@userCanEdit(Candidature)
@transaction.commit_on_success
def validate(request, appel_id, object_id=None):
    """Ajout d'une candidature en validant tout les champs
    marque comme blank

    @param request
    @param appel_id
    """ 
    return add(request, appel_id, object_id, validation=True)
        

@login_required
@userCanEdit(Candidature)
@transaction.commit_on_success
def edit(request, object_id):
    """Edition d'une candidature existante et sa validation

    @param request La requete http
    @param candidute_id L'identificateur de candidature ou None
    """
    candidature = get_object_or_404(Candidature, pk=object_id)
    appel_id = None
    form = CandidatureEditForm(instance=candidature)

    # Gestion des criteres supplementaires
    CriteresFormset = inlineformset_factory(Candidature, CritereSupplementaireCandidature, 
                                            formset=CandidatureCriteresFormSet)
    form_criteres = CriteresFormset(instance=candidature)

    # Gestion des pieces jointes
    PiecesJointesFormset = inlineformset_factory(Candidature, PieceJointeCandidature, 
                                                 formset=CandidaturePieceJointeFormSet)
    form_pieces = PiecesJointesFormset(instance=candidature)

    # La liste des experts
    expert_list = ExpertCandidature.objects.filter(candidature=form.instance)

    # On recupere les blocs de champs de l appel
    bloc_list = {}
    blocs = BlocChamps.objects.filter(categorie=candidature.appel.projetposte.getCategorie())
    for bloc in blocs:
        bloc_list[bloc] = CandidatureBlocForm(bloc, candidature)

    if "appel_id" in request.GET:
        appel_id = request.GET["appel"]
        appel = get_object_or_404(Appel, pk=appel_id)
        form.instance.appel = appel

    elif request.method == "POST":
        form = CandidatureEditForm(request.POST, instance=candidature)
        form_criteres = CriteresFormset(request.POST, instance=candidature)
        form_pieces = PiecesJointesFormset(request.POST, request.FILES, instance=candidature)

        appel_id = request.POST["appel"]
        appel = get_object_or_404(Appel, pk=appel_id)
        form.instance.appel = appel

        for bloc in blocs:
            bloc_list[bloc] = CandidatureBlocForm(bloc, candidature, request.POST)

        if form.is_valid() and form_criteres.is_valid() and form_pieces.is_valid():
            # on verifie que tous les bloc de champs soient correct
            for bloc, champs_form in bloc_list.items():
                # On vérifie que le form courant est bon
                if not champs_form.is_valid():
                    return render_to_response(request,
                              'sigma.www/candidature_edit.html',
                              {'form' : form,
                               'candidature' : candidature,
                               'object_id' : object_id,
                               'appel_id': appel_id,
                               'bloc_list' : bloc_list,
                               'expert_list' : expert_list,
                               })                

            form_criteres.save()
            form_pieces.save()
            form.save()
            
            for bloc, champs_form in bloc_list.items():
                # on sauvegarde tous les champs
                for champs, data in champs_form.cleaned_data.items():
                    # on recupere l objet answer que l'on va modifier
                    answer = champs_form.fields[champs].answer
                    # on modifie la valeur
                    answer.value = data
                    answer.save()

            return HttpResponseRedirect('/candidatures/detail/%s/' % form.instance.id)
    else:
        appel_id = candidature.appel.id

    return render_to_response(request,
                              'sigma.www/candidature_edit.html',
                              {'form' : form,
                               'candidature' : candidature,
                               'object_id' : object_id,
                               'appel_id': appel_id,
                               'bloc_list' : bloc_list,
                               'form_criteres' : form_criteres,
                               'form_pieces' : form_pieces,
                               'expert_list' : expert_list,
                               })
    

@login_required
@userCanEdit(Candidature)
@transaction.commit_on_success
def edit_statut(request, object_id):
    """
    Edition du statut d'une candidature qui permet de lancer la procedure

    @param request La requete Http
    @param object_id L'identificateur de candidature
    """
    candidature = get_object_or_404(Candidature, pk=object_id)
    if request.method == "POST":
        form = CandidatureStatutForm(request.POST, instance=candidature)
        action = request.POST["action"]
        commentaires = request.POST["commentaires"]
        user = request.user
        workflow.Manager().execute(candidature, user, action, commentaires)
        return HttpResponseRedirect('/candidatures/detail/%s/' % candidature.id)
    else:
        form = CandidatureStatutForm(instance=candidature)
    return render_to_response(request,
                              'sigma.www/candidature_statut_edit.html',
                              { 'form': form } )


@login_required
@userCanEdit(Candidature)
@transaction.commit_on_success
def undo(request, object_id):
    """Annule le dernier changement de transition si cela est possible

    @param request
    @param object_id
    """
    user = request.user
    candidature = get_object_or_404(Candidature, pk=object_id)

    workflow.Manager().undo(candidature, user)

    if 'appels/detail' in request.META['HTTP_REFERER']:
        return HttpResponseRedirect('/appels/detail/%s/' % candidature.appel.id)
    else:
        return HttpResponseRedirect('/candidatures/detail/%s/' % candidature.id)


@login_required
@userCanEdit(Candidature)
@transaction.commit_on_success        
def delete(request, object_id):
    """Supprime une candidature d'un appel d'offre

    @param request
    @param object_id
    """
    user = request.user
    candidature = get_object_or_404(Candidature, pk=object_id)
    appel = candidature.appel

    workflow.Manager().execute(candidature, user, "Supprimer")

    return HttpResponseRedirect('/appels/detail/%s/' % appel.id)


def detail(request, object_id=None):
    """Affichage des details d'une candidature

    @param request La requete http
    @param object_id L'identificateur de candidature
    """
    candidature = get_object_or_404(Candidature, pk=object_id)
    user = request.user

    # On recupere les blocs de champs de l appel
    bloc_list = {}
    blocs = BlocChamps.objects.filter(categorie=candidature.appel.projetposte.getCategorie())
    for bloc in blocs:
        bloc_list[bloc] = []
        # On recupere les champs du bloc 
        for champs in ChampsCategorie.objects.filter(bloc=bloc):
            # On recupere les valeurs de chaque champs
            answer = Answer.objects.filter(champscategorie=champs).filter(candidature=candidature)
            # Si il y a un champs on l'ajoute dans la liste
            if not answer:
                valeur = ""
            else:
                valeur = answer.get()
            bloc_list[bloc].append((champs, valeur))

    # Obtention des pieces jointes du candidat
    piece_list = PieceJointeCandidature.objects.filter(candidature=candidature)

    # Obtention des notes du candidat
    notes = Note.objects.filter(candidature=candidature)

    # contruction du fil d'arianne
    ariannes = generate_arianne(candidature, user)
    
    # Obtention des criteres du candidat
    critere_list = CritereSupplementaireCandidature.objects.filter(candidature=candidature)

    # Obtention des Candidature Expert du candidat
    expert_list = ExpertCandidature.objects.filter(candidature=candidature)
    
    # obtention de la liste des sujets
    subject_list = getSubjectList(candidature)

    # obtention du journal
    handler = workflow.Manager().get_handler(candidature, user)
    infos = handler.get_logs(candidature, WorkflowLogger.INFO)
    erreurs = handler.get_logs(candidature, WorkflowLogger.ERROR)

    # obtention des erreurs bloquantes de la candidature
    error_list = []
    if not handler.is_valid(candidature):
        error_list.append(_("Cette candidature n'est pas complete"))
    
    return render_to_response(request,
                              'sigma.www/candidature_detail.html',
                              {"candidature" : candidature,
                               'user' : user,
                               'subject_list' : subject_list,
                               'bloc_list' : bloc_list,
                               'critere_list' : critere_list,
                               "piece_list" : piece_list,
                               'expert_list' : expert_list,
                               'error_list' : error_list,
                               'notes' : notes,
                               'ariannes': ariannes,
                               "infos" : infos,
                               "erreurs": erreurs,
                               })

@login_required
def json(request, object_id=None):
    """Obtention des differents champs d'une candidature par json
    
    @param request 
    @param object_id Id de la candidature a rechercher"""
    candidature = None
    if object_id is not None:
        candidature = get_object_or_404(Candidature, pk=object_id)
    else:
        candidature = Candidature()
    json = serializers.serialize('json', [candidature], 
                                 fields=Candidature.serialisable_fields)

    return HttpResponse(json)

@login_required
def json_field_dependencies(request):
    """Obtention des champs qui ont des dependances, 
    notons que nous ne supportons que les dependances simples
    
    @param request
    """
    serialisable = []
    can = Candidature()
    for field in Candidature.field_dependencies:
        try:
            serialisable.append(field)
            setattr(can, field, Candidature.field_dependencies[field])
        except ValueError:
            pass # ForeignKey are really a problem but we deal with them a couple if lines downthere
    json = serializers.serialize('json', [can],
                                 fields=serialisable)
    
    json = simplejson.load(StringIO(json))
    
    for field in json[0]['fields']:
        json[0]['fields'][field] = Candidature.field_dependencies[field]
    return HttpResponse(simplejson.dumps(json))


@login_required
def json_warning_messages(request, object_id, action):
    """Obtention des message d'avertissement lie au passage d'une candidature
    a un nouveau statut

    @param request
    @param object_id
    @param action
    """
    candidature = get_object_or_404(Candidature, pk=object_id)
    user = request.user
    warning_list = {}

    for warning in workflow.Manager().get_warnings(candidature, user, action):
        warning_list[warning['commentaires']] = warning['description']
    return HttpResponse(simplejson.dumps(warning_list))


@login_required
@userCanEdit(Candidature)
@transaction.commit_on_success
def piecesjointes(request, object_id):
    """Ajout d'une piece jointe a une candidature ou gestion des pieces d'une candidature
    
    @param request
    @param object_id
    """
    candidature = get_object_or_404(Candidature, pk=object_id)
    PiecesJointesFormset = inlineformset_factory(Candidature, PieceJointeCandidature, formset=CandidaturePieceJointeFormSet)
    form = PiecesJointesFormset(instance=candidature)

    if request.method == "POST":
        form = PiecesJointesFormset(request.POST, request.FILES, instance=candidature)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/candidatures/detail/%s/' % object_id)
    return render_to_response(request,
                              "sigma.www/piecesjointes_edit.html",
                              {'form' : form,
                               'object_id': object_id,
                               })


def lettretype(request, object_id=None):
    """Generation d'une lettre type pour une candidature d'un statut

    @param request La requete http
    @param object_id L'identificateur d'une note
    """
    candidature = get_object_or_404(Candidature, pk=object_id)
    user = request.user

    lettre = workflow.Manager().export(candidature, user, workflow.exporter.ODFType)

    response = HttpResponse(lettre, mimetype="application/vnd.oasis.opendocument.text")
    response['Content-Disposition'] = 'attachment; filename=%s.odt' \
        % unicode(candidature).replace(" ","_")
    return response


@login_required
@userCanEdit(Candidature)
@transaction.commit_on_success
def delete_expert(request, object_id, candidature_expert_id):
    """
    @param request
    @param expert_id
    """
    ExpertCandidature.objects.filter(id=int( candidature_expert_id)).delete()

    return HttpResponse('ok');
    

@login_required
@userCanEdit(Candidature)
@transaction.commit_on_success
def add_expert(request, object_id):
    """
    @param request
    @param object_id
    """
    candidature = get_object_or_404(Candidature, pk=object_id)
    user = request.user

    form = CandidatureExpertAjout()

    if request.method == "POST":
        form = CandidatureExpertAjout(request.POST)
        if form.is_valid():
            expert_id = int(form.data['expert'])
            expert = Expert.objects.get(id=expert_id)
            ExpertCandidature(expert=expert, candidature=candidature).save()
            expert_list = ExpertCandidature.objects.filter(candidature=candidature)
            return render_to_response(request,
                              'sigma.www/candidature_expert_save.html',
                              {'form' : form,
                               'expert_list' : expert_list,
                               'candidature': candidature})

    return render_to_response(request,
                              'sigma.www/candidature_expert_add.html',
                              {'form' : form,
                               'candidature': candidature})


@login_required
@userCanNote(Candidature)
@transaction.commit_on_success
def noter(request, object_id, candidature_expert_id):
    """Noter une candidature par assignation de cette note a son association avec un expert

    @param request
    @param candidature_expert_id
    """
    candidature_expert = get_object_or_404(ExpertCandidature, pk=candidature_expert_id)
    candidature = get_object_or_404(Candidature, pk=object_id)

    user = request.user
    form = CandidatureExpertNoter(instance=candidature_expert)
    expert_list = ExpertCandidature.objects.filter(candidature=candidature)

    if request.method == "POST":
        form = CandidatureExpertNoter(request.POST, instance=candidature_expert)
        if form.is_valid():
            candidature_expert.is_note=True
            form.save()
            return render_to_response(request,
                               'sigma.www/candidature_expert_noter_save.html',
                              {'form' : form,
                               'candidature' : candidature,
                               'candidature_expert': candidature_expert,
                               'expert_list' : expert_list})

    return render_to_response(request,
                              'sigma.www/candidature_expert_noter.html',
                              {'form' : form,
                               'candidature' : candidature,
                               'candidature_expert': candidature_expert,
                               'expert_list' : expert_list})


def piece(request, object_id):
    """
    Telechargement d'une piece jointe 

    @param request La requete web
    @param object_id L'identificateur de la piece jointe a afficher
    """
    p = get_object_or_404(PieceJointeCandidature, pk=object_id)

    response = ''
    mimetype = mimetypes.guess_type(p.fichier.name)
    if mimetype[0] == None:
        response = HttpResponse(p.fichier.readlines(), mimetype='application/octet-stream')
    else:
        response = HttpResponse(p.fichier.readlines(), mimetype=mimetype[0])
    response['Content-Disposition'] = 'attachment; filename=%s' % p.getFilename()
    return response


def export(request, object_id=None):
    """Generation de l'exportion ods de cette candidature

    @param request
    @param object_id
    """
    user = request.user

    candidature = None

    if object_id:
        candidature = get_object_or_404(Candidature, pk=object_id)
    else:
        candidature = Candidature.objects.all()

    export = workflow.exporter.GenericODSExporter(candidature, user)

    response = HttpResponse(export(), mimetype="application/vnd.oasis.opendocument.spreadsheet")
    response['Content-Disposition'] = 'attachment; filename=%s' % export.getFilename()
    return response


def export_search(request, value):
    """Exporation d'un projet vers le format ods"""
    user = request.user

    candidature = Candidature.search(user, value, False)

    export = workflow.exporter.GenericODSExporter(candidature, user)
    
    response = HttpResponse(export(), mimetype="application/vnd.oasis.opendocument.spreadsheet")
    response['Content-Disposition'] = 'attachment; filename=%s' % export.getFilename()

    return response
