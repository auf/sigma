# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from forms import DisciplineForm, NoteExpertForm, CommentaireForm, EvaluationForm, ExpertForm
from models import Dossier, Note, Commentaire

@login_required
def mes_disciplines(request, ):
    if request.method == "POST":
        form = DisciplineForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="Les disciplines ont été enregistrées.")
            return redirect(reverse('admin:index'))
    else:
        form = DisciplineForm(instance=request.user.profile)
    
    c = {'form' : form, }
    return render_to_response("admin/sigma/mes_disciplines.html", \
                               Context(c), \
                               context_instance = RequestContext(request))
@login_required
def evaluer(request, dossier_id):
    dossier = Dossier.objects.get(id=dossier_id)
    if request.method == "POST":
        noteForm = NoteExpertForm(instance=dossier, data=request.POST)
        commentaireForm = CommentaireForm(data=request.POST)
        evaluationForm = EvaluationForm(data=request.POST, instance=dossier)

        if noteForm.is_valid():
            noteForm.save()
            message = "Les notes ont été enregistrées."
            request.user.message_set.create(message=message)

        if commentaireForm.is_valid():
            commentaire = commentaireForm.save(commit=False)
            commentaire.user = request.user
            commentaire.dossier = dossier
            commentaire.save()
            dossier.annotations.add(commentaire)
            dossier.save()
            message = "Le commentaire a été ajouté."
            request.user.message_set.create(message=message)

        if  evaluationForm.is_valid():
            evaluationForm.save()
            message = "Les évaluations ont été enregistrées."
            request.user.message_set.create(message=message)

        return redirect(reverse('evaluer', args=[dossier.id]))
    else:
        noteForm = NoteExpertForm(instance=dossier)
        commentaireForm = CommentaireForm()
        evaluationForm = EvaluationForm(instance=dossier)
    
    c = {
        'dossier' : dossier,
        'noteForm' : noteForm,
        'commentaireForm' : commentaireForm,
        'evaluationForm' : evaluationForm,    
    }
    return render_to_response("admin/sigma/evaluer.html", \
                               Context(c), \
                               context_instance = RequestContext(request))
        
@login_required
def supprimer_mon_commentaire(request, note_id):
    commentaire = Commentaire.objects.get(id=note_id)
    dossier = commentaire.dossier_set.all()[0]
    dossier_url = reverse('evaluer', args=[dossier.id])
    if request.user == commentaire.user:
        commentaire.delete()
        request.user.message_set.create(message="Votre commentaire a été supprimé.")
    return redirect(dossier_url)
    
@login_required 
def affecter_experts_dossiers(request):
    dossier_ids = request.GET.get('ids').split(',')
    dossiers = Dossier.objects.filter(id__in=dossier_ids)
    
    if request.method == "POST":
        form = ExpertForm(request.POST, dossiers=dossiers)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Les experts ont été affectés aux dossiers.")
            return redirect("admin:sigma_appel_changelist")
    else:
        form = ExpertForm(dossiers=dossiers)

    c = {'form' : form}
    return render_to_response("admin/sigma/affecter_experts.html", \
                               Context(c), \
                               context_instance = RequestContext(request))
        
