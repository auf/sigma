# -*- encoding: utf-8 -*-

from django.db.models.signals import post_init

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
    for type_property in instance_type_properties:
        if type_property not in meta_properties:
            type_property.delete()

class PropertyRegisty(object):

    mapping = {}    

    def register(self, instance_model):
        post_init.connect(synchro, sender=instance_model)
        

dynamo_registry = PropertyRegisty()

