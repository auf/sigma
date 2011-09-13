# -*- encoding: utf-8 -*-

import os
import re
from django import forms
from datamaster_modeles import models as ref

def code_from_pattern(pattern=r'^$', s=u''):
    if s is None:
        s = u''
    output = s
    if s :
        m = re.match(pattern, s)
        if m and m.group('code'):
            output = m.group('code')
    return output

def str2pays(s):
    """
    Exemple :
    input = Arménie (AM - Europe centrale et orientale)
    output = id de l'objet Pays
    """
    if s is None:
        return s

    pattern = r'.*\((?P<code>\w{2}).*\)$'
    code_pays = code_from_pattern(pattern, s)
    try:
        return ref.Pays.objects.get(code=code_pays).id
    except:
        raise forms.ValidationError("REGEX Pays : %s" % s)

def str2discipline(s):
    """
    Exemple :
    input = Anthropologie (D104)
    output = id de l'objet Reference
    """
    if s is None:
        return s
    pattern = r'.*\((?P<code>\w*)\)$'
    code_discipline = code_from_pattern(pattern, s)
    try:
        return ref.Discipline.objects.get(code=code_discipline).id
    except:
        raise forms.ValidationError("REGEX Discipline : %s" % s)
    
