# -*- encoding: utf-8 -*-

from django import forms
from project.sigma import models as sigma


class DossierForm(forms.ModelForm):
    
    class Meta:
        model = sigma.Dossier
        exclude = ('etat', 'appel', 'candidat', )

class CandidatForm(forms.ModelForm):
 
    def clean_pays(self, value):
   
    class Meta:
        model = sigma.Candidat
        exclude = ('dossier', )
