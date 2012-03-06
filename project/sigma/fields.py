# -*- encoding: utf-8 -*-

from django import forms
from auf.django.references.models import Etablissement
from dynamo import dynamo_registry

ETABLISSEMENT = 1001
ETABLISSEMENT_CHOICES = [(e.id, e.nom) for e in Etablissement.objects.all()]
field_etablissement = {
    ETABLISSEMENT : {
        'name' : u"[AUF] Établissement",
        'field' : forms.ChoiceField,
        'extra' : {'required' : False, 'choices' : ETABLISSEMENT_CHOICES},
    },
}

dynamo_registry.add_properties(field_etablissement)
