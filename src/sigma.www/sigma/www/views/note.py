# -=- encoding: utf-8 -=-
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from sigma.www.utils import render_to_response
from sigma.www.models import Note, Candidature
from sigma.www.forms.note import NoteEditForm

@login_required
def detail(request, object_id=None):
    """Affichage des details d'une note d'une candidature

    @param request La requete http
    @param object_id L'identificateur d'une note
    """
    note = get_object_or_404(Note, pk=object_id)
    user = request.user

    return render_to_response(request,
                              'sigma.www/note_detail.html',
                              {"note" : note,
                               'request': request,
                               'user' : user,
                                })

@login_required
def edit(request, object_id):
    """Edition d'une note d'une candidature

    @param request La requete http
    @param object_id L'identificateur de la note
    """
    note = get_object_or_404(Note, pk=object_id)
    candidature_id = None

    form = NoteEditForm(instance=note)

    if "candidature_id" in request.GET:
        candidature_id = request.GET["candidature"]
        candidature = get_object_or_404(Candidature, pk=candidature_id)
        form.instance.candidature = candidature
    elif request.method == "POST":
        form = NoteEditForm(request.POST, instance=note)
        candidature_id = request.POST["candidature"]
        candidature = get_object_or_404(Candidature, pk=candidature_id)
        form.instance.candidature = candidature
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/notes/detail/%s/' % form.instance.id)
    else:
        candidature_id = note.candidature.id

    return render_to_response(request,
                              'sigma.www/note_edit.html',
                              {'form': form,
                               'object_id': object_id,
                               'candidature_id': candidature_id,
                               })
            
