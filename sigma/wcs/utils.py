# -*- encoding: utf-8 -*-

from django.core.files.uploadedfile import InMemoryUploadedFile
from sigma.candidatures import models as sigma

class Importeur(object):

    def __init__(self, appel, wcs_data, mapping_module):
        self.mapping_module = mapping_module
        self.wcs_data = wcs_data
        self.appel = appel
        self.forms = {}

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
        for classname in ['Dossier', 'Candidat', 'Diplome', 'DossierOrigine',
                          'DossierAccueil', 'DossierMobilite', 'Piece']:
            data = mapped_data.get(classname, {})
            form_name = "%sForm" % classname
            klass = getattr(self.mapping_module, form_name)
            files = {}
            for k, v in data.items():
                if isinstance(v, InMemoryUploadedFile):
                    files[k] = v
            self.forms[classname] = klass(data, files)

    def validate(self):
        """
        Validation de tous les forms.
        """
        status = True
        errors = {}
        for classname, f in self.forms.items():
            if not f.is_valid():
                status = False
                errors[classname] = f.errors
        return status, errors
    
    def dbwrite(self):
        """
        Écriture des objets en BD si l'objet n'existe pas.
        Établissement des liens entre les objets.
        """
        dossierForm = self.forms.pop('Dossier')
        candidatForm = self.forms.pop('Candidat')
        dossier = dossierForm.save(commit=False)
        candidat = candidatForm.save(commit=False)

        # Test la présence d'un dossier similaire
        test = sigma.Dossier.objects.filter(
            appel=self.appel, 
            candidat__nom=candidat.nom, 
            candidat__prenom=candidat.prenom
        )
        if len(test) > 0:
            return True, u"Ce dossier a déjà été importé : %s" % test[0]

        # Création des objets et de leurs relations
        dossier.appel = self.appel
        dossier.save()

        candidat.dossier = dossier
        candidat.save()

        if self.forms.has_key('Piece'):
            pieceForm = self.forms.pop('Piece')
            instances = pieceForm.save(commit=False)
            for instance in instances:
                instance.dossier = dossier
                instance.save()

        for key, form in self.forms.iteritems():
            instance = form.save(commit=False)
            instance.dossier = dossier
            if key in ['DossierOrigine', 'DossierAccueil'] and instance.etablissement:
                instance.pays = instance.etablissement.pays
            instance.save()

        # Copie des données WCS
        for k, v in self.wcs_data.items():
            data = sigma.AttributWCS()
            data.dossier = dossier
            data.attribut = k
            data.valeur = unicode(v)
            try:
                data.save()
            except Exception, e:
                print e
                print dossier
                print k
                print type(v)
                print v
        return True, None

    def run(self):
        self.preprocess()
        status, errors = self.validate()
        if not status:
            return errors
        status, data = self.dbwrite()
        if not status:
            return data
        else:
            return data
           
