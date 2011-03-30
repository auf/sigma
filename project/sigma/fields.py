# -*- encoding: utf-8 -*-

import os
from django import forms
from django.core.files.storage import FileSystemStorage as Storage
from django.utils.safestring import mark_safe
import settings

PIECE_STORAGE = Storage(location=os.path.join(settings.MEDIA_PRIVE_ROOT, 'pieces'), base_url='/media_prive/pieces/')

class PieceFileInput(forms.widgets.FileInput):

    def render(self, name, value, attrs=None):
        html = super(PieceFileInput, self).render(name, None, attrs=attrs)
        if value != '' and PIECE_STORAGE.exists(value):
            lien = u"<a href='%s'>Télécharger</a>" % (PIECE_STORAGE.url(value))
        else:
            lien = u""
        return  mark_safe(u"%s %s" % (html, lien))

TEXT = 1
TEXTAREA = 2
EMAIL = 3
CHECKBOX = 4
CHECKBOX_MULTIPLE = 5
SELECT = 6
SELECT_MULTIPLE = 7
RADIO_MULTIPLE = 8
FILE = 9
DATE = 10
DATE_TIME = 11
HIDDEN = 12

TYPE_PIECES = {
    TEXT : {
        'nom' : "Une ligne",
        'field' : forms.CharField,
        'extra' : {'help_text' : 'help!', }, },
    TEXTAREA : {
        'nom' : "Plusieurs lignes",
        'field' : forms.CharField,
        'extra' : {},
    },
    CHECKBOX : {
        'nom' : "Case à cocher",
        'field' : forms.BooleanField,
        'extra' : {'required' : False, },
     },
    FILE : {
        'nom' :  "Fichier",
        'field' : forms.FileField,
        'extra' : {'widget' : PieceFileInput, },
    },
    DATE : {
        'nom' : "Date",
        'field' : forms.DateField,
        'extra' : {},
    },
}


