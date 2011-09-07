# -*- encoding: utf-8 -*-

from django.db import models
#from wrappers import WCSAppel
from project.sigma import models as sigma

MODELES_SIGMA = ('Dossier', 'DossierOrigine', 'DossierAccueil', 'DossierMobilite', )

class DossierProxy(sigma.Dossier):

    class Meta:
        proxy = True

#wcs = WCSAppel()
#
#WCS_APPELS_CHOICES =[(v, v) for v in wcs.liste()]
#
#
#
#CHAMPS_SIGMA_DISPONIBLES = []
#for modele_name in MODELES_SIGMA:
#    mod = getattr(sigma, modele_name)
#    CHAMPS_SIGMA_DISPONIBLES += [("%s.%s" % (modele_name, f.name), "%s.%s (%s)" % (modele_name, f.name, f.verbose_name), ) for f in  mod._meta.fields]
#    
#TRAITEMENT_CHAMPS_WCS = (
#    ('pays', u'Pays'),
#)
#
#
#class WCSAppel(models.Model):
#    """
#    Associe un appel WCS à un appel SIGMA.
#    """
#    wcs = models.CharField(max_length=255, verbose_name=u"Appel WCS", choices=WCS_APPELS_CHOICES)
#    sigma = models.ForeignKey('sigma.Appel', verbose_name=u"Appel SIGMA")
#
#    class Meta:
#        verbose_name = u"Appel WCS"
#        verbose_name_plural = u"Appels WCS"
#
#    def __unicode__(self):
#        return self.wcs
#
#class WCSChamps(models.Model):
#    """
#    Mapping champs WCS à un champs SIGMA pour un appel.
#    """
#    appel = models.ForeignKey(WCSAppel, verbose_name=u"Appel WCS")
#    wcs = models.CharField(max_length=255, verbose_name=u"Champs WCS")
#    traitement = models.CharField(max_length=255, verbose_name=u"Traitement à l'importation", choices=TRAITEMENT_CHAMPS_WCS, null=True, blank=True)
#    sigma = models.CharField(max_length=255, verbose_name=u"Champs SIGMA", choices=CHAMPS_SIGMA_DISPONIBLES)
#    note = models.CharField(max_length=255, verbose_name=u"Note", null=True, blank=True)
#
#    class Meta:
#        verbose_name = u"Champs WCS"
#        verbose_name_plural = u"Champs WCS"
#
#    def __unicode__(self):
#        return u"WCS:%s <=> SIGMA:%s" % (self.wcs, self.sigma)

