# -*- encoding: utf-8 -*-

from django import forms
from fields import PROPERTY_STORAGE, PROPERTY_TYPES

class PropertyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Dynamically add each of the form fields for the given form model 
        instance and its related field model instances.
        """
        super(PropertyForm,  self).__init__(*args, **kwargs)
        try:
            code_type = self.instance.type.field_type
            class_type = PROPERTY_TYPES[code_type]['field']
            extra = PROPERTY_TYPES[code_type]['extra']
            self.fields['value'] = class_type(**extra)
        except:
            # Si c'est une piece sans instance, on ne fait rien.
            # Ce cas ne devrait pas se produite car les instances 
            # Pieces sont prépopulées à partir de l'appel
            pass


    def save(self, **kwargs):
        prop = super(PropertyForm, self).save(commit=False)

        if prop.type.field_type == 9:
            tmp_upload = self.cleaned_data['value']
            instance = getattr(prop, prop.get_instance_fieldname(), None)
            name = "%s/%s_%s" % (instance.id, prop.id, tmp_upload.name)
            PROPERTY_STORAGE.save(name, tmp_upload)
            prop.value = name

        prop.save()
        return prop

