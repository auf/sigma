# -*- encoding: utf-8 -*-

import os
from wrappers import WCSAppel
from models import MODELES_SIGMA
from utils import Importeur
from project.sigma import models as sigma
from django.template.loader import render_to_string

DEFAULT_MAPPING = 'default_mapping'

class Appel:

    wcs = WCSAppel()

    def clear(self):
        self.wcs.clear()

    def liste(self):
        appels = self.wcs.liste()
        print u"Liste des appels"
        print "="*80
        for idx, appel in enumerate(appels):
            print u"* %s : %s" % (str(idx).zfill(3), appel)

    def dossiers(self, appel_id):
        dossiers = self.wcs.dossiers(appel_id)
        print u"Liste des dossiers de l'appel : %s" % self.wcs.appel_id2txt(appel_id)
        print "="*80
        for idx, dossier in enumerate(dossiers):
            print u"* %s : %s" % (str(idx).zfill(3), dossier)

    def test(self, appel_id):
        print u"Test des données l'appel : %s" % self.wcs.appel_id2txt(appel_id)
        statut, errors = self.wcs.test(appel_id)
        if statut:
            print 'Intégrité OK'
        else:
            for e in errors:
                print "* %s : %s" % e

    def dossier(self, appel_id, dossier_id):
        print u"Dossier : %s" % self.wcs.dossier_id2txt(appel_id, dossier_id)
        print "="*80
        for k, v in self.wcs.dossier(appel_id, dossier_id).items():
            print "* %-40s : %s" % (k, v)

    def default_mapping(self):
        champs = {}
        for modele_name in MODELES_SIGMA:
            mod = getattr(sigma, modele_name)
            champs[modele_name] = {}
            for f in  mod._meta.fields:
                k = "sigma|%s|%s" % (modele_name, f.name)
                champs[modele_name][k] = (modele_name, f.name)
        data = render_to_string('wcs/default_mapping.txt', {"champs": champs}, )

        default_mapping = os.path.join(os.path.dirname(__file__), 'conf', "%s.py" % DEFAULT_MAPPING)
        if not os.path.exists(default_mapping):
            f = open(default_mapping, 'w+',)
            f.write(data)
            f.close()
            print "Fichier crée : %s" % default_mapping
        else:
            print "Le fichier existe déjà!"


    def _safe_module_name(self, nom):
        nom.lower()
        nom = nom.replace('-', '_')
        nom = nom.replace('.', '_')
        return nom

    def custom_mapping(self, appel_id):
        from conf import default_mapping
        statut, data = self.wcs.test(appel_id)
        if statut is False:
            return
        surcharge = {}
        wcs = {}
        for f in data:
            if f in default_mapping.MAPPING.keys():
                surcharge[f] = ('', '')
            else:
                wcs[f] = ('', '')

        champs = {u'surcharge defaut' : surcharge, u'wcs specifique' : wcs, }
        data = render_to_string('wcs/custom_mapping.txt', {"champs": champs}, )

        appel_nom = self._safe_module_name(self.wcs.appel_id2txt(appel_id))
        custom_mapping = os.path.join(os.path.dirname(__file__), 'conf', "%s.py" % appel_nom)
        if not os.path.exists(custom_mapping):
            f = open(custom_mapping, 'w+',)
            f.write(data)
            f.close()
            print "Fichier crée : %s" % custom_mapping
        else:
            print "Le fichier existe déjà!"
    
    def get_mapping_module(self, module_name):
        conf = __import__('conf',  globals(), locals(), [module_name, DEFAULT_MAPPING], -1)
        try:
            mapping = conf.__dict__[module_name]
        except:
            mapping = conf.__dict__[DEFAULT_MAPPING]
        return mapping

    def importer(self, appel_id, mode='dryrun'):
        if mode not in ('dryrun', 'run'):
            print "mode : 'dryrun', 'run'"
            return

        appel_nom = self.wcs.appel_id2txt(appel_id)
        module_name =  self._safe_module_name(appel_nom)
        mapping = self.get_mapping_module(module_name)
        dossiers = self.wcs.dossiers(appel_id)

        try:
            appel = sigma.Appel.objects.get(nom=appel_nom)
        except:
            print "L'appel n'existe pas dans SIGMA : %s" % appel_nom
            return

        print u"Importation des dossiers de l'appel : %s" % appel_nom
        for dossier_id, dossier_nom in enumerate(dossiers[0:1]):
            dossier_data = self.wcs.dossier(appel_id, dossier_id)
            importeur = Importeur(appel, dossier_data, mapping)
            method = getattr(importeur, mode)
            errors = method()
            if errors:
                print errors
                
