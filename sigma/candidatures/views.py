# -*- encoding: utf-8 -*-

from auf.django.permissions import get_rules
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from forms import \
        DisciplineForm, NoteExpertForm, CommentaireForm, \
        EvaluationForm, ExpertForm
from models import Dossier, Commentaire, Expert


@login_required
def mes_disciplines(request, ):
    if request.method == "POST":
        form = DisciplineForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Les disciplines ont été enregistrées.")
            return redirect(reverse('admin:index'))
    else:
        form = DisciplineForm(instance=request.user.profile)

    return render_to_response("admin/candidatures/mes_disciplines.html", {
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
def evaluer(request, dossier_id):
    dossier = Dossier.objects.get(id=dossier_id)
    if request.method == "POST":
        noteForm = NoteExpertForm(instance=dossier, data=request.POST)
        commentaireForm = CommentaireForm(data=request.POST)
        evaluationForm = EvaluationForm(data=request.POST, instance=dossier)

        if noteForm.is_valid():
            noteForm.save()
            messages.success(request, "Les notes ont été enregistrées.")

        if commentaireForm.is_valid():
            commentaire = commentaireForm.save(commit=False)
            commentaire.user = request.user
            commentaire.dossier = dossier
            commentaire.save()
            dossier.annotations.add(commentaire)
            dossier.save()
            messages.success(request, "Le commentaire a été ajouté.")

        if  evaluationForm.is_valid():
            evaluationForm.save()
            messages.success(request, "Les évaluations ont été enregistrées.")

        return redirect(reverse('evaluer', args=[dossier.id]))
    else:
        noteForm = NoteExpertForm(instance=dossier)
        commentaireForm = CommentaireForm()
        evaluationForm = EvaluationForm(instance=dossier)

    return render_to_response("admin/candidatures/evaluer.html", {
        'dossier': dossier,
        'noteForm': noteForm,
        'commentaireForm': commentaireForm,
        'evaluationForm': evaluationForm,
    }, context_instance=RequestContext(request))


@login_required
def supprimer_mon_commentaire(request, note_id):
    commentaire = Commentaire.objects.get(id=note_id)
    dossier = commentaire.dossier_set.all()[0]
    dossier_url = reverse('evaluer', args=[dossier.id])
    if request.user == commentaire.user:
        commentaire.delete()
        messages.success(request, "Votre commentaire a été supprimé.")
    return redirect(dossier_url)


@login_required
def affecter_experts_dossiers(request):
    dossier_ids = request.GET.get('ids').split(',')
    dossiers = Dossier.objects.filter(id__in=dossier_ids)

    if request.method == "POST":
        form = ExpertForm(request.POST, dossiers=dossiers)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Les experts ont été affectés aux dossiers.")
            return redirect("admin:candidatures_dossier_changelist")
    else:
        form = ExpertForm(dossiers=dossiers)

    form.fields['experts'].queryset = get_rules().filter_queryset(
        request.user, 'assign', Expert.objects.all()
    )

    return render_to_response("admin/candidatures/affecter_experts.html", {
        'form': form,
    }, context_instance=RequestContext(request))
