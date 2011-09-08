# -*- encoding: utf-8 -*-

from models import Appel

class Importeur(object):

    appel = None
    wcs_data = None
    mapped_data = None
    mapping_module = None
    instances = {}

    def __init__(self, appel, wcs_data, mapping_module):
        self.mapping_module = mapping_module
        self.wcs_data = wcs_data
        self.appel = appel


    def get_instance_by_type(self, classname):
        if classname == '':
            return None

        if self.instances.has_key(classname):
            return self.instances[classname]

        klass = getattr(self.mapping_module, classname)
        instance = klass()
        self.instances[classname] = instance

        return instance
    
    def run(self):
        for k, v in self.wcs_data.items():
            if k in self.mapping_module.MAPPING.keys():
                classname, attribut = self.mapping_module.MAPPING[k]
                instance = self.get_instance_by_type(classname)
                if instance:
                    setattr(instance, attribut, v)


        dossier = self.instances['Dossier']
        dossier.appel = self.appel
        candidat = self.instances['Candidat']

        dossier.candidat = candidat
        print candidat
        print dossier
