# -*- encoding: utf-8 -*-

from project.sigma import models as sigma

class Importeur(object):

    appel = None
    wcs_data = None
    mapped_data = None
    mapping_module = None
    forms = {}

    def __init__(self, appel, wcs_data, mapping_module):
        self.mapping_module = mapping_module
        self.wcs_data = wcs_data
        self.appel = appel


    def map_wcs2sigma(self):
        """
        Map les données provenant de WCS avec les champs de SIGMA.
        """
        mapped_data = {}
        for k, v in self.wcs_data.items():
            if k in self.mapping_module.MAPPING.keys():
                classname, attribut = self.mapping_module.MAPPING[k]
                if not mapped_data.has_key(classname):
                    mapped_data[classname] = {}
                mapped_data[classname][attribut] = v
        return mapped_data
    

    def preprocess(self):
        """
        Construction des forms à partir des data.
        """
        mapped_data = self.map_wcs2sigma()

        for classname, data in mapped_data.items():
            form_name = "%sForm" % classname
            klass = getattr(self.mapping_module, form_name)
            self.forms[classname] = klass(data)

    def validate(self):
        """
        Validation de tous les forms.
        """
        status = True
        errors = None
        for classname, f in self.forms.items():
            if not f.is_valid():
                status = False
                errors[classname] = f.errors
        return status, errors
            
    def dbwrite(self):
        """
        Écriture des objets en BD si l'objet n'existe pas.
        """
        dossierForm = self.forms['Dossier']
        candidatForm = self.forms['Candidat']
        
        dossier = dossierForm.save(commit=False)
        candidat = candidatForm.save(commit=False)

        test = sigma.Dossier.objects.filter(appel=self.appel, candidat__nom=candidat.nom, candidat__prenom=candidat.prenom)
        if len(test) > 0:    
            print "Ce dossier a déjà été importé : %s" % test[0]
            return

        dossier.appel = self.appel
        dossier.save()

        candidat.dossier = dossier
        candidat.save()

    def dryrun(self):
        """
        Test SANS écritures db.
        """
        self.preprocess()
        status, errors = self.validate()
        if not status:
            return errors
  
    def run(self):
        """
        Test AVEC écritures db.
        """
        self.dryrun()
        self.dbwrite()
