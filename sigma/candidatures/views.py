# -*- encoding: utf-8 -*-

from auf.django.permissions import get_rules
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from forms import \
        DisciplineForm, CommentaireForm, \
        EvaluationForm, ExpertForm, NoteFormSet
from models import Dossier, Commentaire, Expert, NOTE_MIN, NOTE_MAX


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
        expert_form = ExpertForm(
            request.POST,
            dossiers=[dossier],
            request=request,
            initial={
                'experts': dossier.experts.all()
                },
            )
        notes_formset = NoteFormSet(instance=dossier, data=request.POST)
        commentaireForm = CommentaireForm(data=request.POST)
        evaluationForm = EvaluationForm(data=request.POST, instance=dossier)

        if expert_form.is_valid():
            expert_form.save()
            messages.success(request, "Les experts ont été affectés.")
        else:
            for key in expert_form.errors.keys():
                for err in expert_form.errors[key]:
                    messages.error(request, err)

        if notes_formset.is_valid():
            notes_formset.save()
            messages.success(request, "Les notes ont été enregistrées.")

        if notes_formset.is_valid() and commentaireForm.is_valid():
            commentaire = commentaireForm.save(commit=False)
            commentaire.user = request.user
            commentaire.dossier = dossier
            commentaire.save()
            dossier.annotations.add(commentaire)
            dossier.save()
            messages.success(request, "Le commentaire a été ajouté.")

        if notes_formset.is_valid() and evaluationForm.is_valid():
            evaluationForm.save()
            messages.success(request, "Les évaluations ont été enregistrées.")

        if notes_formset.is_valid():
            return redirect(reverse('evaluer', args=[dossier.id]))

    else:
        expert_form = ExpertForm(
            dossiers=[dossier],
            request=request,
            initial={
                'experts': dossier.experts.all()
                },
            )
        notes_formset = NoteFormSet(instance=dossier)
        commentaireForm = CommentaireForm()
        evaluationForm = EvaluationForm(instance=dossier)

    return render_to_response(
        "admin/candidatures/evaluer.html", {
            'dossier': dossier,
            'NOTE_MIN': NOTE_MIN,
            'NOTE_MAX': NOTE_MAX,
            'expert_form': expert_form,
            'notes_formset': notes_formset,
            'commentaireForm': commentaireForm,
            'evaluationForm': evaluationForm,
            },
        context_instance=RequestContext(request))


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
        form = ExpertForm(request.POST, dossiers=dossiers, request=request)
        if form.is_valid():
            form.save()
            messages.success(request,
                             "Les experts ont été affectés aux dossiers.")
            return redirect("admin:candidatures_dossier_changelist")
    else:
        form = ExpertForm(dossiers=dossiers, request=request)

    return render_to_response("admin/candidatures/affecter_experts.html", {
        'form': form,
    }, context_instance=RequestContext(request))
