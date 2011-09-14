# -*- encoding: utf-8 -*-

import datetime
from django.db import models

MODELES_SIGMA = ('Dossier', 'DossierOrigine', 'DossierAccueil', 'DossierMobilite', 'Candidat', 'Piece', 'AttributWCS',)

class Spool(models.Model):
    appel = models.ForeignKey('sigma.Appel', verbose_name=u"Appel", related_name="spools")

    requesting = models.BooleanField(default=False)
    date_requesting_debut = models.DateTimeField(null=True)
    date_requesting_fin = models.DateTimeField(null=True)

    processing = models.BooleanField(default=False)
    date_processing_debut = models.DateTimeField(null=True)
    date_processing_fin = models.DateTimeField(null=True)

    log = models.TextField(null=True)

    def __unicode__(self):
        return u"%s REQ:%s PRO:%s" % (self.appel, self.requesting, self.processing)

    def _get_importeur(self):
        from tools import Appel as AppelImporteur
        return AppelImporteur()
    importeur = property(_get_importeur)
        

    def preparer(self):
        if self.appel and self.appel.formulaire_wcs:
            self.requesting = True
            self.save()

    def demander(self):
        if self.appel and self.appel.formulaire_wcs and self.date_requesting_fin is not None:
            self.processing = True
            self.save()

    def dryrun(self):
        if self.appel and self.appel.formulaire_wcs:
            self.importeur.importer(self.appel.formulaire_wcs)
            self.date_requesting_fin = datetime.datetime.now()
            self.requesting = False
            self.log = u"\n".join(self.importeur.messages)
            self.save()

    def run(self):
        if self.appel and self.appel.formulaire_wcs:
            self.importeur.importer(self.appel.formulaire_wcs, mode='run')
            self.date_processing_fin = datetime.datetime.now()
            self.processing = False
            self.log = u"\n".join(self.importeur.messages)
            self.save()

    def diff_champs(self):
        if self.appel and self.appel.formulaire_wcs:
            module_name =  self.importeur._safe_module_name(self.appel.formulaire_wcs)
            mapping = self.importeur.get_mapping_module(module_name)

            status, data = self.importeur.wcs.test(self.appel.formulaire_wcs)
            if status:
                champs_traites = [mapping.MAPPING[f] for f in mapping.MAPPING.keys() if f in data]
                champs_non_traites = [f for f in data if f not in mapping.MAPPING.keys()]
                return {'champs_traites' : champs_traites, 'champs_non_traites' : champs_non_traites}
        return None
        
