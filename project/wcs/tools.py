# -*- encoding: utf-8 -*-

from wrappers import WCSAppel

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
