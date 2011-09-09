# -*- encoding: utf-8 -*-

import os
import re
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
    pattern = r'.*\((?P<code>\w{2}).*\)$'
    code_pays = code_from_pattern(pattern, s)
    try:
        return ref.Pays.objects.get(code=code_pays).id
    except:
        raise forms.ValidationError("REGEX Pays : %s" % s)

    
