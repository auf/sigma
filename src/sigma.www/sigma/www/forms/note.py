# -=- encoding: utf-8 -=-
from django import forms
from django.db import models

from sigma.www.models import Note

import unicodedata

class NoteAddForm(forms.ModelForm):
    """Formulaire d'ajout d'une note"""
    class Meta:
        model = Note
        exclude = ['candidature']

    def get_action_url(self):
        return "candidatures/note/%s/" % self.instance.candidature.id

    def get_return_url(self):
        return "/candidatures/detail/%s/" % self.instance.candidature.id

class NoteEditForm(forms.ModelForm):
    """Formulaire d'edition d'une note"""
    class Meta:
        model = Note
        exclude = ['candidature']
