# -*- encoding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from fields import PROPERTY_TYPES_CHOICES

class TypeProperty(models.Model):
    """
    Class which represent a property : type + name.
    It's used by the MetaModel and the ValueProperty.
    """
    name = models.CharField(verbose_name=_("Nom"), max_length=255)
    field_type = models.IntegerField(verbose_name=_("Type"), choices=PROPERTY_TYPES_CHOICES)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

class MetaModel(models.Model):
    """
    Class where properties type and name will be defined.
    """
    class Meta:
        abstract = True

    def get_properties_fieldname(self):
        """
        Introspect child instance, to get the m2m field name which represents TypeProperty.
        """
        for f in self._meta.many_to_many:
            if TypeProperty in f.related.parent_model.__bases__:
                return f.name
        
        raise Exception('%s : There is no TypeProperty child class m2m in %s' % \
                        (self._meta.app_label, self.__class__.__name__))


class InstanceModel(models.Model):
    """
    Class where properties will be linked and filled with data.
    """
    # demo for child class
    # metathing = models.ForeignKey(MetaModel)

    class Meta:
        abstract = True


    def get_metamodel_fieldname(self):
        """
        Introspect child instance, to get the foreignkey field name which represents MetaModel.
        """       
        fk_fields = [f for f in self._meta.fields if f.__class__.__name__ == 'ForeignKey']
        for f in fk_fields:
            if MetaModel in f.related.parent_model.__bases__:
                return f.name
        
        raise Exception('%s : There is no MetaModel child class foreign key in %s' % \
                        (self._meta.app_label, self.__class__.__name__))

    def get_properties_model(self):
        """
        Introspect child instance, to get the foreignkey model which represents ValueProperty.
        """       
        for o in self._meta.get_all_related_objects():
            if ValueProperty in o.model.__bases__:
                return o.model
        
        raise Exception('%s : There is no ValueProperty child class foreign key in %s' % \
                        (self._meta.app_label, self.__class__.__name__))

    def get_properties_fieldname(self):
        """
        Introspect child instance, to get the foreignkey field name which represents ValueProperty.
        """       
        for o in self._meta.get_all_related_objects():
            if ValueProperty in o.model.__bases__:
                return o.var_name
        
        raise Exception('%s : There is no ValueProperty child class foreign key in %s' % \
                        (self._meta.app_label, self.__class__.__name__))


class ValueProperty(models.Model):
    """
    Class which store property value of an Instance.
    """
    # demo for child class
    # thing = models.ForeignKey(InstanceModel)

    value = models.CharField(verbose_name=_("Valeur"), max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def get_instance_fieldname(self):
        """
        Introspect child instance, to get the foreignkey field name which represents InstanceModel.
        """       
        fk_fields = [f for f in self._meta.fields if f.__class__.__name__ == 'ForeignKey']
        for f in fk_fields:
            if InstanceModel in f.related.parent_model.__bases__:
                return f.name
        
        raise Exception('%s : There is no InstanceModel child class foreign key in %s' % \
                        (self._meta.app_label, self.__class__.__name__))

    def __unicode__(self,):
        return self.type.__unicode__()

