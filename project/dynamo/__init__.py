# -*- encoding: utf-8 -*-

from django.db.models.signals import post_init
from fields import PROPERTY_TYPES

def synchro(sender, instance, signal, *args, **kwargs):
    
    # To setup properties, instance has to exists
    if instance.id is None:
        return

    # Get MetaModel
    f_meta_model = instance.get_metamodel_fieldname()
    metamodel = getattr(instance, f_meta_model)
    
    # Get MetaModel defined properties
    f_meta_properties = metamodel.get_properties_fieldname()
    meta_properties = getattr(metamodel, f_meta_properties).all()

    # Get InstanceModel prorperties already presents
    f_inst_properties = instance.get_properties_fieldname()
    instance_properties = getattr(instance, "%s_set" % f_inst_properties).all()

    # Loop in properties in MetaModel but not yet in InstanceModel and create ones
    instance_type_properties = [p.type for p in instance_properties]    
    for new_type_property in [p for p in meta_properties if p not in instance_type_properties]:
        ClassProperty = instance.get_properties_model()
        new_property = ClassProperty()
        f_instance = new_property.get_instance_fieldname()
        setattr(new_property, f_instance, instance)
        new_property.type = new_type_property
        new_property.save()

    # Delete properties remove from MetaModel
    for p in instance_properties:
        if p.type not in meta_properties:
            p.delete()

class PropertyRegisty(object):

    def register(self, instance_model):
        """
        Register InstanceModel in your application.
        """
        post_init.connect(synchro, sender=instance_model)
        
    def add_properties(self, prop):
        """
        Extends property type available : 

        from django import forms
        from datamaster_modeles.models import Etablissement
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
        """
        PROPERTY_TYPES.update(prop)

dynamo_registry = PropertyRegisty()
