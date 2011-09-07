# -*- encoding: utf-8 -*-

import simplejson as json
import re
import urllib2
import os
from django.conf import settings

CACHE_PATH = os.path.join(os.path.dirname(__file__), '_cache')

class WCS(object):

    def __init__(self):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, settings.WCS_SIGMA_URL, settings.WCS_SIGMA_USER, settings.WCS_SIGMA_PASS)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)

        if not os.path.exists(CACHE_PATH):
            os.mkdir(CACHE_PATH)
 
    def clear(self):
        """
        Supprime tous les fichiers de caches.
        """
        for root, dirs, files in os.walk(CACHE_PATH):
            for f in files:
                os.remove(os.path.join(root, f))

    def _retrieve(self, url):
        key = "_" + url.replace('/', '-')
        file_path = os.path.join(CACHE_PATH, key)
        if os.path.exists(file_path):
            f = open(file_path, 'r')
            data = f.read()
            f.close()
        else:
            url = "%s%s" % (settings.WCS_SIGMA_URL, url)
            if settings.DEBUG:
                print url
            req = urllib2.urlopen(url)
            data = req.read()
            f = open(file_path, 'w+')
            f.write(data)
            f.close()
            req.close()
        return data


class WCSAppel(WCS):
    """
    Wrapper pour obtenir les infos de formulaires.auf.org
    """
    _cache_dossiers = None
    _cache_appels = None

    re_appel = re.compile('href=[\'"]([^?\'"]+)/[\'"]')
    re_dossier = re.compile('href=[\'"]([^?\'"]+)\.json[\'"]')

    def liste(self):
        """
        retourne la liste des appels disponibles.
        """
        if self._cache_appels is not None:
            return self._cache_appels
        html_liste = self._retrieve('')
        self._cache_appels = self.re_appel.findall(html_liste, re.M)
        return self._cache_appels

    def appel_id2txt(self, appel_id):
        """
        retourne le nom de l'appel à partir de l'id de la liste.
        """
        try:
            idx = int(appel_id)
            liste_appels = self.liste()
            return liste_appels[idx]
        except ValueError:
            return appel_id

    def dossiers(self, appel_id):
        """
        retourne la liste des dossiers d'un appel (id).
        """
        if self._cache_dossiers is not None:
            return self._cache_dossiers

        appel_nom = self.appel_id2txt(appel_id)
        url = "%s/data" % appel_nom
        html_liste = self._retrieve(url)
        self._cache_dossiers = self.re_dossier.findall(html_liste, re.M)
        return self._cache_dossiers

    def dossier_id2txt(self, appel_id, dossier_id):
        """
        retourne le nom du dossier à partir de l'id de la liste.
        """
        idx = int(dossier_id)
        liste_dossiers = self.dossiers(appel_id)
        return liste_dossiers[idx]

    def dossier(self, appel_id, dossier_id):
        """
        retourne un dictionnaire représentant le dossier.
        """
        appel_nom = self.appel_id2txt(appel_id)
        d = self.dossier_id2txt(appel_id, dossier_id)
        url = "%s/data/%s.json" % (appel_nom, d)
        dossier_json = self._retrieve(url)
        return json.loads(dossier_json)

    def test(self, appel_id):
        """
        Test d'intégrité de tous les dossiers entre eux.
        """
        # dico de tous les dossiers
        dossiers = []
        liste_dossiers = self.dossiers(appel_id)
        for idx, dossier_nom in enumerate(liste_dossiers):
            dossier = self.dossier(appel_id, idx)
            dossiers.append(dossier)
        
        # création d'un set étalon pour comparer
        etalon_champs = []
        for d in dossiers:
            etalon_champs.extend(d.keys())
        etalon_set = set(etalon_champs)

        # comparasion de tous les dossier à l'étalon
        errors = []
        champs = {}
        for d in dossiers:
            diff = etalon_set.difference(set(d.keys()))
            if len(diff) > 0:
                errors.append((d, diff))
            champs = d.keys()

        if len(errors) == 0:
            return True, champs
        else:
            return False, errors


