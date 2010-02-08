# -=- encoding: utf-8 -=-
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.core import serializers

from sigma.references.models import Etablissement

def json(request, object_id):
    """
    @param request
    @param etablissement_id
    """
    etablissement = get_object_or_404(Etablissement, pk=object_id)

    json = serializers.serialize('json', [etablissement], fields=['id', 'nom', 'region'])

    return HttpResponse(json)
