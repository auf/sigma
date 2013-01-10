# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Allocation


@login_required
def desiste(request):
    redirect = (request.GET.get('redirect', None)
                or reverse('admin:boursiers_allocataire_changelist'))
    allocation = get_object_or_404(
        Allocation,
        pk=request.GET.get('allocation', None))
    allocation.desiste = True
    allocation.save()
    return HttpResponseRedirect(redirect)


@login_required
def undesiste(request):
    redirect = (request.GET.get('redirect', None)
                or reverse('admin:boursiers_allocataire_changelist'))
    allocation = get_object_or_404(
        Allocation,
        pk=request.GET.get('allocation', None))
    allocation.desiste = False
    allocation.save()
    return HttpResponseRedirect(redirect)
