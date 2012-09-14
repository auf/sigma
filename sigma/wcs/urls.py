# -*- encoding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'sigma.wcs.views',
    url(r'^formulaire.wcs', 'formulaire_wcs', name='wcs-formulaire_wcs'),
)
