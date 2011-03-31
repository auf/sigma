# -*- encoding: utf-8 -*-

import os
from django import forms
from django.core.files.storage import FileSystemStorage as Storage
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
import settings

media_dynamo_root = getattr(settings, 'MEDIA_DYNAMO_ROOT', settings.MEDIA_ROOT)
media_dynamo_url = getattr(settings, 'MEDIA_DYNAMO_URL', settings.MEDIA_URL)

PROPERTY_STORAGE = Storage(location=media_dynamo_root, base_url=media_dynamo_url)

class PropertyFileInput(forms.widgets.FileInput):
    """
    Improve the basic File Widget to provide a link to download the file.
    """
    def render(self, name, value, attrs=None):
        html = super(PropertyFileInput, self).render(name, None, attrs=attrs)

        link = u""
        if value != '' and PROPERTY_STORAGE.exists(value):
            link = u"<a target='_blank' href='%s'>%s</a>" % (PROPERTY_STORAGE.url(value), _(u'Télécharger'))

        return  mark_safe(u"%s %s" % (html, link))

TEXT = 1
TEXTAREA = 2
EMAIL = 3
CHECKBOX = 4
FILE = 5
DATE = 6

PROPERTY_TYPES = {
    TEXT : {
        'name' : _(u"Une ligne"),
        'field' : forms.CharField,
        'extra' : {'required' : False, },
    },
    TEXTAREA : {
        'name' : _(u"Plusieurs lignes"),
        'field' : forms.CharField,
        'extra' : {'required' : False, },
    },
    CHECKBOX : {
        'name' : _(u"Case à cocher"),
        'field' : forms.BooleanField,
        'extra' : {'required' : False, },
     },
    FILE : {
        'name' :  _(u"Fichier"),
        'field' : forms.FileField,
        'extra' : {'required' : False, 'widget' : PropertyFileInput, },
    },
    DATE : {
        'name' : _(u"Date"),
        'field' : forms.DateField,
        'extra' : {'required' : False, 'widget' : AdminDateWidget, },
    },
}


PROPERTY_TYPES_CHOICES = [(code, p['name']) for code, p in PROPERTY_TYPES.items()]
