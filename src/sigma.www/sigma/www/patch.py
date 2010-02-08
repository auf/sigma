# -=- encoding: utf-8 -=-

from django.utils.translation import ugettext as _
from sigma.www.forms import SigmaModelForm
from sigma.www import DEFAULT_SUBJECT

#
# Ajout d'un champs subject aux champs du modele de donnees
#
import django.db.models.fields

from django.db.models import NOT_PROVIDED

old__django_forms_fields_init__ = django.db.models.fields.Field.__init__

def new__django_forms_fields_init__(self, *args, **kwargs):
    """ 
    Ajout du champs subject aux champs du modele afin de pouvoir les regroupes
    dans des blocs bien definies dans les formulaires par exemple

    @param ...
    @param subject
    """
    try:
        setattr(self, 'subject', kwargs['subject'])
        del kwargs['subject']
    except (AttributeError, KeyError):
        setattr(self, 'subject', DEFAULT_SUBJECT)
    old__django_forms_fields_init__(self, *args, **kwargs)
django.db.models.fields.Field.__init__ = new__django_forms_fields_init__


#
# Ajout d'un champs subject aux champs des formulaires
#
import django.forms
import django.forms.fields
import django.db.models.fields

old_django_forms_fields_field___init__ = django.forms.fields.Field.__init__

def new_django_forms_fields_field___init__(self, *args, **kwargs):
    """Initialisation du sujet du champs du formulaire a notre sujet par defaut

    @param ...
    """
    setattr(self, 'subject', DEFAULT_SUBJECT)
    old_django_forms_fields_field___init__(self, *args, **kwargs)
django.forms.fields.Field.__init__ = new_django_forms_fields_field___init__


old_django_db_models_fields__init___Field_formfield = django.db.models.fields.Field.formfield

def new_django_db_models_fields__init___Field_formfield(self, *args, **kwargs):
    """Extraction du sujet qui a ete definit dans le modele et application au champs du formulaire

    @param ...
    """
    form_obj = old_django_db_models_fields__init___Field_formfield(self, *args, **kwargs)
    try:
        subject = getattr(self, 'subject')
        setattr(form_obj, 'subject', subject)
    except (AttributeError, KeyError):
        setattr(form_obj, 'subject', DEFAULT_SUBJECT)
    return form_obj
django.db.models.fields.Field.formfield = new_django_db_models_fields__init___Field_formfield

#
# Gestion des champs obligatoire pour les boundfield des formulaires
#
import django.forms.forms

old_django_forms_forms_boundfield_label_tag = django.forms.forms.BoundField.label_tag

def new_django_forms_forms_boundfield_label_tag(self, contents=None, attrs=None):
    """
    Gestion des champs obligatoire pour les formulaires

    @param contents=None
    @param attrs=None
    """
    if not isinstance(self.form, SigmaModelForm):
        return old_django_forms_forms_boundfield_label_tag(self, contents, attrs)

    if contents is not None:
        if self.field.required:
            contents = "* %s" % contents
    content = old_django_forms_forms_boundfield_label_tag(self, contents, attrs)
    
    if self.field and self.field.required:
        return content.replace("label", "label class='mandatory'", 1)
    else:
        return content
django.forms.forms.BoundField.label_tag = new_django_forms_forms_boundfield_label_tag
        




