# -*- encoding: utf-8 -*-

from django import forms
from models import WCSChamps

class WCSChampsForm(forms.ModelForm):
    
    wcs = forms.ChoiceField(label=u"Champs WCS", choices=())

    class Meta:
        model = WCSChamps
