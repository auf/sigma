# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import Context, RequestContext
from django.shortcuts import render_to_response, redirect
from forms import DisciplineForm, NoteForm, CommentaireForm
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
        noteForm = NoteForm(data=request.POST)
        commentaireForm = CommentaireForm(data=request.POST)
        if noteForm.is_valid():
            note = noteForm.save(commit=False)
            note.user = request.user
            note.save()
            dossier.notes.add(note)
            dossier.save()
            message = "La note a été ajoutée."
        if commentaireForm.is_valid():
            commentaire = commentaireForm.save(commit=False)
            commentaire.user = request.user
            commentaire.dossier = dossier
            commentaire.save()
            dossier.commentaires.add(commentaire)
            dossier.save()
            message = "Le commentaire a été ajouté."
        if noteForm.is_valid() or commentaireForm.is_valid():
            request.user.message_set.create(message=message)
            return redirect(reverse('evaluer', args=[dossier.id]))
    else:
        noteForm = NoteForm(instance=dossier)
        commentaireForm = CommentaireForm(instance=dossier)
    
    c = {'dossier' : dossier, 'noteForm' : noteForm, 'commentaireForm' : commentaireForm, }
    return render_to_response("admin/sigma/evaluer.html", \
                               Context(c), \
                               context_instance = RequestContext(request))
@login_required
def supprimer_ma_note(request, note_id):
    note = Note.objects.get(id=note_id)
    dossier = note.dossier_set.all()[0]
    dossier_url = reverse('evaluer', args=[dossier.id])
    if request.user == note.user:
        note.delete()
        request.user.message_set.create(message="Votre note a été supprimée.")
    return redirect(dossier_url)
        
@login_required
def supprimer_mon_commentaire(request, note_id):
    commentaire = Commentaire.objects.get(id=note_id)
    dossier = commentaire.dossier_set.all()[0]
    dossier_url = reverse('evaluer', args=[dossier.id])
    if request.user == commentaire.user:
        commentaire.delete()
        request.user.message_set.create(message="Votre commentaire a été supprimé.")
    return redirect(dossier_url)
        
